# -*- coding: utf-8 -*-
"""
Suíte Integrada de Testes: Banco GTFS, Matriz 1.260 Pares O-D, Segurança XSS,
Voz PT-BR e Teste E2E Real em Google Chrome Headless (CDP + HTTP Local).

Execução: uv run pytest code/grafoparada_tec/test_e2e_e_motor.py -v
"""
from __future__ import annotations

import functools
import http.server
import json
import os
import re
import shutil
import socket
import socketserver
import subprocess
import tempfile
import threading
import time
import urllib.request
from pathlib import Path

import pytest
from websockets.sync.client import connect as ws_connect

TEC_DIR = Path(__file__).resolve().parent
ROOT_DIR = TEC_DIR.parent.parent
WEB_DIR = ROOT_DIR / "code" / "grafoparada_web"
INDEX_HTML = WEB_DIR / "index.html"
ENGINE_JS = WEB_DIR / "real_transit_engine.js"
LAYA_VOICE_JS = WEB_DIR / "laya_voice_engine.js"
GTFS_JSON = WEB_DIR / "data" / "gtfs_real_network.json"
GTFS_SCHEDULES_JSON = WEB_DIR / "data" / "gtfs_schedules.json"
MODEL_STATUS_JSON = WEB_DIR / "data" / "model_training_status.json"

CHROME_PATHS = [
    Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
]


def _find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])


def _get_browser_exe() -> Path | None:
    for p in CHROME_PATHS:
        if p.is_file():
            return p
    return None


# ---------------------------------------------------------------------------
# 1. INTEGRIDADE DE BUNDLE, ASSETS LOCAIS, IDS E GTFS (14k+ PONTOS / 45 HUBS)
# ---------------------------------------------------------------------------

class TestBundleAndGTFSIntegrity:
    def test_gtfs_bounding_box_linhas_e_hubs(self):
        data = json.loads(GTFS_JSON.read_text(encoding="utf-8"))
        popular = data.get("popular_lines", {})
        assert data.get("total_lines_ready") == len(popular) == 393

        for code, line in popular.items():
            poly = line.get("polyline") or []
            assert len(poly) >= 2, f"Linha {code} sem polyline"
            for pt in poly:
                assert -9.5 <= pt[0] <= -7.0 and -36.5 <= pt[1] <= -34.5, f"Coordenada fora de PE na linha {code}: {pt}"
            for st in line.get("stops") or []:
                assert -9.5 <= st["lat"] <= -7.0 and -36.5 <= st["lon"] <= -34.5, f"Parada fora de PE na linha {code}"

        hubs = data.get("hub_graph") or []
        assert len(hubs) >= 44
        for hub in hubs:
            assert hub.get("lines"), f"Hub vazio: {hub}"
            for lcode in hub["lines"]:
                assert lcode in popular, f"Linha órfã {lcode} no hub {hub.get('name')}"

    def test_html_zero_ids_duplicados_e_zero_assets_404(self):
        html = INDEX_HTML.read_text(encoding="utf-8")
        ids = re.findall(r'\bid=["\']([^"\']+)["\']', html)
        counts: dict[str, int] = {}
        for item in ids:
            counts[item] = counts.get(item, 0) + 1
        dups = {k: v for k, v in counts.items() if v > 1}
        assert not dups, f"IDs duplicados no index.html: {dups}"

        # Verifica referências locais src="..." e href="..." em todos os HTMLs de grafoparada_web
        for page_name in ["index.html", "roteiro.html", "slides_canva.html", "slides_sem2.html", "conversa.html"]:
            page = WEB_DIR / page_name
            if not page.is_file():
                continue
            txt = page.read_text(encoding="utf-8")
            refs = re.findall(r'(?:src|href)=["\']([^"\']+)["\']', txt)
            for ref in refs:
                if ref.startswith(("http://", "https://", "data:", "blob:", "#", "mailto:", "tel:")):
                    continue
                if "{" in ref or "${" in ref:
                    continue
                clean_ref = ref.split("?")[0].split("#")[0].lstrip("/")
                if not clean_ref:
                    continue
                target = WEB_DIR / clean_ref
                assert target.exists(), f"Asset 404 referenciado em {page_name}: {ref}"

    def test_documentos_sem2_sincronizados_com_medir_custo(self):
        assert (TEC_DIR / "medir_custo_sem2.py").is_file()
        docs = [
            WEB_DIR / "roteiro.html",
            ROOT_DIR / "va2" / "roteiro_fala_aula_hoje_sem2.html",
            WEB_DIR / "slides_canva.html",
        ]
        required_tokens = ("14,3 min", "0,96 ms", "324,7 MB", "56,68 µs", "393")
        stale_tokens = ("18 min", "18 minutos", "400 linhas", "Quarta, 11/11")

        for doc in docs:
            assert doc.is_file(), f"Documento Sem2 ausente: {doc}"
            content = doc.read_text(encoding="utf-8")
            for token in required_tokens:
                assert token in content, f"Métrica '{token}' ausente em {doc.relative_to(ROOT_DIR)}"
            for stale in stale_tokens:
                assert stale not in content, f"Valor desatualizado '{stale}' presente em {doc.relative_to(ROOT_DIR)}"


# ---------------------------------------------------------------------------
# 2. BATERIA NODE.JS: MATRIZ 1.260 PARES O-D, LEAFLET MOCK, XSS E VOZ
# ---------------------------------------------------------------------------

class TestTransitEngineExhaustive:
    def test_matriz_completa_1260_pares_od_xss_gps_e_voz(self):
        js_harness = r"""
const fs = require('fs');
const vm = require('vm');
const enginePath = process.argv[1];
const gtfsPath = process.argv[2];
const indexPath = process.argv[3];

const registeredTools = [];
global.window = {};
global.document = { getElementById: () => null };
global.localStorage = {
  _store: {},
  getItem(k) { return this._store[k] || null; },
  setItem(k, v) { this._store[k] = String(v); }
};
Object.defineProperty(global, 'navigator', {
  value: {
    modelContext: { registerTool: (def) => registeredTools.push(def && def.name) }
  },
  configurable: true
});

eval(fs.readFileSync(enginePath, 'utf8'));
const gtfs = JSON.parse(fs.readFileSync(gtfsPath, 'utf8'));
const loadRouteCalls = [];
window.RealTransit.networkData = gtfs;
window.RealTransit.loadRoute = (c) => { loadRouteCalls.push(String(c)); };
window.RealTransit.selectStop = () => {};

// A) Matriz completa 36 x 35 = 1260 pares O-D
const corridors = window.RealTransit.getSemanticCorridors();
let odTotal = 0;
let odOk = 0;
const odFails = [];
const odLoops = [];
for (let i = 0; i < corridors.length; i++) {
  for (let j = 0; j < corridors.length; j++) {
    if (i === j) continue;
    odTotal++;
    const o = corridors[i];
    const d = corridors[j];
    const plan = window.RealTransit.planSmartTrip(o.key, d.key);
    if (!plan || !plan.routeOptions || plan.routeOptions.length === 0) {
      odFails.push(`${o.key} -> ${d.key}`);
    } else {
      odOk++;
      for (const opt of plan.routeOptions) {
        const codes = opt.codes || [];
        if (new Set(codes).size !== codes.length || !Number.isFinite(opt.totalMin) || opt.totalMin <= 0) {
          odLoops.push(`${o.key}->${d.key}: ${codes.join(',')}`);
        }
      }
    }
  }
}

// B) Teste renderMultiLegRoute com Mock completo do Leaflet
const leafletCalls = { polylines: [], markers: [], fitBounds: 0 };
const makeLayer = () => ({
  _layers: [],
  addTo() { return this; },
  clearLayers() { this._layers = []; },
  addLayer(l) { this._layers.push(l); },
  getLayers() { return this._layers; },
  getBounds() { return { isValid: () => true }; }
});
global.L = {
  layerGroup: makeLayer,
  latLngBounds: () => ({
    _valid: false,
    extend() { this._valid = true; return this; },
    isValid() { return this._valid; }
  }),
  polyline: (pts, opts) => {
    leafletCalls.polylines.push(opts && opts.color === '#334155' ? 'walk' : 'bus');
    const obj = {
      pts, opts,
      addTo() { return this; },
      bindPopup() { return this; },
      getBounds() { return { pts }; }
    };
    return obj;
  },
  divIcon: (cfg) => cfg,
  marker: (coords, opts) => {
    leafletCalls.markers.push(coords);
    return { addTo() { return this; }, bindPopup() { return this; }, getLatLng() { return coords; } };
  }
};
window.RealTransit.map = {
  fitBounds() { leafletCalls.fitBounds++; },
  removeLayer() {}
};
window.RealTransit.renderMultiLegRoute(
  ['199', '185', '1971'],
  ['Ti Cabo', 'Cais de Santa Rita'],
  [-8.5149, -35.1235],
  [-8.0101, -34.8545]
);

// C) Teste XSS na NLU (remove apenas ícones UI confiáveis de _layaSvgIcon após validar atributos)
const xssResults = [
  window.RealTransit.answerLayaQuery('Quero ir de Olinda <img src=x onerror=alert(1)> até Boa Viagem'),
  window.RealTransit.answerLayaQuery('Quero ir de <script>alert(1)</script> até Olinda'),
  window.RealTransit.answerLayaQuery('Quero ir para <svg onload=alert(1)>')
];
const stripTrustedUiIcons = (html) => String(html || '').replace(/<svg class="gp-svg" width="\d+" height="\d+" style="width:\d+px;height:\d+px;flex-shrink:0;" aria-hidden="true" viewBox="0 0 24 24">(?:<(?:circle|polyline|polygon|line|path|rect)\b[^<>]*\/>)+<\/svg>/g, '');
const xssLeaky = xssResults.length !== 3 || xssResults.some((r) => {
  const rawHtml = (r && r.html) || '';
  if (!rawHtml) return true;
  if (/<[^>]*\bon(?:load|error)\s*=/i.test(rawHtml) || /\bjavascript\s*:/i.test(rawHtml)) {
    return true;
  }
  const stripped = stripTrustedUiIcons(rawHtml);
  return /<(img|script|svg|iframe|object|embed)\b/i.test(stripped);
});
const escapeHtmlSvgOk = window.RealTransit.escapeHtml('<svg onload=alert(1)>') === '&lt;svg onload=alert(1)&gt;';

// D) Destino implicito ancorado em GPS real + bordas RMR
const gpsPoints = [
  { lat: -8.0631, lon: -34.8711, name: 'Recife Antigo', expectOut: false },
  { lat: -8.5149, lon: -35.1235, name: 'Camela', expectOut: false },
  { lat: -7.9912, lon: -34.8415, name: 'Casa Caiada', expectOut: false },
  { lat: -8.2856, lon: -35.9761, name: 'Caruaru', expectOut: true },
  { lat: -23.5505, lon: -46.6333, name: 'SP', expectOut: true }
];
const gpsOk = gpsPoints.every(pt => {
  const r = window.RealTransit.adaptToUserLocation(pt.lat, pt.lon, pt.name);
  return Boolean(r && r.outOfCoverage) === pt.expectOut;
});

// Recalibra em Recife Antigo e testa destino implicito ("Quero ir para Casa Caiada")
window.RealTransit.adaptToUserLocation(-8.0631, -34.8711, 'Recife Antigo');
const impTrip = window.RealTransit.answerLayaQuery('Quero ir para Casa Caiada');
const okImp = impTrip && (impTrip.routeOptions || []).length >= 1 && (impTrip.html || '').includes('Casa Caiada');

// Verifica current_stop sob gps_denied (sem coords em cache) sem vazar código 160107 nem "GPS indisponível"
window.userCurrentCoords = null;
localStorage._store = {};
window.RealTransit.userAdaptState = {
  status: 'gps_denied',
  stopName: 'GPS indisponível · Escolha sua parada',
  distanceKm: null,
  originSource: null,
  isManualOrigin: false,
  gpsErrorCode: 'unavailable'
};
const currentStopDeniedRes = window.RealTransit.answerLayaQuery('onde estou', { activeStopName: '160107' });
const currentStopDeniedHtml = (currentStopDeniedRes && currentStopDeniedRes.html) || '';
const currentStopDeniedOk = Boolean(
  currentStopDeniedRes &&
  currentStopDeniedRes.intent === 'current_stop' &&
  currentStopDeniedHtml.includes('sua região atual') &&
  !currentStopDeniedHtml.includes('160107') &&
  !/gps indispon[ií]vel/i.test(currentStopDeniedHtml)
);

// E) Extrai e valida formatSpeechPortuguese de index.html
const htmlText = fs.readFileSync(indexPath, 'utf8');
const fnMatch = htmlText.match(/function formatSpeechPortuguese\(raw\)\s*\{[\s\S]*?\n\s*\}/);
let speechCheck = '';
if (fnMatch) {
  const sandbox = {};
  vm.runInNewContext(fnMatch[0], sandbox);
  speechCheck = sandbox.formatSpeechPortuguese('🚌 TI Cabo ➔ ST-GCN na PE-60 em 10 min e 3 km na RMR.');
}

console.log(JSON.stringify({
  odTotal, odOk, odFails, odLoops,
  loadRouteLeg0: loadRouteCalls[0] || '',
  leafletWalkCount: leafletCalls.polylines.filter(x => x === 'walk').length,
  leafletBusCount: leafletCalls.polylines.filter(x => x === 'bus').length,
  leafletMarkers: leafletCalls.markers.length,
  leafletFitBounds: leafletCalls.fitBounds,
  xssLeaky,
  escapeHtmlSvgOk,
  gpsOk,
  okImp,
  currentStopDeniedOk,
  speechCheck
}));
"""
        res = subprocess.run(
            ["node", "-e", js_harness, str(ENGINE_JS), str(GTFS_JSON), str(INDEX_HTML)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=30,
        )
        assert res.returncode == 0, f"Erro executando bateria Node.js: {res.stderr}"
        out = json.loads(res.stdout.strip().splitlines()[-1])

        assert out["odTotal"] >= 1260
        assert out["odOk"] == out["odTotal"], f"Pares falhos: {out['odFails']}"
        assert out["odLoops"] == [], f"Loops/tempos inválidos: {out['odLoops']}"
        assert out["loadRouteLeg0"] == "199"
        assert out["leafletBusCount"] == 2
        assert out["leafletWalkCount"] >= 2
        assert out["leafletMarkers"] >= 3
        assert out["leafletFitBounds"] == 1
        assert out["xssLeaky"] is False
        assert out["escapeHtmlSvgOk"] is True
        assert out["gpsOk"] is True
        assert out["okImp"] is True
        assert out["currentStopDeniedOk"] is True
        assert "Terminal Integrado Cabo" in out["speechCheck"]
        assert "rede neural espaço-temporal" in out["speechCheck"]
        assert "10 minutos" in out["speechCheck"]
        assert "3 quilômetros" in out["speechCheck"]

    def test_regressao_busca_xss_e_embarque_fim_rota_camela(self):
        js_harness = r"""
const fs = require('fs');
const enginePath = process.argv[1];
const gtfsPath = process.argv[2];

const mockElements = {
  'search-results-dropdown': { innerHTML: '', style: { display: 'none' } },
  'search-clear-btn': { style: { display: 'none' } }
};
global.window = {};
global.document = {
  getElementById: (id) => mockElements[id] || null
};
global.localStorage = {
  _store: {},
  getItem(k) { return this._store[k] || null; },
  setItem(k, v) { this._store[k] = String(v); }
};

let liveBusCall = null;
window.updateLiveBusMarker = (lat, lon, code, eta, seats) => {
  liveBusCall = { lat, lon, code: String(code), eta, seats };
};

const makeLayer = () => ({
  _layers: [],
  addTo() { return this; },
  clearLayers() { this._layers = []; },
  addLayer(l) { this._layers.push(l); },
  getLayers() { return this._layers; }
});
global.L = {
  layerGroup: makeLayer,
  polyline: (pts, opts) => ({
    pts, opts,
    addTo() { return this; },
    getBounds() { return { isValid: () => true }; }
  }),
  divIcon: (cfg) => cfg,
  marker: (coords) => ({
    addTo() { return this; },
    bindPopup() { return this; },
    on() { return this; },
    getLatLng() { return coords; }
  })
};

eval(fs.readFileSync(enginePath, 'utf8'));
const gtfs = JSON.parse(fs.readFileSync(gtfsPath, 'utf8'));
window.RealTransit.networkData = gtfs;
window.RealTransit.map = {
  fitBounds() {},
  removeLayer() {},
  panTo() {}
};
window.RealTransit.stopsLayer = makeLayer();

// 1. Escape XSS no estado vazio da busca (handleSearch)
window.RealTransit.handleSearch('<img src=x onerror=alert(1)>');
const dropHtml = mockElements['search-results-dropdown'].innerHTML;

// 2. Embarque próximo ao fim da rota em Camela (Linha 199): ônibus sem colisão com Seu Embarque
window.RealTransit.loadRoute('199', { originCoords: [-8.514931, -35.123469] });
const dirData = window.RealTransit.getDirectionData(
  window.RealTransit.activeRoute,
  window.RealTransit.activeDirection
);
const boardIdx = window.RealTransit.activeBoardingIndex;
const boardStop = dirData.stops[boardIdx];
const busDistKm = liveBusCall && boardStop
  ? window.RealTransit.haversineKm(boardStop.lat, boardStop.lon, liveBusCall.lat, liveBusCall.lon)
  : null;

console.log(JSON.stringify({
  hasEscapedImg: dropHtml.includes('&lt;img'),
  hasRawImgTag: /<img\b/i.test(dropHtml) || /<[^>]*\bon(?:error|load)\s*=/i.test(dropHtml),
  dropDisplay: mockElements['search-results-dropdown'].style.display,
  activeRouteCode: window.RealTransit.activeRouteCode,
  boardIdx,
  liveBusCall,
  busDistKm
}));
"""
        res = subprocess.run(
            ["node", "-e", js_harness, str(ENGINE_JS), str(GTFS_JSON)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=20,
        )
        assert res.returncode == 0, f"Erro no harness Node.js: {res.stderr}"
        out = json.loads(res.stdout.strip().splitlines()[-1])

        assert out["hasEscapedImg"] is True
        assert out["hasRawImgTag"] is False
        assert out["dropDisplay"] == "flex"
        assert out["activeRouteCode"] == "199"
        assert out["liveBusCall"] is not None
        assert out["busDistKm"] is not None and out["busDistKm"] >= 0.35, (
            f"liveBusMarker colidindo com Seu Embarque (dist={out['busDistKm']} km)"
        )

    def test_cloud_proxy_tts_revalida_get_apos_cooldown(self):
        js_harness = r"""
const path = require('path');
const { CloudProxyTTSProvider } = require(path.resolve(process.argv[1]));

(async () => {
  let fakeNow = 10000;
  const fetchLog = [];
  const provider = new CloudProxyTTSProvider({
    endpoint: '/api/tts',
    cooldownMs: 1000,
    now: () => fakeNow,
    window: { location: { protocol: 'https:', hostname: 'grafoparadaweb.vercel.app' } },
    storage: { getItem: () => null, setItem: () => {} },
    playAudioFn: async (url) => ({ played: true, url }),
    createObjectURL: () => 'blob:mock-audio',
    revokeObjectURL: () => {},
    fetchFn: async (url, init = {}) => {
      const method = String(init.method || 'GET').toUpperCase();
      fetchLog.push({ url, method });
      if (method === 'GET') {
        return {
          ok: true,
          status: 200,
          json: async () => ({
            available: false,
            fallback: 'web_speech',
            reason: 'missing_api_key',
            presets: ['ptbr_warm']
          })
        };
      }
      return { ok: false, status: 501, headers: { get: () => 'application/json' } };
    }
  });

  const errors = [];
  // 1a tentativa: GET /api/tts retorna available=false -> entra em cooldown sem POST
  try {
    await provider.synthesize('Primeira fala de teste');
  } catch (err) {
    errors.push(err.message);
  }
  const availableDuringCooldown = provider.isAvailable();

  // 2a tentativa durante cooldown: rejeita localmente sem qualquer requisição HTTP
  fakeNow = 10500;
  try {
    await provider.synthesize('Segunda fala em cooldown');
  } catch (err) {
    errors.push(err.message);
  }
  const callsBeforeExpiry = fetchLog.slice();

  // 3a tentativa após expirar cooldownMs: deve refazer GET /api/tts antes de qualquer POST
  fakeNow = 11001;
  const availableAfterCooldown = provider.isAvailable();
  try {
    await provider.synthesize('Terceira fala pos cooldown');
  } catch (err) {
    errors.push(err.message);
  }

  console.log(JSON.stringify({
    availableDuringCooldown,
    availableAfterCooldown,
    callsBeforeExpiry,
    fetchLog,
    errors
  }));
})().catch((err) => {
  console.error(err);
  process.exit(1);
});
"""
        res = subprocess.run(
            ["node", "-e", js_harness, str(LAYA_VOICE_JS)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=15,
        )
        assert res.returncode == 0, f"Erro testando CloudProxyTTSProvider: {res.stderr}"
        out = json.loads(res.stdout.strip().splitlines()[-1])

        assert out["availableDuringCooldown"] is False
        assert out["availableAfterCooldown"] is True
        assert [c["method"] for c in out["callsBeforeExpiry"]] == ["GET"]
        assert [c["method"] for c in out["fetchLog"]] == ["GET", "GET"]
        assert all(c["method"] != "POST" for c in out["fetchLog"])
        assert len(out["errors"]) == 3

    def test_novos_metodos_rmr_horarios_gtfs_e_status_treino(self):
        js_harness = r"""
const fs = require('fs');
const enginePath = process.argv[1];
const gtfsPath = process.argv[2];
const schedPath = process.argv[3];
const statusPath = process.argv[4];

global.window = {};
global.document = { getElementById: () => null };
global.localStorage = {
  _store: {},
  getItem(k) { return this._store[k] || null; },
  setItem(k, v) { this._store[k] = String(v); }
};

eval(fs.readFileSync(enginePath, 'utf8'));
window.RealTransit.networkData = JSON.parse(fs.readFileSync(gtfsPath, 'utf8'));
window.RealTransit.schedulesData = JSON.parse(fs.readFileSync(schedPath, 'utf8'));
window.RealTransit.modelTrainingStatus = JSON.parse(fs.readFileSync(statusPath, 'utf8'));

const emptySearch = window.RealTransit.searchRmrPlaces('', 8);
const camelaHits = window.RealTransit.searchRmrPlaces('Camela', 8);
const olindaHits = window.RealTransit.searchRmrPlaces('Olinda', 8);
const boaViagemHits = window.RealTransit.searchRmrPlaces('Boa Viagem', 8);
const tiCaboHits = window.RealTransit.searchRmrPlaces('TI Cabo', 8);

const camelaStops = window.RealTransit.getStopsForPlace(
  camelaHits[0].lat, camelaHits[0].lon, camelaHits[0].label, 6
);
const tiCaboStops = window.RealTransit.getStopsForPlace(
  tiCaboHits[0].lat, tiCaboHits[0].lon, tiCaboHits[0].label, 6
);

const mondayMorning = new Date('2026-11-16T08:00:00');
const sched199 = window.RealTransit.getScheduledEstimate('199', 'ida', null, mondayMorning);
const schedUnknown = window.RealTransit.getScheduledEstimate('999999', 'ida', null, mondayMorning);

const line199Stops = window.RealTransit.networkData.popular_lines['199'].stops;
const suggestedDirect = window.RealTransit.suggestLinesBetweenStops(
  line199Stops[0].stop_id,
  line199Stops[Math.min(5, line199Stops.length - 1)].stop_id,
  mondayMorning
);
const suggestedPlaces = window.RealTransit.suggestLinesBetweenStops(
  camelaStops[0].stop_id,
  tiCaboStops[0].stop_id,
  mondayMorning
);
const trainStatus = window.RealTransit.getModelTrainingStatus();

console.log(JSON.stringify({
  emptySearch,
  camelaHitsCount: camelaHits.length,
  camelaFirst: camelaHits[0] || null,
  olindaHitsCount: olindaHits.length,
  boaViagemHitsCount: boaViagemHits.length,
  camelaStopsCount: camelaStops.length,
  camelaStop0: camelaStops[0] || null,
  tiCaboStopsCount: tiCaboStops.length,
  sched199,
  schedUnknown,
  suggestedDirectCount: suggestedDirect.length,
  suggestedDirect0: suggestedDirect[0] || null,
  suggestedPlacesCount: suggestedPlaces.length,
  suggestedPlacesCodes: suggestedPlaces.map(s => s.code),
  trainStatus
}));
"""
        res = subprocess.run(
            [
                "node",
                "-e",
                js_harness,
                str(ENGINE_JS),
                str(GTFS_JSON),
                str(GTFS_SCHEDULES_JSON),
                str(MODEL_STATUS_JSON),
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=25,
        )
        assert res.returncode == 0, f"Erro testando novos métodos RealTransit v3: {res.stderr}"
        out = json.loads(res.stdout.strip().splitlines()[-1])

        assert out["emptySearch"] == []
        assert out["camelaHitsCount"] >= 1 and out["camelaFirst"] is not None
        assert out["olindaHitsCount"] >= 1
        assert out["boaViagemHitsCount"] >= 1
        assert out["camelaStopsCount"] >= 1 and out["camelaStop0"]["stop_id"]
        assert out["camelaStop0"]["lines"]
        assert out["tiCaboStopsCount"] >= 1

        sched = out["sched199"]
        assert sched is not None
        assert sched["routeCode"] == "199"
        assert sched["serviceDay"] == "DUT"
        assert sched["provenanceLabel"] == "Horário Programado · GTFS"
        assert sched["firstDep"] and sched["lastDep"] and sched["nextDepFormatted"]
        assert out["schedUnknown"] is None

        assert out["suggestedDirectCount"] >= 1
        assert out["suggestedDirect0"]["code"] == "199"
        assert out["suggestedDirect0"]["isDirect"] is True
        assert out["suggestedDirect0"]["schedule"]["provenanceLabel"] == "Horário Programado · GTFS"
        assert out["suggestedPlacesCount"] >= 1 and "199" in out["suggestedPlacesCodes"]

        ts = out["trainStatus"]
        assert ts is not None
        assert ts["lines_covered"] == 393
        assert ts["schedules_indexed"] == 393
        assert ts["validation_393_passed"] is True


# ---------------------------------------------------------------------------
# 3. TESTE END-TO-END REAL NO CHROME HEADLESS VIA CDP + SERVIDOR HTTP LOCAL
# ---------------------------------------------------------------------------

class TestRealBrowserE2E:
    def test_fluxo_completo_mobile_e_desktop_sem_erros(self):
        browser_exe = _get_browser_exe()
        if not browser_exe:
            pytest.skip("Chrome/Edge não encontrado nesta máquina para E2E headless")

        # Sobe servidor HTTP local com suporte a /api/* degradado graciosamente (client_local)
        class QuietHandler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=str(WEB_DIR), **kwargs)

            def log_message(self, format, *args):
                pass

            def _send_json(self, status_code: int, payload: dict):
                raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
                self.send_response(status_code)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(raw)))
                self.end_headers()
                self.wfile.write(raw)

            def do_OPTIONS(self):
                self.send_response(204)
                self.send_header("Allow", "GET, POST, OPTIONS")
                self.end_headers()

            def do_GET(self):
                clean_path = self.path.split("?")[0]
                if clean_path in ("/api/register", "/api/routine", "/api/telemetry"):
                    self._send_json(200, {
                        "ok": True,
                        "available": False,
                        "db_configured": False,
                        "storage": "client_local",
                    })
                    return
                super().do_GET()

            def do_POST(self):
                clean_path = self.path.split("?")[0]
                length = int(self.headers.get("Content-Length") or 0)
                raw_body = self.rfile.read(length) if length > 0 else b"{}"
                try:
                    parsed = json.loads(raw_body.decode("utf-8"))
                except Exception:
                    parsed = {}
                if clean_path in ("/api/register", "/api/routine", "/api/telemetry"):
                    rec = dict(parsed) if isinstance(parsed, dict) else {}
                    rec.setdefault("id", "local_e2e_rec")
                    self._send_json(202, {
                        "ok": True,
                        "persisted": "client_local_pending_db",
                        "db_configured": False,
                        "available": False,
                        "storage": "client_local",
                        "record": rec,
                    })
                    return
                self._send_json(404, {"ok": False, "error": "not_found"})

        server = socketserver.ThreadingTCPServer(("127.0.0.1", 0), QuietHandler)
        http_port = server.server_address[1]
        server_thread = threading.Thread(target=server.serve_forever, daemon=True)
        server_thread.start()

        cdp_port = _find_free_port()
        user_data_dir = Path(tempfile.mkdtemp(prefix="gp_chrome_e2e_"))
        proc = None

        try:
            proc = subprocess.Popen(
                [
                    str(browser_exe),
                    "--headless=new",
                    "--disable-gpu",
                    "--no-first-run",
                    "--no-default-browser-check",
                    "--disable-extensions",
                    f"--remote-debugging-port={cdp_port}",
                    f"--user-data-dir={user_data_dir}",
                    "--window-size=390,844",
                    "about:blank",
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            # Aguarda endpoint JSON do CDP ficar pronto
            targets = None
            deadline = time.time() + 12.0
            while time.time() < deadline:
                try:
                    with urllib.request.urlopen(f"http://127.0.0.1:{cdp_port}/json/list", timeout=1.0) as resp:
                        data = json.loads(resp.read().decode("utf-8"))
                        page_targets = [t for t in data if t.get("type") == "page" and t.get("webSocketDebuggerUrl")]
                        if page_targets:
                            targets = page_targets[0]
                            break
                except Exception:
                    time.sleep(0.25)

            assert targets is not None, "Chrome headless não abriu endpoint CDP a tempo"

            with ws_connect(targets["webSocketDebuggerUrl"], open_timeout=8, close_timeout=4) as ws:
                msg_id = 0
                runtime_exceptions = []
                console_errors = []
                http_4xx_5xx = []

                def cdp_call(method: str, params: dict | None = None):
                    nonlocal msg_id
                    msg_id += 1
                    cur_id = msg_id
                    ws.send(json.dumps({"id": cur_id, "method": method, "params": params or {}}))
                    end_t = time.time() + 10.0
                    while time.time() < end_t:
                        raw = ws.recv(timeout=10.0)
                        pkt = json.loads(raw)
                        if pkt.get("id") == cur_id:
                            if "error" in pkt:
                                raise RuntimeError(f"CDP error on {method}: {pkt['error']}")
                            return pkt.get("result", {})
                        # Registra eventos assíncronos relevantes
                        ev_method = pkt.get("method")
                        ev_params = pkt.get("params", {})
                        if ev_method == "Runtime.exceptionThrown":
                            desc = ev_params.get("exceptionDetails", {}).get("text", "")
                            exc_val = ev_params.get("exceptionDetails", {}).get("exception", {}).get("description", "")
                            runtime_exceptions.append(f"{desc} {exc_val}".strip())
                        elif ev_method == "Runtime.consoleAPICalled" and ev_params.get("type") == "error":
                            args = " ".join(str(a.get("value") or a.get("description") or "") for a in ev_params.get("args", []))
                            console_errors.append(args)
                        elif ev_method == "Network.responseReceived":
                            r = ev_params.get("response", {})
                            status = r.get("status", 200)
                            url = r.get("url", "")
                            if status >= 400 and "127.0.0.1" in url:
                                http_4xx_5xx.append(f"{status} {url}")

                def eval_js(expr: str):
                    res = cdp_call(
                        "Runtime.evaluate",
                        {"expression": expr, "returnByValue": True, "awaitPromise": True},
                    )
                    if "exceptionDetails" in res:
                        raise AssertionError(f"JS eval exception: {res['exceptionDetails']}")
                    return res.get("result", {}).get("value")

                def wait_until(expr: str, timeout_s: float = 8.0, err_msg: str = "Condição não satisfeita"):
                    deadline_w = time.time() + timeout_s
                    while time.time() < deadline_w:
                        if eval_js(expr):
                            return
                        time.sleep(0.15)
                    raise AssertionError(err_msg)

                cdp_call("Page.enable")
                cdp_call("Runtime.enable")
                cdp_call("Network.enable")
                cdp_call(
                    "Emulation.setDeviceMetricsOverride",
                    {"width": 390, "height": 844, "deviceScaleFactor": 2, "mobile": True},
                )

                cdp_call("Page.navigate", {"url": f"http://127.0.0.1:{http_port}/index.html"})

                # Aguarda RealTransit carregar os dados GTFS reais (rede + horários 393 + status)
                wait_until(
                    "Boolean(window.RealTransit && window.RealTransit.networkData && window.RealTransit.networkData.total_lines_ready === 393 && window.RealTransit.schedulesData && Object.keys(window.RealTransit.schedulesData.lines || {}).length === 393)",
                    timeout_s=10.0,
                    err_msg="window.RealTransit.networkData/schedulesData (393 linhas) não carregou no Chrome",
                )

                # Garante estado limpo em localStorage no primeiro acesso
                eval_js("localStorage.clear(); if (typeof checkAuthStatus === 'function') checkAuthStatus();")
                time.sleep(0.2)

                # 1) Primeiro acesso em passenger abre #modal-onboarding no Passo 1 (#onboarding-step-register)
                onb_step1 = eval_js("""(() => {
                  const modal = document.getElementById('modal-onboarding');
                  const s1 = document.getElementById('onboarding-step-register');
                  const s2 = document.getElementById('onboarding-step-routine');
                  const ids = Array.from(document.querySelectorAll('[id]')).map(e => e.id);
                  const counts = {};
                  ids.forEach(i => counts[i] = (counts[i] || 0) + 1);
                  const dups = Object.entries(counts).filter(([, c]) => c > 1);
                  return {
                    modalVisible: Boolean(modal && getComputedStyle(modal).display === 'flex'),
                    step1Visible: Boolean(s1 && getComputedStyle(s1).display !== 'none'),
                    step2Hidden: Boolean(s2 && getComputedStyle(s2).display === 'none'),
                    dups,
                    overflowPx: document.documentElement.scrollWidth - window.innerWidth
                  };
                })()""")
                assert onb_step1["modalVisible"] is True
                assert onb_step1["step1Visible"] is True
                assert onb_step1["step2Hidden"] is True
                assert onb_step1["dups"] == [], f"IDs duplicados no DOM ao vivo: {onb_step1['dups']}"
                assert onb_step1["overflowPx"] <= 2, f"Overflow horizontal mobile no Onboarding Passo 1: {onb_step1['overflowPx']}px"

                # Em Desktop 1280x800 com onboarding aberto, .desktop-outer-bar (#mode-btn-ctm / #mode-btn-lab) segue visível e acessível
                cdp_call(
                    "Emulation.setDeviceMetricsOverride",
                    {"width": 1280, "height": 800, "deviceScaleFactor": 1, "mobile": False},
                )
                time.sleep(0.2)
                desk_onb_bar = eval_js("""(() => {
                  const bar = document.querySelector('.desktop-outer-bar');
                  const btnCtm = document.getElementById('mode-btn-ctm');
                  const btnLab = document.getElementById('mode-btn-lab');
                  const hitCheck = (el) => {
                    if (!el) return false;
                    const r = el.getBoundingClientRect();
                    if (r.width <= 0 || r.height <= 0) return false;
                    const hit = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
                    return Boolean(hit && (hit === el || el.contains(hit)));
                  };
                  return {
                    barVisible: Boolean(bar && getComputedStyle(bar).display !== 'none'),
                    ctmAccessible: hitCheck(btnCtm),
                    labAccessible: hitCheck(btnLab),
                    overflowPx: document.documentElement.scrollWidth - window.innerWidth
                  };
                })()""")
                assert desk_onb_bar["barVisible"] is True
                assert desk_onb_bar["ctmAccessible"] is True, "Botão #mode-btn-ctm bloqueado durante onboarding em 1280x800"
                assert desk_onb_bar["labAccessible"] is True, "Botão #mode-btn-lab bloqueado durante onboarding em 1280x800"
                assert desk_onb_bar["overflowPx"] <= 2

                # Volta para Mobile 390x844 para concluir cadastro + rotina em cascata
                cdp_call(
                    "Emulation.setDeviceMetricsOverride",
                    {"width": 390, "height": 844, "deviceScaleFactor": 2, "mobile": True},
                )
                time.sleep(0.2)

                # 2) Preenche #inp-name e clica #btn-onb-register-continue -> Passo 2 (#onboarding-step-routine)
                eval_js("""(() => {
                  const nameEl = document.getElementById('inp-name');
                  const contactEl = document.getElementById('inp-sync-contact');
                  nameEl.value = 'Maria Silva';
                  if (contactEl) contactEl.value = 'maria@recife.pe';
                  document.getElementById('btn-onb-register-continue').click();
                })()""")
                wait_until(
                    "getComputedStyle(document.getElementById('onboarding-step-routine')).display !== 'none'",
                    timeout_s=6.0,
                    err_msg="Passo 2 (#onboarding-step-routine) não abriu após clicar #btn-onb-register-continue",
                )

                # Busca origem em #onb-origin-place -> seleciona em #onb-origin-place-list -> seleciona parada em #onb-origin-stops-list
                eval_js("""(() => {
                  const inp = document.getElementById('onb-origin-place');
                  inp.value = 'Camela';
                  inp.dispatchEvent(new Event('input', { bubbles: true }));
                })()""")
                wait_until(
                    "document.querySelectorAll('#onb-origin-place-list .gp-place-option').length > 0",
                    timeout_s=5.0,
                    err_msg="Autocomplete #onb-origin-place-list não exibiu opções para Camela",
                )
                eval_js("document.querySelector('#onb-origin-place-list .gp-place-option').click()")
                wait_until(
                    "document.querySelectorAll('#onb-origin-stops-list .gp-stop-card').length > 0",
                    timeout_s=5.0,
                    err_msg="Lista #onb-origin-stops-list não exibiu paradas reais",
                )
                eval_js("document.querySelector('#onb-origin-stops-list .gp-stop-card').click()")

                # Busca destino em #onb-dest-place -> seleciona em #onb-dest-place-list -> seleciona parada em #onb-dest-stops-list
                eval_js("""(() => {
                  const inp = document.getElementById('onb-dest-place');
                  inp.value = 'TI Cabo';
                  inp.dispatchEvent(new Event('input', { bubbles: true }));
                })()""")
                wait_until(
                    "document.querySelectorAll('#onb-dest-place-list .gp-place-option').length > 0",
                    timeout_s=5.0,
                    err_msg="Autocomplete #onb-dest-place-list não exibiu opções para TI Cabo",
                )
                eval_js("document.querySelector('#onb-dest-place-list .gp-place-option').click()")
                wait_until(
                    "document.querySelectorAll('#onb-dest-stops-list .gp-stop-card').length > 0",
                    timeout_s=5.0,
                    err_msg="Lista #onb-dest-stops-list não exibiu paradas reais",
                )
                eval_js("document.querySelector('#onb-dest-stops-list .gp-stop-card').click()")

                # Verifica sugestões GTFS em #onb-suggested-lines-box com "Horário Programado · GTFS"
                wait_until(
                    "document.querySelectorAll('#onb-suggested-lines-box .gp-suggested-line-card').length > 0 && document.getElementById('onb-suggested-lines-box').innerText.includes('Horário Programado · GTFS')",
                    timeout_s=5.0,
                    err_msg="#onb-suggested-lines-box não exibiu linhas sugeridas com 'Horário Programado · GTFS'",
                )

                # Preenche horários e clica #btn-onb-save-routine
                eval_js("""(() => {
                  document.getElementById('inp-custom-time').value = '06:15';
                  document.getElementById('inp-custom-return').value = '18:10';
                  document.getElementById('btn-onb-save-routine').click();
                })()""")
                wait_until(
                    "getComputedStyle(document.getElementById('modal-onboarding')).display === 'none'",
                    timeout_s=6.0,
                    err_msg="#modal-onboarding não fechou após salvar rotina",
                )

                # 3) Verifica Home (saudação com primeiro nome, zero "Cauã", rotina salva, favoritos vazio inicial)
                home_audit = eval_js("""(() => {
                  const greet = (document.getElementById('home-dynamic-greeting') || {}).textContent || '';
                  const brief = (document.getElementById('home-routine-brief') || {}).textContent || '';
                  const favRow = document.getElementById('favorites-pills-row');
                  const favPills = favRow ? favRow.querySelectorAll('.fav-stop-pill').length : -1;
                  const favEmpty = Boolean(favRow && favRow.querySelector('.gp-fav-empty'));
                  const overflowPx = document.documentElement.scrollWidth - window.innerWidth;
                  return { greet, brief, favPills, favEmpty, overflowPx };
                })()""")
                assert "Maria" in home_audit["greet"], f"Saudação inesperada na Home: {home_audit['greet']}"
                assert "Cauã" not in home_audit["greet"] and "Cauã" not in home_audit["brief"]
                assert "Configure sua rotina diária" not in home_audit["brief"]
                assert "→" in home_audit["brief"]
                assert home_audit["favPills"] == 0 and home_audit["favEmpty"] is True
                assert home_audit["overflowPx"] <= 2, f"Overflow horizontal mobile na Home: {home_audit['overflowPx']}px"

                # Fluxo 1 -> 2 -> Escolher Camela -> Digitar Olinda -> Opções Google Maps -> Traçar Mapa -> Tela 3
                eval_js("startGoingNowFlow()")
                time.sleep(0.25)
                screen2_active = eval_js("document.getElementById('app-screen-locate').classList.contains('screen-active')")
                assert screen2_active is True

                eval_js("""(() => {
                  const btn = Array.from(document.querySelectorAll('.locate-preset-btn')).find(b => b.textContent.includes('Camela'));
                  if (btn) btn.click();
                  const inp = document.getElementById('locate-dest-input');
                  inp.value = 'Olinda';
                  askLayaFromLocate();
                })()""")
                time.sleep(0.2)

                options_audit = eval_js("""(() => {
                  const box = document.getElementById('locate-route-options');
                  const txt = box ? box.innerText : '';
                  return {
                    visible: box && box.style.display !== 'none',
                    hasObjectObject: txt.includes('[object Object]'),
                    hasCode199: txt.includes('199'),
                    cardCount: box ? box.querySelectorAll('button').length : 0
                  };
                })()""")
                assert options_audit["visible"] is True
                assert options_audit["hasObjectObject"] is False, "BUG [object Object] detectado nas opções!"
                assert options_audit["hasCode199"] is True
                assert options_audit["cardCount"] >= 2

                # Clica em "Traçar no Mapa" (Opção 1)
                eval_js("selectGoogleMapsOption(0)")
                time.sleep(0.35)
                radar_state = eval_js("""(() => ({
                  currentScreen: typeof currentScreenId !== 'undefined' ? currentScreenId : '',
                  locateHidden: !document.getElementById('app-screen-locate').classList.contains('screen-active'),
                  activeCode: window.RealTransit ? window.RealTransit.activeRouteCode : '',
                  chipText: (document.getElementById('route-chip-label') || {}).textContent || '',
                  topLine: (document.getElementById('top-line-label') || {}).textContent || ''
                }))()""")
                assert radar_state["currentScreen"] == "radar"
                assert radar_state["locateHidden"] is True
                assert radar_state["activeCode"] == "199"
                assert "Linha 522 · Dois Irmãos" not in radar_state["chipText"]

                # Testa Chat Laya com payload XSS e consulta real de destino implicito
                eval_js("openLayaModal()")
                time.sleep(0.15)
                eval_js("""(() => {
                  const inp = document.getElementById('laya-chat-input');
                  inp.value = '<img src=x onerror=window.__xssHit=1>';
                  sendLayaTextMessage();
                })()""")
                time.sleep(0.5)
                assert eval_js("window.__xssHit") is None, "FALHA CRITICA XSS no chat da Laya!"

                eval_js("handleLayaQuickPrompt('Quero ir para Casa Caiada')")
                time.sleep(0.55)
                bot_text = eval_js("""(() => {
                  const msgs = document.querySelectorAll('#laya-chat-history .laya-msg-bot');
                  return msgs.length ? msgs[msgs.length - 1].innerText : '';
                })()""")
                assert "Casa Caiada" in bot_text

                # Testa controles e estados de voz da Laya (Laya PT-BR -> Sulafat IA -> Offline) sem HTTP 404/501
                voice_init = eval_js("""(() => {
                  const status = document.getElementById('laya-voice-status');
                  const btn = document.getElementById('btn-laya-voice-style');
                  const pill = document.getElementById('laya-voice-status-pill');
                  return {
                    hasStatus: Boolean(status),
                    styleLabel: btn ? btn.textContent.trim() : '',
                    pillText: pill ? pill.textContent.trim() : ''
                  };
                })()""")
                assert voice_init["hasStatus"] is True
                assert voice_init["styleLabel"] == "Laya PT-BR"

                eval_js("cycleLayaVoice()")
                time.sleep(0.2)
                voice_sulafat = eval_js("""(() => ({
                  profile: (document.getElementById('btn-laya-voice-style') || {}).textContent.trim(),
                  statusText: (document.getElementById('laya-voice-status-text') || {}).textContent.trim(),
                  stateAttr: (document.getElementById('laya-voice-status') || {}).getAttribute('data-voice-state') || ''
                }))()""")
                assert voice_sulafat["profile"] == "Sulafat IA"
                assert "Sulafat IA" in voice_sulafat["statusText"]

                eval_js("cycleLayaVoice()")
                time.sleep(0.15)
                voice_offline = eval_js("""(() => ({
                  profile: (document.getElementById('btn-laya-voice-style') || {}).textContent.trim(),
                  statusText: (document.getElementById('laya-voice-status-text') || {}).textContent.trim(),
                  stateAttr: (document.getElementById('laya-voice-status') || {}).getAttribute('data-voice-state') || ''
                }))()""")
                assert voice_offline["profile"] == "Offline"
                assert "Offline" in voice_offline["statusText"]

                eval_js("speakDriverCourtesyAudio()")
                time.sleep(0.15)
                eval_js("cycleLayaVoice(); toggleLayaVoiceMute(); closeLayaModal();")
                time.sleep(0.1)

                # Testa abertura dos modais principais sem lançar exceções JS
                for open_fn, close_fn in [
                    ("openProfileModal", "closeProfileModal"),
                    ("openDispatchModal", "closeDispatchModal"),
                    ("openAuditModal", "closeAuditModal"),
                    ("openRoutineModal", "closeRoutineModal"),
                ]:
                    eval_js(f"if (typeof {open_fn} === 'function') {open_fn}();")
                    time.sleep(0.1)
                    eval_js(f"if (typeof {close_fn} === 'function') {close_fn}();")

                # Regressão Mobile (390x844): Laya IA -> Trânsito na PE-60 agora -> Simular no Mapa
                eval_js("openLayaModal()")
                time.sleep(0.15)
                has_legacy_jargon = eval_js("""(() => {
                  return Array.from(document.querySelectorAll('#modal-laya .laya-quick-cmd'))
                    .some(b => b.textContent.includes('Anomalia PE-60 (Nó 10)'));
                })()""")
                assert has_legacy_jargon is False, "Jargão acadêmico 'Anomalia PE-60 (Nó 10)' ainda presente em #modal-laya"

                clicked_quick = eval_js("""(() => {
                  const btn = Array.from(document.querySelectorAll('#modal-laya .laya-quick-cmd'))
                    .find(b => b.textContent.includes('Trânsito na PE-60 agora'));
                  if (!btn) return false;
                  btn.click();
                  return true;
                })()""")
                assert clicked_quick is True, "Botão rápido 'Trânsito na PE-60 agora' não encontrado na Laya IA"

                clicked_sim = False
                for _ in range(20):
                    clicked_sim = eval_js("""(() => {
                      const btn = Array.from(document.querySelectorAll('#laya-chat-history button'))
                        .find(b => b.textContent.includes('Simular Anomalia Nó 10 (PE-60) no Mapa'));
                      if (!btn) return false;
                      btn.click();
                      return true;
                    })()""")
                    if clicked_sim:
                        break
                    time.sleep(0.15)
                assert clicked_sim is True, "Botão 'Simular Anomalia Nó 10 (PE-60) no Mapa' não apareceu no chat"

                time.sleep(0.5)  # Aguarda transição CSS de max-height (0.35s) do bottom sheet
                slide3_audit = eval_js("""(() => {
                  const modal = document.getElementById('modal-laya');
                  const sheet = document.getElementById('main-bottom-sheet');
                  const etaVal = document.getElementById('resting-eta-val');
                  const banner = document.getElementById('resting-reallocation-banner');
                  const nav = document.querySelector('.mobile-tab-nav');
                  const bannerRect = banner ? banner.getBoundingClientRect() : null;
                  const sheetRect = sheet ? sheet.getBoundingClientRect() : null;
                  const navRect = nav ? nav.getBoundingClientRect() : null;
                  return {
                    modalDisplay: modal ? modal.style.display : null,
                    hasFailureClass: Boolean(sheet && sheet.classList.contains('slide3-failure-active')),
                    etaText: etaVal ? etaVal.textContent.trim() : '',
                    bannerDisplay: banner ? getComputedStyle(banner).display : 'none',
                    bannerWidth: bannerRect ? bannerRect.width : 0,
                    bannerHeight: bannerRect ? bannerRect.height : 0,
                    bannerFitsInSheet: Boolean(
                      bannerRect && sheetRect &&
                      bannerRect.top >= sheetRect.top - 1 &&
                      bannerRect.bottom <= sheetRect.bottom + 1
                    ),
                    bannerAboveNav: Boolean(bannerRect && navRect && bannerRect.bottom <= navRect.top),
                    overflowX: document.documentElement.scrollWidth - window.innerWidth
                  };
                })()""")
                assert slide3_audit["modalDisplay"] == "none"
                assert slide3_audit["hasFailureClass"] is True
                assert slide3_audit["etaText"] == "14,3*"
                assert slide3_audit["bannerDisplay"] != "none"
                assert slide3_audit["bannerWidth"] > 0 and slide3_audit["bannerHeight"] > 0
                assert slide3_audit["bannerFitsInSheet"] is True, f"Banner cortado no bottom sheet: {slide3_audit}"
                assert slide3_audit["bannerAboveNav"] is True, f"Banner invadindo/cortado pela .mobile-tab-nav: {slide3_audit}"
                assert slide3_audit["overflowX"] <= 2, f"Overflow horizontal mobile na anomalia Slide 3: {slide3_audit['overflowX']}px"

                # Valida layout Desktop (1280x800) sem overflow nem exceções
                cdp_call(
                    "Emulation.setDeviceMetricsOverride",
                    {"width": 1280, "height": 800, "deviceScaleFactor": 1, "mobile": False},
                )
                time.sleep(0.2)
                desk_overflow = eval_js("document.documentElement.scrollWidth - window.innerWidth")
                assert desk_overflow <= 2, f"Overflow horizontal Desktop: {desk_overflow}px"

                # Regressão Desktop CTM (1280x800): setAppMode('ctm') + despacho Linha 522
                eval_js("setAppMode('ctm')")
                time.sleep(0.15)
                eval_js("document.getElementById('btn-ctm-dispatch-522').click()")
                time.sleep(0.25)
                ctm_audit = eval_js("""(() => {
                  const btn = document.getElementById('btn-ctm-dispatch-522');
                  const kpi = document.getElementById('ctm-kpi-alerts-val');
                  return {
                    appMode: document.body ? document.body.dataset.appMode : '',
                    ariaPressed: btn ? btn.getAttribute('aria-pressed') : null,
                    isActive: Boolean(btn && btn.classList.contains('is-active')),
                    btnText: btn ? btn.innerText.trim() : '',
                    kpiAlertsVal: kpi ? kpi.textContent.trim() : '',
                    overflowX: document.documentElement.scrollWidth - window.innerWidth
                  };
                })()""")
                assert ctm_audit["appMode"] == "ctm"
                assert ctm_audit["ariaPressed"] == "true"
                assert ctm_audit["isActive"] is True
                assert "Cenário Ativo" in ctm_audit["btnText"]
                assert ctm_audit["kpiAlertsVal"] == "1"
                assert ctm_audit["overflowX"] <= 2, f"Overflow horizontal Desktop CTM: {ctm_audit['overflowX']}px"

                # Alternância Desktop para Pesquisa & Banca (#mode-btn-lab) e retorno para Passageiro (#mode-btn-passenger)
                eval_js("document.getElementById('mode-btn-lab').click()")
                time.sleep(0.2)
                lab_audit = eval_js("""(() => {
                  const lab = document.getElementById('desktop-lab-workspace');
                  return {
                    appMode: document.body ? document.body.dataset.appMode : '',
                    labVisible: Boolean(lab && getComputedStyle(lab).display !== 'none'),
                    overflowX: document.documentElement.scrollWidth - window.innerWidth
                  };
                })()""")
                assert lab_audit["appMode"] == "lab"
                assert lab_audit["labVisible"] is True
                assert lab_audit["overflowX"] <= 2, f"Overflow horizontal Desktop Lab: {lab_audit['overflowX']}px"

                eval_js("document.getElementById('mode-btn-passenger').click()")
                time.sleep(0.2)
                assert eval_js("document.body ? document.body.dataset.appMode : ''") == "passenger"

                # Filtra apenas erros locais reais (ignora eventuais bloqueios de tiles externos se offline)
                local_console_errors = [e for e in console_errors if "tile" not in e.lower()]
                assert not runtime_exceptions, f"Exceções JS em runtime no Chrome: {runtime_exceptions}"
                assert not local_console_errors, f"Erros de console no Chrome: {local_console_errors}"
                assert not http_4xx_5xx, f"Recursos locais retornaram HTTP >= 400: {http_4xx_5xx}"
        finally:
            if proc and proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=3)
                except Exception:
                    proc.kill()
            server.shutdown()
            server.server_close()
            shutil.rmtree(user_data_dir, ignore_errors=True)
