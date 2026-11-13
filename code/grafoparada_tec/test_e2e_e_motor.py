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
GTFS_JSON = WEB_DIR / "data" / "gtfs_real_network.json"

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
        for page_name in ["index.html", "roteiro.html", "slides_canva.html", "conversa.html"]:
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
window.RealTransit.networkData = gtfs;
window.RealTransit.loadRoute = () => {};
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

// C) Teste XSS na NLU
const xssResults = [
  window.RealTransit.answerLayaQuery('Quero ir de Olinda <img src=x onerror=alert(1)> até Boa Viagem'),
  window.RealTransit.answerLayaQuery('Quero ir de <script>alert(1)</script> até Olinda'),
  window.RealTransit.answerLayaQuery('Quero ir para <svg onload=alert(1)>')
];
const xssLeaky = xssResults.some(r => /<(img|script|svg)\b/i.test((r && r.html) || ''));

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
  leafletWalkCount: leafletCalls.polylines.filter(x => x === 'walk').length,
  leafletBusCount: leafletCalls.polylines.filter(x => x === 'bus').length,
  leafletMarkers: leafletCalls.markers.length,
  leafletFitBounds: leafletCalls.fitBounds,
  xssLeaky,
  gpsOk,
  okImp,
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

        assert out["odTotal"] == 1260
        assert out["odOk"] == 1260, f"Pares falhos: {out['odFails']}"
        assert out["odLoops"] == [], f"Loops/tempos inválidos: {out['odLoops']}"
        assert out["leafletBusCount"] == 3
        assert out["leafletWalkCount"] >= 2
        assert out["leafletMarkers"] >= 3
        assert out["leafletFitBounds"] == 1
        assert out["xssLeaky"] is False
        assert out["gpsOk"] is True
        assert out["okImp"] is True
        assert "Terminal Integrado Cabo" in out["speechCheck"]
        assert "rede neural espaço-temporal" in out["speechCheck"]
        assert "10 minutos" in out["speechCheck"]
        assert "3 quilômetros" in out["speechCheck"]


# ---------------------------------------------------------------------------
# 3. TESTE END-TO-END REAL NO CHROME HEADLESS VIA CDP + SERVIDOR HTTP LOCAL
# ---------------------------------------------------------------------------

class TestRealBrowserE2E:
    def test_fluxo_completo_mobile_e_desktop_sem_erros(self):
        browser_exe = _get_browser_exe()
        if not browser_exe:
            pytest.skip("Chrome/Edge não encontrado nesta máquina para E2E headless")

        # Sobe servidor HTTP estático em thread daemon apontando para code/grafoparada_web
        handler_cls = functools.partial(
            http.server.SimpleHTTPRequestHandler,
            directory=str(WEB_DIR),
        )

        class QuietHandler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=str(WEB_DIR), **kwargs)

            def log_message(self, format, *args):
                pass

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

                cdp_call("Page.enable")
                cdp_call("Runtime.enable")
                cdp_call("Network.enable")
                cdp_call(
                    "Emulation.setDeviceMetricsOverride",
                    {"width": 390, "height": 844, "deviceScaleFactor": 2, "mobile": True},
                )

                cdp_call("Page.navigate", {"url": f"http://127.0.0.1:{http_port}/index.html"})

                # Aguarda RealTransit carregar os dados GTFS reais no navegador
                loaded = False
                for _ in range(30):
                    state = eval_js("Boolean(window.RealTransit && window.RealTransit.networkData && window.RealTransit.networkData.total_lines_ready === 393)")
                    if state:
                        loaded = True
                        break
                    time.sleep(0.25)
                assert loaded, "window.RealTransit.networkData (393 linhas) não carregou no Chrome"

                # Checa 0 IDs duplicados no DOM real e 0 overflow horizontal na Tela 1 (Mobile)
                dom_audit = eval_js("""(() => {
                  const ids = Array.from(document.querySelectorAll('[id]')).map(e => e.id);
                  const counts = {};
                  ids.forEach(i => counts[i] = (counts[i] || 0) + 1);
                  const dups = Object.entries(counts).filter(([, c]) => c > 1);
                  const overflowPx = document.documentElement.scrollWidth - window.innerWidth;
                  return { dups, overflowPx };
                })()""")
                assert dom_audit["dups"] == [], f"IDs duplicados no DOM ao vivo: {dom_audit['dups']}"
                assert dom_audit["overflowPx"] <= 2, f"Overflow horizontal mobile na Tela 1: {dom_audit['overflowPx']}px"

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

                # Valida layout Desktop (1280x800) sem overflow nem exceções
                cdp_call(
                    "Emulation.setDeviceMetricsOverride",
                    {"width": 1280, "height": 800, "deviceScaleFactor": 1, "mobile": False},
                )
                time.sleep(0.2)
                desk_overflow = eval_js("document.documentElement.scrollWidth - window.innerWidth")
                assert desk_overflow <= 2, f"Overflow horizontal Desktop: {desk_overflow}px"

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
