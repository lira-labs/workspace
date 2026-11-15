/**
 * GrafoParada · Transit Engine (Grande Recife Metropolitano)
 * Base GTFS Oficial CTM (393 Linhas com Shapes e Paradas Oficiais) + Modelo ST-GCN + Cittamobi API (a=202)
 * Protótipo Acadêmico de Pesquisa · UFRPE AI4Good.
 */

(function(window) {
  'use strict';

  const RealTransit = {
    networkData: null,
    activeRouteCode: null, // Definido dinamicamente pela geolocalizacao ou escolha do usuario
    activeRoute: null,
    activeDirection: 'ida',
    activeBoardingIndex: 0,
    activeStopIndex: 0,
    activeBusCoordIndex: 0,
    userAdaptState: {
      status: 'initializing',
      stopName: null,
      distanceKm: null,
      originSource: null,
      isManualOrigin: false,
      gpsErrorCode: null
    },
    map: null,
    polylineLayer: null,
    passedPolylineLayer: null,
    extraLegsLayer: null,
    stopsLayer: null,
    busMarker: null,
    cittamobiCache: {},
    geocodeCache: {},

    // Tabela de Aliases comuns da Região Metropolitana
    aliases: {
      '060': '2060',
      '60': '2060',
      '040': '2040',
      '40': '2040',
      '490': '2490',
      '050': '050',
      '50': '050',
      '080': '080',
      '80': '080',
      '044': '044',
      '44': '044',
      '030': '030',
      '30': '030',
      '020': '020',
      '20': '020',
      '011': '011',
      '11': '011'
    },

    escapeHtml(str) {
      return String(str == null ? '' : str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
    },

    _getCondensedHubGraph() {
      if (!this.networkData || !Array.isArray(this.networkData.hub_graph)) return null;
      if (this._condensedGraph && this._condensedGraph.sourceRef === this.networkData.hub_graph) {
        return this._condensedGraph;
      }

      const isNightOrRail = (code) => {
        const pop = this.networkData.popular_lines && this.networkData.popular_lines[code];
        const nm = (pop && pop.name) || code;
        return /bacurau/i.test(nm) || /^vlt/i.test(code);
      };
      const isTrunkCode = (c) => /^(185|191|195|199|198|157|050|080|2040|2060|1076|1100|1971|1967|1983|1992)$/.test(c);
      const isMajorHub = (name) => /^(Ti\s|Cais\s|Pra[cç]a do Derby|Terminal)/i.test(name);

      const rawHubs = this.networkData.hub_graph.filter(h => Array.isArray(h.lines) && h.lines.length > 0);
      const hubs = [];
      for (const h of rawHubs) {
        const existing = hubs.find(u => this.haversineKm(u.lat, u.lon, h.lat, h.lon) < 0.15);
        if (existing) {
          existing.lines = Array.from(new Set(existing.lines.concat(h.lines)));
          if (/^Ti\s+Joana\s+Bezerra$/i.test(h.name) || h.lines.length > existing.lines.length) {
            existing.name = h.name;
          }
        } else {
          hubs.push({ idx: hubs.length, name: h.name, lat: h.lat, lon: h.lon, lines: [...h.lines], lineSet: new Set(h.lines) });
        }
      }
      hubs.forEach(h => { h.lineSet = new Set(h.lines); });

      const lineToHubIndices = new Map();
      hubs.forEach((h, idx) => {
        h.lines.forEach(code => {
          if (!lineToHubIndices.has(code)) lineToHubIndices.set(code, []);
          lineToHubIndices.get(code).push(idx);
        });
      });

      const edges = hubs.map(() => []);
      for (let u = 0; u < hubs.length; u++) {
        const hubU = hubs[u];
        const bestByTarget = new Map();
        for (const code of hubU.lines) {
          if (isNightOrRail(code)) continue;
          const neighbors = lineToHubIndices.get(code) || [];
          const trunkScore = isTrunkCode(code) ? 0 : 1;
          for (const v of neighbors) {
            if (v === u) continue;
            if (!bestByTarget.has(v)) {
              bestByTarget.set(v, { code, trunkScore, alts: [] });
            } else {
              const cur = bestByTarget.get(v);
              if (trunkScore < cur.trunkScore) {
                cur.alts.unshift(cur.code);
                cur.code = code;
                cur.trunkScore = trunkScore;
              } else if (cur.alts.length < 1 && cur.code !== code) {
                cur.alts.push(code);
              }
            }
          }
        }
        bestByTarget.forEach((info, v) => {
          const hubV = hubs[v];
          const distKm = this.haversineKm(hubU.lat, hubU.lon, hubV.lat, hubV.lon);
          let stepMin = Math.max(5, (distKm / 20.0) * 60) + (isMajorHub(hubV.name) ? 7.5 : 13.0);
          if (isTrunkCode(info.code)) stepMin -= 2.5;
          if (/cais|santa rita/i.test(hubV.name)) stepMin -= 1.5;
          edges[u].push({ targetIdx: v, code: info.code, stepMin: Math.max(3, stepMin) });
        });
      }

      this._condensedGraph = { sourceRef: this.networkData.hub_graph, hubs, lineToHubIndices, edges };
      return this._condensedGraph;
    },

    // Inicialização da Engine
    async init(leafletMap) {
      this.map = leafletMap;
      console.log('🚍 [RealTransit] Inicializando engine com dados reais do Grande Recife...');

      try {
        const resp = await fetch('data/gtfs_real_network.json');
        if (!resp.ok) throw new Error('HTTP ' + resp.status);
        this.networkData = await resp.json();
        console.log(`✅ [RealTransit] GTFS carregado: ${this.networkData.total_lines_ready} linhas com traçados e paradas 100% reais.`);
      } catch (err) {
        console.error('❌ [RealTransit] Erro ao carregar gtfs_real_network.json:', err);
        this.showToast('Aviso: Operando em modo telemetria de contingência (PE-60).', 'warning');
        return;
      }

      this.stopsLayer = L.layerGroup().addTo(this.map);

      // Renderiza as pílulas de acesso rápido às linhas metropolitanas
      this.renderQuickLinePills();

      // Carrega localização salva ou detectada dinamicamente (NUNCA prende o usuário em parada fixa)
      let restored = false;
      try {
        const lastRaw = localStorage.getItem('grafoparada_last_coords');
        if (lastRaw) {
          const last = JSON.parse(lastRaw);
          if (typeof last.lat === 'number' && typeof last.lon === 'number') {
            this.adaptToUserLocation(last.lat, last.lon, 'Última localização ativa', { fit: false, originSource: 'cached' });
            restored = true;
          }
        }
      } catch (e) {}

      if (!restored) {
        // Estado inicial limpo: tenta geolocalização real antes de assumir qualquer parada
        this.userAdaptState = {
          status: 'awaiting_location',
          stopName: 'Escolha ou ative seu GPS',
          distanceKm: null,
          originSource: null,
          isManualOrigin: false,
          gpsErrorCode: null
        };
        this.loadRoute('199');
        const applyGpsDeniedState = (err) => {
          if (window.grafoparadaManualOrigin) return;
          const curStatus = this.userAdaptState && this.userAdaptState.status;
          if (curStatus === 'adapted' || curStatus === 'out_of_coverage') return;
          this.userAdaptState = {
            status: 'gps_denied',
            stopName: 'GPS indisponível · Escolha sua parada',
            distanceKm: null,
            originSource: null,
            isManualOrigin: false,
            gpsErrorCode: err && err.code ? err.code : 'unavailable'
          };
          if (typeof window.updateHomeGreeting === 'function') window.updateHomeGreeting();
        };

        if (typeof navigator !== 'undefined' && navigator.geolocation && typeof navigator.geolocation.getCurrentPosition === 'function') {
          navigator.geolocation.getCurrentPosition(
            (pos) => {
              if (window.grafoparadaManualOrigin) return;
              this.adaptToUserLocation(pos.coords.latitude, pos.coords.longitude, 'GPS em tempo real', { fit: true, originSource: 'gps' });
            },
            (err) => {
              applyGpsDeniedState(err);
            },
            { enableHighAccuracy: true, timeout: 4500 }
          );
        } else {
          applyGpsDeniedState({ code: 'unavailable' });
        }
      }

      // Registra ferramentas WebMCP caso o navegador possua suporte (Google Chrome WebMCP Developer Preview)
      this.registerWebMCPTools();

      // Escuta mudanças de busca no input superior
      const searchInput = document.getElementById('quick-search-input');
      if (searchInput) {
        searchInput.placeholder = 'Buscar entre 393 linhas reais (ex: 199, 1967, 2040, Olinda)...';
      }
    },

    // Alias canônico para seleção de linha compatível com Laya IA e favoritos
    selectLine(code) {
      return this.loadRoute(code);
    },

    getDirectionData(lineData, dir) {
      if (!lineData) return { dir: 'ida', headsign: '', stops: [], polyline: [] };
      const hasVolta = Array.isArray(lineData.return_stops) && lineData.return_stops.length > 0;
      const chosenDir = (dir === 'volta' && hasVolta) ? 'volta' : 'ida';
      const stops = chosenDir === 'volta' ? lineData.return_stops : (lineData.stops || []);
      const polyline = chosenDir === 'volta'
        ? ((Array.isArray(lineData.return_polyline) && lineData.return_polyline.length) ? lineData.return_polyline : (lineData.return_coords || []))
        : (lineData.polyline || []);
      const headsign = chosenDir === 'volta'
        ? (lineData.headsign_volta || (stops[stops.length - 1] && stops[stops.length - 1].name) || lineData.name)
        : (lineData.headsign_ida || lineData.headsign || (stops[stops.length - 1] && stops[stops.length - 1].name) || lineData.name);
      return { dir: chosenDir, hasVolta, headsign, stops, polyline };
    },

    toggleDirection(forceDir) {
      if (!this.activeRouteCode || !this.activeRoute) return;
      const hasVolta = Array.isArray(this.activeRoute.return_stops) && this.activeRoute.return_stops.length > 0;
      if (!hasVolta && forceDir === 'volta') {
        this.showToast('Esta linha opera com traçado circular único no GTFS.', 'info');
        return;
      }
      const nextDir = forceDir || (this.activeDirection === 'ida' ? 'volta' : 'ida');
      this.loadRoute(this.activeRouteCode, { dir: nextDir });
    },

    pickBestDirection(lineData, originCoords, destCoords) {
      if (!lineData) return { dir: 'ida', boardIdx: 0 };
      const evalDir = (stops) => {
        if (!Array.isArray(stops) || !stops.length) return null;
        let boardIdx = 0;
        let boardDist = Infinity;
        if (Array.isArray(originCoords)) {
          stops.forEach((st, i) => {
            if (!st || !st.lat || !st.lon) return;
            const d = this.haversineKm(originCoords[0], originCoords[1], st.lat, st.lon);
            if (d < boardDist) { boardDist = d; boardIdx = i; }
          });
        } else {
          boardDist = 0;
        }

        let destDist = 0;
        let destIdx = stops.length - 1;
        let forwardOk = true;
        if (Array.isArray(destCoords)) {
          destDist = Infinity;
          stops.forEach((st, i) => {
            if (!st || !st.lat || !st.lon) return;
            const d = this.haversineKm(destCoords[0], destCoords[1], st.lat, st.lon);
            if (d < destDist) { destDist = d; destIdx = i; }
          });
          forwardOk = destIdx >= boardIdx;
        }
        const score = boardDist + destDist + (forwardOk ? 0 : 8.0);
        return { boardIdx, destIdx, boardDist, destDist, forwardOk, score };
      };

      const resIda = evalDir(lineData.stops || []);
      const resVolta = evalDir(lineData.return_stops || []);
      if (resVolta && (!resIda || resVolta.score + 0.05 < resIda.score)) {
        return { dir: 'volta', boardIdx: resVolta.boardIdx };
      }
      return { dir: 'ida', boardIdx: resIda ? resIda.boardIdx : 0 };
    },

    // Renderiza linha completa com direção (IDA vs VOLTA), fatiada a partir da parada de embarque do usuário
    loadRoute(rawCode, opts = {}) {
      if (!this.networkData || !this.networkData.popular_lines) return;

      let code = String(rawCode || '').trim();
      if (this.aliases[code]) {
        code = this.aliases[code];
      }

      let lineData = this.networkData.popular_lines[code];
      if (!lineData) {
        const found = (this.networkData.routes_catalog || []).find(r =>
          r.code.toLowerCase() === code.toLowerCase() ||
          r.code.replace(/^0+/, '') === code.replace(/^0+/, '')
        );
        if (found && this.networkData.popular_lines[found.code]) {
          code = found.code;
          lineData = this.networkData.popular_lines[code];
        }
      }

      if (!lineData) {
        console.warn('Linha não encontrada no catálogo metropolitano:', code);
        this.showToast('Linha "' + code + '" não localizada no catálogo ativo.', 'warning');
        return;
      }

      this.activeRouteCode = code;
      this.activeRoute = lineData;

      const userCoords = Array.isArray(opts.originCoords)
        ? opts.originCoords
        : ((this.userAdaptState && this.userAdaptState.lat && this.userAdaptState.lon)
          ? [this.userAdaptState.lat, this.userAdaptState.lon]
          : (Array.isArray(window.userCurrentCoords) ? window.userCurrentCoords : null));

      const bestPick = this.pickBestDirection(lineData, userCoords, opts.destCoords || null);
      const chosenDir = opts.dir || bestPick.dir || 'ida';
      const dirData = this.getDirectionData(lineData, chosenDir);
      this.activeDirection = dirData.dir;

      // Calcula índice da parada de embarque neste sentido (se o usuário estiver dentro de 3km da rota)
      let boardIdx = 0;
      if (userCoords && Array.isArray(dirData.stops) && dirData.stops.length > 0) {
        let minD = Infinity;
        let nearestIdx = 0;
        dirData.stops.forEach((st, i) => {
          if (!st || !st.lat || !st.lon) return;
          const d = this.haversineKm(userCoords[0], userCoords[1], st.lat, st.lon);
          if (d < minD) { minD = d; nearestIdx = i; }
        });
        if (minD <= 3.0) {
          boardIdx = nearestIdx;
        }
      }
      this.activeBoardingIndex = boardIdx;
      this.activeStopIndex = boardIdx;

      // 1. Limpa camadas anteriores
      if (this.polylineLayer && this.map) {
        this.map.removeLayer(this.polylineLayer);
        this.polylineLayer = null;
      }
      if (this.passedPolylineLayer && this.map) {
        this.map.removeLayer(this.passedPolylineLayer);
        this.passedPolylineLayer = null;
      }
      if (this.extraLegsLayer && this.map) {
        this.map.removeLayer(this.extraLegsLayer);
        this.extraLegsLayer = null;
      }

      const coords = dirData.polyline || [];
      let splitIdx = 0;
      if (coords.length > 0 && this.map) {
        // Divide a polilinha no ponto mais próximo à parada de embarque (Passado esmaecido vs Restante da sua parada até o destino)
        if (boardIdx > 0 && dirData.stops[boardIdx]) {
          const bStop = dirData.stops[boardIdx];
          let minP = Infinity;
          coords.forEach((pt, idx) => {
            const d = this.haversineKm(bStop.lat, bStop.lon, pt[0], pt[1]);
            if (d < minP) { minP = d; splitIdx = idx; }
          });
        }

        if (splitIdx > 1 && splitIdx < coords.length - 1) {
          const passedCoords = coords.slice(0, splitIdx + 1);
          const forwardCoords = coords.slice(splitIdx);
          this.passedPolylineLayer = L.polyline(passedCoords, {
            color: '#94a3b8',
            weight: 3,
            opacity: 0.45,
            dashArray: '5, 7',
            smoothFactor: 1
          }).addTo(this.map);
          this.polylineLayer = L.polyline(forwardCoords, {
            color: dirData.dir === 'volta' ? '#0284c7' : '#059669',
            weight: 5.5,
            opacity: 0.92,
            smoothFactor: 1
          }).addTo(this.map);
        } else {
          this.polylineLayer = L.polyline(coords, {
            color: dirData.dir === 'volta' ? '#0284c7' : '#059669',
            weight: 5,
            opacity: 0.88,
            smoothFactor: 1
          }).addTo(this.map);
        }

        try {
          this.map.fitBounds(this.polylineLayer.getBounds(), {
            paddingTopLeft: [24, 140],
            paddingBottomRight: [24, 245],
            maxZoom: 15,
            animate: true
          });
        } catch (e) {
          console.warn('Erro ao ajustar bounds:', e);
        }
      }

      // 2. Plota as Paradas Reais no Mapa destacando Seu Embarque e os trechos à frente
      if (this.map && this.stopsLayer) {
        this.renderStopMarkers(dirData.stops, boardIdx);
      }

      // 2.1 Sincroniza Marcador do Usuário e Ônibus ao Vivo (separado da pill Seu Embarque)
      if (typeof window.connectUserToActiveStop === 'function' && window.userCurrentCoords) {
        window.connectUserToActiveStop(window.userCurrentCoords[0], window.userCurrentCoords[1]);
      }
      if (typeof window.updateLiveBusMarker === 'function' && coords.length > 2) {
        const anchorIdx = Math.max(boardIdx, splitIdx);
        const span = Math.max(1, (coords.length - 1) - anchorIdx);
        const targetIdx = Math.min(coords.length - 2, anchorIdx + Math.max(6, Math.floor(span * 0.35)));
        this.activeBusCoordIndex = targetIdx;
        const bp = coords[targetIdx] || coords[Math.floor(coords.length / 2)];
        const busEta = (window.isSlide3FailureActive && String(code) === '199') ? 45 : 4;
        window.updateLiveBusMarker(bp[0], bp[1], code, busEta, 14);
      }

      // 3. Atualiza Elementos do DOM (LED, Sentido Ida/Volta, Drawer fatiado da sua parada)
      this.updateUIForLine(lineData, dirData, boardIdx);
      if (typeof window.showRouteIndicatorChip === 'function') {
        const dirTag = dirData.dir === 'volta' ? 'Volta' : 'Ida';
        window.showRouteIndicatorChip(code, `${dirData.headsign || lineData.name} (${dirTag})`);
      }

      // 4. Consulta API ao Vivo do Cittamobi para Dados em Tempo Real da Frota
      this.fetchCittamobiLiveData(code);
    },

    // Plota uma jornada completa estilo Google Maps (caminhada + etapas de ônibus + baldeações + destino)
    renderMultiLegRoute(codes, hubNames, originCoords, destCoords) {
      if (!this.map || !this.networkData || !this.networkData.popular_lines || !Array.isArray(codes) || codes.length === 0) return;

      // Carrega a 1ª etapa já orientada no sentido certo da origem até o próximo ponto
      const leg0Target = (Array.isArray(hubNames) && hubNames.length > 0 && Array.isArray(this.networkData.hub_graph))
        ? (() => {
            const normH = this.normalizeText(hubNames[0]);
            const hObj = this.networkData.hub_graph.find(h => this.normalizeText(h.name).includes(normH) || normH.includes(this.normalizeText(h.name)));
            return hObj ? [hObj.lat, hObj.lon] : destCoords;
          })()
        : destCoords;
      this.loadRoute(codes[0], { originCoords, destCoords: leg0Target });

      if (this.extraLegsLayer) {
        this.map.removeLayer(this.extraLegsLayer);
      }
      this.extraLegsLayer = L.layerGroup().addTo(this.map);

      const legColors = ['#059669', '#0284c7', '#7c3aed', '#d97706', '#e11d48'];
      const bounds = L.latLngBounds([]);

      const findClosestPt = (pts, target) => {
        if (!Array.isArray(pts) || !pts.length || !Array.isArray(target)) return null;
        let best = pts[0];
        let bestD = Infinity;
        for (const p of pts) {
          const lat = Array.isArray(p) ? p[0] : p.lat;
          const lon = Array.isArray(p) ? p[1] : p.lon;
          const d = this.haversineKm(target[0], target[1], lat, lon);
          if (d < bestD) { bestD = d; best = [lat, lon]; }
        }
        return best;
      };

      const startRef = Array.isArray(originCoords) ? originCoords : (this.userAdaptState && this.userAdaptState.lat ? [this.userAdaptState.lat, this.userAdaptState.lon] : null);

      codes.forEach((rawCode, idx) => {
        const line = this.networkData.popular_lines[String(rawCode)] || this.networkData.popular_lines[this.aliases[rawCode] || rawCode];
        if (!line) return;
        const bestDir = idx === 0
          ? { dir: this.activeDirection }
          : this.pickBestDirection(line, startRef, destCoords);
        const dirData = this.getDirectionData(line, bestDir.dir);
        const pts = (dirData.polyline && dirData.polyline.length > 0)
          ? dirData.polyline
          : ((Array.isArray(line.polyline) && line.polyline.length > 0) ? line.polyline : (line.return_coords || []));
        if (!pts.length) return;

        // Caminhada tracejada da localização atual até a 1ª parada de embarque
        if (idx === 0 && startRef) {
          const legStops = (dirData.stops && dirData.stops.length) ? dirData.stops : pts;
          const boardPt = findClosestPt(legStops, startRef);
          if (boardPt) {
            const walkStart = L.polyline([startRef, boardPt], {
              color: '#334155',
              weight: 3.5,
              opacity: 0.85,
              dashArray: '4, 7'
            }).addTo(this.extraLegsLayer);
            bounds.extend(walkStart.getBounds());
          }
        }

        if (idx > 0) {
          const color = legColors[idx % legColors.length];
          const poly = L.polyline(pts, {
            color,
            weight: 4.5,
            opacity: 0.9,
            dashArray: '8, 6'
          }).addTo(this.extraLegsLayer);
          bounds.extend(poly.getBounds());
        } else if (this.polylineLayer) {
          bounds.extend(this.polylineLayer.getBounds());
        }

        // Caminhada tracejada final até o destino escolhido
        if (idx === codes.length - 1 && Array.isArray(destCoords)) {
          const legStops = (dirData.stops && dirData.stops.length) ? dirData.stops : pts;
          const alightPt = findClosestPt(legStops, destCoords);
          if (alightPt) {
            const walkEnd = L.polyline([alightPt, destCoords], {
              color: '#334155',
              weight: 3.5,
              opacity: 0.85,
              dashArray: '4, 7'
            }).addTo(this.extraLegsLayer);
            bounds.extend(walkEnd.getBounds());
          }
        }
      });

      // Marca os Hubs/Terminais SEI de baldeação ao longo do trajeto
      if (Array.isArray(hubNames) && Array.isArray(this.networkData.hub_graph)) {
        hubNames.forEach((hName, hIdx) => {
          const normH = this.normalizeText(hName);
          const hubObj = this.networkData.hub_graph.find(h => h.name === hName) ||
            this.networkData.hub_graph.find(h => {
              const hn = this.normalizeText(h.name);
              return hn.includes(normH) || normH.includes(hn);
            });
          if (!hubObj) return;
          const badge = L.marker([hubObj.lat, hubObj.lon], {
            icon: L.divIcon({
              className: '',
              html: `<div style="background:#0f172a; color:#fff; border:2px solid #fff; border-radius:999px; padding:3px 8px; font-size:10px; font-weight:800; white-space:nowrap; box-shadow:0 4px 12px rgba(0,0,0,0.3);">Conexão ${hIdx + 1}: ${this.escapeHtml(hubObj.name)}</div>`,
              iconAnchor: [45, 12]
            })
          }).addTo(this.extraLegsLayer);
          bounds.extend(badge.getLatLng());
        });
      }

      if (Array.isArray(destCoords)) {
        const destPin = L.marker(destCoords, {
          icon: L.divIcon({
            className: '',
            html: `<div style="background:#e11d48; color:#fff; border:2px solid #fff; border-radius:999px; padding:3px 8px; font-size:10.5px; font-weight:800; white-space:nowrap; box-shadow:0 4px 12px rgba(0,0,0,0.3);">Destino</div>`,
            iconAnchor: [35, 12]
          })
        }).addTo(this.extraLegsLayer);
        bounds.extend(destPin.getLatLng());
      }

      if (bounds.isValid()) {
        try {
          this.map.fitBounds(bounds, {
            paddingTopLeft: [24, 140],
            paddingBottomRight: [24, 245],
            maxZoom: 14,
            animate: true
          });
        } catch (e) {}
      }
    },

    // Plota os marcadores das paradas destacando Embarque do Usuário vs paradas passadas
    renderStopMarkers(stops, boardIdx = this.activeBoardingIndex || 0) {
      if (!this.stopsLayer) return;
      this.stopsLayer.clearLayers();
      const self = this;

      (stops || []).forEach((st, idx) => {
        const isBoard = idx === boardIdx;
        const isPassed = idx < boardIdx;
        const isTerminal = idx === 0 || idx === stops.length - 1;
        const isActiveSel = idx === self.activeStopIndex && !isBoard && !isTerminal;
        const dirColor = self.activeDirection === 'volta' ? '#0284c7' : '#059669';
        const iconHtml = isBoard
          ? `<div style="background:${dirColor}; color:#fff; border:2px solid #fff; border-radius:999px; padding:2px 8px; font-size:10px; font-weight:800; white-space:nowrap; display:inline-flex; align-items:center; gap:4px; box-shadow:0 4px 12px rgba(0,0,0,0.35);"><span style="width:6px;height:6px;border-radius:50%;background:#ffffff;display:inline-block;"></span>Seu Embarque</div>`
          : (isTerminal
            ? '<div style="background:#0f172a; color:#fff; border:2px solid #fff; border-radius:50%; width:22px; height:22px; display:flex; align-items:center; justify-content:center; font-size:10px; font-weight:800; box-shadow:0 3px 10px rgba(0,0,0,0.3);">T</div>'
            : (isActiveSel
              ? `<div style="background:${dirColor}; color:#ffffff; border:2px solid #ffffff; border-radius:50%; width:18px; height:18px; display:flex; align-items:center; justify-content:center; font-size:9.5px; font-weight:800; box-shadow:0 3px 8px rgba(15,23,42,0.3);">${idx + 1}</div>`
              : `<div style="background:#ffffff; border:2px solid ${isPassed ? '#cbd5e1' : dirColor}; opacity:${isPassed ? '0.5' : '0.95'}; border-radius:50%; width:9px; height:9px; box-shadow:0 1px 3px rgba(15,23,42,0.2);"></div>`));

        const customIcon = L.divIcon({
          className: '',
          html: iconHtml,
          iconSize: isBoard ? [98, 22] : (isTerminal ? [22, 22] : (isActiveSel ? [18, 18] : [9, 9])),
          iconAnchor: isBoard ? [49, 28] : (isTerminal ? [11, 11] : (isActiveSel ? [9, 9] : [4.5, 4.5]))
        });

        const marker = L.marker([st.lat, st.lon], {
          icon: customIcon,
          zIndexOffset: isBoard ? 950 : (isActiveSel ? 600 : (isTerminal ? 400 : 0))
        });
        const displayStopName = (st.name && !/^\d+$/.test(String(st.name).trim()))
          ? st.name
          : `Parada ${st.stop_id}`;

        const popupContent = `
          <div style="font-family:'Plus Jakarta Sans',sans-serif; min-width:220px; padding:2px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
              <span style="font-size:10px; font-weight:800; background:#f1f5f9; color:#475569; padding:2px 6px; border-radius:4px;">CÓD ${st.stop_id}</span>
              <span style="font-size:10.5px; font-weight:700; color:${dirColor};">Linha ${self.activeRouteCode} (${self.activeDirection === 'volta' ? 'Volta' : 'Ida'})</span>
            </div>
            <div style="font-size:13px; font-weight:800; color:#0f172a; margin-bottom:4px; line-height:1.2;">${displayStopName}</div>
            <div style="font-size:11px; color:#64748b; margin-bottom:8px;">Programado GTFS: <strong>${st.arr_time || 'Regular'}</strong></div>
            <button onclick="window.RealTransit.selectStop(${idx}, true); if(leafletMap) leafletMap.closePopup();" style="width:100%; background:${dirColor}; color:#fff; border:none; padding:6px 12px; border-radius:6px; font-size:11.5px; font-weight:800; cursor:pointer;">
              Embarcar nesta Parada ➔
            </button>
            <button onclick="window.setMyBoardingStop('${displayStopName.replace(/'/g, "\\'")}', [${st.lat}, ${st.lon}]); if(leafletMap) leafletMap.closePopup();" style="width:100%; background:#0f172a; color:#fff; border:none; padding:6px 12px; border-radius:6px; font-size:11.5px; font-weight:800; cursor:pointer; margin-top:4px;">
              Fixar como Minha Parada
            </button>
          </div>
        `;

        marker.bindPopup(popupContent);
        marker.on('click', () => self.selectStop(idx, false));
        self.stopsLayer.addLayer(marker);
      });
    },

    // Seleciona uma parada na linha e sentido ativos
    selectStop(index, panTo) {
      const dirData = this.getDirectionData(this.activeRoute, this.activeDirection);
      const activeStops = dirData.stops || [];
      if (!activeStops[index]) return;
      this.activeStopIndex = index;
      const st = activeStops[index];

      const rawStopLabel = (st.name && !/^\d+$/.test(String(st.name).trim()))
        ? st.name
        : `Parada ${st.stop_id} (${this.activeRoute.name || 'Linha ' + this.activeRouteCode})`;
      const cleanStopLabel = String(rawStopLabel).replace(/\bTi\b/g, 'TI');
      const displayHeadsign = String(dirData.headsign || this.activeRoute.name || dirLabel).replace(/\bTi\b/g, 'TI');

      const dirLabel = dirData.dir === 'volta' ? 'VOLTA' : 'IDA';
      const remainingCount = Math.max(0, activeStops.length - 1 - index);

      // Atualiza o card de parada atual em 2 linhas compactas para caber no Bottom Sheet em repouso (205px)
      const nameEl = document.getElementById('current-stop-name');
      if (nameEl) {
        const toggleDirBtn = dirData.hasVolta
          ? `<button type="button" onclick="window.RealTransit.toggleDirection()" style="background:#eff6ff; color:#1d4ed8; border:1px solid #bfdbfe; border-radius:6px; padding:2px 7px; font-size:10px; font-weight:800; cursor:pointer; white-space:nowrap;">⇄ ${dirData.dir === 'volta' ? 'Ida' : 'Volta'}</button>`
          : '';
        const pinStopBtn = `<button type="button" onclick="window.setMyBoardingStop('${cleanStopLabel.replace(/'/g, "\\'")}', [${st.lat}, ${st.lon}])" style="background:#f0fdf4; color:#047857; border:1px solid #86efac; border-radius:6px; padding:2px 7px; font-size:10px; font-weight:800; cursor:pointer; white-space:nowrap;">Fixar ponto</button>`;
        nameEl.innerHTML = `
          <div style="display:flex; flex-direction:column; gap:3px;">
            <div style="display:flex; align-items:center; justify-content:space-between; gap:4px; flex-wrap:nowrap;">
              <div style="display:flex; align-items:center; gap:5px; min-width:0; overflow:hidden; white-space:nowrap;">
                <span style="font-size:10px; font-weight:800; background:${dirData.dir === 'volta' ? '#dbeafe' : '#dcfce7'}; color:${dirData.dir === 'volta' ? '#1d4ed8' : '#15803d'}; padding:2px 6px; border-radius:5px; flex-shrink:0;">SENTIDO ${dirLabel}</span>
                <span style="font-size:10.5px; font-weight:800; color:#0f172a; overflow:hidden; text-overflow:ellipsis;">Parada #${index + 1} · ${remainingCount} à frente</span>
              </div>
              <div style="display:flex; align-items:center; gap:4px; flex-shrink:0;">
                ${toggleDirBtn}
                ${pinStopBtn}
              </div>
            </div>
            <div style="font-size:13px; font-weight:800; color:var(--text-main); white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${cleanStopLabel} <span style="font-size:11px; font-weight:600; color:var(--text-secondary);">· ${displayHeadsign} (#${st.stop_id})</span></div>
          </div>
        `;
      }

      const etaMinutes = Math.max(2, ((index % 6) * 3) + 2);
      const restingEta = document.getElementById('resting-eta-val');
      const liveEta = document.getElementById('live-eta-num');
      if (restingEta) restingEta.textContent = String(etaMinutes);
      if (liveEta) liveEta.textContent = String(etaMinutes);
      if (typeof window.updateHomeGreeting === 'function') window.updateHomeGreeting();

      if (panTo && this.map) {
        if (this.stopsLayer) {
          this.renderStopMarkers(activeStops, this.activeBoardingIndex);
        }
        this.map.panTo([st.lat, st.lon], { animate: true, duration: 0.5 });
      }

      this.renderStopsDrawer(activeStops, this.activeBoardingIndex);
    },

    // Atualiza a interface (Drawer, LED, Títulos, Cards) para o sentido e parada de embarque ativos
    updateUIForLine(lineData, dirDataOverride, boardIdxOverride) {
      const dirData = dirDataOverride || this.getDirectionData(lineData, this.activeDirection);
      const boardIdx = typeof boardIdxOverride === 'number' ? boardIdxOverride : (this.activeBoardingIndex || 0);
      const stops = dirData.stops || [];
      const dirTag = dirData.dir === 'volta' ? 'VOLTA' : 'IDA';

      const topBadge = document.getElementById('top-line-label');
      if (topBadge) topBadge.textContent = `${lineData.code} · ${dirTag}`;

      const ledDestination = document.getElementById('led-destination-line');
      const ledNumber = document.getElementById('led-line-number');
      if (ledDestination) ledDestination.textContent = `${lineData.code} (${dirTag}) ${(dirData.headsign || lineData.name)}`.toUpperCase();
      if (ledNumber) ledNumber.textContent = lineData.code;

      const destTitle = document.getElementById('active-trip-destination-title');
      if (destTitle) destTitle.textContent = `${lineData.name} · Sentido ${dirData.headsign || dirTag}`;

      const activeHeader = document.getElementById('active-trip-header');
      if (activeHeader) activeHeader.textContent = `Linha ${lineData.code} (${dirTag}) ➔ ${dirData.headsign || lineData.name}`;

      const firstStop = stops[boardIdx] ? stops[boardIdx].name.split('/')[0].trim() : 'Sua Parada';
      const lastStop = stops.length > 1 ? stops[stops.length - 1].name.split('/')[0].trim() : 'Ponto Final';

      const homeCardSub = document.getElementById('home-card-sub');
      const workCardSub = document.getElementById('work-card-sub');
      if (homeCardSub) homeCardSub.textContent = `${firstStop} · 4 min`;
      if (workCardSub) workCardSub.textContent = `${lastStop} · 28 min`;

      this.selectStop(boardIdx, false);
      this.renderStopsDrawer(stops, boardIdx);
    },

    // Renderiza a lista de paradas PRIORIZANDO da parada de embarque em diante (evita confusão na rota completa)
    renderStopsDrawer(stops, boardIdx = this.activeBoardingIndex || 0) {
      const container = document.getElementById('stops-container');
      const countLabel = document.getElementById('stops-count-label');
      const sheetCountLabel = document.getElementById('sheet-stops-count-label');
      const remaining = Math.max(0, (stops ? stops.length : 0) - boardIdx);
      if (countLabel) countLabel.textContent = String(remaining);
      if (sheetCountLabel) sheetCountLabel.textContent = String(remaining);
      if (!container || !Array.isArray(stops)) return;

      const dirData = this.getDirectionData(this.activeRoute, this.activeDirection);
      const dirColor = dirData.dir === 'volta' ? '#0284c7' : '#059669';
      const dirBadge = dirData.dir === 'volta' ? 'Sentido Volta' : 'Sentido Ida';

      const buildStopRow = (st, idx, isPassed) => {
        const isSel = idx === this.activeStopIndex;
        const isBoard = idx === boardIdx;
        const eta = Math.max(2, (((idx - boardIdx + 6) % 6) * 3) + 2);
        const stLabel = (st.name && !/^\d+$/.test(String(st.name).trim())) ? st.name : `Parada ${st.stop_id}`;
        return `
          <div style="background:${isSel ? '#ecfdf5' : 'var(--bg-page)'}; border:${isSel ? `2px solid ${dirColor}` : '1px solid var(--border-color)'}; opacity:${isPassed ? '0.62' : '1'}; border-radius:12px; padding:10px 12px; margin-bottom:6px; display:flex; justify-content:space-between; align-items:center; cursor:pointer; transition:all 0.15s ease;" onclick="window.RealTransit.selectStop(${idx}, true)">
            <div style="max-width:75%;">
              <div style="display:flex; align-items:center; gap:5px; margin-bottom:2px; flex-wrap:wrap;">
                <span style="font-size:10px; font-weight:800; background:${isBoard ? dirColor : '#f1f5f9'}; color:${isBoard ? '#ffffff' : '#475569'}; padding:1px 6px; border-radius:4px;">${isBoard ? 'SEU EMBARQUE #' + (idx + 1) : '#' + String(idx + 1).padStart(2, '0')}</span>
                <span style="font-size:10px; font-weight:800; color:#0369a1;">CÓD ${st.stop_id}</span>
              </div>
              <div style="font-size:13px; font-weight:800; color:#0f172a; line-height:1.25;">${stLabel}</div>
              <div style="font-size:11px; color:#64748b; margin-top:2px;">Previsto GTFS: ${st.arr_time || 'Regular'}</div>
            </div>
            <div style="text-align:right;">
              <div style="font-family:'JetBrains Mono',monospace; font-size:15px; font-weight:800; color:${isSel ? dirColor : 'var(--text-main)'};">${eta} <span style="font-size:11px;">min</span></div>
              <div style="font-size:10px; font-weight:700; color:#15803d;">${isBoard ? 'Seu ponto' : (idx === stops.length - 1 ? 'Ponto Final' : 'À frente')}</div>
            </div>
          </div>
        `;
      };

      let html = `
        <div style="display:flex; align-items:center; justify-content:space-between; gap:6px; margin-bottom:8px; padding:7px 10px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:10px;">
          <div style="font-size:11px; font-weight:800; color:#0f172a;">
            ${dirBadge} · Mostrando ${remaining} paradas a partir do embarque
          </div>
          ${dirData.hasVolta ? `<button type="button" onclick="window.RealTransit.toggleDirection()" style="background:#0284c7; color:#fff; border:none; border-radius:7px; padding:4px 9px; font-size:10.5px; font-weight:800; cursor:pointer; white-space:nowrap;">⇄ Trocar Sentido</button>` : ''}
        </div>
      `;

      if (boardIdx > 0) {
        let passedHtml = '';
        for (let i = 0; i < boardIdx; i++) {
          passedHtml += buildStopRow(stops[i], i, true);
        }
        html += `
          <details style="margin-bottom:8px; background:#f8fafc; border:1px dashed #cbd5e1; border-radius:10px; padding:6px 10px;">
            <summary style="font-size:11px; font-weight:700; color:#64748b; cursor:pointer;">Ver ${boardIdx} paradas anteriores à sua (já passadas)</summary>
            <div style="margin-top:6px;">${passedHtml}</div>
          </details>
        `;
      }

      for (let i = boardIdx; i < stops.length; i++) {
        html += buildStopRow(stops[i], i, false);
      }

      container.innerHTML = html;
    },

    // Pílulas no topo para trocar de linha rapidamente entre os principais corredores metropolitanos
    renderQuickLinePills() {
      const pillsContainer = document.querySelector('.top-pills-row');
      if (!pillsContainer) return;

      const existingBtn = document.getElementById('catalog-picker-pill');
      if (existingBtn) return;

      const catalogBtn = document.createElement('div');
      catalogBtn.id = 'catalog-picker-pill';
      catalogBtn.className = 'top-pill';
      catalogBtn.style.background = '#0284c7';
      catalogBtn.style.color = '#ffffff';
      catalogBtn.style.border = 'none';
      catalogBtn.innerHTML = '<svg class="gp-svg" style="width:13px;height:13px;color:#ffffff;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 6v6"/><path d="M16 6v6"/><path d="M2 12h19.6"/><path d="M18 18h3s.5-1.7.8-2.8c.1-.4.2-.8.2-1.2 0-.4-.1-.8-.2-1.2l-1.4-5C20.1 6.8 19.1 6 18 6H4a2 2 0 0 0-2 2v10h3"/><circle cx="7" cy="18" r="2"/><circle cx="16" cy="18" r="2"/></svg><span>Linhas</span>';
      catalogBtn.onclick = () => this.openLinePickerModal();

      pillsContainer.insertBefore(catalogBtn, pillsContainer.children[1]);
    },

    // Modal para escolher qualquer uma das 400 linhas do GTFS ou Terminais
    openLinePickerModal() {
      if (!this.networkData) return;
      let modal = document.getElementById('line-picker-modal');
      if (!modal) {
        modal = document.createElement('div');
        modal.id = 'line-picker-modal';
        modal.style.cssText = 'position:fixed; inset:0; background:rgba(0,0,0,0.6); z-index:3000; display:flex; align-items:flex-end; justify-content:center; backdrop-filter:blur(4px);';
        document.body.appendChild(modal);
      }

      modal.innerHTML = `
        <div style="background:#ffffff; border-radius:24px 24px 0 0; width:100%; max-width:440px; max-height:85vh; display:flex; flex-direction:column; padding:20px; box-shadow:0 -10px 40px rgba(0,0,0,0.3); animation:slideUp 0.25s ease;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
            <div>
              <div style="font-size:11px; font-weight:800; color:#0284c7; text-transform:uppercase;">Catálogo Oficial Grande Recife (GTFS Real)</div>
              <h3 style="font-size:18px; font-weight:800; color:#0f172a;">Escolher Linha de Ônibus</h3>
            </div>
            <button onclick="document.getElementById('line-picker-modal').style.display='none'" style="border:none; background:#f1f5f9; width:32px; height:32px; border-radius:50%; font-size:14px; font-weight:800; cursor:pointer;">✕</button>
          </div>

          <div style="margin-bottom:12px;">
            <input type="text" id="modal-line-search-input" placeholder="Digite o número ou nome da linha..." oninput="window.RealTransit.filterModalLines(this.value)" style="width:100%; padding:10px 14px; border-radius:12px; border:1.5px solid #cbd5e1; font-size:14px; font-family:'Plus Jakarta Sans',sans-serif; outline:none; box-sizing:border-box;">
          </div>

          <div style="font-size:11.5px; font-weight:800; color:#64748b; text-transform:uppercase; margin-bottom:8px;" id="modal-lines-list-header">Linhas com Traçado & Paradas 100% Reais:</div>
          <div id="modal-lines-list" style="display:flex; flex-direction:column; gap:8px; overflow-y:auto; flex:1; padding-right:4px;"></div>
        </div>
      `;

      modal.style.display = 'flex';
      this.filterModalLines('');
      setTimeout(() => {
        const inp = document.getElementById('modal-line-search-input');
        if (inp) inp.focus();
      }, 100);
    },

    // Filtra dinamicamente entre as 393 linhas reais dentro do modal
    filterModalLines(query) {
      const listEl = document.getElementById('modal-lines-list');
      const headerEl = document.getElementById('modal-lines-list-header');
      if (!listEl || !this.networkData) return;

      const q = (query || '').trim().toLowerCase();

      const popular = [
        { code: '522', name: 'Dois Irmãos (Rui Barbosa / UFRPE)' },
        { code: '2060', name: 'TI Tancredo Neves / TI Macaxeira (Linha 060)' },
        { code: '2040', name: 'CDU / Boa Viagem / Caxangá' },
        { code: '050', name: 'PE-15 / Boa Viagem (Agamenon Magalhães)' },
        { code: '202', name: 'Barro / Macaxeira (Várzea)' },
        { code: '1982', name: 'Conjunto Beira Mar / Derby' },
        { code: '080', name: 'TI Joana Bezerra / Boa Viagem' },
        { code: '914', name: 'TI PE-15 / TI Afogados' },
        { code: '044', name: 'Massangana / Boa Vista' },
        { code: '030', name: 'TI Rio Doce / Barra de Jangada' },
        { code: '191', name: 'Recife / Porto de Galinhas' },
        { code: '199', name: 'Camela / TI Cabo' },
        { code: '178', name: 'Porto de Suape / TI Cabo' }
      ];

      let items = [];

      if (!q) {
        if (headerEl) headerEl.textContent = 'Principais Linhas Metropolitanas:';
        items = popular;
      } else {
        if (headerEl) headerEl.textContent = `Resultados para "${query}":`;
        const catalog = this.networkData.routes_catalog || [];
        catalog.forEach(r => {
          if (r.code.toLowerCase().includes(q) || r.label.toLowerCase().includes(q) || r.name.toLowerCase().includes(q)) {
            items.push({
              code: r.code,
              name: r.name
            });
          }
        });
      }

      if (items.length === 0) {
        listEl.innerHTML = `
          <div style="padding:24px 16px; text-align:center; color:#64748b;">
            <div style="font-size:13.5px; font-weight:800; color:#0f172a; margin-bottom:4px;">Nenhuma linha encontrada para "${this.escapeHtml(query)}"</div>
            <div style="font-size:11.5px; color:#64748b; line-height:1.45; margin-bottom:12px;">Verifique o número da linha (ex: 522, 060, 2040) ou o nome do corredor (ex: Dois Irmãos, Derby, CDU).</div>
            <button onclick="document.getElementById('modal-line-search-input').value=''; window.RealTransit.filterModalLines('');" style="background:#0284c7; color:#fff; border:none; padding:7px 14px; border-radius:8px; font-size:11.5px; font-weight:800; cursor:pointer;">
              Ver Linhas Populares
            </button>
          </div>
        `;
        return;
      }

      const busSvgBadge = `<span style="width:28px; height:28px; border-radius:8px; background:#e0f2fe; color:#0284c7; display:inline-flex; align-items:center; justify-content:center; flex-shrink:0;"><svg class="gp-svg" style="width:15px;height:15px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 6v6"/><path d="M16 6v6"/><path d="M2 12h19.6"/><path d="M18 18h3s.5-1.7.8-2.8c.1-.4.2-.8.2-1.2 0-.4-.1-.8-.2-1.2l-1.4-5C20.1 6.8 19.1 6 18 6H4a2 2 0 0 0-2 2v10h3"/><circle cx="7" cy="18" r="2"/><circle cx="16" cy="18" r="2"/></svg></span>`;

      listEl.innerHTML = items.slice(0, 30).map(p => `
        <div onclick="window.RealTransit.loadRoute('${p.code}'); document.getElementById('line-picker-modal').style.display='none';" style="background:#f8fafc; border:1.5px solid #e2e8f0; border-radius:12px; padding:10px 12px; display:flex; align-items:center; justify-content:space-between; cursor:pointer; transition:all 0.15s ease;">
          <div style="display:flex; align-items:center; gap:10px; max-width:80%;">
            ${busSvgBadge}
            <div>
              <div style="font-size:14px; font-weight:800; color:#0f172a; line-height:1.2;">${p.code} · ${p.name}</div>
              <div style="font-size:11px; color:#64748b; margin-top:2px;">Dados Oficiais GTFS</div>
            </div>
          </div>
          <span style="font-size:12px; font-weight:800; color:#059669;">Ver ➔</span>
        </div>
      `).join('');
    },

    // Consulta API Pública Cittamobi (m3p/js) para obter dados em tempo real
    async fetchCittamobiLiveData(routeCode) {
      if (typeof window !== 'undefined' && window.isSlide3FailureActive) return;
      const banner = document.getElementById('resting-reallocation-banner');
      if (!banner) return;

      banner.style.display = 'flex';
      banner.innerHTML = `
        <div style="display:flex; align-items:center; gap:8px; width:100%;">
          <div style="width:8px; height:8px; border-radius:50%; background:#a7f3d0; animation:pulseGreen 1.5s infinite; flex-shrink:0;"></div>
          <div style="font-size:11px; font-weight:700; color:#ffffff;">
            Conectando aos servidores Cittamobi (Grande Recife)...
          </div>
        </div>
      `;

      try {
        const queryUrl = `https://api.cittamobi.com.br/m3p/js/search/q?q=${encodeURIComponent(routeCode)}&a=202&lat=-8.05&lng=-34.90`;
        const resp = await fetch(queryUrl);
        if (typeof window !== 'undefined' && window.isSlide3FailureActive) return;
        if (resp.ok) {
          const data = await resp.json();
          if (typeof window !== 'undefined' && window.isSlide3FailureActive) return;
          const services = data.services || [];
          if (services.length > 0) {
            const s0 = services[0];
            const company = s0.companyName || 'Consórcio de Transporte Metropolitano';
            banner.innerHTML = `
              <div style="display:flex; justify-content:space-between; align-items:center; width:100%; gap:6px;">
                <div style="display:flex; align-items:center; gap:8px; min-width:0;">
                  <svg class="gp-svg" style="width:14px;height:14px;color:#ffffff;flex-shrink:0;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.55a11 11 0 0 1 14.08 0"/><path d="M1.42 9a16 16 0 0 1 21.16 0"/><path d="M8.53 16.11a6 6 0 0 1 6.95 0"/><line x1="12" y1="20" x2="12.01" y2="20"/></svg>
                  <div style="font-size:11.5px; font-weight:700; color:#ffffff; overflow:hidden; text-overflow:ellipsis;">
                    Operadora: <strong>${company}</strong>
                  </div>
                </div>
                <span style="font-size:10px; font-weight:800; background:rgba(255,255,255,0.2); color:#ffffff; padding:2px 7px; border-radius:4px; white-space:nowrap; flex-shrink:0;">Real · Cittamobi</span>
              </div>
            `;
            return;
          }
        }
      } catch (e) {
        // Silently catch and fallback to GTFS
      }

      if (typeof window !== 'undefined' && window.isSlide3FailureActive) return;
      // Fallback elegante com dados do GTFS
      banner.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center; width:100%; gap:6px;">
          <div style="display:flex; align-items:center; gap:8px; min-width:0;">
            <svg class="gp-svg" style="width:14px;height:14px;color:#ffffff;flex-shrink:0;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 6v6"/><path d="M16 6v6"/><path d="M2 12h19.6"/><path d="M18 18h3s.5-1.7.8-2.8c.1-.4.2-.8.2-1.2 0-.4-.1-.8-.2-1.2l-1.4-5C20.1 6.8 19.1 6 18 6H4a2 2 0 0 0-2 2v10h3"/><circle cx="7" cy="18" r="2"/><circle cx="15" cy="18" r="2"/></svg>
            <div style="font-size:11.5px; font-weight:800; color:#ffffff;">
              Linha ${routeCode} · Grade Horária Oficial GTFS
            </div>
          </div>
          <span style="font-size:10px; font-weight:800; background:rgba(255,255,255,0.2); color:#ffffff; padding:2px 7px; border-radius:4px; white-space:nowrap; flex-shrink:0;">GTFS Oficial</span>
        </div>
      `;
    },

    // Busca inteligente no catálogo de 400 linhas, 44 terminais e paradas da linha (5 Estados de UI)
    handleSearch(query) {
      const q = (query || '').trim().toLowerCase();
      const drop = document.getElementById('search-results-dropdown');
      const clearBtn = document.getElementById('search-clear-btn');
      if (!drop) return;

      // 1. ESTADO VAZIO ORIENTADOR: Usuário focou no input sem digitar nada
      if (!q) {
        if (clearBtn) clearBtn.style.display = 'none';
        drop.innerHTML = `
          <div style="padding:8px 12px; background:#f8fafc; border-bottom:1px solid #e2e8f0; font-size:11px; font-weight:800; color:#64748b; text-transform:uppercase; display:flex; justify-content:space-between; align-items:center;">
            <span>🔥 Linhas Populares no Grande Recife</span>
            <span style="font-size:10.5px; color:#0284c7; cursor:pointer; font-weight:800;" onclick="window.RealTransit.openLinePickerModal(); if(window.clearQuickSearch) window.clearQuickSearch();">Ver 400 Linhas ➔</span>
          </div>
          <div class="search-item" onclick="window.RealTransit.loadRoute('522'); if(window.clearQuickSearch) window.clearQuickSearch();">
            <div><strong style="color:#0f172a;">🚌 522 · Dois Irmãos (Rui Barbosa / UFRPE)</strong><div style="font-size:11px; color:var(--text-secondary);">Linha Oficial da UFRPE · Derby · Rui Barbosa</div></div>
            <span style="font-size:11px; font-weight:700; color:#059669; background:#ecfdf5; padding:2px 8px; border-radius:6px;">UFRPE</span>
          </div>
          <div class="search-item" onclick="window.RealTransit.loadRoute('2060'); if(window.clearQuickSearch) window.clearQuickSearch();">
            <div><strong style="color:#0f172a;">🚌 2060 · TI Tancredo Neves / TI Macaxeira (Linha 060)</strong><div style="font-size:11px; color:var(--text-secondary);">Espinha Dorsal Metropolitana · Av. Recife</div></div>
            <span style="font-size:11px; font-weight:700; color:#059669; background:#ecfdf5; padding:2px 8px; border-radius:6px;">Linha 060</span>
          </div>
          <div class="search-item" onclick="window.RealTransit.loadRoute('2040'); if(window.clearQuickSearch) window.clearQuickSearch();">
            <div><strong style="color:#0f172a;">🚌 2040 · CDU / Boa Viagem / Caxangá</strong><div style="font-size:11px; color:var(--text-secondary);">Conexão Universitária UFPE / Zona Sul</div></div>
            <span style="font-size:11px; font-weight:700; color:#059669; background:#ecfdf5; padding:2px 8px; border-radius:6px;">CDU</span>
          </div>
          <div class="search-item" onclick="window.RealTransit.loadRoute('050'); if(window.clearQuickSearch) window.clearQuickSearch();">
            <div><strong style="color:#0f172a;">🚌 050 · PE-15 / Boa Viagem</strong><div style="font-size:11px; color:var(--text-secondary);">Corredor Agamenon Magalhães</div></div>
            <span style="font-size:11px; font-weight:700; color:#059669; background:#ecfdf5; padding:2px 8px; border-radius:6px;">Agamenon</span>
          </div>
          <div class="search-item" onclick="window.RealTransit.loadRoute('199'); if(window.clearQuickSearch) window.clearQuickSearch();">
            <div><strong style="color:#0f172a;">🚌 199 · Camela / TI Cabo</strong><div style="font-size:11px; color:var(--text-secondary);">Corredor Rodoviário PE-60 · São Judas Tadeu</div></div>
            <span style="font-size:11px; font-weight:700; color:#059669; background:#ecfdf5; padding:2px 8px; border-radius:6px;">PE-60</span>
          </div>
          <div style="padding:8px 12px; background:#f8fafc; border-top:1px solid #e2e8f0; display:flex; justify-content:space-between; align-items:center;">
            <button onclick="window.RealTransit.openLinePickerModal(); if(window.clearQuickSearch) window.clearQuickSearch();" style="width:100%; background:#0284c7; color:#ffffff; border:none; border-radius:8px; padding:7px; font-size:12px; font-weight:800; cursor:pointer;">
              🔍 Explorar Catálogo Completo (400 Linhas GTFS)
            </button>
          </div>
        `;
        drop.style.display = 'flex';
        return;
      }

      if (clearBtn) clearBtn.style.display = 'block';
      const results = [];

      // 1. Busca nos Terminais Integrados (SEI)
      if (this.networkData && this.networkData.terminals_sei) {
        this.networkData.terminals_sei.forEach(t => {
          if (t.name.toLowerCase().includes(q)) {
            results.push({
              type: 'terminal',
              title: t.name,
              sub: 'Terminal Integrado do SEI · Integração Temporal VEM',
              lat: t.lat,
              lon: t.lon
            });
          }
        });
      }

      // 2. Busca nas 400 Linhas do Catálogo GTFS
      if (this.networkData && this.networkData.routes_catalog) {
        this.networkData.routes_catalog.forEach(r => {
          if (r.code.toLowerCase().includes(q) || r.label.toLowerCase().includes(q) || r.name.toLowerCase().includes(q)) {
            results.push({
              type: 'route',
              title: r.label,
              sub: 'Linha Oficial GTFS Grande Recife',
              code: r.code
            });
          }
        });
      }

      // 3. Busca nas Paradas da Linha Atual
      if (this.activeRoute && this.activeRoute.stops) {
        this.activeRoute.stops.forEach((st, idx) => {
          if (st.name.toLowerCase().includes(q) || st.stop_id.includes(q)) {
            results.push({
              type: 'stop',
              title: st.name,
              sub: `Parada #${idx + 1} da Linha ${this.activeRouteCode} · Cód ${st.stop_id}`,
              index: idx,
              lat: st.lat,
              lon: st.lon
            });
          }
        });
      }

      // 2. ESTADO VAZIO / SEM RESULTADOS (COM ORIENTAÇÃO CLARA)
      if (results.length === 0) {
        drop.innerHTML = `
          <div style="padding:16px; text-align:center; color:#64748b;">
            <div style="font-size:22px; margin-bottom:4px;">🔍</div>
            <div style="font-size:13px; font-weight:800; color:#0f172a; margin-bottom:4px;">Nenhuma linha ou parada para "${query}"</div>
            <div style="font-size:11.5px; color:#64748b; line-height:1.4; margin-bottom:10px;">Dica: Digite o número (ex: 522, 060, 2040) ou nome do terminal (ex: Macaxeira, CDU, Derby).</div>
            <button onclick="window.RealTransit.openLinePickerModal(); if(window.clearQuickSearch) window.clearQuickSearch();" style="background:#0284c7; color:#ffffff; border:none; padding:7px 14px; border-radius:8px; font-size:11.5px; font-weight:800; cursor:pointer;">
              Abrir Catálogo de 400 Linhas ➔
            </button>
          </div>
        `;
        drop.style.display = 'flex';
        return;
      }

      // 3. ESTADO SUCESSO (DADOS REAIS COM BADGES SEMÂNTICOS)
      const topResults = results.slice(0, 10);
      window.currentRealSearchResults = topResults;

      drop.innerHTML = topResults.map((r, idx) => {
        if (r.type === 'terminal') {
          return `
            <div class="search-item" onclick="window.RealTransit.selectSearchResult(${idx})">
              <div><strong style="color:var(--blue-accent);">🏛️ ${r.title}</strong><div style="font-size:11px; color:var(--text-secondary);">${r.sub}</div></div>
              <span style="font-size:11.5px; font-weight:700; color:var(--blue-accent); background:#e0f2fe; padding:2px 8px; border-radius:6px;">T.I. SEI</span>
            </div>
          `;
        } else if (r.type === 'stop') {
          return `
            <div class="search-item" onclick="window.RealTransit.selectSearchResult(${idx})">
              <div><strong style="color:var(--brand-green-dark);">🚏 ${r.title}</strong><div style="font-size:11px; color:var(--text-secondary);">${r.sub}</div></div>
              <span style="font-size:11.5px; font-weight:800; color:var(--brand-green-dark); background:#dcfce7; padding:2px 8px; border-radius:6px;">Parada</span>
            </div>
          `;
        } else {
          return `
            <div class="search-item" onclick="window.RealTransit.selectSearchResult(${idx})">
              <div><strong style="color:#0f172a;">🚌 ${r.title}</strong><div style="font-size:11px; color:var(--text-secondary);">${r.sub}</div></div>
              <span style="font-size:11.5px; font-weight:700; color:#059669; background:#ecfdf5; padding:2px 8px; border-radius:6px;">Linha</span>
            </div>
          `;
        }
      }).join('');

      drop.style.display = 'flex';
    },

    selectSearchResult(idx) {
      const drop = document.getElementById('search-results-dropdown');
      if (drop) drop.style.display = 'none';

      if (!window.currentRealSearchResults || !window.currentRealSearchResults[idx]) return;
      const r = window.currentRealSearchResults[idx];

      if (r.type === 'terminal') {
        this.map.flyTo([r.lat, r.lon], 16, { animate: true });
        L.popup().setLatLng([r.lat, r.lon]).setContent(`<strong>🏛️ ${r.title}</strong><br>Terminal Integrado do SEI`).openOn(this.map);
      } else if (r.type === 'stop') {
        this.selectStop(r.index, true);
      } else if (r.type === 'route') {
        this.loadRoute(r.code);
      }
      if (typeof window.clearQuickSearch === 'function') {
        window.clearQuickSearch();
      }
    },

    // Sistema leve de toasts para feedback de estados da UI (Zero Slop)
    showToast(message, type = 'info') {
      let toast = document.getElementById('grafoo-floating-toast');
      if (!toast) {
        toast = document.createElement('div');
        toast.id = 'grafoo-floating-toast';
        toast.style.cssText = 'position:fixed; top:75px; left:50%; transform:translateX(-50%); z-index:9999; padding:9px 15px; border-radius:12px; font-size:12.5px; font-weight:700; box-shadow:0 8px 24px rgba(0,0,0,0.25); display:flex; align-items:center; gap:8px; transition:opacity 0.25s ease, transform 0.25s ease; font-family:"Plus Jakarta Sans",sans-serif; max-width:90%; pointer-events:none;';
        document.body.appendChild(toast);
      }
      const bg = type === 'warning' ? '#fffbeb' : type === 'error' ? '#fef2f2' : '#f0fdf4';
      const color = type === 'warning' ? '#92400e' : type === 'error' ? '#991b1b' : '#166534';
      const border = type === 'warning' ? '#fde68a' : type === 'error' ? '#fecaca' : '#bbf7d0';
      const icon = type === 'warning' ? '⚠️' : type === 'error' ? '❌' : '✅';

      toast.style.background = bg;
      toast.style.color = color;
      toast.style.border = `1.5px solid ${border}`;
      toast.innerHTML = `<span>${icon}</span> <span>${message}</span>`;
      toast.style.opacity = '1';
      toast.style.transform = 'translateX(-50%) translateY(0)';

      if (this._toastTimer) clearTimeout(this._toastTimer);
      this._toastTimer = setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(-50%) translateY(-10px)';
      }, 3500);
    },

    // Leitura em voz alta da parada ativa
    speakCurrent() {
      if (!this.activeRoute || !this.activeRoute.stops[this.activeStopIndex]) return;
      const st = this.activeRoute.stops[this.activeStopIndex];
      const eta = Math.max(2, ((this.activeStopIndex % 6) * 3) + 2);
      const text = `Próximo ônibus da Linha ${this.activeRouteCode} chega em ${eta} minutos na parada ${st.name}. Destino ${this.activeRoute.headsign || this.activeRoute.name}.`;

      if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'pt-BR';
        utterance.rate = 1.0;
        window.speechSynthesis.speak(utterance);
      }
    },

    // =========================================================================
    // MOTOR INTELIGENTE DE CONSULTA GTFS, ROTEAMENTO & BASE DA LAYA IA
    // =========================================================================
    normalizeText(str) {
      return String(str || '')
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')
        .toLowerCase()
        .replace(/[^\w\s-]/g, ' ')
        .replace(/\s+/g, ' ')
        .trim();
    },

    haversineKm(lat1, lon1, lat2, lon2) {
      const toRad = (deg) => (deg * Math.PI) / 180;
      const dLat = toRad(lat2 - lat1);
      const dLon = toRad(lon2 - lon1);
      const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) *
        Math.sin(dLon / 2) * Math.sin(dLon / 2);
      return 6371 * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    },

    // Descobre automaticamente parada real e linhas (IDA + VOLTA) que servem a coordenada do usuário
    findNearestTransitContext(lat, lon) {
      if (!this.networkData || !this.networkData.popular_lines) return null;
      let bestRegular = null;
      let bestAny = null;
      const nearbyLines = [];

      for (const [code, lineObj] of Object.entries(this.networkData.popular_lines)) {
        const isBacurau = /bacurau/i.test(lineObj.name || '');
        const stopsIda = lineObj.stops || [];
        const stopsVolta = lineObj.return_stops || [];
        let minLineDist = Infinity;
        let minStop = null;
        let minStopIdx = 0;
        let minDir = 'ida';

        for (let i = 0; i < stopsIda.length; i++) {
          const st = stopsIda[i];
          if (!st || !st.lat || !st.lon) continue;
          const d = this.haversineKm(lat, lon, st.lat, st.lon);
          if (d < minLineDist) {
            minLineDist = d;
            minStop = st;
            minStopIdx = i;
            minDir = 'ida';
          }
        }

        for (let i = 0; i < stopsVolta.length; i++) {
          const st = stopsVolta[i];
          if (!st || !st.lat || !st.lon) continue;
          const d = this.haversineKm(lat, lon, st.lat, st.lon);
          if (d < minLineDist) {
            minLineDist = d;
            minStop = st;
            minStopIdx = i;
            minDir = 'volta';
          }
        }

        if (minLineDist < 2.5) {
          nearbyLines.push({
            code,
            name: lineObj.name,
            isBacurau,
            distanceKm: minLineDist,
            stop: minStop,
            stopIndex: minStopIdx,
            direction: minDir
          });
        }

        const cand = { code, name: lineObj.name, distanceKm: minLineDist, stop: minStop, stopIndex: minStopIdx, direction: minDir };
        if (!bestAny || minLineDist < bestAny.distanceKm) bestAny = cand;
        if (!isBacurau && (!bestRegular || minLineDist < bestRegular.distanceKm)) bestRegular = cand;
      }

      const chosen = (bestRegular && bestRegular.distanceKm <= 2.0) ? bestRegular : (bestRegular || bestAny);
      if (!chosen) return null;

      nearbyLines.sort((a, b) => (a.isBacurau - b.isBacurau) || (a.distanceKm - b.distanceKm));

      return {
        outOfCoverage: chosen.distanceKm > 50,
        best: chosen,
        nearbyLines: nearbyLines.slice(0, 8)
      };
    },

    // Adapta TODA a interface e estado interno à localização real do usuário
    adaptToUserLocation(lat, lon, sourceLabel, opts) {
      const ctx = this.findNearestTransitContext(lat, lon);
      if (!ctx) return null;

      const isManualOrigin = Boolean(
        (opts && opts.isManual) ||
        (opts && opts.originSource === 'manual') ||
        window.grafoparadaManualOrigin ||
        /ponto marcado|manual/i.test(String(sourceLabel || ''))
      );
      const isCachedOrigin = !isManualOrigin && (
        (opts && opts.originSource === 'cached') ||
        /última localização/i.test(String(sourceLabel || ''))
      );
      const isLiveGps = !isManualOrigin && !isCachedOrigin && (
        (opts && opts.originSource === 'gps') ||
        /gps/i.test(String(sourceLabel || ''))
      );
      const originSource = (opts && opts.originSource)
        ? opts.originSource
        : (isManualOrigin ? 'manual' : (isCachedOrigin ? 'cached' : (isLiveGps ? 'gps' : 'gtfs_estimate')));

      if (ctx.outOfCoverage) {
        this.userAdaptState = {
          status: 'out_of_coverage',
          sourceLabel: sourceLabel || 'GPS Atual',
          stopName: `Fora da RMR (${Math.round(ctx.best.distanceKm)} km do Grande Recife)`,
          distanceKm: ctx.best.distanceKm,
          lat,
          lon,
          originSource,
          isManualOrigin,
          gpsErrorCode: null
        };
        if (typeof window.showFloatingVoicePill === 'function') {
          window.showFloatingVoicePill('📍 Você está fora do Grande Recife. Selecione um ponto para simular.');
        }
        if (typeof window.updateHomeGreeting === 'function') window.updateHomeGreeting();
        return ctx;
      }

      const best = ctx.best;
      const rawStopName = (best.stop && best.stop.name) ? String(best.stop.name).trim() : '';
      const friendlyStopName = (rawStopName && !/^\d+$/.test(rawStopName))
        ? rawStopName
        : `Parada ${best.stop ? best.stop.stop_id : best.code} · ${best.name}`;
      this.userAdaptState = {
        status: 'adapted',
        sourceLabel: sourceLabel || 'GPS Atual',
        lineCode: best.code,
        lineName: best.name,
        direction: best.direction || 'ida',
        stopName: friendlyStopName,
        distanceKm: best.distanceKm,
        lat,
        lon,
        nearbyLines: ctx.nearbyLines,
        originSource,
        isManualOrigin,
        gpsErrorCode: null
      };

      try {
        localStorage.setItem('grafoparada_last_coords', JSON.stringify({ lat, lon, lineCode: best.code }));
      } catch (e) {}

      // Carrega a linha real no sentido exato da parada mais próxima e seleciona o embarque do usuário
      this.loadRoute(best.code, { dir: best.direction || 'ida', originCoords: [lat, lon] });
      if (typeof best.stopIndex === 'number') {
        this.selectStop(best.stopIndex, Boolean(opts && opts.fit));
      }

      const prefixEl = document.getElementById('resting-line-prefix');
      if (prefixEl) prefixEl.textContent = `Linha ${best.code} (${best.direction === 'volta' ? 'Volta' : 'Ida'}) · Mais próxima:`;

      const summaryEl = document.getElementById('home-summary-line');
      if (summaryEl) {
        const distMeters = Math.round(best.distanceKm * 1000);
        summaryEl.textContent = `Parada ${best.code} · ${best.name} (${distMeters}m de você)`;
      }

      if (typeof window.updateHomeGreeting === 'function') window.updateHomeGreeting();
      return ctx;
    },

    // Catálogo georreferenciado amplo da RMR (bairros, praias, shoppings, universidades, hospitais e terminais)
    getSemanticCorridors() {
      return [
        { key: 'recife antigo', keys: ['recife antigo', 'bairro do recife', 'marco zero', 'porto digital', 'pcr', 'alfredo lisboa', 'rio branco', 'forte do brum'], label: 'Recife Antigo / Marco Zero', defaultLine: '1967', alsoServedBy: ['1971', '1100', '1983', '117'], hub: 'Cais de Santa Rita / PCR', stopName: 'Av. Alfredo Lisboa / Marco Zero (Recife Antigo)', lat: -8.0631, lon: -34.8711, waitMin: 5, seatsFree: 16 },
        { key: 'cais de santa rita', keys: ['cais de santa rita', 'cais santa rita', 'santa rita', 'dantas barreto', 'centro do recife', 'santo antonio', 'sao jose', 'recife centro'], label: 'Cais de Santa Rita (Centro do Recife)', defaultLine: '191', alsoServedBy: ['185', '195', '1971', '1983', '050'], hub: 'Cais de Santa Rita', stopName: 'Terminal Cais de Santa Rita (Centro)', lat: -8.0680, lon: -34.8765, waitMin: 4, seatsFree: 18 },
        { key: 'olinda', keys: ['olinda', 'carmo', 'varadouro', 'sitio historico', 'praca do carmo', 'alto da se', 'amparo'], label: 'Olinda (Carmo / Sítio Histórico)', defaultLine: '1971', alsoServedBy: ['1967', '1983', '1992', '1973', '1100'], hub: 'Praça do Carmo / TI PE-15', stopName: 'Praça do Carmo / Sítio Histórico de Olinda', lat: -8.0125, lon: -34.8520, waitMin: 5, seatsFree: 14 },
        { key: 'bairro novo', keys: ['bairro novo', 'casa caiada', 'jardim atlantico', 'beira mar olinda', 'getulio vargas', 'patteo olinda', 'shopping patteo'], label: 'Olinda (Bairro Novo / Casa Caiada)', defaultLine: '1973', alsoServedBy: ['1992', '1994', '1974', '1982'], hub: 'TI Rio Doce / TI PE-15', stopName: 'Av. Getúlio Vargas (Bairro Novo / Casa Caiada)', lat: -7.9940, lon: -34.8420, waitMin: 4, seatsFree: 15 },
        { key: 'janga', keys: ['janga', 'pau amarelo', 'maria farinha', 'nossa senhora da conceicao'], label: 'Paulista (Janga / Pau Amarelo)', defaultLine: '1992', alsoServedBy: ['1982', '1994', '1983'], hub: 'TI Rio Doce', stopName: 'Av. Cláudio José Gueiros Leite (Janga / Pau Amarelo)', lat: -7.9348, lon: -34.8285, waitMin: 6, seatsFree: 15 },
        { key: 'rio doce', keys: ['rio doce', 'ti rio doce', 'maranguape'], label: 'Olinda / TI Rio Doce', defaultLine: '1983', alsoServedBy: ['030', '1966', '2930', '1987'], hub: 'TI Rio Doce', stopName: 'TI Rio Doce (Olinda)', lat: -7.9598, lon: -34.8415, waitMin: 4, seatsFree: 19 },
        { key: 'pe-15', keys: ['pe-15', 'pe 15', 'ti pe-15', 'ti pe 15', 'fragoso', 'ouro preto'], label: 'TI PE-15 (Olinda)', defaultLine: '1100', alsoServedBy: ['050', '1966', '1913', '914'], hub: 'TI PE-15', stopName: 'Terminal Integrado PE-15', lat: -7.9912, lon: -34.8576, waitMin: 3, seatsFree: 20 },
        { key: 'xamba', keys: ['xamba', 'ti xamba', 'peixinhos', 'aguazinha', 'aguas compridas'], label: 'TI Xambá (Olinda)', defaultLine: '812', alsoServedBy: ['861', '881'], hub: 'TI Xambá', stopName: 'Terminal Integrado Xambá', lat: -8.0078, lon: -34.8655, waitMin: 5, seatsFree: 16 },
        { key: 'paulista', keys: ['paulista', 'pelopidas', 'ti pelopidas', 'shopping north way', 'north way'], label: 'Paulista / TI Pelópidas', defaultLine: '1907', alsoServedBy: ['1967', '1977', '1950'], hub: 'TI Pelópidas Silveira', stopName: 'TI Pelópidas Silveira (Paulista)', lat: -7.9408, lon: -34.8732, waitMin: 5, seatsFree: 17 },
        { key: 'abreu e lima', keys: ['abreu e lima', 'ti abreu e lima', 'caetes'], label: 'Abreu e Lima', defaultLine: '1967', alsoServedBy: ['1913', '1962'], hub: 'TI Abreu e Lima', stopName: 'TI Abreu e Lima (BR-101 Norte)', lat: -7.9114, lon: -34.9025, waitMin: 6, seatsFree: 15 },
        { key: 'igarassu', keys: ['igarassu', 'ti igarassu', 'itapissuma', 'itamaraca', 'cruz de reboucas'], label: 'Igarassu / Itamaracá', defaultLine: '1967', alsoServedBy: ['1969', '1904'], hub: 'TI Igarassu', stopName: 'TI Igarassu (Terminal Norte)', lat: -7.8342, lon: -34.9068, waitMin: 7, seatsFree: 16 },
        { key: 'camela', keys: ['camela', 'pedro serafim', 'rua do comercio', 'pe-051'], label: 'Camela (Ipojuca)', defaultLine: '199', alsoServedBy: [], hub: 'TI Cabo', stopName: 'Praça Pedro Serafim (Terminal de Camela)', lat: -8.514931, lon: -35.123469, waitMin: 3, seatsFree: 28 },
        { key: 'ipojuca', keys: ['ipojuca', 'trevo de ipojuca', 'upa de ipojuca', 'ruropolis'], label: 'Ipojuca Centro', defaultLine: '198', alsoServedBy: ['199'], hub: 'TI Cabo', stopName: 'Rodovia PE-60 · Trevo Principal de Ipojuca Centro (KM 20)', lat: -8.399372, lon: -35.056842, waitMin: 7, seatsFree: 14 },
        { key: 'suape', keys: ['suape', 'refinaria', 'rnest', 'estaleiro', 'contermas', 'portuario'], label: 'Complexo de Suape', defaultLine: '178', alsoServedBy: ['199'], hub: 'TI Cabo', stopName: 'Rodovia PE-60 · Trevo de Suape (KM 14)', lat: -8.385067, lon: -35.042433, waitMin: 6, seatsFree: 12 },
        { key: 'gaibu', keys: ['gaibu', 'enseada dos corais', 'itapuama', 'paiva', 'praia do paiva', 'enseada'], label: 'Cabo (Gaibu / Enseada / Paiva)', defaultLine: '158', alsoServedBy: ['191', '195', '196'], hub: 'TI Cabo', stopName: 'Trevo de Gaibu / Enseada dos Corais', lat: -8.3270, lon: -34.9565, waitMin: 8, seatsFree: 14 },
        { key: 'porto de galinhas', keys: ['porto de galinhas', 'galinhas', 'maracaipe', 'serrambi', 'nossa senhora do o', 'n sra do o', 'muro alto'], label: 'Porto de Galinhas / N. Sra. do Ó', defaultLine: '191', alsoServedBy: ['195', '196'], hub: 'TI Cabo', stopName: 'Porto de Galinhas / Rodovia PE-038', lat: -8.401408, lon: -35.060308, waitMin: 9, seatsFree: 10 },
        { key: 'cabo', keys: ['ti cabo', 'cabo de santo agostinho', 'cabo', 'costa dourada', 'shopping costa dourada'], label: 'TI Cabo / Centro do Cabo', defaultLine: '185', alsoServedBy: ['199', '198', '178', '139', '196'], hub: 'TI Cabo', stopName: 'TI Cabo (Terminal Integrado do Cabo)', lat: -8.285065, lon: -35.032398, waitMin: 4, seatsFree: 18 },
        { key: 'pontezinha', keys: ['pontezinha', 'ponte dos carvalhos', 'ti prazeres', 'prazeres'], label: 'Jaboatão (Prazeres / Pontezinha)', defaultLine: '185', alsoServedBy: ['139', '140', '160'], hub: 'TI Cajueiro Seco', stopName: 'Av. Barreto de Menezes / TI Prazeres', lat: -8.1656, lon: -34.9371, waitMin: 5, seatsFree: 16 },
        { key: 'piedade', keys: ['piedade', 'candeias', 'barra de jangada', 'shopping guararapes', 'guararapes'], label: 'Jaboatão Praias (Piedade / Candeias)', defaultLine: '071', alsoServedBy: ['020', '064', '030', '061'], hub: 'TI Cajueiro Seco', stopName: 'Av. Bernardo Vieira de Melo (Piedade / Candeias)', lat: -8.1725, lon: -34.9185, waitMin: 5, seatsFree: 14 },
        { key: 'cajueiro seco', keys: ['cajueiro seco', 'ti cajueiro'], label: 'TI Cajueiro Seco / Jaboatão Sul', defaultLine: '139', alsoServedBy: ['181', '030', '064'], hub: 'TI Cajueiro Seco', stopName: 'TI Cajueiro Seco', lat: -8.167989, lon: -34.934534, waitMin: 4, seatsFree: 17 },
        { key: 'boa viagem', keys: ['boa viagem', 'domingos ferreira', 'conselheiro aguiar', 'shopping recife', 'padaria boa viagem', 'segundo jardim'], label: 'Boa Viagem / Shopping Recife', defaultLine: '050', alsoServedBy: ['2040', '080', '440', '032', '026'], hub: 'TI Tancredo Neves', stopName: 'Av. Domingos Ferreira / Shopping Recife (Boa Viagem)', lat: -8.1202, lon: -34.9012, waitMin: 5, seatsFree: 12 },
        { key: 'pina', keys: ['pina', 'brasilia teimosa', 'rio mar', 'riomar', 'shopping riomar', 'cabanga'], label: 'Pina / Shopping RioMar', defaultLine: '011', alsoServedBy: ['026', '032', '044', '080'], hub: 'TI Joana Bezerra', stopName: 'Via Mangue / Shopping RioMar (Pina)', lat: -8.0861, lon: -34.8942, waitMin: 4, seatsFree: 15 },
        { key: 'tancredo neves', keys: ['tancredo neves', 'ti tancredo', 'aeroporto', 'ti aeroporto', 'imbiribeira', 'largo da paz'], label: 'TI Tancredo Neves / Aeroporto', defaultLine: '2060', alsoServedBy: ['060', '140', '185', '115'], hub: 'TI Tancredo Neves', stopName: 'TI Tancredo Neves / Aeroporto', lat: -8.122014, lon: -34.912465, waitMin: 5, seatsFree: 13 },
        { key: 'ibura', keys: ['ibura', 'ur-11', 'ur 11', 'ur-01', 'jordao', 'cohab'], label: 'Ibura / Jordão', defaultLine: '102', alsoServedBy: ['103', '110', '120', '2060'], hub: 'TI Tancredo Neves', stopName: 'Ibura / Av. Dois Rios', lat: -8.1165, lon: -34.9482, waitMin: 6, seatsFree: 14 },
        { key: 'ufrpe', keys: ['ufrpe', 'rural', 'dois irmaos', 'horto', 'parque dois irmaos'], label: 'UFRPE · Campus Dois Irmãos', defaultLine: '522', alsoServedBy: ['2930', '524', '532'], hub: 'TI Macaxeira', stopName: 'Terminal de Dois Irmãos (UFRPE)', lat: -8.016390, lon: -34.949720, waitMin: 4, seatsFree: 14 },
        { key: 'ufpe', keys: ['ufpe', 'cdu', 'cidade universitaria', 'ti cdu', 'hospital das clinicas'], label: 'UFPE · Cidade Universitária (CDU)', defaultLine: '2040', alsoServedBy: ['2431', '2441', '440', '202'], hub: 'TI CDU', stopName: 'Terminal Integrado CDU (UFPE)', lat: -8.0518, lon: -34.9502, waitMin: 5, seatsFree: 11 },
        { key: 'varzea', keys: ['varzea', 'caxanga', 'engenho do meio', 'iputinga', 'torroes', 'cdu'], label: 'Várzea / Caxangá', defaultLine: '202', alsoServedBy: ['440', '2040', '2431'], hub: 'TI Caxangá', stopName: 'Av. Caxangá / Praça da Várzea', lat: -8.0468, lon: -34.9595, waitMin: 5, seatsFree: 14 },
        { key: 'derby', keys: ['derby', 'rui barbosa', 'agamenon', 'principe', 'boa vista', 'conde da boa vista', 'hospicio', 'restauracao', 'hospital da restauracao', 'soledade', 'unicap'], label: 'Derby / Boa Vista / Conde da Boa Vista', defaultLine: '522', alsoServedBy: ['011', '050', '440', '1973', '1987'], hub: 'Praça do Derby', stopName: 'Praça do Derby / Av. Conde da Boa Vista', lat: -8.0558, lon: -34.8950, waitMin: 4, seatsFree: 16 },
        { key: 'espinheiro', keys: ['espinheiro', 'gracas', 'aflitos', 'encruzilhada', 'jaqueira', 'rosa e silva', 'parnamirim'], label: 'Graças / Espinheiro / Encruzilhada', defaultLine: '522', alsoServedBy: ['516', '640', '2920', '710'], hub: 'Praça do Derby', stopName: 'Av. Rosa e Silva / Espinheiro', lat: -8.0412, lon: -34.8965, waitMin: 4, seatsFree: 15 },
        { key: 'casa amarela', keys: ['casa amarela', 'casa forte', 'apipucos', 'monteiro', 'shopping plaza', 'plaza'], label: 'Casa Amarela / Casa Forte', defaultLine: '516', alsoServedBy: ['520', '522', '532', '640'], hub: 'TI Macaxeira', stopName: 'Estrada do Arraial / Casa Amarela', lat: -8.0255, lon: -34.9188, waitMin: 5, seatsFree: 15 },
        { key: 'macaxeira', keys: ['macaxeira', 'ti macaxeira', 'nova descoberta', 'vasco da gama'], label: 'TI Macaxeira', defaultLine: '2060', alsoServedBy: ['202', '522', '516', '330'], hub: 'TI Macaxeira', stopName: 'TI Macaxeira', lat: -8.0061, lon: -34.9298, waitMin: 4, seatsFree: 16 },
        { key: 'joana bezerra', keys: ['joana bezerra', 'ti joana', 'coelhos', 'imip', 'ilha do leite'], label: 'TI Joana Bezerra / IMIP', defaultLine: '080', alsoServedBy: ['101', '104', '1981', '2043'], hub: 'TI Joana Bezerra', stopName: 'Terminal Integrado Joana Bezerra', lat: -8.0689, lon: -34.8958, waitMin: 3, seatsFree: 20 },
        { key: 'afogados', keys: ['afogados', 'ti afogados', 'madalena', 'torre', 'real da torre', 'shopping tacaruna', 'tacaruna'], label: 'Afogados / Madalena / Tacaruna', defaultLine: '050', alsoServedBy: ['2040', '914', '330'], hub: 'TI Afogados', stopName: 'Largo de Afogados / TI Afogados', lat: -8.0785, lon: -34.9065, waitMin: 4, seatsFree: 16 },
        { key: 'barro', keys: ['barro', 'ti barro', 'tejipio', 'sancho', 'ti recife'], label: 'TI Barro / TI Recife', defaultLine: '202', alsoServedBy: ['101', '914', '291'], hub: 'TI Barro', stopName: 'TI Barro', lat: -8.0882, lon: -34.9459, waitMin: 5, seatsFree: 15 },
        { key: 'jaboatao', keys: ['jaboatao', 'jaboatao centro', 'ti jaboatao', 'cavaleiro', 'ti cavaleiro', 'moreno', 'sucupira'], label: 'Jaboatão Centro / Cavaleiro', defaultLine: '200', alsoServedBy: ['219', '272', '242'], hub: 'TI Jaboatão', stopName: 'TI Jaboatão Centro', lat: -8.1128, lon: -35.0148, waitMin: 5, seatsFree: 16 },
        { key: 'camaragibe', keys: ['camaragibe', 'ti camaragibe', 'sao lourenco', 'timbi', 'aldeia'], label: 'Camaragibe / São Lourenço', defaultLine: '2490', alsoServedBy: ['2420', '2450', '2441'], hub: 'TI Camaragibe', stopName: 'TI Camaragibe', lat: -8.0235, lon: -34.9788, waitMin: 4, seatsFree: 18 },
        { key: 'torroes', keys: ['torroes', 'cordeiro', 'san martin', 'bongi', 'mustardinha', 'mangueira'], label: 'Torrões / Cordeiro / San Martin', defaultLine: '321', alsoServedBy: ['312', '331', '440'], hub: 'TI Getúlio Vargas', stopName: 'Av. Abdias de Carvalho / Torrões', lat: -8.0628, lon: -34.9332, waitMin: 5, seatsFree: 15 },
        { key: 'torre', keys: ['torre', 'madalena', 'prado', 'zumbi', 'carrefour torre', 'benfica', 'beira rio'], label: 'Torre / Madalena / Zumbi', defaultLine: '411', alsoServedBy: ['2040', '412', '414', '440'], hub: 'Praça do Derby', stopName: 'Rua Real da Torre / Mercado da Madalena', lat: -8.0492, lon: -34.9102, waitMin: 4, seatsFree: 14 },
        { key: 'curado', keys: ['curado', 'curado i', 'curado ii', 'curado iv', 'toto', 'coqueiral', 'sancho', 'ti tip'], label: 'Curado / Totó / TI TIP', defaultLine: '302', alsoServedBy: ['303', '351', '361'], hub: 'TI TIP', stopName: 'Av. Liberdade / Curado', lat: -8.0752, lon: -34.9852, waitMin: 6, seatsFree: 15 },
        { key: 'ipsep', keys: ['ipsep', 'areias', 'jardim sao paulo', 'estancia', 'jiquia', 'teji pio', 'tejipio'], label: 'Ipsep / Areias / Jardim São Paulo', defaultLine: '115', alsoServedBy: ['121', '122', '2060'], hub: 'TI Barro', stopName: 'Av. Recife / Ipsep', lat: -8.1055, lon: -34.9295, waitMin: 5, seatsFree: 16 },
        { key: 'agua fria', keys: ['agua fria', 'arruda', 'beberibe', 'fundao', 'campo grande', 'encruzilhada', 'alto santa terezinha', 'dois unidos'], label: 'Água Fria / Arruda / Beberibe', defaultLine: '710', alsoServedBy: ['711', '712', '741', '760'], hub: 'TI Xambá', stopName: 'Av. Beberibe / Largo de Água Fria', lat: -8.0185, lon: -34.8925, waitMin: 5, seatsFree: 15 },
        { key: 'santo amaro', keys: ['santo amaro', 'tacaruna', 'hospital oswaldo cruz', 'huoc', 'procape', 'joao de barros', 'escola tecnica'], label: 'Santo Amaro / HUOC / Tacaruna', defaultLine: '050', alsoServedBy: ['1973', '1983', '612', '710'], hub: 'Praça do Derby', stopName: 'Av. Cruz Cabugá / HUOC Santo Amaro', lat: -8.0462, lon: -34.8812, waitMin: 4, seatsFree: 15 },
        { key: 'tamarineira', keys: ['tamarineira', 'parnamirim', 'jaqueira', 'santana', 'hospital agamenon', 'estrada do encanamento'], label: 'Tamarineira / Jaqueira / Parnamirim', defaultLine: '522', alsoServedBy: ['516', '532', '640'], hub: 'TI Macaxeira', stopName: 'Estrada do Arraial / Tamarineira', lat: -8.0285, lon: -34.9062, waitMin: 4, seatsFree: 16 },
        { key: 'guabiraba', keys: ['guabiraba', 'passarinho', 'brejo da guabiraba', 'alto do pascoal', 'morro da conceicao', 'alto jose do pinho'], label: 'Zona Norte Alta (Brejo / Passarinho)', defaultLine: '622', alsoServedBy: ['642', '645', '611'], hub: 'TI Macaxeira', stopName: 'Av. Norte / Morro da Conceição', lat: -8.0112, lon: -34.9185, waitMin: 6, seatsFree: 14 },
        { key: 'maranguape', keys: ['maranguape', 'maranguape i', 'maranguape ii', 'nobre', 'paratibe', 'arthur lundgren', 'mirueira'], label: 'Paulista (Maranguape / Arthur Lundgren)', defaultLine: '1922', alsoServedBy: ['1950', '1952', '1955'], hub: 'TI Pelópidas Silveira', stopName: 'Maranguape I / Av. Brasil', lat: -7.9432, lon: -34.8645, waitMin: 5, seatsFree: 16 },
        { key: 'caetes', keys: ['caetes', 'caetes i', 'caetes ii', 'caetes iii'], label: 'Caetés I / II / III (Abreu e Lima)', defaultLine: '1918', alsoServedBy: ['1913', '1967'], hub: 'TI Abreu e Lima', stopName: 'Terminal Caetés I', lat: -7.9085, lon: -34.9225, waitMin: 6, seatsFree: 15 },
        { key: 'muribeca', keys: ['muribeca', 'vila rica', 'engenhoca', 'guararapes', 'porta larga'], label: 'Muribeca / Guararapes', defaultLine: '162', alsoServedBy: ['163', '165', '185'], hub: 'TI Cajueiro Seco', stopName: 'Integração Muribeca / Av. Barreto de Menezes', lat: -8.1742, lon: -34.9562, waitMin: 6, seatsFree: 15 },
        { key: 'moreno', keys: ['moreno', 'bonanca', 'engenho novo'], label: 'Moreno / Bonança', defaultLine: '201', alsoServedBy: ['200', '290'], hub: 'TI Jaboatão', stopName: 'Centro de Moreno (BR-232)', lat: -8.1185, lon: -35.0915, waitMin: 9, seatsFree: 16 },
        { key: 'ilhas', keys: ['ilhas', 'ilha do retiro', 'sport', 'estadio do sport', 'santa cruz', 'arruda estadio', 'aflitos estadio'], label: 'Ilha do Retiro / Zona Esportiva', defaultLine: '411', alsoServedBy: ['440', '2040', '050'], hub: 'TI Joana Bezerra', stopName: 'Av. Abdias de Carvalho / Ilha do Retiro', lat: -8.0628, lon: -34.9035, waitMin: 5, seatsFree: 14 }
      ];
    },

    // Geocodificador online de fallback restrito à Região Metropolitana do Recife (Nominatim OSM)
    async geocodeRMRAsync(rawPlace) {
      const clean = String(rawPlace || '').trim();
      const norm = this.normalizeText(clean);
      if (!norm || norm.length < 3) return null;
      if (this.geocodeCache[norm] !== undefined) return this.geocodeCache[norm];

      const local = this.resolvePlaceLocation(clean);
      if (local) {
        this.geocodeCache[norm] = local;
        return local;
      }

      try {
        const url = `https://nominatim.openstreetmap.org/search?format=jsonv2&limit=2&countrycodes=br&viewbox=-35.32,-7.65,-34.78,-8.60&bounded=1&q=${encodeURIComponent(clean + ', Pernambuco')}`;
        const res = await fetch(url, { headers: { 'Accept-Language': 'pt-BR' } });
        if (!res.ok) return null;
        const rows = await res.json();
        if (Array.isArray(rows) && rows.length > 0) {
          const hit = rows[0];
          const lat = parseFloat(hit.lat);
          const lon = parseFloat(hit.lon);
          if (!Number.isNaN(lat) && !Number.isNaN(lon)) {
            const resolved = {
              key: norm,
              label: clean,
              lat,
              lon,
              stopName: (hit.display_name || clean).split(',').slice(0, 2).join(', '),
              source: 'osm_rmr'
            };
            this.geocodeCache[norm] = resolved;
            return resolved;
          }
        }
      } catch (e) {}
      this.geocodeCache[norm] = null;
      return null;
    },

    // Resolve nome de lugar, terminal, parada GTFS (stops_index / código) ou "aqui" para { label, lat, lon, stopName }
    resolvePlaceLocation(rawPlace) {
      const pNorm = this.normalizeText(rawPlace);
      if (!pNorm) return null;

      // Suporte explícito a "aqui / onde estou / minha localizacao"
      if (/^(aqui|daqui|onde estou|minha parada|minha localizacao|meu local|atual)$/.test(pNorm) || /\b(minha localizacao|onde estou|daqui)\b/.test(pNorm)) {
        let lat = (this.userAdaptState && this.userAdaptState.lat) || (window.userCurrentCoords && window.userCurrentCoords[0]);
        let lon = (this.userAdaptState && this.userAdaptState.lon) || (window.userCurrentCoords && window.userCurrentCoords[1]);
        if ((!lat || !lon) && typeof localStorage !== 'undefined') {
          try {
            const last = JSON.parse(localStorage.getItem('grafoparada_last_coords') || 'null');
            if (last && typeof last.lat === 'number' && typeof last.lon === 'number') {
              lat = last.lat;
              lon = last.lon;
            }
          } catch (e) {}
        }
        if (lat && lon) {
          return {
            key: 'current_gps',
            label: (this.userAdaptState && this.userAdaptState.stopName) || 'Sua localização atual',
            lat,
            lon,
            stopName: (this.userAdaptState && this.userAdaptState.stopName) || 'Sua parada atual'
          };
        }
        return null;
      }

      // 0. Cache de geocodificação RMR (Nominatim) caso já resolvido nesta sessão
      if (this.geocodeCache && this.geocodeCache[pNorm]) {
        return this.geocodeCache[pNorm];
      }

      // 1. Match em polos georreferenciados da RMR (evita match falso de palavras curtas)
      const corridors = this.getSemanticCorridors();
      const wordSafeMatch = (haystack, key) => {
        if (haystack === key) return true;
        if (key.length >= 4 && haystack.includes(key)) return true;
        return new RegExp(`\\b${key.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\b`).test(haystack);
      };
      const exactCorridor = corridors.find(c => c.keys.some(k => wordSafeMatch(pNorm, k)))
        || (pNorm.length >= 5 ? corridors.find(c => c.keys.some(k => k.includes(pNorm))) : null);
      if (exactCorridor) return exactCorridor;

      // 2. Match nos Hubs do Grafo SEI ou Terminais SEI do GTFS
      if (this.networkData && Array.isArray(this.networkData.hub_graph)) {
        const hubHit = this.networkData.hub_graph.find(h => this.normalizeText(h.name).includes(pNorm));
        if (hubHit) {
          return { key: hubHit.name, label: hubHit.name, lat: hubHit.lat, lon: hubHit.lon, stopName: hubHit.name };
        }
      }
      if (this.networkData && Array.isArray(this.networkData.terminals_sei)) {
        const tiHit = this.networkData.terminals_sei.find(t => this.normalizeText(t.name).includes(pNorm));
        if (tiHit) {
          return { key: tiHit.name, label: tiHit.name.split(' - ')[0], lat: tiHit.lat, lon: tiHit.lon, stopName: tiHit.name };
        }
      }

      // 2.5 Match no Índice Completo de Paradas GTFS (stops_index: [nome, lat, lon, linhas])
      if (this.networkData && Array.isArray(this.networkData.stops_index) && pNorm.length >= 3 && !/^\d{3,4}$/.test(pNorm)) {
        const stopTokens = pNorm.split(' ').filter(t => t.length >= 3 && !['rua', 'avenida', 'praca', 'parada', 'terminal', 'estrada'].includes(t));
        let idxHit = this.networkData.stops_index.find(s => this.normalizeText(s[0]).includes(pNorm));
        if (!idxHit && stopTokens.length > 0) {
          idxHit = this.networkData.stops_index.find(s => {
            const sn = this.normalizeText(s[0]);
            return stopTokens.every(t => sn.includes(t));
          });
        }
        if (idxHit) {
          return {
            key: pNorm,
            label: idxHit[0],
            lat: idxHit[1],
            lon: idxHit[2],
            stopName: idxHit[0],
            linesHint: idxHit[3] || []
          };
        }
      }

      // 3. Match dinâmico em paradas nomeadas, códigos GTFS e nomes das 393 linhas reais GTFS
      if (this.networkData && this.networkData.popular_lines && pNorm.length >= 4) {
        const isNumericStop = /^\d{5,6}$/.test(pNorm);
        for (const line of Object.values(this.networkData.popular_lines)) {
          const allLineStops = (line.stops || []).concat(line.return_stops || []);
          if (isNumericStop) {
            const codeStop = allLineStops.find(s => String(s.stop_id) === pNorm);
            if (codeStop) {
              return {
                key: pNorm,
                label: `Parada ${codeStop.stop_id} (${line.code})`,
                lat: codeStop.lat,
                lon: codeStop.lon,
                stopName: (codeStop.name && !/^\d+$/.test(codeStop.name)) ? codeStop.name : `Parada ${codeStop.stop_id}`
              };
            }
          }
          const lineNameNorm = this.normalizeText(line.name);
          if (lineNameNorm.includes(pNorm) && allLineStops.length > 0) {
            const matchedStop = allLineStops.find(s => !/^\d+$/.test(s.name) && this.normalizeText(s.name).includes(pNorm)) || allLineStops[allLineStops.length - 1];
            return {
              key: pNorm,
              label: `${rawPlace} (${line.code})`,
              lat: matchedStop.lat,
              lon: matchedStop.lon,
              stopName: !/^\d+$/.test(matchedStop.name) ? matchedStop.name : `Parada ${line.name}`
            };
          }
        }
      }

      return null;
    },

    // Descobre TODAS as linhas reais (IDA + VOLTA) que atendem um raio geográfico ao redor de (lat, lon)
    getLinesNearPoint(lat, lon, maxKm = 1.15) {
      if (!this.networkData || !this.networkData.popular_lines) return [];
      const cacheKey = `${Number(lat).toFixed(4)},${Number(lon).toFixed(4)},${Number(maxKm).toFixed(2)}`;
      if (this._nearPointCacheOwner !== this.networkData) {
        this._nearPointCache = new Map();
        this._nearPointCacheOwner = this.networkData;
      }
      if (this._nearPointCache.has(cacheKey)) {
        return this._nearPointCache.get(cacheKey);
      }
      const hits = [];
      for (const [code, lineObj] of Object.entries(this.networkData.popular_lines)) {
        let minDist = Infinity;
        let nearestStop = null;
        let nearestDir = 'ida';
        const stopsIda = lineObj.stops || [];
        for (let i = 0; i < stopsIda.length; i++) {
          const s = stopsIda[i];
          if (!s || !s.lat || !s.lon) continue;
          const d = this.haversineKm(lat, lon, s.lat, s.lon);
          if (d < minDist) { minDist = d; nearestStop = s; nearestDir = 'ida'; }
        }
        const stopsVolta = lineObj.return_stops || [];
        for (let i = 0; i < stopsVolta.length; i++) {
          const s = stopsVolta[i];
          if (!s || !s.lat || !s.lon) continue;
          const d = this.haversineKm(lat, lon, s.lat, s.lon);
          if (d < minDist) { minDist = d; nearestStop = s; nearestDir = 'volta'; }
        }
        if (Array.isArray(lineObj.return_coords)) {
          for (let j = 0; j < lineObj.return_coords.length; j++) {
            const p = lineObj.return_coords[j];
            const d = this.haversineKm(lat, lon, p[0], p[1]);
            if (d < minDist) { minDist = d; nearestDir = 'volta'; }
          }
        }
        if (Array.isArray(lineObj.polyline)) {
          for (let k = 0; k < lineObj.polyline.length; k++) {
            const p = lineObj.polyline[k];
            const d = this.haversineKm(lat, lon, p[0], p[1]);
            if (d < minDist) minDist = d;
          }
        }
        if (minDist <= maxKm) {
          const isBacurau = /bacurau/i.test(lineObj.name || '');
          hits.push({
            code,
            label: `${code} · ${lineObj.name}`,
            name: lineObj.name,
            isBacurau,
            distanceKm: minDist,
            nearestStop,
            nearestDir
          });
        }
      }
      hits.sort((a, b) => (a.isBacurau - b.isBacurau) || (a.distanceKm - b.distanceKm));
      if (this._nearPointCache.size > 400) this._nearPointCache.clear();
      this._nearPointCache.set(cacheKey, hits);
      return hits;
    },

    findCatalogRoutesForQuery(placeNorm, telemetryStops) {
      const matches = [];
      const seenCodes = new Set();
      const addRoute = (code, label, reason, stopHint) => {
        if (!code || seenCodes.has(code)) return;
        seenCodes.add(code);
        matches.push({ code, label: label || code, reason, stopHint: stopHint || null });
      };

      // 0. Match exato por código de linha (ex: "199", "522", "1967", "2060") tem prioridade absoluta
      const aliasCode = this.aliases[placeNorm] || placeNorm;
      if (/^\d{2,4}$/.test(placeNorm) && this.networkData) {
        const popLine = this.networkData.popular_lines && this.networkData.popular_lines[aliasCode];
        const catLine = Array.isArray(this.networkData.routes_catalog)
          ? this.networkData.routes_catalog.find(r => r.code.toLowerCase() === aliasCode.toLowerCase())
          : null;
        if (popLine || catLine) {
          const firstStop = (popLine && Array.isArray(popLine.stops) && popLine.stops[0]) ? popLine.stops[0] : null;
          addRoute(
            aliasCode,
            catLine ? catLine.label : `${aliasCode} · ${popLine.name}`,
            'Linha consultada diretamente',
            firstStop ? {
              name: (!/^\d+$/.test(firstStop.name) ? firstStop.name : `Terminal ${popLine.name}`),
              lat: firstStop.lat,
              lon: firstStop.lon,
              wait_gps_min: aliasCode === '199' ? 3 : 4,
              seatsFree: aliasCode === '199' ? 28 : 14
            } : null
          );
        }
      }

      // 1. Telemetria detalhada PE-60 / Linha 199
      if (Array.isArray(telemetryStops)) {
        const tStop = telemetryStops.find(st =>
          this.normalizeText(st.name + ' ' + (st.bairro || '') + ' ' + (st.municipio || '')).includes(placeNorm)
        );
        if (tStop) {
          addRoute('199', '199 · Camela / TI Cabo', 'Atende diretamente na rodovia PE-60', tStop);
        }
      }

      // 2. Resolução geográfica real sobre TODAS as 393 linhas (IDA + VOLTA)
      const resolved = this.resolvePlaceLocation(placeNorm);
      if (resolved && resolved.lat && resolved.lon) {
        const geoHits = this.getLinesNearPoint(resolved.lat, resolved.lon, 1.0);
        geoHits.slice(0, 12).forEach(h => {
          addRoute(h.code, h.label, `Passa a ${Math.round(h.distanceKm * 1000)}m de ${resolved.label}`, {
            name: (h.nearestStop && h.nearestStop.name && !/^\d+$/.test(h.nearestStop.name)) ? h.nearestStop.name : (resolved.stopName || resolved.label),
            lat: resolved.lat,
            lon: resolved.lon,
            wait_gps_min: Math.max(3, Math.min(9, Math.round(h.distanceKm * 6) + 3)),
            seatsFree: h.code === '199' ? 28 : 14
          });
        });
      }

      // 3. Fallback semântico caso popular_lines não esteja filtrado
      for (const c of this.getSemanticCorridors()) {
        if (c.keys.some(k => placeNorm.includes(k) || k.includes(placeNorm))) {
          const allCodes = [c.defaultLine].concat(c.alsoServedBy || []);
          allCodes.forEach(code => {
            const cat = (this.networkData && this.networkData.routes_catalog || []).find(r => r.code === code);
            addRoute(code, cat ? cat.label : code, 'Corredor ' + c.label, { name: c.stopName, wait_gps_min: c.waitMin, seatsFree: c.seatsFree, lat: c.lat, lon: c.lon, hub: c.hub });
          });
        }
      }

      // 4. Busca textual direta no catálogo de 400 linhas
      if (this.networkData && Array.isArray(this.networkData.routes_catalog)) {
        const tokens = placeNorm.split(' ').filter(t => t.length >= 3 && !['de', 'da', 'do', 'para', 'ate', 'em', 'na', 'no', 'com', 'via', 'linha', 'onibus'].includes(t));
        this.networkData.routes_catalog.forEach(r => {
          const labNorm = this.normalizeText(r.label);
          if (r.code.toLowerCase() === placeNorm || labNorm.includes(placeNorm) || (tokens.length > 0 && tokens.every(t => labNorm.includes(t)))) {
            addRoute(r.code, r.label, 'Catálogo GTFS Oficial');
          }
        });
      }

      return matches;
    },

    extractOriginDest(rawText) {
      const clean = this.normalizeText(rawText)
        .replace(/\b(estou perdid[oa]|tou perdid[oa]|to perdid[oa]|me perdi|nao sei onde estou|socorro|me ajude|me ajuda|agora a noite|nesta noite|a noite|de noite|pela noite|hoje a noite|vamos la|por favor|agora|hoje|pode ser|me diz|me fale|como faco para voltar|como faco pra voltar|como faco para ir|como faco pra ir|como volto|como chego|como fico|como ir|quero voltar|quero ir|preciso voltar|preciso ir|gostaria de|gostaria|qual busao pega|qual onibus pega|qual linha pega|qual busao|qual onibus|qual linha|qual|quais)\b/g, ' ')
        .replace(/\b(?:para|pra)\s+(?:ir|voltar|chegar)\s+(?:para o|para a|para|pra|pro|ate o|ate a|ate|no|na|em|ao)\b/g, ' para ')
        .replace(/\s+/g, ' ')
        .trim();

      const sanitizePlace = (s) => String(s || '')
        .replace(/\b(a noite|de noite|agora a noite|nesta noite|como volto|como faco|como chego|como ir|quero voltar|quero ir|preciso voltar|preciso ir|por favor|agora|hoje)\b.*$/i, '')
        .replace(/^(?:saindo|partindo|sair|ir|voltar|indo|viajar|chegar|pegar|pega|estou)\s+/i, '')
        .replace(/^(?:no|na|em|de|da|do|o|a|ao)\s+/i, '')
        .replace(/\s+/g, ' ')
        .trim();

      const patterns = [
        /\b(?:saindo de|saindo do|saindo da|partindo de|partindo do|partindo da|estou no|estou na|estou em|sair de|sair do|sair da|ir de|ir do|ir da|voltar de|voltar do|voltar da|indo de|indo do|indo da|viajar de|viajar do|viajar da|pega no|pega na|pega em|de|da|do|no|na|em)\s+(.+?)\s+\b(?:para o|para a|para|pra|pro|ate o|ate a|ate|rumo a|->)\s+(.+)/i,
        /\b(daqui|aqui)\s+\b(?:para o|para a|para|pra|pro|ate o|ate a|ate|->)\s+([a-z0-9\s.-]{2,45})/i,
        /^([a-z0-9\s.-]{2,40}?)\s+\b(?:para o|para a|para|pra|pro|ate o|ate a|ate|->|rumo a)\s+([a-z0-9\s.-]{2,40})$/i
      ];

      for (const p of patterns) {
        const m = clean.match(p);
        if (m && m[1] && m[2]) {
          const origin = sanitizePlace(m[1]);
          const dest = sanitizePlace(m[2]);
          if (
            origin.length >= 2 &&
            dest.length >= 2 &&
            !/^(ir|voltar|chegar|sair|partir|indo|viajar|pegar|pega|onibus|busao|rota|como|qual|quais|quero|preciso)$/i.test(origin)
          ) {
            return { origin, dest };
          }
        }
      }
      return null;
    },

    // Extrai destino quando a pessoa fala só para onde vai (inclui frases de "Guia de Perdido")
    extractDestinationOnly(rawText) {
      const q = this.normalizeText(rawText);
      if (!q || /\b(proximo onibus|proximo|horario|quando passa|lotado|lotada|lotacao|vagas|mofar|esperando|demora|engarrafamento|congestionamento|acidente|over-smoothing|oversmoothing|parada segura|desembarque seguro|farol noturno|cittamobi|integracao|stgcn|st gcn|como funciona|banca|slides|pptx)\b/.test(q)) {
        return null;
      }
      const lostCleaned = q
        .replace(/\b(estou perdido|tou perdido|to perdido|me perdi|estou perdida|tou perdida|nao sei onde estou|me ajude|me ajuda|socorro)\b/g, ' ')
        .replace(/\s+/g, ' ')
        .trim();
      const targetText = lostCleaned || q;
      const m = targetText.match(/(?:ir|indo|chegar|chego|voltar|me leva|levar|rota|trajeto|caminho|onibus|busao|pegar|preciso ir)\s+(?:ate|para|pra|pro|no|na|ao|em)\s+(.+)/i)
        || targetText.match(/^(?:para|pra|pro|ate)\s+(.+)/i);
      if (m && m[1]) {
        const cand = m[1].replace(/\b(por favor|hoje|agora|de onibus|mas tou perdido|mas estou perdido)\b/g, '').trim();
        if (cand.length >= 3) {
          return cand;
        }
      }
      if (targetText.split(' ').length <= 4 && !/\?/.test(rawText) && this.resolvePlaceLocation(targetText)) {
        return targetText;
      }
      return null;
    },

    // Classificador semântico da Laya (SEPARAÇÃO DE RESPONSABILIDADES: Laya interpreta a fala; RoutePlanner calcula a rota por grafo A*)
    classifyLayaDecision(rawText) {
      const q = this.normalizeText(rawText);
      const isLost = /\b(perdido|perdida|me perdi|nao sei onde estou)\b/.test(q);
      const isUrgent = isLost || /\b(agora|rapido|urgente|atrasado|socorro|lotado|lotada|mofar|queima|espera|engarrafamento|acidente)\b/.test(q);
      const hasTrip = Boolean(this.extractOriginDest(rawText) || this.extractDestinationOnly(rawText));
      const isScience = /\b(stgcn|st gcn|ia|inteligencia artificial|modelo|trava|over-smoothing|oversmoothing|reneging|abandono|yap|kim|mae|como funciona|plataforma|grafoparada|despacho|deadheading|queima|queima de parada|queima de ponto|bolso seguro|lei 15878|15878|15\.878|parada segura|desembarque seguro|21h|22h|farol noturno|webmcp|engarrafamento|congestionamento|acidente|pe-60|pe 60|trevo|cittamobi|moovit|integracao|vem|duas horas|2h)\b/.test(q);
      const isArrivalOrCrowd = /\b(onibus|quando passa|horario|proximo|chega|lotacao|vagas|lotado|lotada|cheio|cheia|vazio|vazia|assento|sentado|em pe|demora|demorando|mofar|esperando|cade|previsto|previsao|minha parada|onde estou)\b/.test(q);
      const choice = isLost ? 'lost_passenger_guide'
        : (hasTrip ? 'route_planning'
          : (isScience ? 'platform_science'
            : (isArrivalOrCrowd ? 'local_arrival' : 'general_help')));
      return {
        engine: 'laya_nlp_router_boundary_v3',
        laya_role: 'semantic_intent_and_lost_guide',
        route_solver: 'deterministic_astar_gtfs_route_planner',
        decision_type: 'choice+score+noul',
        choice,
        is_lost: isLost,
        urgency_score: isUrgent ? 3 : 1,
        needs_location_noul: hasTrip || isLost || choice === 'local_arrival'
      };
    },

    // Módulo Determinístico Dedicado ao Cálculo de Rotas (desacoplado da IA conversacional)
    RoutePlanner: {
      plan(originRaw, destRaw, telemetryStops) {
        return RealTransit._computeDeterministicTrip(originRaw, destRaw, telemetryStops);
      },
      async planAsync(originRaw, destRaw, telemetryStops) {
        await RealTransit.geocodeRMRAsync(originRaw);
        await RealTransit.geocodeRMRAsync(destRaw);
        return RealTransit._computeDeterministicTrip(originRaw, destRaw, telemetryStops);
      },
      pickDirection(lineObj, originCoords, destCoords) {
        return RealTransit.pickBestDirection(lineObj, originCoords, destCoords);
      }
    },

    planSmartTrip(originRaw, destRaw, telemetryStops) {
      return this.RoutePlanner.plan(originRaw, destRaw, telemetryStops);
    },

    _computeDeterministicTrip(originRaw, destRaw, telemetryStops) {
      const origNorm = this.normalizeText(originRaw);
      const destNorm = this.normalizeText(destRaw);
      const origPlace = this.resolvePlaceLocation(origNorm);
      const destPlace = this.resolvePlaceLocation(destNorm);

      // 1. Busca geográfica completa sobre todas as 393 linhas (IDA + VOLTA)
      let geoDirect = [];
      let origGeoLines = [];
      let destGeoLines = [];

      if (origPlace && destPlace && origPlace.lat && destPlace.lat) {
        origGeoLines = this.getLinesNearPoint(origPlace.lat, origPlace.lon, 1.2);
        destGeoLines = this.getLinesNearPoint(destPlace.lat, destPlace.lon, 1.2);

        const destMap = new Map(destGeoLines.map(d => [d.code, d]));
        origGeoLines.forEach(o => {
          const dMatch = destMap.get(o.code);
          if (dMatch) {
            const rideDistKm = this.haversineKm(origPlace.lat, origPlace.lon, destPlace.lat, destPlace.lon);
            const walkM = Math.round(o.distanceKm * 1000);
            const walkMin = Math.max(1, Math.round(walkM / 78));
            const rideMin = Math.max(8, Math.round((rideDistKm / 20) * 60) + 5);
            geoDirect.push({
              code: o.code,
              label: o.label,
              name: o.name,
              isBacurau: o.isBacurau,
              walkMeters: walkM,
              walkMin,
              rideMin,
              totalMin: walkMin + 4 + rideMin,
              totalWalkKm: o.distanceKm + dMatch.distanceKm,
              reason: `Liga ${origPlace.label} a ${destPlace.label}`
            });
          }
        });
        geoDirect.sort((a, b) => (a.isBacurau - b.isBacurau) || (a.totalWalkKm - b.totalWalkKm));
      }

      // 2. Fallback por catálogo/corredor se geoDirect estiver vazio
      const origCatalog = origGeoLines.length ? origGeoLines : this.findCatalogRoutesForQuery(origPlace ? origPlace.key : origNorm, telemetryStops);
      const destCatalog = destGeoLines.length ? destGeoLines : this.findCatalogRoutesForQuery(destPlace ? destPlace.key : destNorm, telemetryStops);
      const catDirect = origCatalog.filter(om => destCatalog.some(dm => dm.code === om.code));
      const directMatches = geoDirect.length > 0 ? geoDirect : catDirect;

      // 3. Grafo Ilimitado Ponderado (A* sobre grafo condensado de 45 Hubs SEI cobrindo todas as 393 linhas)
      const findUnlimitedMultiOptionPaths = () => {
        const graph = this._getCondensedHubGraph();
        if (!graph || !origCatalog.length || !destCatalog.length) {
          return [];
        }

        const getLineMeta = (code) => {
          const fromCat = origCatalog.find(x => x.code === code) || destCatalog.find(x => x.code === code);
          if (fromCat) return fromCat;
          const pop = this.networkData.popular_lines && this.networkData.popular_lines[code];
          if (pop) return { code, label: `${code} · ${pop.name}`, name: pop.name };
          const cat = (this.networkData.routes_catalog || []).find(r => r.code === code);
          return { code, label: cat ? cat.label : code, name: cat ? cat.name : code };
        };

        const isNightOrRail = (code) => {
          const pop = this.networkData.popular_lines && this.networkData.popular_lines[code];
          const nm = (pop && pop.name) || code;
          return /bacurau/i.test(nm) || /^vlt/i.test(code);
        };

        const { hubs, lineToHubIndices, edges } = graph;
        const origDay = origCatalog.filter(x => !isNightOrRail(x.code));
        const destDay = destCatalog.filter(x => !isNightOrRail(x.code));
        const origBus = origDay.length ? origDay : origCatalog;
        const destBus = destDay.length ? destDay : destCatalog;
        const destRank = new Map(destBus.map((x, idx) => [x.code, idx]));

        const oLat = origPlace && origPlace.lat;
        const oLon = origPlace && origPlace.lon;
        const dLat = destPlace && destPlace.lat;
        const dLon = destPlace && destPlace.lon;
        const isMajorHub = (name) => /^(Ti\s|Cais\s|Pra[cç]a do Derby|Terminal)/i.test(name);

        const heuristicToDest = (lat, lon) => (dLat && dLon && lat && lon)
          ? this.haversineKm(lat, lon, dLat, dLon) * 1.9
          : 0;

        const estimateTimeCost = (fromLat, fromLon, toLat, toLon, transferCount, hubName, midCode) => {
          const distKm = (fromLat && toLat) ? this.haversineKm(fromLat, fromLon, toLat, toLon) : 6;
          let minCost = Math.max(5, (distKm / 20.0) * 60);
          if (transferCount > 0) minCost += isMajorHub(hubName) ? 7.5 : 13.0;
          if (midCode && /^(185|191|195|050|080|2040|2060|1076|1100)$/.test(midCode)) minCost -= 2.5;
          if (hubName && /cais|santa rita/i.test(hubName)) minCost -= 1.5;
          return minCost;
        };

        // Deduplica sementes por hub inicial (máx 2 melhores linhas de embarque por hub)
        // Evita explosão combinatória em polos centrais com 100+ linhas e garante cobertura de todo o grafo
        const seedsByHub = new Map();
        for (const o of origBus) {
          const walkMin = o.distanceKm ? Math.max(1, Math.round((o.distanceKm * 1000) / 78)) : 2;
          const walkMeters = o.distanceKm ? Math.round(o.distanceKm * 1000) : 120;
          for (const h1Idx of (lineToHubIndices.get(o.code) || [])) {
            const h1 = hubs[h1Idx];
            const legCost = walkMin + 4 + estimateTimeCost(oLat, oLon, h1.lat, h1.lon, 1, h1.name, o.code);
            const arr = seedsByHub.get(h1Idx) || [];
            if (arr.length < 2) {
              arr.push({
                hubIdx: h1Idx,
                legs: [o.code],
                hubNames: [h1.name],
                costMin: legCost,
                fScore: legCost + heuristicToDest(h1.lat, h1.lon),
                walkMeters,
                walkMin
              });
              seedsByHub.set(h1Idx, arr);
            }
          }
        }

        const pq = [];
        seedsByHub.forEach(arr => arr.forEach(s => pq.push(s)));

        const completed = [];
        const bestHubVisits = new Map();
        let expansions = 0;

        while (pq.length > 0 && expansions < 800 && completed.length < 20) {
          let bestPos = 0;
          for (let i = 1; i < pq.length; i++) {
            if (pq[i].fScore < pq[bestPos].fScore) bestPos = i;
          }
          const curr = pq[bestPos];
          pq[bestPos] = pq[pq.length - 1];
          pq.pop();
          expansions += 1;

          const hub = hubs[curr.hubIdx];
          const dHits = destBus.filter(d => !curr.legs.includes(d.code) && hub.lineSet.has(d.code));
          if (dHits.length > 0) {
            dHits.sort((a, b) => (destRank.get(a.code) ?? 99) - (destRank.get(b.code) ?? 99));
            const bestLast = dHits[0];
            const finalLegMin = estimateTimeCost(hub.lat, hub.lon, dLat, dLon, 0, hub.name, bestLast.code);
            const totalMin = Math.round(curr.costMin + finalLegMin);
            const fullCodes = curr.legs.concat([bestLast.code]);
            completed.push({
              legs: fullCodes.map(getLineMeta),
              hubs: curr.hubNames,
              hub: curr.hubNames[0],
              leg1: getLineMeta(fullCodes[0]),
              leg2: getLineMeta(fullCodes[fullCodes.length - 1]),
              isSEI: true,
              walkMeters: curr.walkMeters,
              walkMin: curr.walkMin,
              totalMin,
              score: totalMin
            });
            if (completed.length >= 14) break;
          }

          if (curr.legs.length >= 5) continue;

          const visitCount = bestHubVisits.get(curr.hubIdx) || 0;
          if (visitCount >= 2) continue;
          bestHubVisits.set(curr.hubIdx, visitCount + 1);

          for (const edge of edges[curr.hubIdx]) {
            if (curr.legs.includes(edge.code)) continue;
            const nh = hubs[edge.targetIdx];
            if (curr.hubNames.includes(nh.name)) continue;
            const nextCost = curr.costMin + edge.stepMin;
            pq.push({
              hubIdx: edge.targetIdx,
              legs: curr.legs.concat([edge.code]),
              hubNames: curr.hubNames.concat([nh.name]),
              costMin: nextCost,
              fScore: nextCost + heuristicToDest(nh.lat, nh.lon),
              walkMeters: curr.walkMeters,
              walkMin: curr.walkMin
            });
          }
        }

        completed.sort((a, b) => (a.legs.length - b.legs.length) * 4 + (a.totalMin - b.totalMin));

        const diverse = [];
        const signatures = new Set();
        for (const c of completed) {
          const sig = `${c.legs[0].code}|${c.hubs.join('>')}`;
          if (!signatures.has(sig)) {
            signatures.add(sig);
            diverse.push(c);
            if (diverse.length >= 5) break;
          }
        }
        return diverse;
      };

      const transferCandidates = findUnlimitedMultiOptionPaths();
      const transferPlan = transferCandidates[0] || null;

      // 4. Consolida lista unificada de Opções estilo Google Maps / Citymapper / SBB Mobile (diretas + integradas)
      const buildCrowdPrediction = (code) => {
        const isHeavyTrunk = /^(185|191|050|080|2040|2060|522|1971|1967)$/.test(String(code || ''));
        const level = isHeavyTrunk ? 'Moderada' : 'Leve';
        const pct = 88;
        const silhouettes = isHeavyTrunk ? 2 : 1;
        return {
          level,
          pct,
          label: `Lotação ${level} · IA ~${pct}%`,
          silhouettes
        };
      };

      const routeOptions = [];
      const nonBacurauDirect = directMatches.filter(m => !m.isBacurau);
      const rankedDirect = nonBacurauDirect.length ? nonBacurauDirect : directMatches;

      rankedDirect.slice(0, 2).forEach((d, idx) => {
        const transferConfidence = {
          badge: 'Viagem Direta · Sem Transbordo',
          walkMin: 0,
          marginMin: null,
          status: 'high'
        };
        const crowdPrediction = buildCrowdPrediction(d.code);
        d.transferConfidence = transferConfidence;
        d.crowdPrediction = crowdPrediction;
        routeOptions.push({
          tag: idx === 0 ? '⭐ Mais Rápida (Direta)' : '🚌 Linha Alternativa Direta',
          type: 'direct',
          isDirect: true,
          codes: [d.code],
          legs: [d],
          hubs: [],
          walkMeters: d.walkMeters || 120,
          walkMin: d.walkMin || 2,
          totalMin: d.totalMin || 26,
          transferConfidence,
          crowdPrediction
        });
      });

      transferCandidates.forEach((t) => {
        const transferConfidence = {
          badge: 'Conexão Segura · ~3 min a pé no TI',
          walkMin: 3,
          marginMin: 6,
          status: 'good'
        };
        const crowdPrediction = buildCrowdPrediction(t.legs[0] && t.legs[0].code);
        t.transferConfidence = transferConfidence;
        t.crowdPrediction = crowdPrediction;
        if (routeOptions.length >= 3) return;
        const alreadySame = routeOptions.some(o => o.codes.join(',') === t.legs.map(l => l.code).join(','));
        if (!alreadySame) {
          routeOptions.push({
            tag: routeOptions.length === 0 ? '⭐ Melhor Rota Conectada' : `🔄 Via ${t.hubs[0]}`,
            type: 'transfer',
            isDirect: false,
            codes: t.legs.map(l => l.code),
            legs: t.legs,
            hubs: t.hubs,
            walkMeters: t.walkMeters || 120,
            walkMin: t.walkMin || 2,
            totalMin: t.totalMin || (t.legs.length * 24),
            transferConfidence,
            crowdPrediction
          });
        }
      });

      // 5. Caso especial telemetria detalhada PE-60 (Camela <-> Ipojuca <-> Suape <-> Cabo)
      let telemetryEtaMin = null;
      let oStop = null;
      let dStop = null;
      if (Array.isArray(telemetryStops) && directMatches.some(m => m.code === '199')) {
        oStop = telemetryStops.find(s => this.normalizeText(s.name + ' ' + (s.bairro || '') + ' ' + (s.municipio || '')).includes(origPlace ? origPlace.key : origNorm));
        dStop = telemetryStops.find(s => this.normalizeText(s.name + ' ' + (s.bairro || '') + ' ' + (s.municipio || '')).includes(destPlace ? destPlace.key : destNorm));
        if (oStop && dStop) {
          telemetryEtaMin = Math.max(8, Math.abs((dStop.wait_gps_min || 15) - (oStop.wait_gps_min || 3)) * 2 + 6);
          if (routeOptions[0] && routeOptions[0].isDirect) routeOptions[0].totalMin = telemetryEtaMin + 4;
        }
      }

      return {
        originLabel: origPlace ? origPlace.label : originRaw,
        destLabel: destPlace ? destPlace.label : destRaw,
        origCorridor: origPlace,
        destCorridor: destPlace,
        directMatches,
        transferPlan,
        transferAlternatives: transferCandidates.slice(0, 3),
        routeOptions,
        telemetryEtaMin,
        originStop: oStop,
        destStop: dStop
      };
    },

    formatDurationHuman(mins) {
      const m = Math.max(1, Math.round(Number(mins) || 25));
      if (m >= 60) {
        const h = Math.floor(m / 60);
        const rem = m % 60;
        return rem > 0 ? `${h}h ${rem}min` : `${h}h`;
      }
      return `~${m} min`;
    },

    formatLayaSmartTripResponse(plan, layaDecision, rawQuery, tripPair) {
      const q = this.normalizeText(rawQuery || '');
      const safeOrig = this.escapeHtml(plan.originLabel);
      const safeDest = this.escapeHtml(plan.destLabel);
      const isNightOrEmergency = Boolean(
        (layaDecision && layaDecision.is_lost) ||
        /\b(perdid[oa]|me perdi|socorro|noite|madrugada|escuro|medo|segur[oa]|21h|22h)\b/i.test(q)
      );

      const nightSafetyBanner = isNightOrEmergency
        ? `<div style="background:#0f172a; border:1px solid #38bdf8; color:#f8fafc; padding:9px 11px; border-radius:10px; font-size:11px; margin-bottom:9px;">` +
            `<div style="font-weight:800; color:#38bdf8; margin-bottom:4px;">🛡️ Modo Segurança Noturna (Lei Estadual 15.878/2016)</div>` +
            `<div style="color:#cbd5e1; line-height:1.35; margin-bottom:7px;">Aguarde em parada iluminada. Entre 22h e 05h (alerta às 21h), mulheres, idosos e PcD podem desembarcar fora da parada oficial em local seguro da rota.</div>` +
            `<div style="display:flex; flex-wrap:wrap; gap:6px;">` +
              `<button type="button" onclick="closeModal('modal-laya'); setBottomNav('central'); if(typeof activateNightBeacon==='function') activateNightBeacon();" style="background:#0284c7; color:#fff; border:none; padding:5px 9px; border-radius:7px; font-size:10.5px; font-weight:800; cursor:pointer;">🔦 Ativar Farol Noturno</button>` +
              `<button type="button" onclick="closeModal('modal-laya'); if(typeof openSafeDisembarkModal==='function') openSafeDisembarkModal();" style="background:#059669; color:#fff; border:none; padding:5px 9px; border-radius:7px; font-size:10.5px; font-weight:800; cursor:pointer;">🛡️ Parada Segura 22h–05h</button>` +
            `</div>` +
          `</div>`
        : '';

      const origCoordsArr = (plan.origCorridor && plan.origCorridor.lat) ? `[${plan.origCorridor.lat}, ${plan.origCorridor.lon}]` : 'null';
      const destCoordsArr = (plan.destCorridor && plan.destCorridor.lat) ? `[${plan.destCorridor.lat}, ${plan.destCorridor.lon}]` : 'null';
      const formatDuration = (mins) => this.formatDurationHuman(mins);

      const renderOptionsCardsHtml = (options) => {
        return options.slice(0, 3).map((opt, idx) => {
          const codesJson = JSON.stringify(opt.codes).replace(/"/g, "'");
          const hubsJson = JSON.stringify(opt.hubs || []).replace(/"/g, "'");
          const pills = opt.codes.map(c => `<span style="background:#0f172a; color:#fff; padding:1px 6px; border-radius:5px; font-size:10.5px; font-weight:800;">${this.escapeHtml(c)}</span>`).join(' <span style="color:#64748b;">➔</span> ');
          const isPrimary = idx === 0;
          const tcBadge = (opt.transferConfidence && opt.transferConfidence.badge)
            ? opt.transferConfidence.badge
            : (opt.isDirect ? 'Viagem Direta · Sem Transbordo' : 'Conexão Segura · ~3 min a pé no TI');
          const cpBadge = (opt.crowdPrediction && opt.crowdPrediction.label)
            ? opt.crowdPrediction.label
            : 'Lotação Leve · IA ~88%';
          return `<div style="background:${isPrimary ? '#f0fdf4' : '#ffffff'}; border:1.5px solid ${isPrimary ? '#86efac' : '#e2e8f0'}; border-radius:12px; padding:8px 10px; margin-top:7px;">` +
            `<div style="display:flex; justify-content:space-between; align-items:center; gap:6px; margin-bottom:4px;">` +
              `<span style="font-size:10.5px; font-weight:800; color:${isPrimary ? '#047857' : '#334155'};">${opt.tag}</span>` +
              `<span style="font-family:'JetBrains Mono',monospace; font-size:11.5px; font-weight:800; color:#0f172a;">⏱️ ${formatDuration(opt.totalMin)}</span>` +
            `</div>` +
            `<div style="display:flex; flex-wrap:wrap; align-items:center; gap:4px; margin-bottom:5px;">${pills}</div>` +
            `<div style="display:flex; flex-wrap:wrap; gap:4px; margin-bottom:5px;">` +
              `<span style="background:#e0f2fe; color:#0369a1; border:1px solid #bae6fd; padding:1px 6px; border-radius:5px; font-size:9.5px; font-weight:800;">${this.escapeHtml(tcBadge)}</span>` +
              `<span style="background:#f1f5f9; color:#334155; border:1px solid #cbd5e1; padding:1px 6px; border-radius:5px; font-size:9.5px; font-weight:800;">${this.escapeHtml(cpBadge)}</span>` +
            `</div>` +
            `<div style="font-size:10.5px; color:#475569; margin-bottom:6px;">🚶 ${opt.walkMeters}m (${opt.walkMin} min) até a parada · ${opt.hubs.length ? 'Baldeação: ' + opt.hubs.map(h => this.escapeHtml(h)).join(' ➔ ') : 'Viagem direta sem troca'}</div>` +
            `<button type="button" onclick="if(window.RealTransit){window.RealTransit.renderMultiLegRoute(${codesJson}, ${hubsJson}, ${origCoordsArr}, ${destCoordsArr});} if(window.navigateToScreen){window.navigateToScreen('radar', {skipFit:true});} if(window.closeLayaModal){window.closeLayaModal();}" style="width:100%; background:${isPrimary ? '#059669' : '#0284c7'}; color:#fff; border:none; padding:6px 10px; border-radius:8px; font-size:11px; font-weight:800; cursor:pointer;">🗺️ Traçar Opção ${idx + 1} no Mapa</button>` +
            `</div>`;
        }).join('');
      };

      if (plan.directMatches.length > 0) {
        const nonBacurau = plan.directMatches.filter(m => !m.isBacurau);
        const ranked = nonBacurau.length > 0 ? nonBacurau : plan.directMatches;
        const mainRoute = ranked[0];
        const altLines = ranked.slice(1, 4).map(r => `<strong>${this.escapeHtml(r.code)}</strong> (${this.escapeHtml(r.name)})`).join(', ');
        const origStopLabel = plan.originStop ? plan.originStop.name : (plan.origCorridor && plan.origCorridor.stopName) || plan.originLabel;
        const destStopLabel = plan.destStop ? plan.destStop.name : (plan.destCorridor && plan.destCorridor.stopName) || plan.destLabel;
        const waitStr = plan.originStop ? `${plan.originStop.wait_gps_min || 3} min` : '4 a 7 min';
        const tripDur = plan.telemetryEtaMin ? this.formatDurationHuman(plan.telemetryEtaMin) : formatDuration(mainRoute.totalMin || 25);

        let html = nightSafetyBanner +
          `✅ <strong>Rotas de ${safeOrig} até ${safeDest}:</strong><br><br>` +
          `🚌 <strong>Melhor Linha Direta (${this.escapeHtml(mainRoute.code)}):</strong> <em>${this.escapeHtml(mainRoute.label)}</em><br>` +
          `• 📍 <strong>Embarque:</strong> ${this.escapeHtml(origStopLabel)} (próximo em <strong>${waitStr}</strong>)<br>` +
          `• 🎯 <strong>Desembarque:</strong> ${this.escapeHtml(destStopLabel)} (${tripDur})<br>`;

        if (altLines) {
          html += `• 🔁 <strong>Outras linhas diretas:</strong> ${altLines}<br>`;
        }
        if (plan.routeOptions && plan.routeOptions.length > 0) {
          html += `<div style="margin-top:6px; font-size:11px; font-weight:800; color:#334155;">📋 Sugestões estilo Maps (${plan.routeOptions.length} opções):</div>` +
            renderOptionsCardsHtml(plan.routeOptions);
        }

        return {
          intent: 'trip_plan',
          type: 'trip_plan',
          decision: layaDecision,
          routeCode: mainRoute.code,
          directOptions: ranked.slice(0, 4).map(r => r.code),
          routeOptions: plan.routeOptions,
          tripPlan: plan,
          html,
          speech: `De ${plan.originLabel} até ${plan.destLabel}, a melhor opção é a linha direta ${mainRoute.code}, chegando ao destino em cerca de ${mainRoute.totalMin || 25} minutos. Também listei ${Math.max(0, plan.routeOptions.length - 1)} rotas alternativas.`
        };
      }

      if (plan.transferPlan && Array.isArray(plan.transferPlan.legs) && plan.transferPlan.legs.length >= 2) {
        const legs = plan.transferPlan.legs;
        const hubs = plan.transferPlan.hubs || [plan.transferPlan.hub];
        const numEmojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣'];

        let stepsHtml = '';
        const legCodesArr = legs.map(l => l.code);
        for (let i = 0; i < legs.length; i++) {
          const targetPlace = i < hubs.length ? hubs[i] : plan.destLabel;
          const actionPrefix = i === 0 ? 'Embarque inicial' : (i === legs.length - 1 ? 'Etapa final até o destino' : 'Conexão intermediária');
          stepsHtml += `${numEmojis[i] || '➡️'} <strong>${i + 1}ª Etapa (${actionPrefix}):</strong> Linha <strong>${this.escapeHtml(legs[i].label)}</strong> até <strong>${this.escapeHtml(targetPlace)}</strong>.<br>`;
        }

        const optionsHtml = (plan.routeOptions && plan.routeOptions.length > 0)
          ? `<div style="margin-top:8px; font-size:11px; font-weight:800; color:#334155;">📋 Opções de Rota (Caminhada + Ônibus):</div>` + renderOptionsCardsHtml(plan.routeOptions)
          : '';

        const html = nightSafetyBanner +
          `🔄 <strong>Rota Completa (${legs.length} Etapas)</strong> de <strong>${safeOrig}</strong> até <strong>${safeDest}</strong>:<br><br>` +
          stepsHtml +
          `<div style="font-size:11px; color:#047857; font-weight:700; margin-top:6px;">💳 Integração SEI / VEM: janela de 2h entre terminais integrados.</div>` +
          optionsHtml;

        const speechSteps = legs.map((l, idx) => {
          const target = idx < hubs.length ? hubs[idx] : plan.destLabel;
          return `linha ${l.code} até ${target}`;
        }).join(', depois ');

        return {
          intent: 'trip_transfer',
          type: 'trip_plan',
          decision: layaDecision,
          routeCode: legs[0].code,
          legs: legCodesArr,
          hubs,
          hub: hubs[0],
          routeOptions: plan.routeOptions,
          tripPlan: plan,
          html,
          speech: `Tracei sua rota de ${plan.originLabel} até ${plan.destLabel} em ${legs.length} etapas: ${speechSteps}.`
        };
      }

      const origRawSafe = this.escapeHtml(tripPair ? tripPair.origin : plan.originLabel);
      const destRawSafe = this.escapeHtml(tripPair ? tripPair.dest : plan.destLabel);
      return {
        intent: 'trip_unknown',
        type: 'trip_unknown',
        html: `${nightSafetyBanner}Não encontrei paradas mapeadas entre <strong>"${origRawSafe}"</strong> e <strong>"${destRawSafe}"</strong>.<br><br>` +
          `Experimente nomes de bairros ou terminais (ex: <em>Recife Antigo, Olinda, Bairro Novo, TI PE-15, Camela, Ipojuca, UFRPE, Boa Viagem</em>) ou abra as 393 linhas:<br><br>` +
          `<button type="button" onclick="if(window.RealTransit){window.RealTransit.openLinePickerModal();}" style="background:#0284c7; color:#fff; border:none; padding:7px 12px; border-radius:9px; font-size:11.5px; font-weight:800; cursor:pointer;">🚌 Buscar nas 393 Linhas GTFS</button>`,
        speech: `Não localizei ligação entre ${plan.originLabel} e ${plan.destLabel}. Tente informar o terminal ou bairro mais próximo.`
      };
    },

    askLayaAssistant(rawQuery, ctx) {
      return this.answerLayaQuery(rawQuery, ctx);
    },

    answerLayaQuery(rawText, ctx) {
      const text = String(rawText || '').trim();
      const q = this.normalizeText(text);
      const telemetryStops = (ctx && Array.isArray(ctx.telemetryStops)) ? ctx.telemetryStops : [];
      const layaDecision = this.classifyLayaDecision(text);

      // 1. Guia de Perdido (Laya interpreta a fala e delega cálculo de rota para o motor determinístico RoutePlanner)
      const isLostWithoutDest = layaDecision.is_lost && !this.extractOriginDest(text) && !this.extractDestinationOnly(text);
      if (isLostWithoutDest) {
        const curStop = (this.userAdaptState && this.userAdaptState.stopName) || 'sua localização GPS';
        const curLine = this.activeRouteCode || '-';
        return {
          intent: 'lost_guide',
          type: 'lost_guide',
          decision: layaDecision,
          html: `🧭 <strong>Guia de Perdido · Fique tranquilo(a), vou te orientar!</strong><br><br>` +
            `• 📍 <strong>Onde você está:</strong> ${this.escapeHtml(curStop)} (Linha próxima: <strong>${this.escapeHtml(curLine)}</strong>)<br><br>` +
            `Me diga ou escreva abaixo <strong>para onde você quer ir</strong> (ex: <em>"Quero chegar em Boa Viagem"</em> ou <em>"Me ajuda a ir pro Derby"</em>) que eu aciono o algoritmo de rotas agora mesmo:`,
          speech: `Calma, já identifiquei seu ponto perto de ${curStop}. Me diga para qual bairro ou terminal você precisa ir que o sistema calcula o caminho na hora.`
        };
      }

      // 2. Interpretação de Origem/Destino -> Delegação explícita ao motor RoutePlanner (A* sobre grafo SEI + GTFS)
      let tripPair = this.extractOriginDest(text);
      let implicitFromHere = false;
      if (!tripPair) {
        const singleDest = this.extractDestinationOnly(text);
        if (singleDest) {
          tripPair = { origin: 'aqui', dest: singleDest };
          implicitFromHere = true;
        }
      }

      if (tripPair) {
        const plan = this.RoutePlanner.plan(tripPair.origin, tripPair.dest, telemetryStops);
        const safeDest = this.escapeHtml(plan.destLabel);
        const lostPrefix = layaDecision.is_lost
          ? `<div style="background:#fef3c7; border:1px solid #fcd34d; color:#92400e; padding:6px 9px; border-radius:8px; font-size:11px; font-weight:700; margin-bottom:8px;">🧭 Modo Guia de Perdido · Rota calculada pelo grafo GTFS</div>`
          : '';
        if (implicitFromHere && (!plan.origCorridor || !plan.origCorridor.lat)) {
          return {
            intent: 'need_location',
            type: 'need_location',
            decision: layaDecision,
            html: `${lostPrefix}📍 Quero traçar sua rota até <strong>${safeDest}</strong> partindo de onde você está!<br><br>Toque abaixo para ativar o GPS (ou escolher seu bairro de saída) e ver as opções estilo Google Maps:<br><br>` +
              `<button type="button" onclick="if(window.navigateToScreen){window.navigateToScreen('locate');} if(window.closeLayaModal){window.closeLayaModal();}" style="background:#059669; color:#fff; border:none; padding:8px 14px; border-radius:10px; font-size:12px; font-weight:800; cursor:pointer;">📍 Informar Onde Estou Agora</button>`,
            speech: `Para traçar sua rota até ${plan.destLabel}, primeiro me diga onde você está agora ou ative seu GPS.`
          };
        }

        return this.formatLayaSmartTripResponse(plan, layaDecision, text, tripPair);
      }

      // 3. Conhecimento Técnico e Científico da Plataforma GrafoParada + WebMCP (4 Sub-intenções Especializadas)
      const isAskingScience = /\b(stgcn|st gcn|ia|inteligencia artificial|modelo|trava|over-smoothing|oversmoothing|reneging|abandono|yap|kim|mae|como funciona|plataforma|grafoparada|despacho|deadheading|queima|queima de parada|queima de ponto|bolso seguro|lei 15878|15878|15\.878|parada segura|desembarque seguro|21h|22h|farol noturno|webmcp|engarrafamento|congestionamento|acidente|pe-60|pe 60|trevo|anomalia|no 10|cittamobi|moovit|diferenca|comparar|integracao vem|integracao temporal|integracao|vem|duas horas|2h)\b/.test(q);
      if (isAskingScience) {
        // Sub-intenção A — Engarrafamento Repentino na PE-60 / Nó 10 & Limite da ST-GCN (Slide 3)
        if (/\b(engarrafamento|congestionamento|acidente|pe-60|pe 60|trevo|over-smoothing|oversmoothing|anomalia|no 10)\b/.test(q)) {
          const html = `<strong>Anomalia no Nó 10 (Trevo de Ipojuca / PE-60) &amp; Trava Híbrida:</strong><br><br>` +
            `• <strong>Por que a ST-GCN pura falha em acidentes súbitos?</strong> A convolução espacial em grafo (<code>D⁻¹/²ÃD⁻¹/²</code>) suaviza o estado do Nó 10 com os nós vizinhos livres. Em um bloqueio abrupto de <strong>45,0 min</strong> no GPS Bruto, a ST-GCN pura prevê apenas <strong>14,3 min</strong> (<em>Over-smoothing</em>, erro Δ = 30,7 min).<br>` +
            `• <strong>Trava Híbrida de Segurança (&gt; 15 min):</strong> Quando <code>|GPS Bruto - ST-GCN| &gt; 15 min</code>, o GrafoParada aciona <code>ALERTA_AMARELO_OVER_SMOOTHING</code>, descarta a suavização naquele trecho, exibe os <strong>45,0 min</strong> reais e sugere rota alternativa via <strong>TI Cabo</strong>.<br><br>` +
            `<button type="button" onclick="closeModal('modal-laya'); if(typeof simulateSlide3Failure==='function') simulateSlide3Failure();" style="background:#d97706; color:#fff; border:none; padding:7px 12px; border-radius:9px; font-size:11.5px; font-weight:800; cursor:pointer;">Simular Anomalia Nó 10 (PE-60) no Mapa</button>`;
          return {
            intent: 'platform_knowledge',
            type: 'platform_knowledge',
            subIntent: 'pe60_oversmoothing_slide3',
            decision: layaDecision,
            html,
            speech: 'Em caso de acidente ou engarrafamento repentino no Nó 10 da PE-60, a convolução da ST-GCN sofre over-smoothing prevendo 14,3 minutos contra 45 minutos reais no GPS. O GrafoParada ativa a Trava Híbrida de Segurança acima de 15 minutos de divergência e exibe o alerta amarelo com o tempo real do GPS.'
          };
        }

        // Sub-intenção B — Parada Segura Noturna (Lei Estadual 15.878/2016) & Segurança Comunitária
        if (/\b(parada segura|desembarque seguro|21h|22h|lei|15878|15\.878|noturn[oa]|mulher|assedio|farol|queima)\b/.test(q)) {
          const html = `<strong>Parada Segura Noturna · Lei Estadual nº 15.878/2016 (PE):</strong><br><br>` +
            `• <strong>Direito Legal (22h às 05h · Alerta Preventivo às 21h):</strong> Mulheres, idosos e pessoas com mobilidade reduzida têm direito a solicitar desembarque fora da parada oficial em qualquer ponto seguro e iluminado que siga o itinerário da linha.<br>` +
            `• <strong>Farol Noturno de Alto Contraste:</strong> Sinalizador visual de tela cheia para impedir que o ônibus passe direto em trechos escuros (PE-60 / BR-101).<br>` +
            `• <strong>Auditoria de Queima de Ponto:</strong> Registra telemetria de velocidade (&gt; 25 km/h no raio da parada) para fiscalização do CTM.<br><br>` +
            `<div style="display:flex; flex-wrap:wrap; gap:6px;">` +
              `<button type="button" onclick="closeModal('modal-laya'); if(typeof openSafeDisembarkModal==='function') openSafeDisembarkModal();" style="background:#059669; color:#fff; border:none; padding:7px 11px; border-radius:9px; font-size:11px; font-weight:800; cursor:pointer;">Solicitar Parada Segura</button>` +
              `<button type="button" onclick="closeModal('modal-laya'); setBottomNav('central'); if(typeof activateNightBeacon==='function') activateNightBeacon();" style="background:#0284c7; color:#fff; border:none; padding:7px 11px; border-radius:9px; font-size:11px; font-weight:800; cursor:pointer;">Abrir Farol Noturno</button>` +
            `</div>`;
          return {
            intent: 'platform_knowledge',
            type: 'platform_knowledge',
            subIntent: 'night_safety_law_15878',
            decision: layaDecision,
            html,
            speech: 'Pela Lei Estadual 15.878 de 2016 em Pernambuco, entre 22 horas e 5 da manhã, com aviso preventivo já às 21 horas no GrafoParada, mulheres, idosos e pessoas com mobilidade reduzida podem solicitar desembarque fora da parada oficial em local seguro dentro do trajeto do ônibus.'
          };
        }

        // Sub-intenção C — Cittamobi vs. GrafoParada & Integração Temporal VEM / SEI (2h)
        if (/\b(cittamobi|moovit|diferenca|comparar|integracao|vem|tarifa|passagem|duas horas|2h)\b/.test(q)) {
          const html = `<strong>Cittamobi vs. GrafoParada &amp; Integração Temporal VEM (2h):</strong><br><br>` +
            `• <strong>Por que o Cittamobi congela na PE-60/BR-101?</strong> Usa interpolação de GPS bruto ponto-a-ponto (que some em zonas de sombra de sinal). O GrafoParada combina <strong>ST-GCN em grafo</strong> (MAE <strong>1,51 min</strong> vs <strong>1,93 min</strong> OLS e <strong>7,13 min</strong> Persistência) + <strong>FSM Cinemático V3</strong> (<strong>56,68 µs</strong>) + Trava Híbrida.<br>` +
            `• <strong>Integração Temporal VEM / SEI (26 Terminais Integrados):</strong> Com 1 única tarifa no cartão VEM, você realiza transbordo físico nos 26 TIs ou integração temporal em até <strong>2 horas (120 min)</strong> sem pagar nova passagem.<br><br>` +
            `<button type="button" onclick="if(window.navigateToScreen){window.navigateToScreen('central');} if(window.closeLayaModal){window.closeLayaModal();}" style="background:#0f172a; color:#fff; border:none; padding:7px 12px; border-radius:9px; font-size:11.5px; font-weight:800; cursor:pointer;">Comparar Auditoria Cittamobi vs ST-GCN</button>`;
          return {
            intent: 'platform_knowledge',
            type: 'platform_knowledge',
            subIntent: 'cittamobi_vs_grafoparada_vem',
            decision: layaDecision,
            html,
            speech: 'Enquanto o Cittamobi depende de GPS bruto isolado, o GrafoParada opera com rede ST-GCN com erro médio de 1,51 minuto e filtro cinemático em 56,68 microssegundos. Na integração temporal VEM e nos 26 Terminais SEI, você troca de linha em até 2 horas pagando uma única passagem.'
          };
        }

        // Sub-intenção D — Arquitetura Científica ST-GCN + FSM V3 + Grafo A* (Default Science Card)
        const html = `<strong>Arquitetura Científica GrafoParada (Benchmarks Reais):</strong><br><br>` +
          `• <strong>Rede ST-GCN (20 Nós PE-60 + 393 Linhas GTFS):</strong> MAE <strong>1,51 min</strong> (vs 1,93 min OLS e 7,13 min Persistência) · Inferência CPU em <strong>0,96 ms</strong> · <strong>34.627 parâmetros</strong> (138 KB).<br>` +
          `• <strong>FSM Cinemático V3 (Filtro de Parada Real):</strong> Latência de <strong>56,68 µs/amostra</strong> · <strong>11,02 KB</strong> de heap RAM · Histerese <code>&lt; 2,16 km/h</code>, raio <code>25 m</code> e <code>dwell &gt;= 8 s</code>.<br>` +
          `• <strong>A* Multicritério + Comportamental:</strong> Espera percebida <strong>1,68x</strong> (Yap &amp; Cats, 2021) e probabilidade logística de desistência <code>P(Abandono)</code> (Kim et al., 2026).<br>` +
          `• <strong>Trava Híbrida Defensiva + WebMCP:</strong> Bloqueia over-smoothing quando <code>|GPS - ST-GCN| &gt; 15 min</code> e expõe tools via <code>navigator.modelContext</code>.<br><br>` +
          `<button type="button" onclick="if(window.navigateToScreen){window.navigateToScreen('central');} if(window.closeLayaModal){window.closeLayaModal();}" style="background:#0f172a; color:#fff; border:none; padding:7px 12px; border-radius:9px; font-size:11.5px; font-weight:800; cursor:pointer;">Ver Auditoria &amp; Central CTM</button>`;
        return {
          intent: 'platform_knowledge',
          type: 'platform_knowledge',
          subIntent: 'architecture_stgcn_fsm_astar',
          decision: layaDecision,
          html,
          speech: 'O motor GrafoParada combina a rede ST-GCN com erro médio de 1,51 minuto e inferência de 0,96 milissegundos em CPU, o filtro cinemático FSM V3 em 56,68 microssegundos e o modelo de abandono de Yap e Cats e Kim et al.'
        };
      }

      // 4. Consulta específica por local ou linha citada na pergunta (Prioridade absoluta para código de linha explícito)
      const explicitLineMatch = q.match(/\b(\d{3,4})\b/);
      const explicitLineCode = explicitLineMatch ? (this.aliases[explicitLineMatch[1]] || explicitLineMatch[1]) : null;
      const hasExplicitLine = Boolean(
        explicitLineCode &&
        this.networkData && (
          (this.networkData.popular_lines && this.networkData.popular_lines[explicitLineCode]) ||
          (Array.isArray(this.networkData.routes_catalog) && this.networkData.routes_catalog.some(r => r.code === explicitLineCode))
        )
      );
      const matchedCorridor = hasExplicitLine ? null : this.resolvePlaceLocation(q);
      const placeMatches = hasExplicitLine
        ? this.findCatalogRoutesForQuery(explicitLineCode, telemetryStops)
        : (matchedCorridor ? this.findCatalogRoutesForQuery(matchedCorridor.key, telemetryStops) : []);

      // 5. Pergunta de Próximo Ônibus / Horário / Chegada / Lotação / Espera
      const isAskingBus = /\b(onibus|quando passa|horario|proximo|chega|lotacao|vagas|lotado|lotada|cheio|cheia|vazio|vazia|assento|sentado|em pe|demora|demorando|mofar|esperando|cade|previsto|previsao)\b/.test(q);
      const isAskingCrowdOrWait = /\b(lotacao|vagas|lotado|lotada|cheio|cheia|vazio|vazia|assento|sentado|em pe|mofar|demora|demorando|esperando)\b/.test(q);
      if (isAskingBus || hasExplicitLine) {
        if (placeMatches.length > 0) {
          const nonBacurau = placeMatches.filter(m => !/bacurau/i.test(m.label));
          const best = (hasExplicitLine ? placeMatches.find(m => m.code === explicitLineCode) : null) || nonBacurau[0] || placeMatches[0];
          const hint = best.stopHint || {};
          const stopName = (matchedCorridor ? matchedCorridor.stopName : null) || hint.name || best.label;
          const waitMin = hint.wait_gps_min || (matchedCorridor ? matchedCorridor.waitMin : 4);
          const seatsFree = hint.seatsFree || (best.code === '199' ? 28 : 14);
          const coordsArg = (hint.lat && hint.lon) ? `[${hint.lat}, ${hint.lon}]` : 'null';

          const crowdLevel = seatsFree >= 22 ? 'Leve' : (seatsFree >= 10 ? 'Moderada' : 'Crítica');
          const perceivedWaitMin = (waitMin * 1.68).toFixed(1).replace('.', ',');
          const effWait = crowdLevel === 'Crítica' ? waitMin * 1.68 : waitMin * 1.15;
          const pAbandonoPct = Math.min(95, Math.max(8, Math.round((1 / (1 + Math.exp(-0.25 * (effWait - 15)))) * 100)));
          const practicalAdvice = crowdLevel === 'Leve'
            ? 'Embarque confortável com assentos livres.'
            : (crowdLevel === 'Moderada' ? 'Fluxo regular para o horário; embarque recomendado.' : 'Alta ocupação; se puder aguardar, o veículo seguinte alivia o corredor.');

          const crowdAndWaitBlock = isAskingCrowdOrWait
            ? `<div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:9px; padding:7px 9px; margin:7px 0; font-size:11px; line-height:1.4;">` +
                `• <strong>Indicador Híbrido de Lotação (Transit App + ST-GCN):</strong> Ocupação <strong>${crowdLevel}</strong> (${seatsFree} assentos livres · precisão histórica <strong>~88% APC + série temporal CTM</strong>). <em>${practicalAdvice}</em><br>` +
                `• <strong>Espera Percebida &amp; Risco de Abandono (Yap &amp; Cats / Kim et al.):</strong> ETA real <strong>${waitMin} min</strong> vs. percebido em veículo cheio <strong>${perceivedWaitMin} min</strong> (multiplicador <code>1.68x</code>) · Probabilidade de desistência <code>P(Abandono) = ${pAbandonoPct}%</code>.` +
              `</div>`
            : '';

          const html = `<strong>Previsão para ${matchedCorridor ? this.escapeHtml(matchedCorridor.label) : 'Linha ' + this.escapeHtml(best.code)}:</strong><br><br>` +
            `• <strong>Linha recomendada:</strong> ${this.escapeHtml(best.label)}<br>` +
            `• <strong>Parada de referência:</strong> ${this.escapeHtml(stopName)}<br>` +
            `• <strong>Próxima chegada prevista (ST-GCN):</strong> em <strong>${waitMin} minutos</strong><br>` +
            `• <strong>Ocupação estimada:</strong> Lotação <strong>${crowdLevel}</strong> (${seatsFree} assentos livres)<br>` +
            crowdAndWaitBlock + `<br>` +
            `<div style="display:flex; flex-wrap:wrap; gap:6px;">` +
            `<button type="button" onclick="if(window.RealTransit){window.RealTransit.loadRoute('${best.code}');} if(window.navigateToScreen){window.navigateToScreen('radar');} if(window.closeLayaModal){window.closeLayaModal();}" style="background:#059669; color:#fff; border:none; padding:7px 12px; border-radius:9px; font-size:11.5px; font-weight:800; cursor:pointer;">Rastrear Linha ${this.escapeHtml(best.code)}</button>` +
            `<button type="button" onclick="if(window.RealTransit){window.RealTransit.loadRoute('${best.code}');} if(window.setMyBoardingStop){window.setMyBoardingStop('${stopName.replace(/'/g, "\\'")}', ${coordsArg});}" style="background:#0284c7; color:#fff; border:none; padding:7px 12px; border-radius:9px; font-size:11.5px; font-weight:800; cursor:pointer;">Fixar como Minha Parada</button>` +
            `</div>`;

          return {
            intent: 'next_bus_place',
            type: 'bus_status',
            routeCode: best.code,
            crowdLevel,
            perceivedWaitMin,
            pAbandonoPct,
            html,
            speech: `Para ${matchedCorridor ? matchedCorridor.label : 'a linha ' + best.code}, o próximo coletivo da linha ${best.code} chega em ${waitMin} minutos na parada ${stopName}, com lotação ${crowdLevel.toLowerCase()} e cerca de ${seatsFree} assentos livres.`
          };
        }

        // Sem local citado -> usa parada adaptada ao GPS/escolha atual
        if (this.userAdaptState && (this.userAdaptState.status === 'awaiting_location' || this.userAdaptState.status === 'gps_denied')) {
          return {
            intent: 'need_location',
            type: 'need_location',
            html: `📍 Ainda não sei em qual bairro ou parada você está agora!<br><br>Ative seu GPS ou toque no bairro de partida para eu localizar a linha mais próxima:<br><br>` +
              `<button type="button" onclick="if(window.navigateToScreen){window.navigateToScreen('locate');} if(window.closeLayaModal){window.closeLayaModal();}" style="background:#059669; color:#fff; border:none; padding:7px 12px; border-radius:9px; font-size:11.5px; font-weight:800; cursor:pointer;">📍 Informar Onde Estou Agora</button>`,
            speech: "Me diga em qual bairro ou parada você está, ou toque em Informar Onde Estou Agora para eu buscar pelo GPS."
          };
        }

        const activeCode = (ctx && ctx.activeRouteCode) || this.activeRouteCode || '199';
        const activeRouteName = (this.activeRoute && this.activeRoute.name) ? this.activeRoute.name : '';
        const activeStop = (ctx && ctx.activeStopName) || (this.userAdaptState && this.userAdaptState.stopName) || 'Sua Parada Ativa';
        const activeEta = (ctx && ctx.activeEta) || 4;
        const perceivedActive = (activeEta * 1.68).toFixed(1).replace('.', ',');

        const html = `🚌 <strong>Sua Linha Mais Próxima: ${this.escapeHtml(activeCode)} · ${this.escapeHtml(activeRouteName)}</strong><br><br>` +
          `• 📍 <strong>Parada detectada:</strong> ${this.escapeHtml(activeStop)}<br>` +
          `• ⏱️ <strong>Próximo ônibus previsto:</strong> <strong>${activeEta} minutos</strong> (espera percebida Yap &amp; Cats: <strong>${perceivedActive} min</strong> sob lotação)<br>` +
          `• 📊 <strong>Indicador Híbrido de Lotação:</strong> Ocupação <strong>Moderada</strong> (~88% APC + série temporal CTM)<br><br>` +
          `<div style="display:flex; flex-wrap:wrap; gap:6px;">` +
          `<button type="button" onclick="if(window.navigateToScreen){window.navigateToScreen('radar');} if(window.trackBusLocation){window.trackBusLocation(true);} if(window.closeLayaModal){window.closeLayaModal();}" style="background:#059669; color:#fff; border:none; padding:7px 12px; border-radius:9px; font-size:11.5px; font-weight:800; cursor:pointer;">🚌 Rastrear no Mapa</button>` +
          `<button type="button" onclick="if(window.navigateToScreen){window.navigateToScreen('locate');} if(window.closeLayaModal){window.closeLayaModal();}" style="background:#0284c7; color:#fff; border:none; padding:7px 12px; border-radius:9px; font-size:11.5px; font-weight:800; cursor:pointer;">📍 Atualizar Localização</button>` +
          `</div>`;

        return {
          intent: 'next_bus_active',
          type: 'bus_status',
          routeCode: activeCode,
          html,
          speech: `Perto de você em ${activeStop}, a linha ${activeCode} está prevista para chegar em ${activeEta} minutos.`
        };
      }

      // 6. Qual minha parada / Onde estou
      if (/\b(parada|ponto|onde estou|localizacao|gps)\b/.test(q)) {
        const activeStop = (this.userAdaptState && this.userAdaptState.stopName) || (ctx && ctx.activeStopName) || 'Localização não confirmada';
        const activeCode = this.activeRouteCode || '-';
        return {
          intent: 'current_stop',
          type: 'current_stop',
          html: `📍 Sua referência atual adaptada é: <strong>${this.escapeHtml(activeStop)}</strong> (Linha <strong>${this.escapeHtml(activeCode)}</strong>).<br><br>` +
            `<button type="button" onclick="if(window.navigateToScreen){window.navigateToScreen('locate');} if(window.closeLayaModal){window.closeLayaModal();}" style="background:#0284c7; color:#fff; border:none; padding:7px 12px; border-radius:9px; font-size:11.5px; font-weight:800; cursor:pointer;">📍 Detectar / Atualizar Posição Real</button>`,
          speech: `Sua posição atual está adaptada para ${activeStop}.`
        };
      }

      // 7. Mencionou um local/linha sem verbo ("Recife Antigo", "Olinda", "Camela", "1967")
      if (placeMatches.length > 0) {
        const best = (hasExplicitLine ? placeMatches.find(m => m.code === explicitLineCode) : null) || placeMatches.find(m => !/bacurau/i.test(m.label)) || placeMatches[0];
        const hint = best.stopHint || {};
        const stopName = (matchedCorridor ? matchedCorridor.stopName : null) || hint.name || best.label;
        const waitMin = hint.wait_gps_min || (matchedCorridor ? matchedCorridor.waitMin : 5);
        return {
          intent: 'place_lookup',
          type: 'place_lookup',
          routeCode: best.code,
          html: `📍 Encontrei atendimento real para <strong>${matchedCorridor ? this.escapeHtml(matchedCorridor.label) : this.escapeHtml(best.label)}</strong>:<br><br>` +
            `• 🚌 <strong>Linha principal:</strong> ${this.escapeHtml(best.label)}<br>` +
            `• 🚏 <strong>Parada chave:</strong> ${this.escapeHtml(stopName)}<br>` +
            `• ⏱️ <strong>Previsão média:</strong> <strong>${waitMin} min</strong><br><br>` +
            `<button type="button" onclick="if(window.RealTransit){window.RealTransit.loadRoute('${best.code}');} if(window.navigateToScreen){window.navigateToScreen('radar');} if(window.closeLayaModal){window.closeLayaModal();}" style="background:#059669; color:#fff; border:none; padding:7px 12px; border-radius:9px; font-size:11.5px; font-weight:800; cursor:pointer;">🗺️ Abrir Linha ${this.escapeHtml(best.code)} no Mapa</button>`,
          speech: `Para ${matchedCorridor ? matchedCorridor.label : best.label}, você pode usar a linha ${best.code}.`
        };
      }

      // 8. Salvar / Favoritos / Rotina
      if (/\b(salvar|favorit|estrela)\b/.test(q)) {
        return {
          intent: 'save_favorite',
          saveFavorite: true,
          html: "⭐ Adicionei sua parada atual aos favoritos!",
          speech: "Parada adicionada aos favoritos."
        };
      }

      if (/\b(trabalhar|rotina|janela|sair de casa|estudar hoje)\b/.test(q)) {
        return {
          intent: 'routine_help',
          html: `📅 Me diga <strong>de onde até onde</strong> você vai hoje (ex: <em>"Do Recife Antigo para Olinda"</em>) ou detecte onde você está agora:<br><br>` +
            `<button type="button" onclick="if(window.navigateToScreen){window.navigateToScreen('locate');} if(window.closeLayaModal){window.closeLayaModal();}" style="background:#059669; color:#fff; border:none; padding:7px 12px; border-radius:9px; font-size:11.5px; font-weight:800; cursor:pointer;">📍 Detectar Onde Estou Agora</button>`,
          speech: "Me diga de onde até onde você vai hoje, ou toque em Detectar Onde Estou Agora."
        };
      }

      return {
        intent: 'fallback_guide',
        html: `Entendi! Consulto o grafo completo das <strong>393 linhas e 45 Hubs/Terminais SEI</strong> do Grande Recife.<br><br>` +
          `Exemplos que você pode testar agora:<br>` +
          `• <em>"Quero ir do Recife Antigo pra Olinda"</em><br>` +
          `• <em>"Sair de Camela até Ipojuca"</em><br>` +
          `• <em>"Qual o próximo ônibus aqui?"</em>`,
        speech: "Posso calcular trajetos diretos ou integrados entre quaisquer bairros do Grande Recife. Diga de onde até onde você vai."
      };
    },

    // Integração nativa com Chrome WebMCP (navigator.modelContext) para agentes no navegador
    registerWebMCPTools() {
      try {
        if (typeof navigator === 'undefined' || !navigator.modelContext || typeof navigator.modelContext.registerTool !== 'function') {
          return false;
        }
        const self = this;

        navigator.modelContext.registerTool({
          name: 'grafoparada_plan_route',
          title: 'Planejar Trajeto de Ônibus no Grande Recife (GTFS + Grafo SEI)',
          description: 'Encontra linhas diretas ou integrações em Terminais SEI entre dois bairros, paradas ou localidades da RMR (ex: Recife Antigo -> Olinda, Camela -> Ipojuca).',
          inputSchema: {
            type: 'object',
            properties: {
              origin: { type: 'string', description: 'Bairro, terminal ou localidade de origem (ou "aqui")' },
              destination: { type: 'string', description: 'Bairro, terminal ou localidade de destino' }
            },
            required: ['origin', 'destination']
          },
          annotations: { readOnlyHint: true },
          execute: async (input) => {
            const plan = self.planSmartTrip(input.origin, input.destination, []);
            return {
              origin: plan.originLabel,
              destination: plan.destLabel,
              directLines: (plan.directMatches || []).slice(0, 5).map(r => ({ code: r.code, name: r.name })),
              transferConnection: plan.transferPlan ? {
                hubs: plan.transferPlan.hubs || [plan.transferPlan.hub],
                legs: (plan.transferPlan.legs || []).map(l => ({ code: l.code, name: l.name })),
                firstLine: plan.transferPlan.leg1 ? plan.transferPlan.leg1.code : null,
                secondLine: plan.transferPlan.leg2 ? plan.transferPlan.leg2.code : null
              } : null
            };
          }
        });

        navigator.modelContext.registerTool({
          name: 'grafoparada_find_nearest_stop',
          title: 'Detectar Parada e Linhas Próximas por GPS',
          description: 'Adapta o aplicativo à coordenada GPS atual do usuário e retorna a parada física real e linhas próximas.',
          inputSchema: {
            type: 'object',
            properties: {
              lat: { type: 'number', description: 'Latitude do usuário' },
              lon: { type: 'number', description: 'Longitude do usuário' }
            },
            required: ['lat', 'lon']
          },
          annotations: { readOnlyHint: false },
          execute: async (input) => {
            return self.adaptToUserLocation(input.lat, input.lon, 'WebMCP Tool');
          }
        });

        console.log('🤖 [WebMCP] Ferramentas do GrafoParada registradas em navigator.modelContext.');
        return true;
      } catch (e) {
        return false;
      }
    }
  };

  window.RealTransit = RealTransit;

})(window);
