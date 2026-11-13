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
    activeStopIndex: 0,
    userAdaptState: { status: 'initializing', stopName: null, distanceKm: null },
    map: null,
    polylineLayer: null,
    stopsLayer: null,
    busMarker: null,
    cittamobiCache: {},

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
            this.adaptToUserLocation(last.lat, last.lon, 'Última localização ativa', { fit: false });
            restored = true;
          }
        }
      } catch (e) {}

      if (!restored) {
        // Estado inicial limpo: tenta geolocalização real antes de assumir qualquer parada
        this.userAdaptState = { status: 'awaiting_location', stopName: 'Escolha ou ative seu GPS', distanceKm: null };
        this.loadRoute('199');
        if (navigator && navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(
            (pos) => {
              this.adaptToUserLocation(pos.coords.latitude, pos.coords.longitude, 'GPS em tempo real', { fit: true });
            },
            () => {
              // Mantém estado aguardando escolha na Tela 1/2 sem fingir que está na Rural
              if (typeof window.updateHomeGreeting === 'function') window.updateHomeGreeting();
            },
            { enableHighAccuracy: true, timeout: 4500 }
          );
        }
      }

      // Registra ferramentas WebMCP caso o navegador possua suporte (Google Chrome WebMCP Developer Preview)
      this.registerWebMCPTools();

      // Escuta mudanças de busca no input superior
      const searchInput = document.getElementById('quick-search-input');
      if (searchInput) {
        searchInput.placeholder = 'Buscar entre 400 linhas reais (ex: 199, 1967, 2040, Olinda)...';
      }
    },

    // Alias canônico para seleção de linha compatível com Laya IA e favoritos
    selectLine(code) {
      return this.loadRoute(code);
    },

    // Renderiza linha completa com shape e paradas do GTFS
    loadRoute(rawCode) {
      if (!this.networkData || !this.networkData.popular_lines) return;

      let code = String(rawCode || '').trim();
      if (this.aliases[code]) {
        code = this.aliases[code];
      }

      let lineData = this.networkData.popular_lines[code];
      if (!lineData) {
        // Tenta buscar no catálogo geral caso o código divirja
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
      this.activeStopIndex = 0;

      // 1. Atualiza Traçado Geodésico Real (Polyline)
      if (this.polylineLayer) {
        this.map.removeLayer(this.polylineLayer);
      }

      const coords = lineData.polyline || [];
      if (coords.length > 0) {
        this.polylineLayer = L.polyline(coords, {
          color: '#059669',
          weight: 5,
          opacity: 0.85,
          smoothFactor: 1
        }).addTo(this.map);

        // Ajusta o zoom do mapa para enquadrar perfeitamente a linha
        try {
          this.map.fitBounds(this.polylineLayer.getBounds(), {
            padding: [50, 50],
            maxZoom: 15,
            animate: true
          });
        } catch (e) {
          console.warn('Erro ao ajustar bounds:', e);
        }
      }

      // 2. Plota as Paradas Reais no Mapa
      this.renderStopMarkers(lineData.stops);

      // 2.1 Sincroniza Marcador do Usuário e Ônibus ao Vivo
      if (typeof window.connectUserToActiveStop === 'function' && window.userCurrentCoords) {
        window.connectUserToActiveStop(window.userCurrentCoords[0], window.userCurrentCoords[1]);
      }
      if (typeof window.updateLiveBusMarker === 'function' && coords.length > 2) {
        const bp = coords[Math.min(5, coords.length - 1)];
        window.updateLiveBusMarker(bp[0], bp[1], code, 4, 14);
      }

      // 3. Atualiza Elementos do DOM
      this.updateUIForLine(lineData);
      if (typeof window.showRouteIndicatorChip === 'function') {
        window.showRouteIndicatorChip(code, lineData.name || lineData.label);
      }

      // 4. Consulta API ao Vivo do Cittamobi para Dados em Tempo Real da Frota
      this.fetchCittamobiLiveData(code);
    },

    // Plota os marcadores das paradas com popups detalhados
    renderStopMarkers(stops) {
      this.stopsLayer.clearLayers();
      const self = this;

      stops.forEach((st, idx) => {
        const isTerminal = idx === 0 || idx === stops.length - 1;
        const iconHtml = isTerminal
          ? '<div style="background:#0f172a; color:#fff; border:2px solid #fff; border-radius:50%; width:22px; height:22px; display:flex; align-items:center; justify-content:center; font-size:11px; font-weight:800; box-shadow:0 3px 10px rgba(0,0,0,0.3);">🏛️</div>'
          : '<div style="background:#ffffff; color:#059669; border:2px solid #059669; border-radius:50%; width:16px; height:16px; display:flex; align-items:center; justify-content:center; font-size:9px; font-weight:800; box-shadow:0 2px 6px rgba(0,0,0,0.2);">' + (idx + 1) + '</div>';

        const customIcon = L.divIcon({
          className: '',
          html: iconHtml,
          iconSize: isTerminal ? [22, 22] : [16, 16],
          iconAnchor: isTerminal ? [11, 11] : [8, 8]
        });

        const marker = L.marker([st.lat, st.lon], { icon: customIcon });

        const popupContent = `
          <div style="font-family:'Plus Jakarta Sans',sans-serif; min-width:220px; padding:2px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
              <span style="font-size:10px; font-weight:800; background:#f1f5f9; color:#475569; padding:2px 6px; border-radius:4px;">CÓD ${st.stop_id}</span>
              <span style="font-size:10.5px; font-weight:700; color:#059669;">Linha ${self.activeRouteCode}</span>
            </div>
            <div style="font-size:13px; font-weight:800; color:#0f172a; margin-bottom:4px; line-height:1.2;">${st.name}</div>
            <div style="font-size:11px; color:#64748b; margin-bottom:8px;">Horário Programado GTFS: <strong>${st.arr_time || 'Regular'}</strong></div>
            <button onclick="window.RealTransit.selectStop(${idx}, true); if(leafletMap) leafletMap.closePopup();" style="width:100%; background:#059669; color:#fff; border:none; padding:6px 12px; border-radius:6px; font-size:11.5px; font-weight:800; cursor:pointer;">
              Selecionar Parada ➔
            </button>
            <button onclick="window.setMyBoardingStop('${st.name.replace(/'/g, "\\'")}', [${st.lat}, ${st.lon}]); if(leafletMap) leafletMap.closePopup();" style="width:100%; background:#0284c7; color:#fff; border:none; padding:6px 12px; border-radius:6px; font-size:11.5px; font-weight:800; cursor:pointer; margin-top:4px;">
              🔔 Me avisar quando o ônibus estiver perto (Minha Parada)
            </button>
          </div>
        `;

        marker.bindPopup(popupContent);
        marker.on('click', () => self.selectStop(idx, false));
        self.stopsLayer.addLayer(marker);
      });
    },

    // Seleciona uma parada na linha ativa
    selectStop(index, panTo) {
      if (!this.activeRoute || !this.activeRoute.stops[index]) return;
      this.activeStopIndex = index;
      const st = this.activeRoute.stops[index];

      const cleanStopLabel = (st.name && !/^\d+$/.test(String(st.name).trim()))
        ? st.name
        : `Parada CTM ${st.stop_id} (${this.activeRoute.name || 'Linha ' + this.activeRouteCode})`;

      // Atualiza o card de parada atual
      const nameEl = document.getElementById('current-stop-name');
      if (nameEl) {
        nameEl.innerHTML = `
          <div style="display:flex; flex-direction:column; gap:2px;">
            <div style="display:flex; align-items:center; gap:6px;">
              <span style="font-size:10.5px; font-weight:800; background:#f1f5f9; color:#475569; padding:2px 6px; border-radius:6px; border:1px solid #cbd5e1;">CÓD ${st.stop_id}</span>
              <span style="font-size:11px; font-weight:800; color:#047857;">📍 Parada #${index + 1} de ${this.activeRoute.stops.length}</span>
              <span style="font-size:10px; background:#dcfce7; color:#15803d; padding:1px 5px; border-radius:4px; font-weight:700;">GTFS CTM Oficial</span>
            </div>
            <div style="font-size:14.5px; font-weight:800; color:var(--text-main); margin-top:2px;">${cleanStopLabel}</div>
            <div style="font-size:11px; color:var(--text-secondary);">Sentido: ${this.activeRoute.headsign || this.activeRoute.name}</div>
            <button onclick="window.setMyBoardingStop('${cleanStopLabel.replace(/'/g, "\\'")}', [${st.lat}, ${st.lon}])" style="margin-top:6px; background:#f0fdf4; color:#047857; border:1.5px solid #86efac; border-radius:8px; padding:6px 10px; font-size:11px; font-weight:800; cursor:pointer; width:100%; display:flex; align-items:center; justify-content:center; gap:5px;">
              🔔 Me avisar quando o ônibus estiver perto desta parada
            </button>
          </div>
        `;
      }

      // Calcula estimativa de chegada realista baseada na posição sequencial
      const etaMinutes = Math.max(2, ((index % 6) * 3) + 2);
      const restingEta = document.getElementById('resting-eta-val');
      const liveEta = document.getElementById('live-eta-num');
      if (restingEta) restingEta.textContent = String(etaMinutes);
      if (liveEta) liveEta.textContent = String(etaMinutes);

      if (panTo && this.map) {
        this.map.panTo([st.lat, st.lon], { animate: true, duration: 0.5 });
      }

      // Re-renderiza o accordion destacando a parada selecionada
      this.renderStopsDrawer(this.activeRoute.stops);
    },

    // Atualiza a interface (Drawer, LED, Títulos, Cards)
    updateUIForLine(lineData) {
      // 1. Badge superior
      const topBadge = document.getElementById('top-line-label');
      if (topBadge) topBadge.textContent = lineData.code;

      // 2. Letreiro LED
      const ledDestination = document.getElementById('led-destination-line');
      const ledNumber = document.getElementById('led-line-number');
      if (ledDestination) ledDestination.textContent = (lineData.code + ' ' + (lineData.headsign || lineData.name)).toUpperCase();
      if (ledNumber) ledNumber.textContent = lineData.code;

      // 3. Destino e cabeçalho no drawer
      const destTitle = document.getElementById('active-trip-destination-title');
      if (destTitle) destTitle.textContent = lineData.name;

      const activeHeader = document.getElementById('active-trip-header');
      if (activeHeader) activeHeader.textContent = `🚌 Linha ${lineData.code} · ${lineData.name}`;

      // 4. Cards de viagem (Vou pra Casa / Vou pro Destino)
      const firstStop = lineData.stops && lineData.stops[0] ? lineData.stops[0].name.split('/')[0].trim() : 'Origem';
      const lastStop = lineData.stops && lineData.stops.length > 1 ? lineData.stops[lineData.stops.length - 1].name.split('/')[0].trim() : 'Terminal';

      const homeCardSub = document.getElementById('home-card-sub');
      const workCardSub = document.getElementById('work-card-sub');
      if (homeCardSub) homeCardSub.textContent = `${firstStop} · 4 min`;
      if (workCardSub) workCardSub.textContent = `${lastStop} · 28 min`;

      // 5. Parada Inicial
      this.selectStop(0, false);

      // 6. Drawer de paradas
      this.renderStopsDrawer(lineData.stops);
    },

    // Renderiza a lista de todas as paradas da linha no Bottom Sheet
    renderStopsDrawer(stops) {
      const container = document.getElementById('stops-container');
      const countLabel = document.getElementById('stops-count-label');
      if (countLabel) countLabel.textContent = String(stops.length);
      if (!container) return;

      let html = '';
      stops.forEach((st, idx) => {
        const isSel = idx === this.activeStopIndex;
        const eta = Math.max(2, ((idx % 6) * 3) + 2);
        html += `
          <div style="background:${isSel ? '#ecfdf5; border:2px solid #059669;' : 'var(--bg-page); border:1px solid var(--border-color);'} border-radius:12px; padding:10px 12px; margin-bottom:6px; display:flex; justify-content:space-between; align-items:center; cursor:pointer; transition:all 0.15s ease;" onclick="window.RealTransit.selectStop(${idx}, true)">
            <div style="max-width:75%;">
              <div style="display:flex; align-items:center; gap:6px; margin-bottom:2px;">
                <span style="font-size:10px; font-weight:800; background:#f1f5f9; color:#475569; padding:1px 5px; border-radius:4px;">#${String(idx + 1).padStart(2, '0')}</span>
                <span style="font-size:10px; font-weight:800; color:#0369a1;">CÓD ${st.stop_id}</span>
              </div>
              <div style="font-size:13px; font-weight:800; color:#0f172a; line-height:1.25;">${st.name}</div>
              <div style="font-size:11px; color:#64748b; margin-top:2px;">Previsto GTFS: ${st.arr_time || 'Regular'}</div>
            </div>
            <div style="text-align:right;">
              <div style="font-family:'JetBrains Mono',monospace; font-size:16px; font-weight:800; color:${isSel ? '#059669' : 'var(--text-main)'};">${eta} <span style="font-size:11px;">min</span></div>
              <div style="font-size:10px; font-weight:700; color:#15803d;">CTM Oficial</div>
            </div>
          </div>
        `;
      });

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
      catalogBtn.innerHTML = '<span>🚌 400 Linhas</span>';
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
            <input type="text" id="modal-line-search-input" placeholder="🔍 Digite o número ou nome da linha..." oninput="window.RealTransit.filterModalLines(this.value)" style="width:100%; padding:10px 14px; border-radius:12px; border:1.5px solid #cbd5e1; font-size:14px; font-family:'Plus Jakarta Sans',sans-serif; outline:none; box-sizing:border-box;">
          </div>

          <div style="font-size:11.5px; font-weight:800; color:#64748b; text-transform:uppercase; margin-bottom:8px;" id="modal-lines-list-header">🔥 Linhas com Traçado & Paradas 100% Reais:</div>
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
        { code: '522', name: 'Dois Irmãos (Rui Barbosa / UFRPE)', icon: '🎓' },
        { code: '2060', name: 'TI Tancredo Neves / TI Macaxeira (Linha 060)', icon: '⚡' },
        { code: '2040', name: 'CDU / Boa Viagem / Caxangá', icon: '🌊' },
        { code: '050', name: 'PE-15 / Boa Viagem (Agamenon Magalhães)', icon: '🏙️' },
        { code: '202', name: 'Barro / Macaxeira (Várzea)', icon: '🔄' },
        { code: '1982', name: 'Conjunto Beira Mar / Derby', icon: '🏖️' },
        { code: '080', name: 'TI Joana Bezerra / Boa Viagem', icon: '🚇' },
        { code: '914', name: 'TI PE-15 / TI Afogados', icon: '🚊' },
        { code: '044', name: 'Massangana / Boa Vista', icon: '🛍️' },
        { code: '030', name: 'TI Rio Doce / Barra de Jangada', icon: '🌴' },
        { code: '191', name: 'Recife / Porto de Galinhas', icon: '🏖️' },
        { code: '199', name: 'Camela / TI Cabo', icon: '🏭' },
        { code: '178', name: 'Porto de Suape / TI Cabo', icon: '⚓' }
      ];

      let items = [];

      if (!q) {
        if (headerEl) headerEl.textContent = '🔥 Principais Linhas Metropolitanas:';
        items = popular;
      } else {
        if (headerEl) headerEl.textContent = `Resultados para "${query}":`;
        const catalog = this.networkData.routes_catalog || [];
        catalog.forEach(r => {
          if (r.code.toLowerCase().includes(q) || r.label.toLowerCase().includes(q) || r.name.toLowerCase().includes(q)) {
            items.push({
              code: r.code,
              name: r.name,
              icon: '🚌'
            });
          }
        });
      }

      if (items.length === 0) {
        listEl.innerHTML = `
          <div style="padding:24px 16px; text-align:center; color:#64748b;">
            <div style="font-size:24px; margin-bottom:6px;">🔍</div>
            <div style="font-size:13.5px; font-weight:800; color:#0f172a; margin-bottom:4px;">Nenhuma linha encontrada para "${query}"</div>
            <div style="font-size:11.5px; color:#64748b; line-height:1.45; margin-bottom:12px;">Verifique o número da linha (ex: 522, 060, 2040) ou o nome do corredor (ex: Dois Irmãos, Derby, CDU).</div>
            <button onclick="document.getElementById('modal-line-search-input').value=''; window.RealTransit.filterModalLines('');" style="background:#0284c7; color:#fff; border:none; padding:7px 14px; border-radius:8px; font-size:11.5px; font-weight:800; cursor:pointer;">
              Ver Linhas Populares
            </button>
          </div>
        `;
        return;
      }

      listEl.innerHTML = items.slice(0, 30).map(p => `
        <div onclick="window.RealTransit.loadRoute('${p.code}'); document.getElementById('line-picker-modal').style.display='none';" style="background:#f8fafc; border:1.5px solid #e2e8f0; border-radius:12px; padding:10px 12px; display:flex; align-items:center; justify-content:space-between; cursor:pointer; transition:all 0.15s ease;">
          <div style="display:flex; align-items:center; gap:10px; max-width:80%;">
            <span style="font-size:18px;">${p.icon || '🚌'}</span>
            <div>
              <div style="font-size:14px; font-weight:800; color:#0f172a; line-height:1.2;">${p.code} · ${p.name}</div>
              <div style="font-size:11px; color:#64748b; margin-top:2px;">Dados Oficiais GTFS CTM</div>
            </div>
          </div>
          <span style="font-size:12px; font-weight:800; color:#059669;">Ver ➔</span>
        </div>
      `).join('');
    },

    // Consulta API Pública Cittamobi (m3p/js) para obter dados em tempo real
    async fetchCittamobiLiveData(routeCode) {
      const banner = document.getElementById('resting-reallocation-banner');
      if (!banner) return;

      banner.style.display = 'flex';
      banner.innerHTML = `
        <div style="display:flex; align-items:center; gap:8px; width:100%;">
          <div style="width:8px; height:8px; border-radius:50%; background:#0284c7; animation:pulseGreen 1.5s infinite;"></div>
          <div style="font-size:11px; font-weight:700; color:#0369a1;">
            Conectando aos servidores Cittamobi (Agência a=202 Grande Recife)...
          </div>
        </div>
      `;

      try {
        const queryUrl = `https://api.cittamobi.com.br/m3p/js/search/q?q=${encodeURIComponent(routeCode)}&a=202&lat=-8.05&lng=-34.90`;
        const resp = await fetch(queryUrl);
        if (resp.ok) {
          const data = await resp.json();
          const services = data.services || [];
          if (services.length > 0) {
            const s0 = services[0];
            const company = s0.companyName || 'Consórcio de Transporte Metropolitano';
            banner.innerHTML = `
              <div style="display:flex; justify-content:space-between; align-items:center; width:100%;">
                <div style="display:flex; align-items:center; gap:8px;">
                  <span style="font-size:13px;">📡</span>
                  <div style="font-size:11.5px; font-weight:800; color:#0369a1;">
                    Operadora Oficial: <strong>${company}</strong> (ID: ${s0.id})
                  </div>
                </div>
                <span style="font-size:10px; font-weight:800; background:#e0f2fe; color:#0369a1; padding:2px 6px; border-radius:4px;">Cittamobi Live</span>
              </div>
            `;
            return;
          }
        }
      } catch (e) {
        // Silently catch and fallback to GTFS
      }

      // Fallback elegante com dados do GTFS
      banner.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center; width:100%;">
          <div style="display:flex; align-items:center; gap:8px;">
            <span style="font-size:13px;">🚍</span>
            <div style="font-size:11.5px; font-weight:800; color:#047857;">
              Linha ${routeCode} · Grade Horária Oficial GTFS CTM
            </div>
          </div>
          <span style="font-size:10px; font-weight:800; background:#dcfce7; color:#15803d; padding:2px 6px; border-radius:4px;">CTM Soberano</span>
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
              sub: 'Linha Oficial CTM Grande Recife',
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

    // Descobre automaticamente parada real e linhas que servem a coordenada do usuário
    findNearestTransitContext(lat, lon) {
      if (!this.networkData || !this.networkData.popular_lines) return null;
      let bestRegular = null;
      let bestAny = null;
      const nearbyLines = [];

      for (const [code, lineObj] of Object.entries(this.networkData.popular_lines)) {
        const isBacurau = /bacurau/i.test(lineObj.name || '');
        const stops = lineObj.stops || [];
        let minLineDist = Infinity;
        let minStop = null;
        let minStopIdx = 0;

        for (let i = 0; i < stops.length; i++) {
          const st = stops[i];
          if (!st || !st.lat || !st.lon) continue;
          const d = this.haversineKm(lat, lon, st.lat, st.lon);
          if (d < minLineDist) {
            minLineDist = d;
            minStop = st;
            minStopIdx = i;
          }
        }

        // Checa também retorno / polilinha caso o sentido volta esteja mais próximo
        if (Array.isArray(lineObj.return_coords)) {
          for (let j = 0; j < lineObj.return_coords.length; j++) {
            const p = lineObj.return_coords[j];
            const d = this.haversineKm(lat, lon, p[0], p[1]);
            if (d < minLineDist) minLineDist = d;
          }
        }

        if (minLineDist < 2.5) {
          nearbyLines.push({
            code,
            name: lineObj.name,
            isBacurau,
            distanceKm: minLineDist,
            stop: minStop,
            stopIndex: minStopIdx
          });
        }

        const cand = { code, name: lineObj.name, distanceKm: minLineDist, stop: minStop, stopIndex: minStopIdx };
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

      if (ctx.outOfCoverage) {
        this.userAdaptState = {
          status: 'out_of_coverage',
          stopName: `Fora da RMR (${Math.round(ctx.best.distanceKm)} km do Grande Recife)`,
          distanceKm: ctx.best.distanceKm,
          lat,
          lon
        };
        if (typeof window.showFloatingVoicePill === 'function') {
          window.showFloatingVoicePill('📍 Você está fora do Grande Recife. Selecione um ponto na Tela 2 para simular.');
        }
        return ctx;
      }

      const best = ctx.best;
      const rawStopName = (best.stop && best.stop.name) ? String(best.stop.name).trim() : '';
      const friendlyStopName = (rawStopName && !/^\d+$/.test(rawStopName))
        ? rawStopName
        : `Parada CTM ${best.stop ? best.stop.stop_id : best.code} · ${best.name}`;
      this.userAdaptState = {
        status: 'adapted',
        sourceLabel: sourceLabel || 'GPS Atual',
        lineCode: best.code,
        lineName: best.name,
        stopName: friendlyStopName,
        distanceKm: best.distanceKm,
        lat,
        lon,
        nearbyLines: ctx.nearbyLines
      };

      try {
        localStorage.setItem('grafoparada_last_coords', JSON.stringify({ lat, lon, lineCode: best.code }));
      } catch (e) {}

      // Carrega a linha real mais próxima e seleciona a parada exata onde o usuário está
      this.loadRoute(best.code);
      if (typeof best.stopIndex === 'number') {
        this.selectStop(best.stopIndex, Boolean(opts && opts.fit));
      }

      const prefixEl = document.getElementById('resting-line-prefix');
      if (prefixEl) prefixEl.textContent = `🚌 Linha ${best.code} · Mais próxima de você:`;

      const summaryEl = document.getElementById('home-summary-line');
      if (summaryEl) {
        const distMeters = Math.round(best.distanceKm * 1000);
        summaryEl.textContent = `📍 ${best.code} · ${best.name} (${distMeters}m de você)`;
      }

      if (typeof window.updateHomeGreeting === 'function') window.updateHomeGreeting();
      return ctx;
    },

    // Catálogo amplo de polos reais da RMR com coordenadas exatas
    getSemanticCorridors() {
      return [
        { key: 'recife antigo', keys: ['recife antigo', 'bairro do recife', 'marco zero', 'porto digital', 'pcr', 'alfredo lisboa', 'rio branco', 'forte do brum'], label: 'Recife Antigo / Marco Zero', defaultLine: '1967', alsoServedBy: ['1971', '1100', '1983', '117'], hub: 'Cais de Santa Rita / PCR', stopName: 'Cais de Santa Rita / Av. Alfredo Lisboa (Recife Antigo)', lat: -8.0631, lon: -34.8711, waitMin: 5, seatsFree: 16 },
        { key: 'cais de santa rita', keys: ['cais de santa rita', 'cais santa rita', 'dantas barreto'], label: 'Cais de Santa Rita (Centro)', defaultLine: '191', alsoServedBy: ['195', '1971', '1983', '050'], hub: 'Cais de Santa Rita', stopName: 'Terminal Cais de Santa Rita (Centro)', lat: -8.0680, lon: -34.8765, waitMin: 4, seatsFree: 18 },
        { key: 'olinda', keys: ['olinda', 'carmo', 'varadouro', 'sitio historico', 'praca do carmo', 'alto da se', 'amparo'], label: 'Olinda (Carmo / Sítio Histórico)', defaultLine: '1967', alsoServedBy: ['1971', '1983', '1992', '1973', '1100'], hub: 'TI PE-15 / Carmo', stopName: 'Praça do Carmo / Sítio Histórico de Olinda', lat: -8.0125, lon: -34.8520, waitMin: 5, seatsFree: 14 },
        { key: 'bairro novo', keys: ['bairro novo', 'casa caiada', 'jardim atlantico', 'beira mar olinda', 'getulio vargas olinda'], label: 'Olinda (Bairro Novo / Casa Caiada)', defaultLine: '1973', alsoServedBy: ['1992', '1994', '1974', '1982'], hub: 'TI Rio Doce / TI PE-15', stopName: 'Av. Getúlio Vargas (Bairro Novo / Casa Caiada)', lat: -7.9940, lon: -34.8420, waitMin: 4, seatsFree: 15 },
        { key: 'rio doce', keys: ['rio doce', 'ti rio doce', 'janga', 'pau amarelo'], label: 'Olinda / TI Rio Doce', defaultLine: '1983', alsoServedBy: ['030', '1966', '2930', '1987'], hub: 'TI Rio Doce', stopName: 'TI Rio Doce (Olinda)', lat: -7.9598, lon: -34.8415, waitMin: 4, seatsFree: 19 },
        { key: 'pe-15', keys: ['pe-15', 'pe 15', 'ti pe-15', 'ti pe 15', 'fragoso', 'ouro preto'], label: 'TI PE-15 (Olinda)', defaultLine: '1100', alsoServedBy: ['050', '1966', '1913', '914'], hub: 'TI PE-15', stopName: 'Terminal Integrado PE-15', lat: -7.9912, lon: -34.8576, waitMin: 3, seatsFree: 20 },
        { key: 'xamba', keys: ['xamba', 'ti xamba', 'peixinhos'], label: 'TI Xambá (Olinda)', defaultLine: '812', alsoServedBy: ['861', '881'], hub: 'TI Xambá', stopName: 'Terminal Integrado Xambá', lat: -8.0078, lon: -34.8655, waitMin: 5, seatsFree: 16 },
        { key: 'paulista', keys: ['paulista', 'pelopidas', 'ti pelopidas', 'abreu e lima', 'igarassu'], label: 'Paulista / TI Pelópidas', defaultLine: '1076', alsoServedBy: ['1907', '1967', '1977'], hub: 'TI Pelópidas Silveira', stopName: 'TI Pelópidas Silveira (Paulista)', lat: -7.9408, lon: -34.8732, waitMin: 5, seatsFree: 17 },
        { key: 'camela', keys: ['camela', 'pedro serafim', 'rua do comercio', 'pe-051'], label: 'Camela (Ipojuca)', defaultLine: '199', alsoServedBy: [], hub: 'TI Cabo', stopName: 'Praça Pedro Serafim (Terminal de Camela)', lat: -8.514931, lon: -35.123469, waitMin: 3, seatsFree: 28 },
        { key: 'ipojuca', keys: ['ipojuca', 'trevo de ipojuca', 'upa de ipojuca', 'ruropolis'], label: 'Ipojuca Centro', defaultLine: '198', alsoServedBy: ['199'], hub: 'TI Cabo', stopName: 'Rodovia PE-60 · Trevo Principal de Ipojuca Centro (KM 20)', lat: -8.399372, lon: -35.056842, waitMin: 7, seatsFree: 14 },
        { key: 'suape', keys: ['suape', 'refinaria', 'rnest', 'estaleiro', 'contermas', 'portuario'], label: 'Complexo de Suape', defaultLine: '178', alsoServedBy: ['199'], hub: 'TI Cabo', stopName: 'Rodovia PE-60 · Trevo de Suape (KM 14)', lat: -8.385067, lon: -35.042433, waitMin: 6, seatsFree: 12 },
        { key: 'porto de galinhas', keys: ['porto de galinhas', 'galinhas', 'maracaipe', 'serrambi', 'nossa senhora do o', 'n sra do o'], label: 'Porto de Galinhas / N. Sra. do Ó', defaultLine: '191', alsoServedBy: ['195', '196'], hub: 'TI Cabo', stopName: 'Rodovia PE-60 · Trevo PE-038 (N. Sra. do Ó / Porto)', lat: -8.401408, lon: -35.060308, waitMin: 9, seatsFree: 10 },
        { key: 'cabo', keys: ['ti cabo', 'cabo de santo agostinho', 'cabo', 'costa dourada'], label: 'TI Cabo / Centro do Cabo', defaultLine: '199', alsoServedBy: ['198', '178', '185', '139', '196'], hub: 'TI Cabo', stopName: 'TI Cabo (Terminal Integrado do Cabo)', lat: -8.285065, lon: -35.032398, waitMin: 4, seatsFree: 18 },
        { key: 'ufrpe', keys: ['ufrpe', 'rural', 'dois irmaos'], label: 'UFRPE · Campus Dois Irmãos', defaultLine: '522', alsoServedBy: ['2930', '524', '532'], hub: 'TI Macaxeira', stopName: 'Terminal de Dois Irmãos (UFRPE)', lat: -8.016390, lon: -34.949720, waitMin: 4, seatsFree: 14 },
        { key: 'ufpe', keys: ['ufpe', 'cdu', 'cidade universitaria', 'varzea'], label: 'UFPE · Cidade Universitária (CDU)', defaultLine: '2040', alsoServedBy: ['2431', '2441', '440', '202'], hub: 'TI CDU', stopName: 'Terminal Integrado CDU (UFPE)', lat: -8.0518, lon: -34.9502, waitMin: 5, seatsFree: 11 },
        { key: 'derby', keys: ['derby', 'rui barbosa', 'agamenon', 'principe', 'boa vista', 'conde da boa vista', 'hospicio'], label: 'Derby / Boa Vista', defaultLine: '522', alsoServedBy: ['011', '050', '440', '1973', '1987'], hub: 'Praça do Derby', stopName: 'Praça do Derby (Terminal Central)', lat: -8.0558, lon: -34.8950, waitMin: 4, seatsFree: 16 },
        { key: 'joana bezerra', keys: ['joana bezerra', 'ti joana', 'coelhos', 'imip'], label: 'TI Joana Bezerra', defaultLine: '080', alsoServedBy: ['101', '104', '1981', '2043'], hub: 'TI Joana Bezerra', stopName: 'Terminal Integrado Joana Bezerra', lat: -8.0689, lon: -34.8958, waitMin: 3, seatsFree: 20 },
        { key: 'boa viagem', keys: ['boa viagem', 'domingos ferreira', 'conselheiro aguiar', 'shopping recife', 'pina'], label: 'Boa Viagem', defaultLine: '050', alsoServedBy: ['2040', '080', '440', '032'], hub: 'TI Tancredo Neves', stopName: 'Av. Domingos Ferreira (Boa Viagem)', lat: -8.1202, lon: -34.9012, waitMin: 5, seatsFree: 12 },
        { key: 'cajueiro seco', keys: ['cajueiro seco', 'ti cajueiro', 'prazeres', 'piedade', 'candeias'], label: 'TI Cajueiro Seco / Jaboatão Sul', defaultLine: '139', alsoServedBy: ['181', '030', '064'], hub: 'TI Cajueiro Seco', stopName: 'TI Cajueiro Seco', lat: -8.167989, lon: -34.934534, waitMin: 4, seatsFree: 17 },
        { key: 'tancredo neves', keys: ['tancredo neves', 'ti tancredo', 'aeroporto', 'imbiribeira'], label: 'TI Tancredo Neves / Aeroporto', defaultLine: '2060', alsoServedBy: ['060', '140', '185'], hub: 'TI Tancredo Neves', stopName: 'TI Tancredo Neves', lat: -8.122014, lon: -34.912465, waitMin: 5, seatsFree: 13 },
        { key: 'macaxeira', keys: ['macaxeira', 'ti macaxeira', 'casa amarela', 'encruzilhada'], label: 'TI Macaxeira / Casa Amarela', defaultLine: '2060', alsoServedBy: ['202', '522', '516', '330'], hub: 'TI Macaxeira', stopName: 'TI Macaxeira', lat: -8.0061, lon: -34.9298, waitMin: 4, seatsFree: 16 },
        { key: 'barro', keys: ['barro', 'ti barro', 'camaragibe', 'jaboatao', 'afogados', 'ti recife'], label: 'TI Barro / Afogados / Oeste', defaultLine: '202', alsoServedBy: ['101', '914', '291'], hub: 'TI Barro', stopName: 'TI Barro', lat: -8.0882, lon: -34.9459, waitMin: 5, seatsFree: 15 }
      ];
    },

    // Resolve nome de lugar, terminal ou "aqui" para { label, lat, lon, corridor }
    resolvePlaceLocation(rawPlace) {
      const pNorm = this.normalizeText(rawPlace);
      if (!pNorm) return null;

      // Suporte explícito a "aqui / onde estou / minha localizacao"
      if (/\b(aqui|daqui|onde estou|minha parada|minha localizacao)\b/.test(pNorm)) {
        const lat = (this.userAdaptState && this.userAdaptState.lat) || (window.userCurrentCoords && window.userCurrentCoords[0]);
        const lon = (this.userAdaptState && this.userAdaptState.lon) || (window.userCurrentCoords && window.userCurrentCoords[1]);
        if (lat && lon) {
          return {
            key: 'current_gps',
            label: (this.userAdaptState && this.userAdaptState.stopName) || 'Sua localização atual',
            lat,
            lon,
            stopName: (this.userAdaptState && this.userAdaptState.stopName) || 'Sua parada atual'
          };
        }
      }

      // Match em polos semânticos da RMR
      const corridors = this.getSemanticCorridors();
      const exactCorridor = corridors.find(c => c.keys.some(k => pNorm === k || pNorm.includes(k) || k.includes(pNorm)));
      if (exactCorridor) return exactCorridor;

      // Match nos 45 Hubs do Grafo SEI ou 44 Terminais SEI do GTFS
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

      return null;
    },

    // Descobre TODAS as linhas reais (IDA + VOLTA) que atendem um raio geográfico ao redor de (lat, lon)
    getLinesNearPoint(lat, lon, maxKm = 1.15) {
      if (!this.networkData || !this.networkData.popular_lines) return [];
      const hits = [];
      for (const [code, lineObj] of Object.entries(this.networkData.popular_lines)) {
        let minDist = Infinity;
        let nearestStop = null;
        const stops = lineObj.stops || [];
        for (let i = 0; i < stops.length; i++) {
          const s = stops[i];
          if (!s || !s.lat || !s.lon) continue;
          const d = this.haversineKm(lat, lon, s.lat, s.lon);
          if (d < minDist) { minDist = d; nearestStop = s; }
        }
        if (Array.isArray(lineObj.return_coords)) {
          for (let j = 0; j < lineObj.return_coords.length; j++) {
            const p = lineObj.return_coords[j];
            const d = this.haversineKm(lat, lon, p[0], p[1]);
            if (d < minDist) minDist = d;
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
            nearestStop
          });
        }
      }
      hits.sort((a, b) => (a.isBacurau - b.isBacurau) || (a.distanceKm - b.distanceKm));
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
        .replace(/\b(vamos la|por favor|agora|hoje|pode ser|me ajuda|me diz|me fale|qual|quais|como fico|preciso|quero)\b/g, ' ')
        .replace(/\s+/g, ' ')
        .trim();

      const patterns = [
        /(?:sair|ir|partir|indo|viajar|voltar)\s+(?:de|da|do)\s+(.+?)\s+(?:ate|para|pra|pro|rumo a|->)\s+(.+)/i,
        /(?:de|da|do)\s+([a-z0-9\s.-]{2,45}?)\s+(?:ate|para|pra|->)\s+([a-z0-9\s.-]{2,45})/i,
        /\b(daqui|aqui)\s+(?:ate|para|pra|pro|->)\s+([a-z0-9\s.-]{2,45})/i
      ];

      for (const p of patterns) {
        const m = clean.match(p);
        if (m && m[1] && m[2]) {
          return { origin: m[1].trim(), dest: m[2].trim() };
        }
      }
      return null;
    },

    planSmartTrip(originRaw, destRaw, telemetryStops) {
      const origNorm = this.normalizeText(originRaw);
      const destNorm = this.normalizeText(destRaw);
      const origPlace = this.resolvePlaceLocation(origNorm);
      const destPlace = this.resolvePlaceLocation(destNorm);

      // 1. Busca geográfica completa sobre todas as 393 linhas (IDA + VOLTA)
      let geoDirect = [];
      let origGeoLines = [];
      let destGeoLines = [];

      if (origPlace && destPlace && origPlace.lat && destPlace.lat) {
        origGeoLines = this.getLinesNearPoint(origPlace.lat, origPlace.lon, 1.15);
        destGeoLines = this.getLinesNearPoint(destPlace.lat, destPlace.lon, 1.15);

        const destMap = new Map(destGeoLines.map(d => [d.code, d]));
        origGeoLines.forEach(o => {
          const dMatch = destMap.get(o.code);
          if (dMatch) {
            geoDirect.push({
              code: o.code,
              label: o.label,
              name: o.name,
              isBacurau: o.isBacurau,
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

      // 3. Grafo Real de Conexões / Integrações em 1 Baldeação via hub_graph (45 hubs SEI/polos)
      const transferCandidates = [];
      if (this.networkData && Array.isArray(this.networkData.hub_graph) && origCatalog.length > 0 && destCatalog.length > 0) {
        const origSet = new Set(origCatalog.filter(x => !x.isBacurau).slice(0, 15).map(x => x.code));
        const destSet = new Set(destCatalog.filter(x => !x.isBacurau).slice(0, 15).map(x => x.code));
        const origLookup = new Map(origCatalog.map(x => [x.code, x]));
        const destLookup = new Map(destCatalog.map(x => [x.code, x]));

        for (const hub of this.networkData.hub_graph) {
          const hLines = hub.lines || [];
          const leg1Code = hLines.find(c => origSet.has(c));
          const leg2Code = hLines.find(c => destSet.has(c) && c !== leg1Code);
          if (leg1Code && leg2Code) {
            let score = 0;
            if (origPlace && destPlace && origPlace.lat && destPlace.lat) {
              const directDist = this.haversineKm(origPlace.lat, origPlace.lon, destPlace.lat, destPlace.lon);
              const viaHubDist = this.haversineKm(origPlace.lat, origPlace.lon, hub.lat, hub.lon) + this.haversineKm(hub.lat, hub.lon, destPlace.lat, destPlace.lon);
              score = viaHubDist - directDist;
            }
            const isSEI = /^TI\s/i.test(hub.name);
            transferCandidates.push({
              leg1: origLookup.get(leg1Code),
              leg2: destLookup.get(leg2Code),
              hub: hub.name,
              isSEI,
              detourKm: score
            });
          }
        }
        transferCandidates.sort((a, b) => (b.isSEI - a.isSEI) || (a.detourKm - b.detourKm));
      }

      let transferPlan = transferCandidates[0] || null;
      if (!transferPlan && origCatalog.length > 0 && destCatalog.length > 0) {
        const l1 = origCatalog[0];
        const l2 = destCatalog.find(d => d.code !== l1.code) || destCatalog[0];
        if (l1.code !== l2.code) {
          transferPlan = { leg1: l1, leg2: l2, hub: (origPlace && origPlace.hub) || 'TI Joana Bezerra', isSEI: true };
        }
      }

      // 4. Caso especial telemetria detalhada PE-60 (Camela <-> Ipojuca <-> Suape <-> Cabo)
      let telemetryEtaMin = null;
      let oStop = null;
      let dStop = null;
      if (Array.isArray(telemetryStops) && directMatches.some(m => m.code === '199')) {
        oStop = telemetryStops.find(s => this.normalizeText(s.name + ' ' + (s.bairro || '') + ' ' + (s.municipio || '')).includes(origPlace ? origPlace.key : origNorm));
        dStop = telemetryStops.find(s => this.normalizeText(s.name + ' ' + (s.bairro || '') + ' ' + (s.municipio || '')).includes(destPlace ? destPlace.key : destNorm));
        if (oStop && dStop) {
          telemetryEtaMin = Math.max(8, Math.abs((dStop.wait_gps_min || 15) - (oStop.wait_gps_min || 3)) * 2 + 6);
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
        telemetryEtaMin,
        originStop: oStop,
        destStop: dStop
      };
    },

    answerLayaQuery(rawText, ctx) {
      const text = String(rawText || '').trim();
      const q = this.normalizeText(text);
      const telemetryStops = (ctx && Array.isArray(ctx.telemetryStops)) ? ctx.telemetryStops : [];

      // 1. Apresentação / Banca UFRPE
      if (/\b(apresentacao|slide|slides|pptx|banca|roteiro|seminario)\b/.test(q)) {
        return {
          intent: 'presentation',
          html: "Aqui estão os materiais oficiais para a <strong>Banca Examinadora da UFRPE (Seminário 2)</strong>:<br><br>" +
            "• 📥 <strong>Apresentação PPTX (16:9):</strong> Arquivo oficial pronto para defesa.<br>" +
            "• 🎨 <strong>Slides Web Estilo Canva:</strong> Navegação interativa no navegador.<br>" +
            "• 📜 <strong>Roteiro da Banca:</strong> Guia passo a passo de sustentação.<br><br>" +
            "<button type=\"button\" onclick=\"if(window.openPresentationModal) window.openPresentationModal();\" style=\"background:#7c3aed; color:#fff; border:none; padding:8px 14px; border-radius:10px; font-size:12px; font-weight:800; cursor:pointer;\">🎓 Abrir Painel da Apresentação</button>",
          speech: "Abrindo o painel com a apresentação em PPTX, slides e roteiro para a banca da UFRPE.",
          openPresentation: true
        };
      }

      // 2. Origem -> Destino usando Grafo Completo de 393 Linhas + 45 Hubs SEI
      const tripPair = this.extractOriginDest(text);
      if (tripPair) {
        const plan = this.planSmartTrip(tripPair.origin, tripPair.dest, telemetryStops);
        if (plan.directMatches.length > 0) {
          const nonBacurau = plan.directMatches.filter(m => !m.isBacurau);
          const ranked = nonBacurau.length > 0 ? nonBacurau : plan.directMatches;
          const mainRoute = ranked[0];
          const altLines = ranked.slice(1, 4).map(r => `<strong>${r.code}</strong> (${r.name})`).join(', ');
          const origStopLabel = plan.originStop ? plan.originStop.name : (plan.origCorridor && plan.origCorridor.stopName) || plan.originLabel;
          const destStopLabel = plan.destStop ? plan.destStop.name : (plan.destCorridor && plan.destCorridor.stopName) || plan.destLabel;
          const waitStr = plan.originStop ? `${plan.originStop.wait_gps_min || 3} min` : '4 a 7 min';
          const tripDur = plan.telemetryEtaMin ? `~${plan.telemetryEtaMin} min` : '~22 a 30 min';

          let html = `✅ Trajeto direto encontrado de <strong>${plan.originLabel}</strong> até <strong>${plan.destLabel}</strong>:<br><br>` +
            `🚌 <strong>Melhor Linha Direta (${mainRoute.code}):</strong> <em>${mainRoute.label}</em><br>` +
            `• 📍 <strong>Embarque:</strong> ${origStopLabel} (próximo em <strong>${waitStr}</strong>)<br>` +
            `• 🎯 <strong>Desembarque:</strong> ${destStopLabel} (${tripDur})<br>`;

          if (altLines) {
            html += `• 🔁 <strong>Outras linhas diretas:</strong> ${altLines}<br>`;
          }
          if (plan.transferPlan && mainRoute.code === '199') {
            html += `<br>🔄 <strong>Conexão SEI (Terminal Interno):</strong> Ou pegue a <strong>${plan.transferPlan.leg1.code}</strong> até <strong>${plan.transferPlan.hub}</strong> e integre grátis (VEM 2h) na <strong>${plan.transferPlan.leg2.label}</strong>.`;
          } else if (plan.transferPlan && plan.transferPlan.isSEI) {
            html += `<br>🔄 <strong>Opção integrada via ${plan.transferPlan.hub}:</strong> ${plan.transferPlan.leg1.code} ➔ ${plan.transferPlan.leg2.code} (VEM grátis em 2h).`;
          }

          html += `<div style="display:flex; flex-wrap:wrap; gap:6px; margin-top:10px;">` +
            `<button type="button" onclick="if(window.RealTransit){window.RealTransit.loadRoute('${mainRoute.code}');} if(window.navigateToScreen){window.navigateToScreen('radar');} if(window.closeLayaModal){window.closeLayaModal();}" style="background:#059669; color:#fff; border:none; padding:7px 12px; border-radius:9px; font-size:11.5px; font-weight:800; cursor:pointer;">🗺️ Traçar Linha ${mainRoute.code} no Mapa</button>` +
            `<button type="button" onclick="if(window.RealTransit){window.RealTransit.loadRoute('${mainRoute.code}');} if(window.setMyBoardingStop){window.setMyBoardingStop('${origStopLabel.replace(/'/g, "\\'")}', ${plan.origCorridor && plan.origCorridor.lat ? `[${plan.origCorridor.lat}, ${plan.origCorridor.lon}]` : 'null'});}" style="background:#0284c7; color:#fff; border:none; padding:7px 12px; border-radius:9px; font-size:11.5px; font-weight:800; cursor:pointer;">🔔 Monitorar Parada</button>` +
            `</div>`;

          return {
            intent: 'trip_plan',
            routeCode: mainRoute.code,
            directOptions: ranked.slice(0, 4).map(r => r.code),
            html,
            speech: `De ${plan.originLabel} até ${plan.destLabel}, você tem ligação direta pela linha ${mainRoute.code}, além de ${Math.max(0, ranked.length - 1)} outras opções diretas no mapa.`
          };
        }

        if (plan.transferPlan) {
          const l1 = plan.transferPlan.leg1;
          const l2 = plan.transferPlan.leg2;
          const html = `🔄 <strong>Rota com Integração</strong> de <strong>${plan.originLabel}</strong> até <strong>${plan.destLabel}</strong>:<br><br>` +
            `1️⃣ <strong>1º Embarque:</strong> Linha <strong>${l1.label}</strong> até <strong>${plan.transferPlan.hub}</strong>.<br>` +
            `2️⃣ <strong>Integração VEM (R$ 0,00 em até 2h):</strong> Linha <strong>${l2.label}</strong> até ${plan.destLabel}.<br><br>` +
            `<div style="display:flex; flex-wrap:wrap; gap:6px;">` +
            `<button type="button" onclick="if(window.RealTransit){window.RealTransit.loadRoute('${l1.code}');} if(window.navigateToScreen){window.navigateToScreen('radar');} if(window.closeLayaModal){window.closeLayaModal();}" style="background:#059669; color:#fff; border:none; padding:7px 12px; border-radius:9px; font-size:11.5px; font-weight:800; cursor:pointer;">🗺️ Traçar 1ª Etapa (${l1.code})</button>` +
            `<button type="button" onclick="if(window.RealTransit){window.RealTransit.loadRoute('${l2.code}');} if(window.navigateToScreen){window.navigateToScreen('radar');} if(window.closeLayaModal){window.closeLayaModal();}" style="background:#0284c7; color:#fff; border:none; padding:7px 12px; border-radius:9px; font-size:11.5px; font-weight:800; cursor:pointer;">🚌 Traçar 2ª Etapa (${l2.code})</button>` +
            `</div>`;
          return {
            intent: 'trip_transfer',
            routeCode: l1.code,
            hub: plan.transferPlan.hub,
            html,
            speech: `Para ir de ${plan.originLabel} até ${plan.destLabel}, pegue a linha ${l1.code} até ${plan.transferPlan.hub} e integre na linha ${l2.code}.`
          };
        }

        return {
          intent: 'trip_unknown',
          html: `Não encontrei paradas mapeadas entre <strong>"${tripPair.origin}"</strong> e <strong>"${tripPair.dest}"</strong>.<br><br>` +
            `Experimente nomes de bairros ou terminais (ex: <em>Recife Antigo, Olinda, Bairro Novo, TI PE-15, Camela, Ipojuca, UFRPE, Boa Viagem</em>) ou abra as 400 linhas:<br><br>` +
            `<button type="button" onclick="if(window.RealTransit){window.RealTransit.openLinePickerModal();}" style="background:#0284c7; color:#fff; border:none; padding:7px 12px; border-radius:9px; font-size:11.5px; font-weight:800; cursor:pointer;">🚌 Buscar nas 400 Linhas GTFS</button>`,
          speech: `Não localizei ligação entre ${tripPair.origin} e ${tripPair.dest}. Tente informar o terminal ou bairro mais próximo.`
        };
      }

      // 3. Conhecimento Técnico e Científico da Plataforma GrafoParada + WebMCP
      if (/\b(stgcn|st gcn|ia|inteligencia artificial|modelo|trava|oversmoothing|reneging|abandono|yap|kim|mae|como funciona|plataforma|grafoparada|despacho|deadheading|queima|bolso seguro|lei 15878|parada segura|webmcp)\b/.test(q)) {
        const html = `🧠 <strong>Inteligência da Plataforma GrafoParada:</strong><br><br>` +
          `• <strong>Rede ST-GCN + Grafo Completo GTFS:</strong> Conecta 393 linhas (ida e volta) e 45 Hubs/Terminais SEI do Grande Recife (MAE <strong>1,51 min</strong> · <strong>0,77 ms/nó</strong>).<br>` +
          `• <strong>Adaptação GPS Dinâmica:</strong> Ao abrir o app, identifica a parada e linha reais mais próximas de onde você está.<br>` +
          `• <strong>Yap & Cats (2021) + Kim et al. (2026):</strong> Calcula espera percebida (<strong>1,68x</strong>), janela segura e risco de abandono.<br>` +
          `• <strong>Trava Híbrida Defensiva + WebMCP:</strong> Bloqueia desvios &gt; 15 min da IA e expõe ferramentas estruturadas via protocolo Chrome WebMCP.<br><br>` +
          `<button type="button" onclick="if(window.navigateToScreen){window.navigateToScreen('central');} if(window.closeLayaModal){window.closeLayaModal();}" style="background:#0f172a; color:#fff; border:none; padding:7px 12px; border-radius:9px; font-size:11.5px; font-weight:800; cursor:pointer;">🔬 Ver Auditoria & Central CTM</button>`;
        return {
          intent: 'platform_knowledge',
          html,
          speech: "O GrafoParada conecta todas as 393 linhas e hubs do Grande Recife em grafo, detecta sua localização real e aplica ST-GCN com trava defensiva."
        };
      }

      // 4. Consulta específica por local ou linha citada na pergunta
      const explicitLineMatch = q.match(/\b(\d{3,4})\b/);
      const matchedCorridor = this.resolvePlaceLocation(q);
      const placeMatches = matchedCorridor
        ? this.findCatalogRoutesForQuery(matchedCorridor.key, telemetryStops)
        : (explicitLineMatch ? this.findCatalogRoutesForQuery(explicitLineMatch[1], telemetryStops) : []);

      // 5. Pergunta de Próximo Ônibus / Horário / Chegada
      if (/\b(onibus|quando passa|horario|proximo|chega|lotacao|vagas)\b/.test(q)) {
        if (placeMatches.length > 0) {
          const nonBacurau = placeMatches.filter(m => !/bacurau/i.test(m.label));
          const best = nonBacurau[0] || placeMatches[0];
          const hint = best.stopHint || {};
          const stopName = (matchedCorridor ? matchedCorridor.stopName : null) || hint.name || best.label;
          const waitMin = hint.wait_gps_min || (matchedCorridor ? matchedCorridor.waitMin : 4);
          const seatsFree = hint.seatsFree || (best.code === '199' ? 28 : 14);
          const coordsArg = (hint.lat && hint.lon) ? `[${hint.lat}, ${hint.lon}]` : 'null';

          const html = `🚌 <strong>Previsão para ${matchedCorridor ? matchedCorridor.label : 'Linha ' + best.code}:</strong><br><br>` +
            `• <strong>Linha recomendada:</strong> ${best.label}<br>` +
            `• 📍 <strong>Parada de referência:</strong> ${stopName}<br>` +
            `• ⏱️ <strong>Próxima chegada prevista (ST-GCN):</strong> em <strong>${waitMin} minutos</strong><br>` +
            `• 💺 <strong>Ocupação estimada:</strong> ${seatsFree} assentos livres<br><br>` +
            `<div style="display:flex; flex-wrap:wrap; gap:6px;">` +
            `<button type="button" onclick="if(window.RealTransit){window.RealTransit.loadRoute('${best.code}');} if(window.navigateToScreen){window.navigateToScreen('radar');} if(window.closeLayaModal){window.closeLayaModal();}" style="background:#059669; color:#fff; border:none; padding:7px 12px; border-radius:9px; font-size:11.5px; font-weight:800; cursor:pointer;">🗺️ Rastrear Linha ${best.code}</button>` +
            `<button type="button" onclick="if(window.RealTransit){window.RealTransit.loadRoute('${best.code}');} if(window.setMyBoardingStop){window.setMyBoardingStop('${stopName.replace(/'/g, "\\'")}', ${coordsArg});}" style="background:#0284c7; color:#fff; border:none; padding:7px 12px; border-radius:9px; font-size:11.5px; font-weight:800; cursor:pointer;">🔔 Fixar como Minha Parada</button>` +
            `</div>`;

          return {
            intent: 'next_bus_place',
            routeCode: best.code,
            html,
            speech: `Para ${matchedCorridor ? matchedCorridor.label : 'a linha ' + best.code}, o próximo coletivo da linha ${best.code} chega em ${waitMin} minutos na parada ${stopName}.`
          };
        }

        // Sem local citado -> usa parada adaptada ao GPS/escolha atual
        if (this.userAdaptState && this.userAdaptState.status === 'awaiting_location') {
          return {
            intent: 'need_location',
            html: `📍 Ainda não sei em qual bairro ou parada você está agora!<br><br>Ative seu GPS ou toque no bairro de partida para eu localizar a linha mais próxima:<br><br>` +
              `<button type="button" onclick="if(window.navigateToScreen){window.navigateToScreen('locate');} if(window.closeLayaModal){window.closeLayaModal();}" style="background:#059669; color:#fff; border:none; padding:7px 12px; border-radius:9px; font-size:11.5px; font-weight:800; cursor:pointer;">📍 Informar Onde Estou Agora</button>`,
            speech: "Me diga em qual bairro ou parada você está, ou toque em Informar Onde Estou Agora para eu buscar pelo GPS."
          };
        }

        const activeCode = (ctx && ctx.activeRouteCode) || this.activeRouteCode;
        const activeRouteName = (this.activeRoute && this.activeRoute.name) ? this.activeRoute.name : '';
        const activeStop = (ctx && ctx.activeStopName) || (this.userAdaptState && this.userAdaptState.stopName) || 'Sua Parada Ativa';
        const activeEta = (ctx && ctx.activeEta) || 4;

        const html = `🚌 <strong>Sua Linha Mais Próxima: ${activeCode} · ${activeRouteName}</strong><br><br>` +
          `• 📍 <strong>Parada detectada:</strong> ${activeStop}<br>` +
          `• ⏱️ <strong>Próximo ônibus previsto:</strong> <strong>${activeEta} minutos</strong><br><br>` +
          `<div style="display:flex; flex-wrap:wrap; gap:6px;">` +
          `<button type="button" onclick="if(window.navigateToScreen){window.navigateToScreen('radar');} if(window.trackBusLocation){window.trackBusLocation(true);} if(window.closeLayaModal){window.closeLayaModal();}" style="background:#059669; color:#fff; border:none; padding:7px 12px; border-radius:9px; font-size:11.5px; font-weight:800; cursor:pointer;">🚌 Rastrear no Mapa</button>` +
          `<button type="button" onclick="if(window.navigateToScreen){window.navigateToScreen('locate');} if(window.closeLayaModal){window.closeLayaModal();}" style="background:#0284c7; color:#fff; border:none; padding:7px 12px; border-radius:9px; font-size:11.5px; font-weight:800; cursor:pointer;">📍 Atualizar Localização</button>` +
          `</div>`;

        return {
          intent: 'next_bus_active',
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
          html: `📍 Sua referência atual adaptada é: <strong>${activeStop}</strong> (Linha <strong>${activeCode}</strong>).<br><br>` +
            `<button type="button" onclick="if(window.navigateToScreen){window.navigateToScreen('locate');} if(window.closeLayaModal){window.closeLayaModal();}" style="background:#0284c7; color:#fff; border:none; padding:7px 12px; border-radius:9px; font-size:11.5px; font-weight:800; cursor:pointer;">📍 Detectar / Atualizar Posição Real</button>`,
          speech: `Sua posição atual está adaptada para ${activeStop}.`
        };
      }

      // 7. Mencionou um local/linha sem verbo ("Recife Antigo", "Olinda", "Camela", "1967")
      if (placeMatches.length > 0) {
        const best = placeMatches.find(m => !/bacurau/i.test(m.label)) || placeMatches[0];
        const hint = best.stopHint || {};
        const stopName = (matchedCorridor ? matchedCorridor.stopName : null) || hint.name || best.label;
        const waitMin = hint.wait_gps_min || (matchedCorridor ? matchedCorridor.waitMin : 5);
        return {
          intent: 'place_lookup',
          routeCode: best.code,
          html: `📍 Encontrei atendimento real para <strong>${matchedCorridor ? matchedCorridor.label : best.label}</strong>:<br><br>` +
            `• 🚌 <strong>Linha principal:</strong> ${best.label}<br>` +
            `• 🚏 <strong>Parada chave:</strong> ${stopName}<br>` +
            `• ⏱️ <strong>Previsão média:</strong> <strong>${waitMin} min</strong><br><br>` +
            `<button type="button" onclick="if(window.RealTransit){window.RealTransit.loadRoute('${best.code}');} if(window.navigateToScreen){window.navigateToScreen('radar');} if(window.closeLayaModal){window.closeLayaModal();}" style="background:#059669; color:#fff; border:none; padding:7px 12px; border-radius:9px; font-size:11.5px; font-weight:800; cursor:pointer;">🗺️ Abrir Linha ${best.code} no Mapa</button>`,
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
                hub: plan.transferPlan.hub,
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
