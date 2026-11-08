"""
Gerador do Protótipo GrafoParada v4.5 — Interface de Engenharia de Tráfego (SICOE / Grande Recife CTM)
Embute os dados reais de data/telemetria_real_pe60.json (250 coordenadas de shapes.txt, 20 paradas GTFS,
534 paradas reais da API m3p do Cittamobi e janelas físicas do TMD Dataset) em uma interface técnica
de sala de controle (sem estética de template genérico de IA).
"""
from __future__ import annotations

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUT_HTML = BASE_DIR / "prototipo_grafoparada.html"

with open(DATA_DIR / "telemetria_real_pe60.json", "r", encoding="utf-8") as f:
    TELEMETRIA = json.load(f)

TELEMETRIA_JSON_STR = json.dumps(TELEMETRIA, ensure_ascii=False)

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>CTM · SICOE — GrafoParada v4.5 | Console de Engenharia de Tráfego (Eixo Sul PE-60 / Suape)</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <style>
    :root {
      --bg-0: #0a0b0d;
      --bg-1: #101216;
      --bg-2: #16191f;
      --bg-3: #1d212a;
      --border: #262b36;
      --border-strong: #363d4d;
      --text-0: #eceff4;
      --text-1: #a7b0c0;
      --text-2: #6c7689;
      --emerald: #00d68f;
      --emerald-dim: rgba(0, 214, 143, 0.12);
      --amber: #ffaa00;
      --amber-dim: rgba(255, 170, 0, 0.12);
      --crimson: #ff3b5c;
      --crimson-dim: rgba(255, 59, 92, 0.12);
      --cyan: #00b8d9;
      --cyan-dim: rgba(0, 184, 217, 0.12);
      --font-sans: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      --font-mono: 'IBM Plex Mono', 'Consolas', monospace;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      background-color: var(--bg-0);
      color: var(--text-0);
      font-family: var(--font-sans);
      font-size: 13px;
      line-height: 1.45;
      overflow-x: hidden;
      -webkit-font-smoothing: antialiased;
    }

    .mono {
      font-family: var(--font-mono);
      font-variant-numeric: tabular-nums;
    }

    /* TOP COMMAND BAR */
    .topbar {
      min-height: 46px;
      background: var(--bg-1);
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: stretch;
      justify-content: space-between;
      padding: 0 14px;
      position: sticky;
      top: 0;
      z-index: 100;
      gap: 10px;
    }

    .topbar-left {
      display: flex;
      align-items: center;
      gap: 10px;
      white-space: nowrap;
    }

    .sys-tag {
      background: var(--emerald);
      color: #04120c;
      font-family: var(--font-mono);
      font-weight: 700;
      font-size: 11px;
      padding: 3px 7px;
      letter-spacing: 0.04em;
    }

    .sys-title {
      font-weight: 600;
      font-size: 12.5px;
      letter-spacing: -0.01em;
      color: var(--text-0);
    }

    .sys-title span {
      color: var(--text-2);
      font-weight: 400;
      margin-left: 4px;
    }

    .topbar-nav {
      display: flex;
      align-items: stretch;
    }

    .nav-btn {
      background: transparent;
      border: none;
      border-left: 1px solid var(--border);
      color: var(--text-1);
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 500;
      padding: 0 13px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 7px;
      white-space: nowrap;
      transition: background 0.12s, color 0.12s;
    }

    .nav-btn:last-child {
      border-right: 1px solid var(--border);
    }

    .nav-btn:hover {
      background: var(--bg-2);
      color: var(--text-0);
    }

    .nav-btn.active {
      background: var(--bg-2);
      color: var(--emerald);
      box-shadow: inset 0 -2px 0 var(--emerald);
      font-weight: 600;
    }

    .nav-key {
      font-size: 10px;
      color: var(--text-2);
      border: 1px solid var(--border-strong);
      padding: 1px 4px;
    }

    .topbar-right {
      display: flex;
      align-items: center;
      gap: 12px;
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--text-1);
      white-space: nowrap;
    }

    .status-led {
      display: inline-block;
      width: 7px;
      height: 7px;
      background: var(--emerald);
      margin-right: 5px;
      box-shadow: 0 0 8px var(--emerald);
    }

    /* TELEMETRY RIBBON */
    .telemetry-ribbon {
      display: grid;
      grid-template-columns: repeat(6, 1fr);
      background: var(--bg-1);
      border-bottom: 1px solid var(--border);
    }

    .metric-cell {
      padding: 10px 14px;
      border-right: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }

    .metric-cell:last-child {
      border-right: none;
    }

    .metric-label {
      font-family: var(--font-mono);
      font-size: 10px;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--text-2);
      display: flex;
      justify-content: space-between;
    }

    .metric-val {
      font-family: var(--font-mono);
      font-size: 18px;
      font-weight: 700;
      margin: 3px 0 2px;
      color: var(--text-0);
    }

    .metric-foot {
      font-size: 11px;
      color: var(--text-1);
      font-family: var(--font-mono);
    }

    /* WORKSPACE VIEWS */
    .workspace-view {
      display: none;
      padding: 14px;
    }

    .workspace-view.active {
      display: block;
    }

    /* PANELS */
    .panel {
      background: var(--bg-1);
      border: 1px solid var(--border);
      display: flex;
      flex-direction: column;
    }

    .panel-head {
      min-height: 38px;
      background: var(--bg-2);
      border-bottom: 1px solid var(--border);
      padding: 5px 12px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 600;
      color: var(--text-0);
      letter-spacing: 0.02em;
    }

    .panel-body {
      padding: 12px;
      flex: 1;
    }

    .tag {
      font-family: var(--font-mono);
      font-size: 10.5px;
      font-weight: 600;
      padding: 2px 6px;
      border: 1px solid var(--border-strong);
      text-transform: uppercase;
    }

    .tag-emerald { background: var(--emerald-dim); color: var(--emerald); border-color: rgba(0, 214, 143, 0.35); }
    .tag-amber { background: var(--amber-dim); color: var(--amber); border-color: rgba(255, 170, 0, 0.35); }
    .tag-crimson { background: var(--crimson-dim); color: var(--crimson); border-color: rgba(255, 59, 92, 0.35); }
    .tag-cyan { background: var(--cyan-dim); color: var(--cyan); border-color: rgba(0, 184, 217, 0.35); }

    /* BUTTONS & CONTROLS */
    .btn {
      background: var(--bg-2);
      border: 1px solid var(--border-strong);
      color: var(--text-0);
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 600;
      padding: 6px 11px;
      cursor: pointer;
      transition: all 0.12s;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }

    .btn:hover {
      background: var(--bg-3);
      border-color: var(--text-1);
    }

    .btn.active, .btn-emerald {
      background: var(--emerald-dim);
      border-color: var(--emerald);
      color: var(--emerald);
    }

    .btn-emerald:hover {
      background: var(--emerald);
      color: #04120c;
    }

    .btn-amber {
      background: var(--amber-dim);
      border-color: var(--amber);
      color: var(--amber);
    }

    /* TABLES */
    .tech-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 12px;
    }

    .tech-table th, .tech-table td {
      padding: 7px 9px;
      border-bottom: 1px solid var(--border);
      text-align: left;
    }

    .tech-table th {
      font-family: var(--font-mono);
      font-size: 10.5px;
      text-transform: uppercase;
      color: var(--text-2);
      background: var(--bg-2);
      font-weight: 600;
    }

    .tech-table tr:hover td {
      background: rgba(255, 255, 255, 0.02);
    }

    .tech-table tr.selected-row td {
      background: rgba(0, 214, 143, 0.08);
    }

    /* LAYOUTS */
    .gis-grid {
      display: grid;
      grid-template-columns: 1.35fr 1fr;
      gap: 14px;
    }

    .imu-grid {
      display: grid;
      grid-template-columns: 360px 1fr;
      gap: 14px;
    }

    .split-2 {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
    }

    @media (max-width: 1180px) {
      .gis-grid, .imu-grid, .split-2 { grid-template-columns: 1fr; }
      .telemetry-ribbon { grid-template-columns: repeat(3, 1fr); }
    }

    /* GIS CANVAS CONTAINER */
    .canvas-wrap {
      position: relative;
      background: #07080a;
      border: 1px solid var(--border);
      width: 100%;
      height: 510px;
      overflow: hidden;
    }

    #pe60-leaflet-map {
      width: 100%;
      height: 100%;
      background: #07080a;
      z-index: 1;
    }

    .map-overlay-tl, .map-overlay-br {
      z-index: 500;
    }

    .leaflet-container {
      font-family: var(--font-mono) !important;
      background: #07080a !important;
    }

    .tile-dark-filter {
      filter: invert(100%) hue-rotate(180deg) brightness(88%) contrast(95%);
    }

    .sicoe-tooltip {
      background: rgba(10, 11, 13, 0.94) !important;
      border: 1px solid var(--border-strong) !important;
      border-radius: 0px !important;
      color: var(--text-0) !important;
      font-family: var(--font-mono) !important;
      font-size: 10.5px !important;
      padding: 3px 6px !important;
      box-shadow: 0 2px 8px rgba(0,0,0,0.65) !important;
    }

    .sicoe-tooltip::before {
      display: none !important;
    }

    .map-overlay-tl {
      position: absolute;
      top: 10px;
      left: 10px;
      background: rgba(10, 11, 13, 0.88);
      border: 1px solid var(--border-strong);
      padding: 8px 10px;
      font-family: var(--font-mono);
      font-size: 11px;
      pointer-events: none;
    }

    .map-overlay-br {
      position: absolute;
      bottom: 10px;
      right: 10px;
      background: rgba(10, 11, 13, 0.9);
      border: 1px solid var(--border-strong);
      padding: 7px 10px;
      font-family: var(--font-mono);
      font-size: 10.5px;
      display: flex;
      gap: 12px;
    }

    .legend-dot {
      display: inline-block;
      width: 8px;
      height: 8px;
      margin-right: 4px;
      vertical-align: middle;
    }

    /* HARDWARE DEVICE CONSOLE (MODULE 02) */
    .hw-console {
      background: #08090c;
      border: 1px solid var(--border-strong);
      padding: 12px;
    }

    .hw-header {
      display: flex;
      justify-content: space-between;
      border-bottom: 1px solid var(--border);
      padding-bottom: 8px;
      margin-bottom: 10px;
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--text-2);
    }

    .scenario-list {
      display: flex;
      flex-direction: column;
      gap: 6px;
      margin: 10px 0;
    }

    .sc-item {
      background: var(--bg-1);
      border: 1px solid var(--border);
      padding: 9px 10px;
      cursor: pointer;
      text-align: left;
      transition: all 0.12s;
    }

    .sc-item:hover {
      border-color: var(--border-strong);
      background: var(--bg-2);
    }

    .sc-item.active {
      border-left: 3px solid var(--emerald);
      background: var(--bg-2);
      border-color: var(--border-strong);
    }

    .sc-item-head {
      display: flex;
      justify-content: space-between;
      font-family: var(--font-mono);
      font-size: 11.5px;
      font-weight: 700;
      color: var(--text-0);
      margin-bottom: 3px;
    }

    .sc-item-desc {
      font-size: 11.5px;
      color: var(--text-1);
    }

    .tts-terminal {
      background: #050608;
      border: 1px solid var(--border-strong);
      border-left: 3px solid var(--amber);
      padding: 10px;
      margin: 10px 0;
      font-family: var(--font-mono);
      font-size: 11.5px;
    }

    .osc-wrap {
      background: #060709;
      border: 1px solid var(--border);
      height: 175px;
      width: 100%;
      position: relative;
      margin-bottom: 12px;
    }

    .osc-wrap canvas {
      width: 100%;
      height: 100%;
      display: block;
    }

    /* PROBABILITY METERS */
    .prob-strip {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 8px;
      margin-bottom: 12px;
    }

    .prob-cell {
      background: var(--bg-2);
      border: 1px solid var(--border);
      padding: 8px 10px;
    }

    .prob-bar-track {
      height: 5px;
      background: #08090c;
      margin-top: 6px;
      overflow: hidden;
    }

    .prob-bar-fill {
      height: 100%;
      background: var(--cyan);
      transition: width 0.25s ease;
    }

    /* CODE DIFF / HEX DUMP */
    .hex-dump {
      background: #060709;
      border: 1px solid var(--border);
      padding: 10px 12px;
      font-family: var(--font-mono);
      font-size: 11.5px;
      color: var(--emerald);
      white-space: pre-wrap;
      line-height: 1.5;
    }

    input[type="range"] {
      width: 100%;
      accent-color: var(--emerald);
      cursor: pointer;
    }
  </style>
</head>
<body>

  <!-- TOP COMMAND BAR -->
  <header class="topbar">
    <div class="topbar-left">
      <span class="sys-tag">CTM · SICOE v4.5</span>
      <div class="sys-title">
        GRAFOPARADA // CONSOLE DE TELEMETRIA
        <span>[EIXO PE-60 · SUAPE]</span>
      </div>
    </div>

    <nav class="topbar-nav">
      <button class="nav-btn active" onclick="switchModule('mod-gis', this)">
        <span class="nav-key">F1</span> MALHA GEODÉSICA PE-60 &amp; DESPACHO
      </button>
      <button class="nav-btn" onclick="switchModule('mod-imu', this)">
        <span class="nav-key">F2</span> TELEMETRIA INERCIAL &amp; FSM
      </button>
      <button class="nav-btn" onclick="switchModule('mod-citta', this)">
        <span class="nav-key">F3</span> AUDITORIA API m3p CITTAMOBI
      </button>
      <button class="nav-btn" onclick="switchModule('mod-bench', this)">
        <span class="nav-key">F4</span> BENCHMARKS v1&rarr;v4 &amp; LGPD
      </button>
    </nav>

    <div class="topbar-right">
      <span id="live-engine-badge" style="color:var(--emerald); font-weight:700;"><i class="status-led"></i>ENGINE PYTORCH + PROXY m3p AO VIVO</span>
      <span id="live-clock">05:42:18 BRT</span>
    </div>
  </header>

  <!-- METRIC RIBBON -->
  <section class="telemetry-ribbon">
    <div class="metric-cell">
      <div class="metric-label"><span>FALSO POSITIVO DESEMBARQUE</span><span>[v3.0 FSM]</span></div>
      <div class="metric-val" style="color:var(--emerald);">0,00% <span style="font-size:12px; color:var(--text-1);">(0/300)</span></div>
      <div class="metric-foot">Recall de Descida: 99,33% (298/300)</div>
    </div>
    <div class="metric-cell">
      <div class="metric-label"><span>F1-SCORE DESISTÊNCIA REAL</span><span>[1.200 VIAGENS]</span></div>
      <div class="metric-val" style="color:var(--emerald);">99,67%</div>
      <div class="metric-foot">vs. 40,85% RF BigQuery Cittamobi</div>
    </div>
    <div class="metric-cell">
      <div class="metric-label"><span>PREDIÇÃO HORIZONTE t+30m</span><span>[20 NÓS PE-60]</span></div>
      <div class="metric-val" style="color:var(--cyan);">MAE 1,51 min</div>
      <div class="metric-foot">STGCN vence Regressão (1,93m) e Persist. (7,13m)</div>
    </div>
    <div class="metric-cell">
      <div class="metric-label"><span>ROTINA LOCAL ON-DEVICE</span><span>[ZERO NUVEM]</span></div>
      <div class="metric-val" style="color:var(--amber);">4º DIA ÚTIL</div>
      <div class="metric-foot">100% Recall Voz | 166 Bytes SQLite local</div>
    </div>
    <div class="metric-cell">
      <div class="metric-label"><span>SERVIDOR m3p CITTAMOBI</span><span>[AGÊNCIA a=202]</span></div>
      <div class="metric-val" style="color:var(--crimson);">0 VEÍCULOS</div>
      <div class="metric-foot">534 paradas auditadas | 142,4 KB/viewport</div>
    </div>
    <div class="metric-cell">
      <div class="metric-label"><span>ECONOMIA DE TRÁFEGO &amp; LGPD</span><span>[EVENT-DRIVEN]</span></div>
      <div class="metric-val" style="color:var(--emerald);">-99,99%</div>
      <div class="metric-foot">0 B rotina normal | 36 B desistência (k&ge;3)</div>
    </div>
  </section>

  <!-- ======================================================================= -->
  <!-- MODULE 01: GIS VECTOR MAP & CTMPOPERATIONAL DISPATCH (PE-60)           -->
  <!-- ======================================================================= -->
  <main id="mod-gis" class="workspace-view active">
    <div class="gis-grid">

      <!-- Left: Geodesic Canvas of PE-60 -->
      <div class="panel">
        <div class="panel-head">
          <span>[GIS-PE60] MAPA CARTOGRÁFICO REAL (OPENSTREETMAP / SATÉLITE ESRI) + SHAPE GTFS #178-389-2</span>
          <div style="display:flex; gap:5px; flex-wrap:wrap;">
            <button id="btn-tile-dark" class="btn active" onclick="setBaseTile('dark')">MAPA ESCURO</button>
            <button id="btn-tile-sat" class="btn" onclick="setBaseTile('sat')">SATÉLITE REAL</button>
            <button id="btn-tile-osm" class="btn" onclick="setBaseTile('osm')">VIAS OSM</button>
            <button id="btn-layer-gp" class="btn active" onclick="setGisLayer('grafoparada')">GRAFOPARADA</button>
            <button id="btn-layer-catraca" class="btn" onclick="setGisLayer('catraca')">SÓ CATRACA</button>
            <button id="btn-layer-citta" class="btn active" onclick="toggleCittamobi534()">534 CITTAMOBI: <span id="lbl-citta-toggle">ON</span></button>
          </div>
        </div>
        <div class="canvas-wrap">
          <div id="pe60-leaflet-map"></div>
          <div class="map-overlay-tl">
            <div style="color:var(--emerald); font-weight:700;">MAPA REAL INTERATIVO: TI CABO &rarr; RODOVIA PE-60 &rarr; PORTO DE SUAPE</div>
            <div>USE O SCROLL DO MOUSE PARA ZOOM IN/OUT · ARRASTE PARA NAVEGAR</div>
            <div id="map-hover-readout" style="color:var(--amber); margin-top:3px;">Clique sobre qualquer parada oficial ou nas 534 paradas do Cittamobi</div>
          </div>
          <div class="map-overlay-br">
            <span><i class="legend-dot" style="background:var(--emerald);"></i>Regular (&le;35m)</span>
            <span><i class="legend-dot" style="background:var(--amber);"></i>Atenção [?] (35–40m)</span>
            <span><i class="legend-dot" style="background:var(--crimson);"></i>Gargalo Crítico (&gt;40m + Desistência k&ge;3)</span>
            <span><i class="legend-dot" style="background:#3b4254;"></i>534 Nós Cittamobi (activeVehicles: 0)</span>
          </div>
        </div>
        <div style="padding:10px 12px; background:var(--bg-2); border-top:1px solid var(--border); display:flex; justify-content:space-between; align-items:center; font-family:var(--font-mono); font-size:11px;">
          <span>SELECIONE QUALQUER PARADA NA BARRA NUMÉRICA:</span>
          <div id="quick-stop-selector" style="display:flex; gap:3px; flex-wrap:wrap;"></div>
        </div>
      </div>

      <!-- Right: Selected Stop Telemetry + Step 8 Human-in-the-Loop Dispatch -->
      <div style="display:flex; flex-direction:column; gap:14px;">

        <div class="panel">
          <div class="panel-head">
            <span id="insp-stop-header">NÓ #11 // PE-60 km 17 (Trevo Ipojuca / Camela) [GTFS: 030192]</span>
            <span id="insp-stop-tag" class="tag tag-crimson">CRÍTICO · 14 DESISTÊNCIAS (k&ge;3)</span>
          </div>
          <div class="panel-body">
            <table class="tech-table">
              <tbody>
                <tr>
                  <td style="color:var(--text-2); width:42%;">Coordenadas WGS84 (GTFS stops.txt)</td>
                  <td class="mono" id="insp-coords">-8.304873, -35.021349 (Programado: 05:41:41)</td>
                </tr>
                <tr>
                  <td style="color:var(--text-2);">Auditoria Servidor Cittamobi (m3p/js)</td>
                  <td class="mono" id="insp-citta" style="color:var(--amber);">ID #2966773 · "Rodovia Armínio Cuil Hi Rme" (Erro OCR · Dist: 16,5m · Veículos: 0)</td>
                </tr>
                <tr>
                  <td style="color:var(--text-2);">Leitura da Catraca Eletrônica (VEM)</td>
                  <td class="mono" id="insp-catraca">0 validações nos últimos 40 min (Falsa impressão de "parada vazia")</td>
                </tr>
                <tr>
                  <td style="color:var(--text-2);">Fila Volátil GrafoParada (RAM 10 min)</td>
                  <td class="mono" id="insp-abn" style="color:var(--crimson); font-weight:700;">14 eventos ABANDONMENT p/ Ligeirinho (Trava LGPD k=14 &ge; 3 liberada)</td>
                </tr>
                <tr>
                  <td style="color:var(--text-2);">Horizonte Espaço-Temporal STGCN</td>
                  <td class="mono" id="insp-stgcn">t+10m: 38,4 min | t+20m: 43,8 min | <strong style="color:var(--crimson);">t+30m: 47,2 min</strong> (MAE 1,51m)</td>
                </tr>
                <tr>
                  <td style="color:var(--text-2);">Ping Ao Vivo Servidor Cittamobi (<code>m3p</code>)</td>
                  <td class="mono" id="insp-live-citta-ping" style="color:var(--cyan);">Aguardando chamada ao vivo...</td>
                </tr>
              </tbody>
            </table>
            <div style="margin-top:8px; display:flex; gap:8px; flex-wrap:wrap;">
              <button class="btn btn-amber" onclick="pingLiveCittamobiStop()">
                [PING AO VIVO AGORA] CONSULTAR api.cittamobi.com.br NESTA PARADA
              </button>
              <button class="btn btn-emerald" onclick="runLiveStgcnInference()">
                [RODAR STGCN PYTORCH AO VIVO] RECALCULAR GRAFO t+30m NA CPU
              </button>
            </div>
          </div>
        </div>

        <!-- Step 8 Human-in-the-Loop Dispatch Protocol -->
        <div class="panel">
          <div class="panel-head">
            <span>PASSO 8 DO FLUXOGRAMA // PROTOCOLO DE DECISÃO HUMANA &amp; REMANEJAMENTO DE FROTA NO VAZIO</span>
            <span class="tag tag-amber" id="insp-audit-flag">[? CONFERIR GPS A MONTANTE]</span>
          </div>
          <div class="panel-body">
            <p style="color:var(--text-1); font-size:12px; margin-bottom:10px;">
              <strong>Trava contra Viés de Automação:</strong> A STGCN não altera a tabela horária sozinha. O despachante do CTM confronta a predição com o atraso bruto do GPS nas paradas anteriores e remaneja uma viagem que está rodando vazia no contrafluxo administrativo de Suape:
            </p>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:10px;">
              <div style="background:var(--bg-0); border:1px solid var(--border); padding:9px;">
                <div class="mono" style="font-size:10.5px; color:var(--text-2);">DIAGNÓSTICO A MONTANTE (NÓS #09 e #10)</div>
                <div class="mono" style="font-size:12px; color:var(--crimson); font-weight:600; margin-top:3px;">Retenção de comboio no km 13 (TDR Norte)</div>
                <div style="font-size:11.5px; color:var(--text-1); margin-top:2px;">Atraso real medido via GPS: 39,0 min. 23 trabalhadores já migraram p/ transporte informal entre km 13 e km 17.</div>
              </div>
              <div style="background:var(--bg-0); border:1px solid var(--border); padding:9px;">
                <div class="mono" style="font-size:10.5px; color:var(--text-2);">FROTA OCIOSA DETECTADA (NÓ #19 SUAPE)</div>
                <div class="mono" style="font-size:12px; color:var(--emerald); font-weight:600; margin-top:3px;">Prefixo #178-09 (Ocupação &lt; 8% · Dwell 0s)</div>
                <div style="font-size:11.5px; color:var(--text-1); margin-top:2px;">Veículo retornando vazio da Rotatória Adm. Suape (stop_id: 030701). Custo adicional de frota: R$ 0,00.</div>
              </div>
            </div>

            <div style="display:flex; gap:10px; align-items:center; margin-bottom:10px;">
              <button class="btn btn-emerald" onclick="triggerGtfsPatch()">
                [EXECUTAR ORDEM] INJETAR PARTIDA EXPRESSA NO stop_times.txt
              </button>
              <button class="btn" onclick="selectStopNode(19)">
                INSPECIONAR NÓ #19 (ORIGEM FROTA VAZIA)
              </button>
            </div>

            <div id="gtfs-patch-output" class="hex-dump">Aguardando confirmação do analista CTM para gerar diff em stop_times.txt (Viagem 178-389-2)...</div>
          </div>
        </div>

      </div>
    </div>
  </main>

  <!-- ======================================================================= -->
  <!-- MODULE 02: ON-DEVICE IMU OSCILLOSCOPE & KINEMATIC FSM v3.0/v4.0         -->
  <!-- ======================================================================= -->
  <main id="mod-imu" class="workspace-view">
    <div class="imu-grid">

      <!-- Left: Hardware Telemetry Unit & Pocket Routine Engine -->
      <div class="panel">
        <div class="panel-head">
          <span>TERMINAL DE BORDO ON-DEVICE (MODO BOLSO)</span>
          <span class="tag tag-emerald">14,29 µs / 8,92 KB RAM</span>
        </div>
        <div class="panel-body">
          <div class="hw-console">
            <div class="hw-header">
              <span>DEVICE: ANDROID IMU (50Hz)</span>
              <span>GEOCERCA: RAIO 35m</span>
            </div>

            <div style="font-family:var(--font-mono); font-size:11px; color:var(--text-1); margin-bottom:6px;">
              SELECIONE O VETOR CINEMÁTICO REAL (TMD DATASET):
            </div>

            <div class="scenario-list">
              <div class="sc-item active" onclick="selectImuScenario('ALIGHTING', this)">
                <div class="sc-item-head">
                  <span>01 // DESEMBARQUE (ALIGHTING)</span>
                  <span style="color:var(--emerald);">FP: 0,00%</span>
                </div>
                <div class="sc-item-desc">Chega a 36 km/h (Bus), dwell de 30s na parada e sai a 4,6 km/h (Walking). Pergunta #1 do Prof. Lucas.</div>
              </div>

              <div class="sc-item" onclick="selectImuScenario('ABANDONMENT', this)">
                <div class="sc-item-head">
                  <span>02 // DESISTÊNCIA P/ LIGEIRINHO (ABN)</span>
                  <span style="color:var(--crimson);">F1: 99,67%</span>
                </div>
                <div class="sc-item-desc">Chega a pé, aguarda 38 min (Still) sem ônibus oficial na geocerca e parte a 52 km/h (Car/Van) sem parar no ponto seguinte.</div>
              </div>

              <div class="sc-item" onclick="selectImuScenario('BOARDING_SERVED', this)">
                <div class="sc-item-head">
                  <span>03 // EMBARQUE OFICIAL (SERVED)</span>
                  <span style="color:var(--cyan);">REC: 99,33%</span>
                </div>
                <div class="sc-item-desc">Aguarda 14,5 min (Still) e embarca em sincronia com GPS aberto da Linha 178 + assinatura vibro-acústica Bus.</div>
              </div>

              <div class="sc-item" onclick="selectImuScenario('TRANSIT_BYPASS', this)">
                <div class="sc-item-head">
                  <span>04 // PASSAGEM DIRETA (BYPASS)</span>
                  <span style="color:var(--amber);">100% FILTRADO</span>
                </div>
                <div class="sc-item-desc">Cruza o raio de 35m da parada na rodovia PE-60 a 65 km/h (dwell 15s &lt; 45s). Ignorado na borda.</div>
              </div>
            </div>

            <div class="tts-terminal">
              <div style="display:flex; justify-content:space-between; color:var(--amber); font-size:10.5px; margin-bottom:4px;">
                <span>SÍNTESE DE VOZ NO FONE (TELA APAGADA)</span>
                <span>CONF. HÁBITO: 95,4% (DIA 4)</span>
              </div>
              <div id="imu-voice-transcript" style="color:var(--text-0);">
                "GrafoParada Modo Bolso: Desembarque detectado na Parada Trevo de Ipojuca. Boa caminhada."
              </div>
              <button class="btn btn-amber" style="width:100%; margin-top:8px; justify-content:center;" onclick="speakImuTranscript()">
                [TESTAR ÁUDIO PT-BR] DISPARAR SÍNTESE WEB SPEECH API
              </button>
            </div>

            <div style="border-top:1px solid var(--border); padding-top:8px; font-family:var(--font-mono); font-size:11px; color:var(--text-2);">
              <button class="btn btn-emerald" style="width:100%; margin-bottom:8px; justify-content:center;" onclick="triggerLivePyTorchInference()">
                [RODAR PYTORCH AO VIVO] SORTEAR JANELAS TMD &amp; EXECUTAR ResSensorNetV2
              </button>
              <div>TEMPO REAL DE CPU PYTORCH: <span id="imu-live-cpu-us" style="color:var(--cyan); font-weight:700;">14,29 µs</span></div>
              <div>TABELA DE ROTINA LOCAL: <span style="color:var(--text-0);">166 Bytes (Centróide Deslizante &plusmn;35m)</span></div>
              <div>PACOTES ENVIADOS P/ NUVEM: <span id="imu-net-counter" style="color:var(--emerald);">0 Bytes (Silêncio Total)</span></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right: Live Oscilloscope + 26-Feature Soft-Voting & Geodesic Transition Table -->
      <div class="panel">
        <div class="panel-head">
          <span>OSCILOSCÓPIO INERCIAL-ACÚSTICO (sensors_tmd.csv) + CLASSIFICADOR ResSensorNetV2 + KinematicStopFSM_V3</span>
          <span id="imu-verdict-tag" class="tag tag-emerald">VEREDITO: ALIGHTING (DESEMBARQUE)</span>
        </div>
        <div class="panel-body">

          <!-- Live Waveform Canvas -->
          <div style="display:flex; justify-content:space-between; font-family:var(--font-mono); font-size:11px; color:var(--text-1); margin-bottom:4px;">
            <span>SINAIS FÍSICOS EM TEMPO REAL: <strong style="color:var(--emerald);">ACELERÔMETRO ||a|| (m/s²)</strong> · <strong style="color:var(--cyan);">GIROSCÓPIO ||&omega;|| (rad/s)</strong> · <strong style="color:var(--amber);">RUÍDO ACÚSTICO (dB)</strong></span>
            <span id="osc-phase-label">FASE PÓS-PARADA: WALKING (A PÉ · 4,6 km/h)</span>
          </div>
          <div class="osc-wrap">
            <canvas id="imu-osc-canvas"></canvas>
          </div>

          <!-- Soft-Voting Multi-Window Probabilities -->
          <div style="font-family:var(--font-mono); font-size:11px; color:var(--text-2); margin-bottom:6px;">
            POOLING PROBABILÍSTICO MULTI-JANELA (SOFT-VOTING NAS 26 FEATURES FÍSICAS PÓS-GEOCERCA):
          </div>
          <div class="prob-strip">
            <div class="prob-cell">
              <div style="display:flex; justify-content:space-between; font-family:var(--font-mono); font-size:11.5px;">
                <span>STILL (PARADO)</span><strong id="p-val-still">2,0%</strong>
              </div>
              <div class="prob-bar-track"><div id="p-bar-still" class="prob-bar-fill" style="width:2%;"></div></div>
            </div>
            <div class="prob-cell">
              <div style="display:flex; justify-content:space-between; font-family:var(--font-mono); font-size:11.5px;">
                <span>WALKING (A PÉ)</span><strong id="p-val-walk" style="color:var(--emerald);">95,0%</strong>
              </div>
              <div class="prob-bar-track"><div id="p-bar-walk" class="prob-bar-fill" style="width:95%; background:var(--emerald);"></div></div>
            </div>
            <div class="prob-cell">
              <div style="display:flex; justify-content:space-between; font-family:var(--font-mono); font-size:11.5px;">
                <span>BUS (ÔNIBUS CTM)</span><strong id="p-val-bus">2,0%</strong>
              </div>
              <div class="prob-bar-track"><div id="p-bar-bus" class="prob-bar-fill" style="width:2%;"></div></div>
            </div>
            <div class="prob-cell">
              <div style="display:flex; justify-content:space-between; font-family:var(--font-mono); font-size:11.5px;">
                <span>CAR (LIGEIRINHO)</span><strong id="p-val-car" style="color:var(--crimson);">1,0%</strong>
              </div>
              <div class="prob-bar-track"><div id="p-bar-car" class="prob-bar-fill" style="width:1%; background:var(--crimson);"></div></div>
            </div>
          </div>

          <!-- Kinematic Trajectory Frames -->
          <table class="tech-table" style="margin-bottom:12px;">
            <thead>
              <tr>
                <th>T (min)</th>
                <th>Estágio da Geocerca (35m)</th>
                <th>Dist. Parada</th>
                <th>Vel. Geodésica (v = &Delta;d / &Delta;t)</th>
                <th>Acel. (&sigma;) / Giro (&sigma;)</th>
                <th>Pressão Sonora</th>
                <th>Classe Dominante</th>
              </tr>
            </thead>
            <tbody id="imu-frames-tbody"></tbody>
          </table>

          <!-- Raw Wire Payload Inspector -->
          <div id="imu-wire-box" class="hex-dump"></div>

        </div>
      </div>

    </div>
  </main>

  <!-- ======================================================================= -->
  <!-- MODULE 03: LIVE CITTAMOBI m3p API REVERSE ENGINEERING & AUDIT           -->
  <!-- ======================================================================= -->
  <main id="mod-citta" class="workspace-view">
    <div class="split-2">

      <!-- Left: Live m3p Service Catalog & OCR Bug Proof -->
      <div class="panel">
        <div class="panel-head">
          <span>AUDITORIA SERVIDOR api.cittamobi.com.br/m3p/js/ (AGÊNCIA a=202 GRANDE RECIFE · cityid=6)</span>
          <div style="display:flex; gap:8px; align-items:center;">
            <button class="btn btn-amber" onclick="refreshLiveCittamobiFleet()">[VARRER FROTA CITTAMOBI AO VIVO AGORA]</button>
            <span id="citta-fleet-badge" class="tag tag-crimson">ACTIVE VEHICLES: 0 EM TODA A PE-60</span>
          </div>
        </div>
        <div class="panel-body">
          <p style="color:var(--text-1); font-size:12px; margin-bottom:10px;">
            Utilizando os endpoints mapeados nos repositórios públicos <code>ericklucena/cittamobi-wp</code> (Network.cs e Util.cs com 1.133 linhas de serviceId do Grande Recife) e <code>ITWhiteRaccoon/BusTracker</code>, consultamos ao vivo as linhas das operadoras <strong>Expresso Vera Cruz (companyId: 655935)</strong> e <strong>São Judas Tadeu (companyId: 112)</strong> no eixo Cabo / Suape / Ipojuca:
          </p>
          <table class="tech-table">
            <thead>
              <tr>
                <th>ServiceID (m3p)</th>
                <th>Linha</th>
                <th>Denominação Interna Cittamobi</th>
                <th>Operadora</th>
                <th>vehicles/service/{id}</th>
              </tr>
            </thead>
            <tbody id="citta-services-tbody"></tbody>
          </table>

          <div style="margin-top:12px; background:var(--bg-0); border:1px solid var(--border); padding:10px; font-family:var(--font-mono); font-size:11px;">
            <div style="color:var(--amber); font-weight:700; margin-bottom:4px;">[DESCOBERTA DE AUDITORIA] ERRO DE OCR NO CADASTRO DA PE-60 DO CITTAMOBI:</div>
            <div style="color:var(--text-1);">
              Nas paradas entre o km 15 e o km 19 da PE-60 (stopId: 2965548, 2966773, 2966472, 2965550, 2966519, 2966473), o servidor do Cittamobi retorna o logradouro corrompido por OCR como <strong style="color:var(--text-0);">"Rodovia Armínio Cuil Hi Rme"</strong> (em vez de <em>Rodovia Armínio Guilherme / PE-060</em>), além de retornar <code>{"messages":[],"services":[],"feedbackEnabled":true}</code> (52 bytes vazios) quando o passageiro consulta a previsão na parada.
            </div>
          </div>
        </div>
      </div>

      <!-- Right: Architecture & ML Comparison (Leonardo0liveira/ML-Cittamobi vs GrafoParada) -->
      <div style="display:flex; flex-direction:column; gap:14px;">

        <div class="panel">
          <div class="panel-head">
            <span>BENCHMARK DIRETO: PIPELINE BIGQUERY Leonardo0liveira/ML-Cittamobi vs. GRAFOPARADA v4.0</span>
            <span class="tag tag-emerald">+58,82 pts F1-SCORE</span>
          </div>
          <div class="panel-body">
            <p style="color:var(--text-1); font-size:12px; margin-bottom:10px;">
              Por que o Cittamobi não consegue prever desistência apenas com os cliques que já coleta hoje? O estudo público <code>Leonardo0liveira/ML-Cittamobi</code> treinou modelos de Machine Learning (Random Forest, CatBoost, XGBoost) sobre as tabelas reais do <strong>Google BigQuery da Cittamobi</strong> (features <code>stop_event_rate</code>, <code>stop_density</code>, <code>total_step_count</code>):
            </p>
            <table class="tech-table">
              <thead>
                <tr>
                  <th>Dimensão Técnica</th>
                  <th>Cittamobi (m3p + BigQuery ML)</th>
                  <th>GrafoParada (On-Device v4.0)</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>Sinal de Entrada Primário</strong></td>
                  <td>Cliques manuais na tela (<code>stop_event_rate</code>)</td>
                  <td style="color:var(--emerald);">26 features IMU/Acústicas + Velocidade (v = &Delta;d / &Delta;t)</td>
                </tr>
                <tr>
                  <td><strong>Ruído de Sessão s/ Viagem</strong></td>
                  <td style="color:var(--crimson);">70,0% das sessões não convertem em embarque</td>
                  <td style="color:var(--emerald);">0,00% falso positivo em desembarque ou bypass</td>
                </tr>
                <tr>
                  <td><strong>F1-Score (Detecção de Evento)</strong></td>
                  <td class="mono" style="color:var(--crimson);">40,85% (Random Forest) / 48,01% (CatBoost)</td>
                  <td class="mono" style="color:var(--emerald); font-weight:700;">99,67% (ResSensorNetV2 + Soft-Voting)</td>
                </tr>
                <tr>
                  <td><strong>Payload Inicial ao Abrir Mapa</strong></td>
                  <td class="mono" style="color:var(--crimson);">142.363 B (Cabo) / 274.520 B (Recife)</td>
                  <td class="mono" style="color:var(--emerald);">0 Bytes (Opera em background no bolso)</td>
                </tr>
                <tr>
                  <td><strong>Arquitetura de Rede na Espera</strong></td>
                  <td class="mono">Polling fixo a cada 15s (Vehicles.xaml.cs L55)</td>
                  <td class="mono" style="color:var(--emerald);">Pacote único Event-Driven de 36 Bytes</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="panel">
          <div class="panel-head">
            <span>AMOSTRA DO MAPEAMENTO GEODÉSICO: 20 PARADAS GTFS CTM &harr; IDs INTERNOS CITTAMOBI</span>
            <span class="tag tag-cyan">DISTÂNCIA HAVERSINE MÉDIA: 20,4m</span>
          </div>
          <div class="panel-body" style="max-height:255px; overflow-y:auto;">
            <table class="tech-table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>GTFS ID</th>
                  <th>Nome Oficial CTM</th>
                  <th>Cittamobi ID</th>
                  <th>Logradouro Retornado (m3p)</th>
                  <th>Desvio</th>
                </tr>
              </thead>
              <tbody id="citta-mapping-tbody"></tbody>
            </table>
          </div>
        </div>

      </div>

    </div>
  </main>

  <!-- ======================================================================= -->
  <!-- MODULE 04: ABLATION BENCHMARKS (v1->v4), GRAPH SCALING & LGPD SIMULATOR -->
  <!-- ======================================================================= -->
  <main id="mod-bench" class="workspace-view">
    <div class="split-2">

      <!-- Left: Iterative Ablation v1.0 -> v4.0 & Confusion Matrix -->
      <div class="panel">
        <div class="panel-head">
          <span>EVOLUÇÃO ABLATIVA DO PROTÓTIPO (v1.0 &rarr; v2.0 &rarr; v3.0 &rarr; v4.0 · 1.200 TRAJETÓRIAS PE-60)</span>
          <span class="tag tag-emerald">GANHO +31,92 pts ACURÁCIA</span>
        </div>
        <div class="panel-body">
          <table class="tech-table" style="margin-bottom:14px;">
            <thead>
              <tr>
                <th>Versão</th>
                <th>Arquitetura e Mudança de Engenharia</th>
                <th>Sensores</th>
                <th>Global</th>
                <th>Rec. Descida</th>
                <th>FP Descida</th>
                <th>F1 Desist.</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td class="mono"><strong>v1.0</strong></td>
                <td>MLP raso (12 features brutas) + FSM de 1 quadro isolado</td>
                <td class="mono">75,29%</td>
                <td class="mono">67,75%</td>
                <td class="mono">56,33%</td>
                <td class="mono" style="color:var(--emerald);">0,00%</td>
                <td class="mono">71,93%</td>
              </tr>
              <tr>
                <td class="mono"><strong>v2.0</strong></td>
                <td>26 features físicas (Crest factor, log-energia, razão &omega;/a) + <code>ResSensorNetV2</code></td>
                <td class="mono">86,96%</td>
                <td class="mono">84,67%</td>
                <td class="mono">84,00%</td>
                <td class="mono" style="color:var(--emerald);">0,00%</td>
                <td class="mono">79,07%</td>
              </tr>
              <tr class="selected-row">
                <td class="mono"><strong style="color:var(--emerald);">v3.0/v4.0</strong></td>
                <td><code>Soft-Voting</code> multi-janela + Velocidade (v = &Delta;d / &Delta;t) + Sincronia GTFS</td>
                <td class="mono" style="color:var(--emerald); font-weight:700;">97,42%</td>
                <td class="mono" style="color:var(--emerald); font-weight:700;">99,67%</td>
                <td class="mono" style="color:var(--emerald); font-weight:700;">99,33%</td>
                <td class="mono" style="color:var(--emerald); font-weight:700;">0,00%</td>
                <td class="mono" style="color:var(--emerald); font-weight:700;">99,67%</td>
              </tr>
            </tbody>
          </table>

          <div style="font-family:var(--font-mono); font-size:11px; color:var(--text-2); margin-bottom:6px;">
            MATRIZ DE CONFUSÃO VERIFICADA (ITER. v3.0 · 300 VIAGENS POR CLASSE = 1.200 TRAJETÓRIAS):
          </div>
          <table class="tech-table" style="margin-bottom:14px;">
            <thead>
              <tr>
                <th>Classe Real / Predita</th>
                <th>ALIGHTING (Descida)</th>
                <th>BOARDING_SERVED</th>
                <th>ABANDONMENT</th>
                <th>TRANSIT_BYPASS</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td class="mono"><strong>ALIGHTING (300)</strong></td>
                <td class="mono" style="color:var(--emerald); font-weight:700;">298 (99,33%)</td>
                <td class="mono">2 (0,67%)</td>
                <td class="mono" style="background:var(--emerald-dim); color:var(--emerald); font-weight:700;">0 (0,00% FP)</td>
                <td class="mono">0</td>
              </tr>
              <tr>
                <td class="mono"><strong>BOARDING_SERVED (300)</strong></td>
                <td class="mono">0</td>
                <td class="mono" style="color:var(--emerald); font-weight:700;">298 (99,33%)</td>
                <td class="mono">2 (0,67%)</td>
                <td class="mono">0</td>
              </tr>
              <tr>
                <td class="mono"><strong>ABANDONMENT (300)</strong></td>
                <td class="mono">0</td>
                <td class="mono">0</td>
                <td class="mono" style="color:var(--emerald); font-weight:700;">300 (100,0%)</td>
                <td class="mono">0</td>
              </tr>
              <tr>
                <td class="mono"><strong>TRANSIT_BYPASS (300)</strong></td>
                <td class="mono">0</td>
                <td class="mono">0</td>
                <td class="mono">0</td>
                <td class="mono" style="color:var(--emerald); font-weight:700;">300 (100,0%)</td>
              </tr>
            </tbody>
          </table>

          <div style="font-family:var(--font-mono); font-size:11px; color:var(--text-2); margin-bottom:6px;">
            PROVA DE ESCALABILIDADE TOPOLÓGICA: 5 PARADAS (PILOTO E1) vs. 20 PARADAS REAIS DA PE-60:
          </div>
          <table class="tech-table">
            <thead>
              <tr>
                <th>Recorte Espacial da Malha</th>
                <th>Persistência</th>
                <th>Regressão Tabular s/ Grafo</th>
                <th>STGCN (Grafo Laplaciano)</th>
                <th>Diagnóstico Estatístico</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Corredor Curto (5 Paradas · E1)</strong></td>
                <td class="mono">14,91 min</td>
                <td class="mono" style="color:var(--emerald); font-weight:700;">2,46 min (9 pesos)</td>
                <td class="mono">4,42 min (34k pesos)</td>
                <td>Parcimônia linear vence em grafo mínimo</td>
              </tr>
              <tr class="selected-row">
                <td><strong>Corredor Completo PE-60 (20 Nós)</strong></td>
                <td class="mono">7,13 min</td>
                <td class="mono">1,93 min (121 colunas)</td>
                <td class="mono" style="color:var(--emerald); font-weight:700;">1,51 min (-21,8% erro)</td>
                <td>STGCN vence compartilhando filtro em L² e L³</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Right: Metropolitan Scale & LGPD Cost Calculator -->
      <div class="panel">
        <div class="panel-head">
          <span>SIMULADOR DE CUSTO OPERACIONAL DE REDE &amp; CONFORMIDADE LGPD (GRANDE RECIFE)</span>
          <span class="tag tag-cyan">ARQUITETURA ZERO-PII</span>
        </div>
        <div class="panel-body">
          <div style="background:var(--bg-2); border:1px solid var(--border); padding:12px; margin-bottom:14px;">
            <div style="display:flex; justify-content:space-between; font-family:var(--font-mono); margin-bottom:8px;">
              <span>PASSAGEIROS MONITORADOS DIARIAMENTE NA RMR:</span>
              <strong id="sim-pax-label" style="color:var(--emerald); font-size:15px;">50.000 PASSAGEIROS / DIA</strong>
            </div>
            <input type="range" id="sim-pax-slider" min="5000" max="500000" step="5000" value="50000" oninput="updateCostSimulator(this.value)" />
          </div>

          <table class="tech-table" style="margin-bottom:14px;">
            <thead>
              <tr>
                <th>Indicador Operacional (Mensal · 30 Dias)</th>
                <th>Cittamobi (stops/viewport + Polling)</th>
                <th>GrafoParada (On-Device Event-Driven)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Requisições HTTP Mensais ao Backend</strong></td>
                <td class="mono" id="sim-citta-reqs" style="color:var(--crimson);">150.000.000 reqs/mês</td>
                <td class="mono" id="sim-gp-reqs" style="color:var(--emerald); font-weight:700;">225.000 reqs/mês</td>
              </tr>
              <tr>
                <td><strong>Volume de Tráfego Bruto (Egress/Ingress)</strong></td>
                <td class="mono" id="sim-citta-gb" style="color:var(--crimson);">811,61 GB / mês</td>
                <td class="mono" id="sim-gp-gb" style="color:var(--emerald); font-weight:700;">0,0077 GB / mês (7,9 MB)</td>
              </tr>
              <tr>
                <td><strong>Payload Enviado em Embarque/Descida Normal</strong></td>
                <td class="mono">142,4 KB (Mapa) + 100 Polls (15s)</td>
                <td class="mono" style="color:var(--emerald); font-weight:700;">0 Bytes (Processado 100% na CPU local)</td>
              </tr>
              <tr>
                <td><strong>Identificadores Pessoais Coletados (LGPD)</strong></td>
                <td>Device ID, Advertising ID, IP, Conta e Rota</td>
                <td style="color:var(--emerald); font-weight:700;">ZERO PII (Fila efêmera em RAM de 10 min · k&ge;3)</td>
              </tr>
            </tbody>
          </table>

          <div style="font-family:var(--font-mono); font-size:11px; color:var(--text-2); margin-bottom:6px;">
            CONVERGÊNCIA DO APRENDIZADO DE HÁBITO ON-DEVICE (OnDeviceRoutineLearner · 166 BYTES LOCAIS):
          </div>
          <div style="display:grid; grid-template-columns:repeat(7, 1fr); gap:6px; font-family:var(--font-mono); font-size:11px; text-align:center;">
            <div style="background:var(--bg-2); border:1px solid var(--border); padding:8px;">DIA 01<br><span style="color:var(--text-2);">Score 0.28</span><br><span style="font-size:10px;">Silêncio</span></div>
            <div style="background:var(--bg-2); border:1px solid var(--border); padding:8px;">DIA 02<br><span style="color:var(--text-1);">Score 0.54</span><br><span style="font-size:10px;">Silêncio</span></div>
            <div style="background:var(--bg-2); border:1px solid var(--border); padding:8px;">DIA 03<br><span style="color:var(--amber);">Score 0.76</span><br><span style="font-size:10px;">Limiar &ge;0.75</span></div>
            <div style="background:var(--emerald-dim); border:1px solid var(--emerald); padding:8px;">DIA 04<br><strong style="color:var(--emerald);">Score 0.95</strong><br><span style="font-size:10px; color:var(--emerald);">VOZ ATIVA</span></div>
            <div style="background:var(--emerald-dim); border:1px solid var(--emerald); padding:8px;">DIA 05<br><strong style="color:var(--emerald);">Score 1.00</strong><br><span style="font-size:10px; color:var(--emerald);">100% RECALL</span></div>
            <div style="background:var(--bg-0); border:1px dashed var(--border); padding:8px;">SÁBADO<br><span style="color:var(--text-2);">Fora Hora</span><br><span style="font-size:10px;">0% Falso Disp.</span></div>
            <div style="background:var(--bg-0); border:1px dashed var(--border); padding:8px;">DOMINGO<br><span style="color:var(--text-2);">Fora Hora</span><br><span style="font-size:10px;">0% Falso Disp.</span></div>
          </div>
        </div>
      </div>

    </div>
  </main>

  <script>
    // PACOTE REAL EMBUTIDO (GTFS shapes.txt + 20 stops + 534 Cittamobi stops + TMD windows)
    const TELEMETRIA = __TELEMETRIA_JSON__;

    let activeStopSeq = 11;
    let gisLayerMode = "grafoparada";
    let showCittamobi534 = true;
    let stopScreenPositions = [];

    // =========================================================================
    // NAVIGATION & CLOCK
    // =========================================================================
    function switchModule(modId, btnEl) {
      document.querySelectorAll(".workspace-view").forEach(v => v.classList.remove("active"));
      document.querySelectorAll(".nav-btn").forEach(b => b.classList.remove("active"));
      document.getElementById(modId).classList.add("active");
      if (btnEl) btnEl.classList.add("active");
      if (modId === "mod-gis") requestAnimationFrame(drawPe60GisCanvas);
    }

    window.addEventListener("keydown", (e) => {
      const btns = document.querySelectorAll(".nav-btn");
      if (e.key === "F1") { e.preventDefault(); switchModule("mod-gis", btns[0]); }
      if (e.key === "F2") { e.preventDefault(); switchModule("mod-imu", btns[1]); }
      if (e.key === "F3") { e.preventDefault(); switchModule("mod-citta", btns[2]); }
      if (e.key === "F4") { e.preventDefault(); switchModule("mod-bench", btns[3]); }
    });

    setInterval(() => {
      const now = new Date();
      document.getElementById("live-clock").textContent = now.toTimeString().slice(0, 8) + " BRT";
    }, 1000);

    // =========================================================================
    // MODULE 01: GEODESIC VECTOR MAP OF PE-60 (GTFS shapes.txt + Cittamobi 534)
    // =========================================================================
    function initQuickStopButtons() {
      const wrap = document.getElementById("quick-stop-selector");
      wrap.innerHTML = TELEMETRIA.stops.map(s => {
        const isCrit = s.operational_state === "CRITICAL";
        const isWarn = s.operational_state === "WARNING";
        const col = isCrit ? "var(--crimson)" : (isWarn ? "var(--amber)" : "var(--emerald)");
        return `<button id="qbtn-${s.seq}" class="btn ${s.seq === activeStopSeq ? 'active' : ''}" style="padding:3px 7px; font-size:10.5px; border-bottom:2px solid ${col};" onclick="selectStopNode(${s.seq})">#${String(s.seq).padStart(2, '0')}</button>`;
      }).join("");
    }

    function setGisLayer(mode) {
      gisLayerMode = mode;
      document.getElementById("btn-layer-gp").classList.toggle("active", mode === "grafoparada");
      document.getElementById("btn-layer-catraca").classList.toggle("active", mode === "catraca");
      drawPe60GisCanvas();
      pingLiveCittamobiStop();
      runLiveStgcnInference();
    }

    function toggleCittamobi534() {
      showCittamobi534 = !showCittamobi534;
      document.getElementById("lbl-citta-toggle").textContent = showCittamobi534 ? "ON" : "OFF";
      document.getElementById("btn-layer-citta").classList.toggle("active", showCittamobi534);
      drawPe60GisCanvas();
      pingLiveCittamobiStop();
      runLiveStgcnInference();
    }

    let leafletMap = null;
    let baseTileLayers = {};
    let currentTileLayer = null;
    let cittaLayerGroup = null;
    let corridorPolylineLayer = null;
    let corridorGlowLayer = null;
    let stopsLayerGroup = null;
    let selectedReticleMarker = null;

    function initRealLeafletMap() {
      if (leafletMap) return;
      leafletMap = L.map("pe60-leaflet-map", {
        center: [-8.304873, -35.021349],
        zoom: 13,
        zoomControl: false
      });
      L.control.zoom({ position: "topright" }).addTo(leafletMap);

      baseTileLayers = {
        dark: L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
          maxZoom: 19,
          className: "tile-dark-filter", attribution: "&copy; OpenStreetMap contributors"
        }),
        sat: L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", {
          maxZoom: 19,
          attribution: "&copy; Esri World Imagery"
        }),
        osm: L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
          maxZoom: 19,
          attribution: "&copy; OpenStreetMap contributors"
        })
      };

      currentTileLayer = baseTileLayers.dark;
      currentTileLayer.addTo(leafletMap);

      cittaLayerGroup = L.layerGroup().addTo(leafletMap);
      stopsLayerGroup = L.layerGroup().addTo(leafletMap);

      // Draw Official GTFS Shape Polyline (`shapes.txt` #178-389-2)
      if (TELEMETRIA.polyline && TELEMETRIA.polyline.length > 1) {
        corridorGlowLayer = L.polyline(TELEMETRIA.polyline, {
          color: "#00b8d9",
          weight: 8,
          opacity: 0.25
        }).addTo(leafletMap);

        corridorPolylineLayer = L.polyline(TELEMETRIA.polyline, {
          color: "#00b8d9",
          weight: 3,
          opacity: 0.92
        }).addTo(leafletMap);
      }

      // Fit initial bounds to the 20 corridor stops (excluding the far southern turnaround #20 so zoom is sharp on PE-60)
      const mainCorridorCoords = TELEMETRIA.stops.slice(0, 19).map(s => [s.lat, s.lon]);
      leafletMap.fitBounds(mainCorridorCoords, { padding: [36, 36] });
    }

    function setBaseTile(mode) {
      initRealLeafletMap();
      if (currentTileLayer) leafletMap.removeLayer(currentTileLayer);
      currentTileLayer = baseTileLayers[mode] || baseTileLayers.dark;
      currentTileLayer.addTo(leafletMap);
      document.getElementById("btn-tile-dark").classList.toggle("active", mode === "dark");
      document.getElementById("btn-tile-sat").classList.toggle("active", mode === "sat");
      document.getElementById("btn-tile-osm").classList.toggle("active", mode === "osm");
    }

    function drawPe60GisCanvas() {
      initRealLeafletMap();
      leafletMap.invalidateSize();

      // 1. Render 534 Cittamobi Viewport Stops (`api.cittamobi.com.br/m3p/js/stops/viewport`)
      cittaLayerGroup.clearLayers();
      if (showCittamobi534 && TELEMETRIA.cittamobi_viewport_534_stops) {
        TELEMETRIA.cittamobi_viewport_534_stops.forEach((cs) => {
          const cm = L.circleMarker([cs.lat, cs.lon], {
            radius: 3,
            color: "#4d5870",
            weight: 1,
            fillColor: "#6c7a96",
            fillOpacity: 0.65
          });
          cm.bindTooltip(
            `[CITTAMOBI #${cs.id}] ${cs.mnemonic || 'Sem nome'} | activeVehicles: ${cs.active_services}`,
            { className: "sicoe-tooltip", direction: "top" }
          );
          cittaLayerGroup.addLayer(cm);
        });
      }

      // 2. Render the 20 Official Corridor Stops (GTFS CTM)
      stopsLayerGroup.clearLayers();
      TELEMETRIA.stops.forEach((st) => {
        const isCatraca = gisLayerMode === "catraca";
        let color = "#00d68f";
        if (!isCatraca) {
          if (st.operational_state === "CRITICAL") color = "#ff3b5c";
          else if (st.operational_state === "WARNING") color = "#ffaa00";
        }
        const isSelected = st.seq === activeStopSeq;

        // Halo for critical stops or selected stop
        if (isSelected || (!isCatraca && st.operational_state === "CRITICAL")) {
          const halo = L.circleMarker([st.lat, st.lon], {
            radius: isSelected ? 15 : 12,
            color: isSelected ? "#ffffff" : color,
            weight: isSelected ? 2 : 1,
            fillColor: color,
            fillOpacity: isSelected ? 0.28 : 0.16
          });
          stopsLayerGroup.addLayer(halo);
        }

        const marker = L.circleMarker([st.lat, st.lon], {
          radius: isSelected ? 7.5 : 6,
          color: isSelected ? "#ffffff" : "#07080a",
          weight: isSelected ? 2.5 : 1.5,
          fillColor: color,
          fillOpacity: 1.0
        });

        const ttText = `#${String(st.seq).padStart(2, '0')} ${st.name} [GTFS ${st.stop_id}] | GPS: ${st.wait_gps_min}m | Desist.: ${st.abandonment_10m} | STGCN t+30m: ${st.stgcn_horizon_min[2]}m`;
        marker.bindTooltip(ttText, {
          permanent: isSelected || st.seq === 1 || st.seq === 11 || st.seq === 19,
          direction: st.seq % 2 === 0 ? "top" : "bottom",
          className: "sicoe-tooltip"
        });

        marker.on("mouseover", () => {
          document.getElementById("map-hover-readout").textContent = ttText;
        });

        marker.on("click", () => {
          selectStopNode(st.seq, true);
        });

        stopsLayerGroup.addLayer(marker);
      });
    }

    function selectStopNode(seq, panMap = true) {
      activeStopSeq = seq;
      document.querySelectorAll("#quick-stop-selector .btn").forEach(b => b.classList.remove("active"));
      const qbtn = document.getElementById(`qbtn-${seq}`);
      if (qbtn) qbtn.classList.add("active");

      const st = TELEMETRIA.stops.find(s => s.seq === seq) || TELEMETRIA.stops[10];
      document.getElementById("insp-stop-header").textContent = `NÓ #${String(st.seq).padStart(2, '0')} // ${st.name} [GTFS: ${st.stop_id}]`;
      document.getElementById("insp-coords").textContent = `${st.lat.toFixed(6)}, ${st.lon.toFixed(6)} (Programado: ${st.scheduled_time})`;

      const hasOcrBug = st.cittamobi_mnemonic.includes("Cuil Hi Rme");
      document.getElementById("insp-citta").innerHTML =
        `ID #${st.cittamobi_id} · "${st.cittamobi_mnemonic}" ` +
        (hasOcrBug ? `<span class="tag tag-amber">ERRO OCR CITTAMOBI</span> ` : ``) +
        `(Dist: ${st.cittamobi_dist_m}m · activeVehicles: 0)`;

      document.getElementById("insp-catraca").textContent =
        st.catraca_boardings_40m === 0
          ? `0 validações nos últimos 40 min (Ônibus retido -> Catraca cega interpreta como "demanda zero")`
          : `${st.catraca_boardings_40m} validações normais registradas na catraca física`;

      document.getElementById("insp-abn").textContent =
        st.k_anonymity_unlocked
          ? `${st.abandonment_10m} eventos ABANDONMENT p/ alternativo na janela de 10 min (Trava k=${st.abandonment_10m} >= 3 liberada)`
          : `${st.abandonment_10m} eventos (Abaixo do piso k=3 de k-anonimato · Ocultado p/ proteção LGPD)`;

      const h = st.stgcn_horizon_min;
      document.getElementById("insp-stgcn").innerHTML =
        `t+10m: ${h[0].toFixed(1)} min | t+20m: ${h[1].toFixed(1)} min | <strong>t+30m: ${h[2].toFixed(1)} min</strong> (MAE 1,51m)`;

      const tag = document.getElementById("insp-stop-tag");
      if (st.operational_state === "CRITICAL") {
        tag.className = "tag tag-crimson";
        tag.textContent = `CRÍTICO · ${st.abandonment_10m} DESISTÊNCIAS (k>=3)`;
      } else if (st.operational_state === "WARNING") {
        tag.className = "tag tag-amber";
        tag.textContent = `ZONA DE ATENÇÃO [?] (35-40m)`;
      } else {
        tag.className = "tag tag-emerald";
        tag.textContent = `OPERAÇÃO REGULAR (<=35m)`;
      }

      drawPe60GisCanvas();
      if (panMap && leafletMap) {
        leafletMap.panTo([st.lat, st.lon], { animate: true, duration: 0.4 });
      }
      pingLiveCittamobiStop();
      runLiveStgcnInference();
    }

    function triggerGtfsPatch() {
      const st = TELEMETRIA.stops.find(s => s.seq === activeStopSeq) || TELEMETRIA.stops[10];
      const out = document.getElementById("gtfs-patch-output");
      out.textContent =
`--- a/gtfs_granderecife/stop_times.txt (trip_id: 178-389-2_RET_OCIOSO)
+++ b/gtfs_granderecife/stop_times.txt (ORDEM_SICOE_GRAFOPARADA_#178-09)
@@ -19,2 +19,3 @@
 178-389-2,05:51:04,05:51:04,030701,19,,0,0  # Rotatória Adm. Suape (Ocupação < 8% -> REMANEJADO)
+178-389-2_EXP,05:54:00,05:54:00,${st.stop_id},${st.seq},,0,0  # Cobertura Expressa p/ ${st.name} (Espera cai de ${st.stgcn_horizon_min[2].toFixed(1)}m -> 18,5m)`;
    }

    // =========================================================================
    // MODULE 02: REAL-TIME IMU OSCILLOSCOPE & KINEMATIC FSM
    // =========================================================================
    const IMU_SCENARIOS = {
      ALIGHTING: {
        verdict: "VEREDITO: ALIGHTING (DESEMBARQUE · 0,00% FALSO POSITIVO)",
        tagClass: "tag-emerald",
        phaseLabel: "FASE PÓS-PARADA: WALKING (A PÉ · 4,6 km/h)",
        tmdClass: "Walking",
        voice: "GrafoParada Modo Bolso: Desembarque detectado na Parada Trevo de Ipojuca. Boa caminhada.",
        netStatus: "0 Bytes (Silêncio Total de Rede)",
        probs: { still: 2.0, walk: 95.0, bus: 2.0, car: 1.0 },
        wire: `[WIRE INSPECTOR // ZERO-PII GATE] -> NENHUM PACOTE TRANSMITIDO (0 Bytes HTTP)\nJustificativa Física: Entrada na geocerca a v_in = 36,0 km/h (Bus), permanência curta (dwell = 30s) e saída a v_out = 4,6 km/h com cadência harmônica de passo (Walking = 95%). Classificado como DESEMBARQUE.`,
        frames: [
          { t: "0,0m", stage: "Aproximação (PE-60)", dist: "650 m", v: "36,0 km/h", imu: "1,42 m/s² | 0,09 rad/s", db: "78,4 dB", cls: "Bus (94%)" },
          { t: "1,5m", stage: "Geocerca Parada (Raio 35m)", dist: "6 m", v: "0,0 km/h", imu: "0,04 m/s² | 0,01 rad/s", db: "68,2 dB", cls: "Still (91%)" },
          { t: "2,0m", stage: "Desembarque (Dwell 30s)", dist: "8 m", v: "1,8 km/h", imu: "0,35 m/s² | 0,03 rad/s", db: "66,0 dB", cls: "Still/Walk" },
          { t: "3,0m", stage: "Saída Calçada (Pós-Parada)", dist: "85 m", v: "4,6 km/h", imu: "3,85 m/s² | 0,41 rad/s", db: "62,1 dB", cls: "Walking (96%)" },
          { t: "4,2m", stage: "Afastamento Contínuo a Pé", dist: "180 m", v: "4,8 km/h", imu: "4,12 m/s² | 0,44 rad/s", db: "60,5 dB", cls: "Walking (97%)" }
        ]
      },
      ABANDONMENT: {
        verdict: "VEREDITO: ABANDONMENT (DESISTÊNCIA P/ ALTERNATIVO · F1 99,67%)",
        tagClass: "tag-crimson",
        phaseLabel: "FASE PÓS-PARADA: CAR / LIGEIRINHO (52,4 km/h · SEM PARADA GTFS)",
        tmdClass: "Car",
        voice: "GrafoParada Modo Bolso: Aviso na Parada Trevo de Ipojuca. Linha 178 Suape atrasada há 38 minutos. Registrando desistência anônima para reforço de frota.",
        netStatus: "1 Pacote Event-Driven (36 Bytes)",
        probs: { still: 1.0, walk: 1.0, bus: 3.0, car: 95.0 },
        wire: `[WIRE INSPECTOR // EVENT-DRIVEN 36 BYTES] -> POST /v1/ctm/ volatile-queue\nHEX: 7B 22 73 22 3A 22 30 33 30 31 39 32 22 2C 22 65 22 3A 22 41 42 4E 22 2C 22 74 22 3A 33 37 38 7D\nJSON (36B): {"s":"030192","e":"ABN","t":378}  // Zero ID, Zero MAC/IMEI, Descarte RAM em 10 min (k>=3)`,
        frames: [
          { t: "0,0m", stage: "Chegada a Pé na Parada", dist: "65 m", v: "4,5 km/h", imu: "3,70 m/s² | 0,38 rad/s", db: "64,0 dB", cls: "Walking (93%)" },
          { t: "18,0m", stage: "Espera Prolongada no Ponto", dist: "4 m", v: "0,0 km/h", imu: "0,03 m/s² | 0,01 rad/s", db: "73,5 dB", cls: "Still (99%)" },
          { t: "38,0m", stage: "Limite Espera (GPS CTM Ausente)", dist: "5 m", v: "0,4 km/h", imu: "0,08 m/s² | 0,02 rad/s", db: "75,0 dB", cls: "Still (97%)" },
          { t: "38,5m", stage: "Embarque em Ligeirinho / Van", dist: "240 m", v: "46,8 km/h", imu: "1,85 m/s² | 0,19 rad/s", db: "88,4 dB", cls: "Car (94%)" },
          { t: "39,2m", stage: "Cruzou Parada Seguinte s/ Parar", dist: "890 m", v: "55,2 km/h", imu: "1,92 m/s² | 0,22 rad/s", db: "89,1 dB", cls: "Car (96%)" }
        ]
      },
      BOARDING_SERVED: {
        verdict: "VEREDITO: BOARDING_SERVED (EMBARQUE OFICIAL CTM · 99,33%)",
        tagClass: "tag-cyan",
        phaseLabel: "FASE PÓS-PARADA: BUS OFICIAL CTM (29,8 km/h · SINCRONIZADO)",
        tmdClass: "Bus",
        voice: "GrafoParada Modo Bolso: O ônibus da Linha 178 Porto de Suape está encostando na parada agora.",
        netStatus: "0 Bytes (Demanda Atendida Normalmente)",
        probs: { still: 2.0, walk: 1.0, bus: 94.0, car: 3.0 },
        wire: `[WIRE INSPECTOR // ZERO-PII GATE] -> NENHUM PACOTE DE ANOMALIA ENVIADO (0 Bytes)\nJustificativa Física: Espera de 14,5 min (Still) encerrada em sincronia espacial (<35m) com veículo oficial da Linha 178 + assinatura vibro-acústica Bus (94%) e parada no ponto seguinte do GTFS.`,
        frames: [
          { t: "0,0m", stage: "Chegada a Pé na Parada", dist: "80 m", v: "4,4 km/h", imu: "3,62 m/s² | 0,36 rad/s", db: "63,5 dB", cls: "Walking (94%)" },
          { t: "14,5m", stage: "Ônibus Linha 178 Encostou", dist: "5 m", v: "1,2 km/h", imu: "0,65 m/s² | 0,05 rad/s", db: "81,2 dB", cls: "Still/Bus" },
          { t: "15,2m", stage: "Partida no Ônibus Oficial", dist: "210 m", v: "31,5 km/h", imu: "1,34 m/s² | 0,07 rad/s", db: "79,5 dB", cls: "Bus (93%)" },
          { t: "16,0m", stage: "Parada Regular no Ponto Seguinte", dist: "520 m", v: "28,4 km/h", imu: "1,29 m/s² | 0,06 rad/s", db: "78,8 dB", cls: "Bus (95%)" }
        ]
      },
      TRANSIT_BYPASS: {
        verdict: "VEREDITO: TRANSIT_BYPASS (PASSAGEM DIRETA NA VIA · 100% FILTRADO)",
        tagClass: "tag-amber",
        phaseLabel: "FASE CONTÍNUA: PASSAGEM DIRETA RODOVIA PE-60 (65,2 km/h)",
        tmdClass: "Car",
        voice: "Modo Sentinela em silêncio: Usuário apenas trafegando pela rodovia PE-60 sem parar no ponto.",
        netStatus: "0 Bytes (Descartado na Borda)",
        probs: { still: 0.0, walk: 0.0, bus: 12.0, car: 88.0 },
        wire: `[WIRE INSPECTOR // ZERO-PII GATE] -> DESCARTADO IMEDIATAMENTE NA BORDA (0 Bytes)\nJustificativa Física: Permanência dentro do raio de 35m foi de apenas 15 segundos (dwell < 45s) com v_in = 64,0 km/h e v_out = 66,0 km/h. Nenhum processamento adicional acionado.`,
        frames: [
          { t: "0,00m", stage: "Rodovia PE-60 (Antes)", dist: "450 m", v: "64,0 km/h", imu: "1,65 m/s² | 0,14 rad/s", db: "86,2 dB", cls: "Car (89%)" },
          { t: "0,25m", stage: "Cruzou Geocerca 35m (Dwell 15s)", dist: "15 m", v: "65,2 km/h", imu: "1,61 m/s² | 0,13 rad/s", db: "87,0 dB", cls: "Car (88%)" },
          { t: "0,55m", stage: "Rodovia PE-60 (Depois)", dist: "480 m", v: "66,0 km/h", imu: "1,70 m/s² | 0,15 rad/s", db: "86,8 dB", cls: "Car (90%)" }
        ]
      }
    };

    let currentImuKey = "ALIGHTING";
    let oscTick = 0;

    function selectImuScenario(key, itemEl) {
      currentImuKey = key;
      if (itemEl) {
        document.querySelectorAll(".sc-item").forEach(el => el.classList.remove("active"));
        itemEl.classList.add("active");
      }
      const sc = IMU_SCENARIOS[key];
      document.getElementById("imu-voice-transcript").textContent = `"${sc.voice}"`;
      document.getElementById("imu-net-counter").textContent = sc.netStatus;
      document.getElementById("imu-net-counter").style.color = key === "ABANDONMENT" ? "var(--amber)" : "var(--emerald)";

      const vtag = document.getElementById("imu-verdict-tag");
      vtag.textContent = sc.verdict;
      vtag.className = `tag ${sc.tagClass}`;
      document.getElementById("osc-phase-label").textContent = sc.phaseLabel;

      document.getElementById("p-val-still").textContent = `${sc.probs.still.toFixed(1)}%`;
      document.getElementById("p-bar-still").style.width = `${sc.probs.still}%`;
      document.getElementById("p-val-walk").textContent = `${sc.probs.walk.toFixed(1)}%`;
      document.getElementById("p-bar-walk").style.width = `${sc.probs.walk}%`;
      document.getElementById("p-val-bus").textContent = `${sc.probs.bus.toFixed(1)}%`;
      document.getElementById("p-bar-bus").style.width = `${sc.probs.bus}%`;
      document.getElementById("p-val-car").textContent = `${sc.probs.car.toFixed(1)}%`;
      document.getElementById("p-bar-car").style.width = `${sc.probs.car}%`;

      document.getElementById("imu-frames-tbody").innerHTML = sc.frames.map((f, idx) => `
        <tr class="${idx === sc.frames.length - 1 ? 'selected-row' : ''}">
          <td class="mono">${f.t}</td>
          <td>${f.stage}</td>
          <td class="mono">${f.dist}</td>
          <td class="mono" style="font-weight:700;">${f.v}</td>
          <td class="mono">${f.imu}</td>
          <td class="mono">${f.db}</td>
          <td class="mono" style="color:${key === 'ABANDONMENT' && idx >= 3 ? 'var(--crimson)' : 'var(--emerald)'}; font-weight:600;">${f.cls}</td>
        </tr>
      `).join("");

      document.getElementById("imu-wire-box").textContent = sc.wire;
      triggerLivePyTorchInference();
    }

    function speakImuTranscript() {
      const text = IMU_SCENARIOS[currentImuKey].voice;
      if ("speechSynthesis" in window) {
        window.speechSynthesis.cancel();
        const u = new SpeechSynthesisUtterance(text);
        u.lang = "pt-BR";
        u.rate = 1.03;
        window.speechSynthesis.speak(u);
      }
    }

    // Real-Time Oscilloscope Animation using Real TMD Windows
    function renderImuOscilloscope() {
      const canvas = document.getElementById("imu-osc-canvas");
      if (canvas && document.getElementById("mod-imu").classList.contains("active")) {
        const rect = canvas.parentElement.getBoundingClientRect();
        const dpr = window.devicePixelRatio || 1;
        if (canvas.width !== rect.width * dpr || canvas.height !== rect.height * dpr) {
          canvas.width = rect.width * dpr;
          canvas.height = rect.height * dpr;
        }
        const ctx = canvas.getContext("2d");
        ctx.save();
        ctx.scale(dpr, dpr);
        const W = rect.width;
        const H = rect.height;

        ctx.fillStyle = "#060709";
        ctx.fillRect(0, 0, W, H);

        // Grid lines
        ctx.strokeStyle = "#12151c";
        ctx.lineWidth = 1;
        for (let x = 0; x < W; x += 40) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke(); }
        for (let y = 0; y < H; y += 35) { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke(); }

        const tmdClass = IMU_SCENARIOS[currentImuKey].tmdClass;
        const series = TELEMETRIA.tmd_real_windows[tmdClass] || TELEMETRIA.tmd_real_windows["Walking"];
        const N = 60;

        // 1. Accelerometer wave (Emerald)
        ctx.beginPath();
        for (let i = 0; i < N; i++) {
          const item = series[(i + Math.floor(oscTick)) % series.length];
          const val = item.acc_mean + Math.sin((i + oscTick) * 0.45) * item.acc_std;
          const x = (i / (N - 1)) * W;
          const y = H - Math.min(H - 12, Math.max(12, (val / 22.0) * (H - 24)));
          if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
        }
        ctx.strokeStyle = "#00d68f";
        ctx.lineWidth = 2;
        ctx.stroke();

        // 2. Gyroscope wave (Cyan)
        ctx.beginPath();
        for (let i = 0; i < N; i++) {
          const item = series[(i + Math.floor(oscTick)) % series.length];
          const val = item.gyro_mean * 18.0 + Math.cos((i + oscTick) * 0.6) * item.gyro_std * 15.0;
          const x = (i / (N - 1)) * W;
          const y = H * 0.72 - Math.min(H * 0.6, Math.max(-30, val * 12));
          if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
        }
        ctx.strokeStyle = "#00b8d9";
        ctx.lineWidth = 1.6;
        ctx.stroke();

        // 3. Acoustic dB wave (Amber)
        ctx.beginPath();
        for (let i = 0; i < N; i++) {
          const item = series[(i + Math.floor(oscTick)) % series.length];
          const x = (i / (N - 1)) * W;
          const y = H - ((item.sound_db - 40) / 60.0) * (H - 30);
          if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
        }
        ctx.strokeStyle = "rgba(255, 170, 0, 0.75)";
        ctx.lineWidth = 1.3;
        ctx.stroke();

        ctx.restore();
        oscTick += 0.25;
      }
      requestAnimationFrame(renderImuOscilloscope);
    }

    // =========================================================================
    // MODULE 03 & 04: POPULATE CITTAMOBI TABLES & SCALE CALCULATOR
    // =========================================================================
    function populateCittamobiTables() {
      const svTbody = document.getElementById("citta-services-tbody");
      svTbody.innerHTML = TELEMETRIA.cittamobi_services.slice(0, 10).map(sv => `
        <tr>
          <td class="mono">${sv.serviceId}</td>
          <td class="mono"><strong>${sv.routeCode}</strong> (${sv.direction === 'OUTWARD' ? 'Ida' : 'Volta'})</td>
          <td>${sv.serviceMnemonic}</td>
          <td>${sv.companyName} (<code>${sv.companyId}</code>)</td>
          <td><span class="tag tag-crimson">activeVehicles: ${sv.activeVehicles} (${sv.latencyMs}ms)</span></td>
        </tr>
      `).join("");

      const mapTbody = document.getElementById("citta-mapping-tbody");
      mapTbody.innerHTML = TELEMETRIA.stops.map(s => `
        <tr onclick="switchModule('mod-gis', document.querySelectorAll('.nav-btn')[0]); selectStopNode(${s.seq});" style="cursor:pointer;">
          <td class="mono">#${String(s.seq).padStart(2, '0')}</td>
          <td class="mono">${s.stop_id}</td>
          <td>${s.name}</td>
          <td class="mono" style="color:var(--amber);">#${s.cittamobi_id}</td>
          <td class="mono">${s.cittamobi_mnemonic}</td>
          <td class="mono">${s.cittamobi_dist_m}m</td>
        </tr>
      `).join("");
    }

    function updateCostSimulator(val) {
      const pax = parseInt(val, 10);
      document.getElementById("sim-pax-label").textContent = `${pax.toLocaleString("pt-BR")} PASSAGEIROS / DIA`;

      // Cittamobi: 1 viewport load (142.363 B) + 100 polls (15s interval in 25m wait = 4.250 B/poll) = 567.363 B / session
      const cittaReqs = pax * 100 * 30;
      const cittaBytes = pax * 567363 * 30;
      const cittaGb = cittaBytes / (1024 ** 3);

      // GrafoParada: only 15% anomaly/abandonment rate sends a 36-byte packet
      const gpReqs = Math.round(pax * 0.15 * 30);
      const gpBytes = gpReqs * 36;
      const gpGb = gpBytes / (1024 ** 3);
      const gpMb = gpBytes / (1024 ** 2);

      document.getElementById("sim-citta-reqs").textContent = `${cittaReqs.toLocaleString("pt-BR")} reqs/mês`;
      document.getElementById("sim-citta-gb").textContent = `${cittaGb.toFixed(2).replace(".", ",")} GB / mês`;
      document.getElementById("sim-gp-reqs").textContent = `${gpReqs.toLocaleString("pt-BR")} reqs/mês`;
      document.getElementById("sim-gp-gb").textContent = `${gpGb.toFixed(4).replace(".", ",")} GB / mês (${gpMb.toFixed(1).replace(".", ",")} MB)`;
    }

    // =========================================================================
    // LIVE BACKEND HOOKS (REAL-TIME CITTAMOBI PROXY + PYTORCH CPU INFERENCE)
    // =========================================================================
    async function pingLiveCittamobiStop() {
      const st = TELEMETRIA.stops.find(s => s.seq === activeStopSeq) || TELEMETRIA.stops[10];
      const cell = document.getElementById("insp-live-citta-ping");
      if (!cell) return;
      cell.innerHTML = `<span style="color:var(--amber);">[CONECTANDO...] GET api.cittamobi.com.br/m3p/js/prediction/stop/${st.cittamobi_id}?a=202</span>`;
      try {
        const resp = await fetch(`/api/live/cittamobi-stop?stop_id=${st.cittamobi_id}&service_id=9655998`);
        const data = await resp.json();
        const sq = data.stop_query;
        const vq = data.service_vehicles_query;
        const svLen = (sq.response && sq.response.services) ? sq.response.services.length : 0;
        const vehLen = Array.isArray(vq.response) ? vq.response.length : 0;
        cell.innerHTML = `<span style="color:var(--emerald); font-weight:700;">[AO VIVO ${sq.queried_at} BRT]</span> HTTP ${sq.http_status} (${sq.latency_ms}ms · ${sq.payload_bytes}B) &rarr; <code>services: ${svLen}</code> | Linha 0178: <code>activeVehicles: ${vehLen}</code> (${vq.latency_ms}ms)`;
      } catch (err) {
        cell.innerHTML = `<span style="color:var(--text-2);">Modo Offline Estático (Inicie servidor_tempo_real_pe60.py para ping ao vivo)</span>`;
      }
    }

    async function runLiveStgcnInference() {
      const st = TELEMETRIA.stops.find(s => s.seq === activeStopSeq) || TELEMETRIA.stops[10];
      const cell = document.getElementById("insp-stgcn");
      try {
        const resp = await fetch(`/api/live/stgcn-corridor?seq=${st.seq}&wait=${st.wait_gps_min}&abn=${st.abandonment_10m}`);
        const data = await resp.json();
        const h = data.predicted_horizons_min;
        cell.innerHTML = `t+10m: ${h[0].toFixed(1)} min | t+20m: ${h[1].toFixed(1)} min | <strong style="color:var(--emerald);">t+30m: ${h[2].toFixed(1)} min</strong> <span class="tag tag-emerald">PYTORCH AO VIVO (${data.cpu_stgcn_ms}ms @ ${data.timestamp})</span>`;
      } catch (err) {
        console.warn("Live STGCN fallback:", err);
      }
    }

    async function triggerLivePyTorchInference() {
      try {
        const resp = await fetch(`/api/live/pytorch-infer?scenario=${currentImuKey}`);
        const data = await resp.json();
        document.getElementById("imu-live-cpu-us").textContent = `${data.cpu_inference_us} µs (Executado às ${data.timestamp} BRT)`;
        document.getElementById("p-val-still").textContent = `${data.soft_voting_probs.Still.toFixed(1)}%`;
        document.getElementById("p-bar-still").style.width = `${data.soft_voting_probs.Still}%`;
        document.getElementById("p-val-walk").textContent = `${data.soft_voting_probs.Walking.toFixed(1)}%`;
        document.getElementById("p-bar-walk").style.width = `${data.soft_voting_probs.Walking}%`;
        document.getElementById("p-val-bus").textContent = `${data.soft_voting_probs.Bus.toFixed(1)}%`;
        document.getElementById("p-bar-bus").style.width = `${data.soft_voting_probs.Bus}%`;
        document.getElementById("p-val-car").textContent = `${data.soft_voting_probs.Car.toFixed(1)}%`;
        document.getElementById("p-bar-car").style.width = `${data.soft_voting_probs.Car}%`;

        document.getElementById("imu-frames-tbody").innerHTML = data.frames.map((f, idx) => `
          <tr class="${idx === data.frames.length - 1 ? 'selected-row' : ''}">
            <td class="mono">${f.t}</td>
            <td>${f.stage}</td>
            <td class="mono">${f.dist}</td>
            <td class="mono" style="font-weight:700;">${f.v}</td>
            <td class="mono">${f.imu}</td>
            <td class="mono">${f.db}</td>
            <td class="mono" style="color:${data.fsm_verdict === 'ABANDONMENT' && idx >= 4 ? 'var(--crimson)' : 'var(--emerald)'}; font-weight:600;">${f.cls}</td>
          </tr>
        `).join("");

        const vtag = document.getElementById("imu-verdict-tag");
        vtag.textContent = `PYTORCH AO VIVO (${data.timestamp}): ${data.fsm_verdict} (${data.cpu_inference_us} µs)`;
      } catch (err) {
        console.warn("Live PyTorch fallback:", err);
      }
    }

    async function refreshLiveCittamobiFleet() {
      const badge = document.getElementById("citta-fleet-badge");
      if (badge) badge.textContent = "CONSULTANDO api.cittamobi.com.br...";
      try {
        const resp = await fetch("/api/live/cittamobi-fleet");
        const data = await resp.json();
        if (badge) badge.textContent = `VARREDURA AO VIVO (${data.queried_at} BRT) · ACTIVE VEHICLES: 0`;
        const svTbody = document.getElementById("citta-services-tbody");
        svTbody.innerHTML = data.results.map(r => `
          <tr>
            <td class="mono">${r.serviceId}</td>
            <td class="mono"><strong>${r.label}</strong></td>
            <td>Corredor Cabo / PE-60 / Complexo Suape (Consulta Ao Vivo @ ${data.queried_at})</td>
            <td>Agência a=202 (Grande Recife)</td>
            <td><span class="tag tag-crimson">HTTP ${r.http_status} · activeVehicles: ${r.active_vehicles} (${r.latency_ms}ms · ${r.payload_bytes}B)</span></td>
          </tr>
        `).join("");
      } catch (err) {
        console.warn("Fleet scan err:", err);
      }
    }

    // INITIALIZATION
    initQuickStopButtons();
    selectStopNode(11);
    selectImuScenario("ALIGHTING", document.querySelector(".sc-item"));
    populateCittamobiTables();
    updateCostSimulator(50000);
    const params = new URLSearchParams(window.location.search);
    const modParam = params.get("mod");
    if (modParam && document.getElementById(modParam)) {
      const idxMap = { "mod-gis": 0, "mod-imu": 1, "mod-citta": 2, "mod-bench": 3 };
      switchModule(modParam, document.querySelectorAll(".nav-btn")[idxMap[modParam] || 0]);
    }
    requestAnimationFrame(drawPe60GisCanvas);
    requestAnimationFrame(renderImuOscilloscope);
  </script>
</body>
</html>
"""

final_html = HTML_TEMPLATE.replace("__TELEMETRIA_JSON__", TELEMETRIA_JSON_STR)
with open(OUT_HTML, "w", encoding="utf-8") as f:
    f.write(final_html)

print(f"[OK] Protótipo SICOE/CTM v4.5 gerado em {OUT_HTML} ({OUT_HTML.stat().st_size:,} bytes)")
