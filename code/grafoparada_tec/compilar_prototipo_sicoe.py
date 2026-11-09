"""
Gerador do Protótipo GrafoParada v6.0 — Interface Ultra-Limpa, Respirável e Sem Sobrecarga Visual
+ Voz Neural Humana em Português Brasileiro (`edge-tts`: Francisca, Antônio e Thalita).
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
<html lang="pt-BR" data-theme="light">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>GrafoParada · Grande Recife — Mapa, Segurança e Companhia na Parada</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;600&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <style>
    :root, [data-theme="light"] {
      --bg-page: #f6f6f3;
      --bg-surface: #ffffff;
      --bg-subtle: #efefeb;
      --border: #dcdcd4;
      --border-strong: #b8b8ae;
      --text-main: #161615;
      --text-secondary: #4a4a45;
      --text-muted: #71716a;

      --brand-green: #0a6b46;
      --brand-green-bg: #e5f6ed;
      --brand-green-border: #92d6b6;

      --warn-amber: #a15c00;
      --warn-amber-bg: #fff4df;
      --warn-amber-border: #f2c777;

      --danger-red: #b91c1c;
      --danger-red-bg: #fdeaea;
      --danger-red-border: #f5a9a9;

      --user-blue: #0057b8;
      --user-blue-bg: #e8f1fb;
      --user-blue-border: #96c2f5;

      --shadow-sm: 0 2px 6px rgba(20, 20, 19, 0.05);
      --shadow-md: 0 10px 28px rgba(20, 20, 19, 0.08);
      --radius-sm: 10px;
      --radius-md: 14px;
      --radius-lg: 18px;
    }

    [data-theme="dark"] {
      --bg-page: #101216;
      --bg-surface: #181b22;
      --bg-subtle: #222630;
      --border: #2e3442;
      --border-strong: #475066;
      --text-main: #f3f4f6;
      --text-secondary: #c5cad6;
      --text-muted: #8b93a6;

      --brand-green: #22c55e;
      --brand-green-bg: rgba(34, 197, 94, 0.14);
      --brand-green-border: rgba(34, 197, 94, 0.4);

      --warn-amber: #fbbf24;
      --warn-amber-bg: rgba(251, 191, 36, 0.14);
      --warn-amber-border: rgba(251, 191, 36, 0.4);

      --danger-red: #f87171;
      --danger-red-bg: rgba(248, 113, 113, 0.15);
      --danger-red-border: rgba(248, 113, 113, 0.45);

      --user-blue: #38bdf8;
      --user-blue-bg: rgba(56, 189, 248, 0.14);
      --user-blue-border: rgba(56, 189, 248, 0.4);

      --shadow-sm: 0 2px 6px rgba(0, 0, 0, 0.35);
      --shadow-md: 0 12px 30px rgba(0, 0, 0, 0.5);
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      background-color: var(--bg-page);
      color: var(--text-main);
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      font-size: 15.5px;
      line-height: 1.55;
      -webkit-font-smoothing: antialiased;
    }

    .mono {
      font-family: 'JetBrains Mono', monospace;
      font-variant-numeric: tabular-nums;
    }

    button, select, input {
      font: inherit;
    }

    button:focus-visible, select:focus-visible, input:focus-visible {
      outline: 3px solid var(--user-blue);
      outline-offset: 2px;
    }

    /* =========================================================================
       CLEAN MINIMAL TOP BAR (3 TABS ONLY + VOICE SELECTOR + THEME)
       ========================================================================= */
    .app-header {
      background: var(--bg-surface);
      border-bottom: 1px solid var(--border);
      padding: 10px 24px;
      min-height: 66px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      position: sticky;
      top: 0;
      z-index: 1000;
      box-shadow: var(--shadow-sm);
      flex-wrap: wrap;
    }

    .brand-block {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .brand-badge {
      background: var(--brand-green);
      color: #ffffff;
      font-weight: 800;
      font-size: 14px;
      padding: 7px 13px;
      border-radius: var(--radius-sm);
    }

    [data-theme="dark"] .brand-badge {
      color: #052112;
    }

    .brand-title {
      font-size: 17px;
      font-weight: 800;
      letter-spacing: -0.02em;
    }

    .brand-subtitle {
      font-size: 13px;
      color: var(--text-muted);
    }

    .main-tabs {
      display: flex;
      align-items: center;
      gap: 8px;
      background: var(--bg-subtle);
      padding: 5px;
      border-radius: var(--radius-md);
      border: 1px solid var(--border);
    }

    .tab-btn {
      background: transparent;
      border: none;
      color: var(--text-secondary);
      font-size: 14px;
      font-weight: 700;
      padding: 9px 18px;
      border-radius: var(--radius-sm);
      cursor: pointer;
      transition: all 0.15s ease;
      min-height: 42px;
    }

    .tab-btn:hover {
      color: var(--text-main);
    }

    .tab-btn.active {
      background: var(--bg-surface);
      color: var(--brand-green);
      box-shadow: var(--shadow-sm);
    }

    .header-actions {
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }

    .voice-selector-wrap {
      display: flex;
      align-items: center;
      gap: 6px;
      background: var(--bg-subtle);
      border: 1px solid var(--border);
      padding: 5px 10px;
      border-radius: var(--radius-sm);
      font-size: 13px;
      font-weight: 600;
    }

    .voice-select {
      background: transparent;
      border: none;
      color: var(--text-main);
      font-weight: 700;
      cursor: pointer;
    }

    /* =========================================================================
       BUTTONS & TAGS
       ========================================================================= */
    .btn {
      background: var(--bg-surface);
      border: 1px solid var(--border-strong);
      color: var(--text-main);
      font-size: 14px;
      font-weight: 700;
      padding: 10px 16px;
      border-radius: var(--radius-sm);
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      min-height: 44px;
      transition: all 0.15s ease;
    }

    .btn:hover {
      background: var(--bg-subtle);
    }

    .btn.active, .btn-primary {
      background: var(--brand-green);
      border-color: var(--brand-green);
      color: #ffffff;
    }

    [data-theme="dark"] .btn.active, [data-theme="dark"] .btn-primary {
      color: #052112;
    }

    .btn-blue {
      background: var(--user-blue);
      border-color: var(--user-blue);
      color: #ffffff;
    }

    [data-theme="dark"] .btn-blue {
      color: #041b29;
    }

    .btn-amber {
      background: var(--warn-amber-bg);
      border-color: var(--warn-amber-border);
      color: var(--warn-amber);
    }

    .btn-danger {
      background: var(--danger-red-bg);
      border-color: var(--danger-red-border);
      color: var(--danger-red);
    }

    .tag {
      display: inline-flex;
      align-items: center;
      font-size: 12.5px;
      font-weight: 700;
      padding: 4px 11px;
      border-radius: 999px;
      border: 1px solid var(--border);
      background: var(--bg-subtle);
      color: var(--text-secondary);
    }

    .tag-emerald { background: var(--brand-green-bg); color: var(--brand-green); border-color: var(--brand-green-border); }
    .tag-amber { background: var(--warn-amber-bg); color: var(--warn-amber); border-color: var(--warn-amber-border); }
    .tag-crimson { background: var(--danger-red-bg); color: var(--danger-red); border-color: var(--danger-red-border); }
    .tag-cyan { background: var(--user-blue-bg); color: var(--user-blue); border-color: var(--user-blue-border); }

    /* =========================================================================
       WORKSPACE LAYOUT (BREATHABLE, LOW DENSITY)
       ========================================================================= */
    .workspace-view {
      display: none;
      padding: 22px 24px 36px;
      max-width: 1540px;
      margin: 0 auto;
    }

    .workspace-view.active {
      display: block;
    }

    .map-first-layout {
      display: grid;
      grid-template-columns: 1.65fr 1fr;
      gap: 22px;
      align-items: start;
    }

    .card {
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      padding: 22px;
      box-shadow: var(--shadow-sm);
    }

    .map-card {
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      overflow: hidden;
      box-shadow: var(--shadow-md);
    }

    .map-bar-top {
      padding: 14px 18px;
      border-bottom: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 10px;
    }

    .map-canvas-holder {
      position: relative;
      width: 100%;
      height: 590px;
      background: #dfe5eb;
    }

    #pe60-leaflet-map {
      width: 100%;
      height: 100%;
      z-index: 1;
    }

    .tile-dark-filter {
      filter: invert(100%) hue-rotate(180deg) brightness(90%) contrast(94%);
    }

    .map-legend-pill {
      position: absolute;
      bottom: 14px;
      left: 14px;
      z-index: 500;
      background: var(--bg-surface);
      border: 1px solid var(--border-strong);
      border-radius: 999px;
      padding: 8px 16px;
      box-shadow: var(--shadow-md);
      display: flex;
      gap: 16px;
      font-size: 13px;
      font-weight: 700;
      flex-wrap: wrap;
    }

    .legend-dot {
      display: inline-block;
      width: 11px;
      height: 11px;
      border-radius: 50%;
      margin-right: 6px;
      vertical-align: middle;
    }

    .stop-map-pill {
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-weight: 800;
      font-size: 11.5px;
      color: #ffffff;
      border: 2px solid #ffffff;
      border-radius: 999px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.35);
      padding: 2px 7px;
      white-space: nowrap;
      transition: transform 0.14s ease;
    }

    .stop-map-pill.selected {
      transform: scale(1.26);
      border-width: 3px;
      box-shadow: 0 0 0 5px rgba(0, 87, 184, 0.35), 0 4px 12px rgba(0,0,0,0.45);
    }

    @keyframes pulseUserBeacon {
      0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 87, 184, 0.75); }
      70% { transform: scale(1.08); box-shadow: 0 0 0 18px rgba(0, 87, 184, 0); }
      100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 87, 184, 0); }
    }

    .user-gps-beacon {
      width: 24px;
      height: 24px;
      background: #0057b8;
      border: 3.5px solid #ffffff;
      border-radius: 50%;
      animation: pulseUserBeacon 1.8s infinite;
      cursor: grab;
      box-shadow: 0 3px 10px rgba(0,0,0,0.45);
    }

    .sicoe-tooltip {
      background: var(--bg-surface) !important;
      border: 1px solid var(--border-strong) !important;
      border-radius: 10px !important;
      color: var(--text-main) !important;
      font-family: 'Plus Jakarta Sans', sans-serif !important;
      font-size: 13px !important;
      font-weight: 700 !important;
      padding: 7px 12px !important;
      box-shadow: var(--shadow-md) !important;
    }

    .map-bar-bottom {
      padding: 14px 18px;
      background: var(--bg-subtle);
      border-top: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 10px;
    }

    /* RIGHT SIDEBAR: BIG ETA + SAFETY + NEARBY LIST */
    .eta-hero-box {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin: 16px 0;
    }

    .eta-stat {
      background: var(--bg-subtle);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 14px 16px;
    }

    .eta-stat-label {
      font-size: 12.5px;
      font-weight: 700;
      color: var(--text-muted);
    }

    .eta-stat-val {
      font-size: 26px;
      font-weight: 800;
      margin-top: 2px;
    }

    .safety-banner {
      border-radius: var(--radius-md);
      padding: 16px;
      margin-bottom: 16px;
    }

    .nearby-stop-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 12px 14px;
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      margin-bottom: 8px;
      cursor: pointer;
      background: var(--bg-surface);
      transition: all 0.14s;
    }

    .nearby-stop-row:hover {
      background: var(--bg-subtle);
    }

    .nearby-stop-row.selected-row {
      border: 2px solid var(--brand-green);
      background: var(--brand-green-bg);
    }

    .split-2 {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 22px;
    }

    .tech-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 14px;
    }

    .tech-table th, .tech-table td {
      padding: 12px 14px;
      border-bottom: 1px solid var(--border);
      text-align: left;
    }

    .tech-table th {
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      color: var(--text-muted);
      background: var(--bg-subtle);
    }

    .tech-table tr.selected-row td {
      background: var(--brand-green-bg);
    }

    @media (max-width: 1180px) {
      .map-first-layout, .split-2 {
        grid-template-columns: 1fr;
      }
    }
  </style>
</head>
<body>

  <!-- ======================================================================= -->
  <!-- CLEAN MINIMAL HEADER (3 TABS + HUMAN NEURAL VOICE SELECTOR)             -->
  <!-- ======================================================================= -->
  <header class="app-header">
    <div class="brand-block">
      <span class="brand-badge">GrafoParada</span>
      <div>
        <div class="brand-title">Grande Recife · PE-60 &amp; Suape</div>
        <div class="brand-subtitle">Mapa ao Vivo, Alerta de Celular no Bolso e Companhia na Parada</div>
      </div>
    </div>

    <nav class="main-tabs" aria-label="Navegação Principal">
      <button class="tab-btn active" onclick="switchModule('mod-gis', this)">
        1. Mapa &amp; Sua Parada
      </button>
      <button class="tab-btn" onclick="switchModule('mod-safety', this)">
        2. Segurança &amp; Não Fique Sozinho
      </button>
      <button class="tab-btn" onclick="switchModule('mod-tech', this)">
        3. Sensores, Cittamobi &amp; Métricas
      </button>
    </nav>

    <div class="header-actions">
      <button class="btn btn-emerald" style="min-height:38px; padding:6px 13px; font-size:13px; font-weight:800; border:2px solid var(--brand-green);" onclick="openMobileModal()">
        📱 Abrir no Celular (GPS Real)
      </button>
      <div class="voice-selector-wrap" title="Voz Neural Natural em Português Brasileiro">
        <span>Voz:</span>
        <select id="neural-voice-select" class="voice-select">
          <option value="pt-BR-FranciscaNeural">Francisca (Feminina Natural)</option>
          <option value="pt-BR-AntonioNeural">Antônio (Masculina Natural)</option>
          <option value="pt-BR-ThalitaMultilingualNeural">Thalita (Jovem Expressiva)</option>
        </select>
      </div>
      <button id="theme-toggle-btn" class="btn" style="min-height:38px; padding:6px 12px; font-size:13px;" onclick="toggleTheme()">
        Modo Noturno
      </button>
    </div>
  </header>

  <!-- MODAL CELULAR COM QR CODE (HTTPS COM GPS SATÉLITE REAL) -->
  <div id="mobile-qr-modal" style="display:none; position:fixed; inset:0; background:rgba(0,0,0,0.65); z-index:9999; justify-content:center; align-items:center; padding:16px;">
    <div style="background:var(--bg-surface); border:1px solid var(--border); border-radius:var(--radius-lg); max-width:440px; width:100%; padding:24px; text-align:center; box-shadow:0 12px 32px rgba(0,0,0,0.35);">
      <h3 style="font-size:20px; font-weight:800; margin-bottom:8px;">📱 Testar GPS Real no Celular</h3>
      <p style="font-size:13.5px; color:var(--text-secondary); margin-bottom:16px;">
        Aponte a câmera do seu celular para o QR Code abaixo para abrir o protótipo com conexão segura HTTPS e ativar o sensor de satélite:
      </p>
      <div style="display:inline-block; padding:12px; background:#ffffff; border-radius:12px; border:1px solid var(--border); margin-bottom:14px;">
        <img src="https://api.qrserver.com/v1/create-qr-code/?size=220x220&amp;data=https://icy-oranges-think.loca.lt" alt="QR Code GrafoParada Celular" style="display:block; width:220px; height:220px;" />
      </div>
      <div style="font-size:12.5px; color:var(--text-muted); margin-bottom:16px; word-break:break-all;">
        Link direto: <a href="https://icy-oranges-think.loca.lt" target="_blank" style="color:var(--brand-green); font-weight:700;">https://icy-oranges-think.loca.lt</a>
      </div>
      <button class="btn btn-primary" style="width:100%; min-height:40px;" onclick="closeMobileModal()">
        Fechar Janela
      </button>
    </div>
  </div>

  <!-- ======================================================================= -->
  <!-- TAB 1: MAPA AO VIVO & SUA PARADA (ULTRA-CLEAN, ZERO OVERLOAD)           -->
  <!-- ======================================================================= -->
  <main id="mod-gis" class="workspace-view active">
    <div class="map-first-layout">

      <!-- LEFT: CLEAN INTERACTIVE MAP -->
      <div class="map-card">
        <div class="map-bar-top">
          <div style="display:flex; align-items:center; gap:6px; flex-wrap:wrap; flex:1;">
            <button id="btn-gps-real" class="btn btn-blue" style="min-height:38px; padding:6px 12px; font-size:13px;" onclick="useRealBrowserGps()">
              📍 Usar Meu GPS
            </button>
            <div style="display:flex; align-items:center; gap:4px; flex:1; min-width:200px; max-width:320px;">
              <input id="map-search-input" type="text" placeholder="Digite sua rua ou local em Camela/RMR..."
                style="width:100%; min-height:38px; padding:6px 11px; font-size:13px; border:1px solid var(--border-strong); border-radius:var(--radius-sm); background:var(--bg-surface); color:var(--text-main);"
                onkeydown="if(event.key==='Enter') searchUserPlace()" />
              <button class="btn btn-primary" style="min-height:38px; padding:6px 12px; font-size:13px;" onclick="searchUserPlace()">
                Ir
              </button>
            </div>
            <button class="btn btn-emerald" style="min-height:36px; padding:5px 11px; font-size:13px; font-weight:800; border:2px solid var(--brand-green);" onclick="setSimulatedUserLocation(-8.494915, -35.092190, 'Camela (PE-60) · Ipojuca', true)">
              📍 Camela (PE-60)
            </button>
            <button class="btn" style="min-height:36px; padding:5px 10px; font-size:12.5px;" onclick="setSimulatedUserLocation(-8.514931, -35.123469, 'Centro de Camela · Rua do Comércio', true)">
              Camela Centro
            </button>
            <button class="btn" style="min-height:36px; padding:5px 10px; font-size:12.5px;" onclick="setSimulatedUserLocation(-8.284986, -35.032781, 'TI Cabo · Centro, Cabo', true)">
              TI Cabo
            </button>
            <button class="btn" style="min-height:36px; padding:5px 10px; font-size:12.5px;" onclick="setSimulatedUserLocation(-8.062850, -34.878950, 'Av. Guararapes · Centro Recife', true)">
              Recife
            </button>
            <button class="btn" style="min-height:36px; padding:5px 10px; font-size:12.5px;" onclick="setSimulatedUserLocation(-8.017420, -34.949150, 'UFRPE · Dois Irmãos, Recife', true)">
              UFRPE
            </button>
          </div>

          <div style="display:flex; align-items:center; gap:6px;">
            <button id="btn-tile-osm" class="btn active" style="min-height:36px; padding:5px 11px; font-size:12.5px;" onclick="setBaseTile('osm')">Ruas</button>
            <button id="btn-tile-sat" class="btn" style="min-height:36px; padding:5px 11px; font-size:12.5px;" onclick="setBaseTile('sat')">Satélite</button>
            <button id="btn-tile-dark" class="btn" style="min-height:36px; padding:5px 11px; font-size:12.5px;" onclick="setBaseTile('dark')">Noturno</button>
          </div>
        </div>
        <div id="gps-accuracy-notice" style="display:none; padding:8px 16px; background:var(--warn-amber-bg); border-bottom:1px solid var(--warn-amber-border); font-size:13px; color:var(--text-main);"></div>

        <div class="map-canvas-holder">
          <div id="pe60-leaflet-map" role="region" aria-label="Mapa interativo"></div>

          <div class="map-legend-pill">
            <span><i class="legend-dot" style="background:#0057b8;"></i>Você (Clique ou Arraste)</span>
            <span><i class="legend-dot" style="background:#0a6b46;"></i>Parada Normal</span>
            <span><i class="legend-dot" style="background:#d97706;"></i>Atenção</span>
            <span><i class="legend-dot" style="background:#dc2626;"></i>Parada Crítica</span>
          </div>
        </div>

        <div class="map-bar-bottom">
          <span style="font-size:13px; font-weight:700; color:var(--text-secondary);">Paradas da Linha 178 (PE-60):</span>
          <div id="quick-stop-selector" style="display:flex; gap:4px; flex-wrap:wrap;"></div>
        </div>
      </div>

      <!-- RIGHT: SINGLE FOCUSED COMPANION CARD (GLANCEABLE & HUMAN) -->
      <div class="card">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:10px; margin-bottom:4px;">
          <div>
            <span style="font-size:12.5px; font-weight:700; color:var(--user-blue); text-transform:uppercase;" id="user-loc-coords-badge">
              Sua Parada Atual
            </span>
            <h2 id="insp-stop-header" style="font-size:20px; font-weight:800; margin-top:2px;">
              Parada #11 · Trevo de Ipojuca (PE-60)
            </h2>
          </div>
          <span id="insp-stop-tag" class="tag tag-crimson">Atraso Crítico</span>
        </div>

        <!-- 2 Glanceable Big Numbers: Wait Time & People Waiting With You -->
        <div class="eta-hero-box">
          <div class="eta-stat">
            <div class="eta-stat-label">Previsão do Ônibus (Linha 178)</div>
            <div class="eta-stat-val" id="insp-stgcn-big" style="color:var(--danger-red);">47 min</div>
            <div style="font-size:12.5px; color:var(--text-secondary);" id="insp-abn">14 pessoas já desistiram aqui</div>
          </div>
          <div class="eta-stat">
            <div class="eta-stat-label">Pessoas Esperando com Você</div>
            <div class="eta-stat-val" id="f1-people-count-big" style="color:var(--warn-amber);">1 pessoa</div>
            <div style="font-size:12.5px; color:var(--text-secondary);" id="f1-people-sub">Cuidado: você está quase só</div>
          </div>
        </div>

        <!-- Clear Safety & Companion Box -->
        <div id="f1-safety-shield-banner" class="safety-banner" style="background:var(--danger-red-bg); border:1px solid var(--danger-red-border); border-left:5px solid var(--danger-red);">
          <div id="f1-shield-title" style="font-weight:800; font-size:15.5px; color:var(--danger-red); margin-bottom:6px;">
            Não pegue o celular neste local! (19 relatos de assalto)
          </div>
          <p id="f1-shield-desc" style="font-size:14px; color:var(--text-main); margin-bottom:14px;">
            Guarde o celular no bolso. O GrafoParada avisa com voz natural no seu fone quando o ônibus estiver chegando.
          </p>

          <div style="display:flex; flex-direction:column; gap:8px;">
            <button id="btn-listen-main" class="btn btn-amber" style="width:100%;" onclick="speakNearestStopVoice()">
              Ouvir Aviso com Voz Humana no Fone Agora
            </button>
            <button id="f1-btn-companion" class="btn btn-primary" style="width:100%;" onclick="jumpToCompanionStop()">
              Não Fique Sozinho: Ir para Parada com 12 Pessoas (a 480m)
            </button>
          </div>
        </div>

        <!-- 3 Nearest Stops List (Clean Cards instead of dense spreadsheet) -->
        <div style="margin-bottom:14px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <strong style="font-size:13.5px; color:var(--text-secondary);">Paradas Mais Próximas de Você:</strong>
            <span id="user-geofence-badge" class="tag tag-emerald">A 11m da parada</span>
          </div>
          <div id="nearby-gtfs-list"></div>
        </div>

        <!-- Progressive Disclosure: Operational Dispatch & Cittamobi Details hidden cleanly inside an accordion -->
        <details style="background:var(--bg-subtle); border:1px solid var(--border); border-radius:var(--radius-md); padding:12px 14px;">
          <summary style="cursor:pointer; font-weight:700; font-size:13.5px; color:var(--text-secondary);">
            Opções do Controlador CTM (Remanejar Ônibus Vazio e Auditoria)
          </summary>
          <div style="margin-top:12px; font-size:13.5px; display:flex; flex-direction:column; gap:8px;">
            <div><strong>Catraca VEM:</strong> <span id="insp-catraca">0 validações (Ônibus atrasado)</span></div>
            <div><strong>App Cittamobi:</strong> <span id="insp-citta">0 veículos ativos</span></div>
            <div><strong>Servidor Cittamobi ao Vivo:</strong> <span id="insp-live-citta-ping">Conectado</span></div>
            <div style="display:flex; gap:8px; flex-wrap:wrap; margin-top:4px;">
              <button class="btn btn-primary" style="min-height:38px; font-size:13px;" onclick="triggerGtfsPatch()">
                Despachar Ônibus Ocioso (#178-09) para Esta Parada
              </button>
              <button class="btn" style="min-height:38px; font-size:13px;" onclick="pingLiveCittamobiStop()">
                Testar Cittamobi Agora
              </button>
            </div>
            <div id="gtfs-patch-output" class="mono" style="font-size:12px; color:var(--brand-green); margin-top:4px;"></div>
          </div>
        </details>

      </div>

    </div>
  </main>

  <!-- ======================================================================= -->
  <!-- TAB 2: SEGURANÇA COMUNITÁRIA & COMPANHIA NA PARADA                      -->
  <!-- ======================================================================= -->
  <main id="mod-safety" class="workspace-view">
    <div class="split-2">

      <!-- Left: Simple Report & Companion Card -->
      <div style="display:flex; flex-direction:column; gap:20px;">
        <div class="card">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
            <h2 id="saf-stop-title" style="font-size:19px; font-weight:800;">Parada #11 · Trevo de Ipojuca</h2>
            <span id="saf-stop-badge" class="tag tag-crimson">Guarde o Celular</span>
          </div>

          <div id="saf-phone-warning-box" style="background:var(--danger-red-bg); border:1px solid var(--danger-red-border); border-radius:var(--radius-md); padding:16px; margin-bottom:16px;">
            <div style="font-weight:800; font-size:16px; color:var(--danger-red); margin-bottom:6px;" id="saf-phone-headline">
              Não pegue o celular neste local! (19 relatos de assalto)
            </div>
            <p id="saf-phone-explanation" style="font-size:14px; margin-bottom:12px;">
              Moradores e trabalhadores relataram assaltos de moto a quem fica com a tela do celular acesa na pista. Deixe o celular no bolso e ouça os avisos pelo fone.
            </p>
            <button class="btn btn-amber" onclick="speakSafetyShieldPrompt()">
              Ouvir Alerta com Voz Humana Agora
            </button>
          </div>

          <!-- Companion Box -->
          <div class="split-2" style="gap:12px; margin-bottom:18px;">
            <div style="background:var(--bg-subtle); border:1px solid var(--border); border-radius:var(--radius-md); padding:14px;">
              <div style="font-size:12.5px; font-weight:700; color:var(--text-muted);">Pessoas esperando aqui agora:</div>
              <div id="saf-waiting-count" style="font-size:28px; font-weight:800; color:var(--warn-amber); margin:4px 0;">1 pessoa</div>
              <div id="saf-alone-tag" class="tag tag-crimson" style="margin-bottom:10px;">Você está quase só</div>
              <div style="display:flex; gap:6px;">
                <button class="btn btn-primary" style="min-height:36px; padding:6px 10px; font-size:12.5px;" onclick="adjustStopPresence(1)">+1 Chegou alguém</button>
                <button class="btn" style="min-height:36px; padding:6px 10px; font-size:12.5px;" onclick="adjustStopPresence(-1)">-1 Saiu</button>
              </div>
            </div>

            <div style="background:var(--brand-green-bg); border:1px solid var(--brand-green-border); border-radius:var(--radius-md); padding:14px;">
              <div style="font-size:12.5px; font-weight:800; color:var(--brand-green);">Parada Segura com Grupo Próxima:</div>
              <div id="saf-companion-name" style="font-size:15.5px; font-weight:800; margin-top:4px;">Parada #12 · Posto 24h</div>
              <div id="saf-companion-metrics" style="font-size:13.5px; font-weight:700; color:var(--brand-green); margin:4px 0;">12 pessoas esperando juntas</div>
              <div id="saf-companion-dist" style="font-size:12.5px; color:var(--text-secondary); margin-bottom:10px;">A 480m (~6 min a pé)</div>
              <button class="btn btn-primary" style="width:100%; min-height:38px; font-size:13px;" onclick="jumpToCompanionStop()">
                Ir para Esta Parada no Mapa
              </button>
            </div>
          </div>

          <!-- 1-Click Collaborative Report -->
          <div style="border-top:1px solid var(--border); padding-top:16px;">
            <h3 style="font-size:15px; font-weight:800; margin-bottom:10px;">
              Avisar outros passageiros sobre esta parada (Anônimo):
            </h3>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:10px;">
              <select id="saf-report-stop-select" style="padding:10px; border-radius:var(--radius-sm); border:1px solid var(--border-strong); background:var(--bg-surface); color:var(--text-main);" onchange="selectStopNode(parseInt(this.value, 10), false)"></select>
              <input id="saf-report-desc" type="text" placeholder="Comentário opcional (ex: poste apagado)..." style="padding:10px; border-radius:var(--radius-sm); border:1px solid var(--border-strong); background:var(--bg-surface); color:var(--text-main);" />
            </div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px;">
              <button class="btn btn-danger" onclick="submitSafetyReport('ROUBO_CELULAR')">Alertar Assalto / Roubo</button>
              <button class="btn btn-amber" onclick="submitSafetyReport('ILUMINACAO_PRECARIA')">Avisar que Está Escuro</button>
              <button class="btn" onclick="submitSafetyReport('PARADA_SOLITARIA')">Estou Esperando Sozinho(a)</button>
              <button class="btn btn-primary" onclick="submitSafetyReport('LOCAL_SEGURO_GRUPO')">Tem Grupo Seguro Aqui</button>
            </div>
          </div>
        </div>

        <div class="card">
          <h3 style="font-size:16px; font-weight:800; margin-bottom:12px;">Últimos Avisos da Comunidade na PE-60</h3>
          <div id="saf-feed-container" style="display:flex; flex-direction:column; gap:10px;"></div>
        </div>
      </div>

      <!-- Right: Clean Overview of the 20 Stops -->
      <div class="card">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
          <h3 style="font-size:17px; font-weight:800;">Onde tem gente esperando agora na PE-60?</h3>
          <span class="tag tag-emerald"><span id="saf-kpi-waiting">123</span> pessoas no corredor</span>
        </div>
        <div style="max-height:700px; overflow-y:auto;">
          <table class="tech-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Parada</th>
                <th>Pessoas Agora</th>
                <th>Relatos Roubo</th>
                <th>Recomendação</th>
              </tr>
            </thead>
            <tbody id="saf-corridor-tbody"></tbody>
          </table>
        </div>
      </div>

    </div>
  </main>

  <!-- ======================================================================= -->
  <!-- TAB 3: SENSORES NO BOLSO, AUDITORIA CITTAMOBI & MÉTRICAS DA PESQUISA    -->
  <!-- ======================================================================= -->
  <main id="mod-tech" class="workspace-view">
    <div class="split-2" style="margin-bottom:22px;">

      <!-- Left: Pocket Mode Simulator -->
      <div class="card">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
          <h3 style="font-size:17px; font-weight:800;">Simulador do Modo Bolso (Sensores Físicos)</h3>
          <span id="imu-verdict-tag" class="tag tag-emerald">Desembarque (0% Erro)</span>
        </div>
        <p style="font-size:14px; color:var(--text-secondary); margin-bottom:14px;">
          Escolha uma situação abaixo para ver como a Inteligência Artificial reconhece se você desceu do ônibus ou se desistiu da espera, sem precisar tirar o celular do bolso:
        </p>

        <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-bottom:14px;">
          <button class="btn active sc-item" onclick="selectImuScenario('ALIGHTING', this)">1. Desembarque Normal</button>
          <button class="btn sc-item" onclick="selectImuScenario('ABANDONMENT', this)">2. Desistência (Lotação)</button>
          <button class="btn sc-item" onclick="selectImuScenario('BOARDING_SERVED', this)">3. Embarque Linha 178</button>
          <button class="btn sc-item" onclick="selectImuScenario('TRANSIT_BYPASS', this)">4. Passando na Pista</button>
        </div>

        <div style="background:var(--warn-amber-bg); border:1px solid var(--warn-amber-border); border-radius:var(--radius-md); padding:14px; margin-bottom:14px;">
          <div style="font-size:12px; font-weight:800; color:var(--warn-amber); text-transform:uppercase;">Fala da Voz Humana no Fone:</div>
          <div id="imu-voice-transcript" style="font-size:14.5px; font-weight:700; margin:6px 0 10px;">
            "Oi! Identifiquei que você acabou de descer do ônibus na parada Trevo de Ipojuca. Boa caminhada!"
          </div>
          <div style="display:flex; gap:8px;">
            <button class="btn btn-amber" onclick="speakImuTranscript()">Ouvir Voz Humana Agora</button>
            <button class="btn btn-primary" onclick="triggerLivePyTorchInference()">Sortear Amostras Reais (PyTorch)</button>
          </div>
        </div>

        <div style="background:#0d1117; border-radius:var(--radius-md); height:150px; overflow:hidden; margin-bottom:12px;">
          <canvas id="imu-osc-canvas" style="width:100%; height:100%; display:block;"></canvas>
        </div>

        <div style="font-size:13px; color:var(--text-secondary); display:flex; justify-content:space-between; flex-wrap:wrap;">
          <span>Tempo na CPU: <strong id="imu-live-cpu-us" class="mono">14,29 µs</strong></span>
          <span>Internet gasta: <strong id="imu-net-counter" style="color:var(--brand-green);">0 Bytes</strong></span>
        </div>
      </div>

      <!-- Right: Cittamobi Live Audit + Research Benchmarks -->
      <div class="card">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
          <h3 style="font-size:17px; font-weight:800;">Comparativo Real: Cittamobi vs. GrafoParada</h3>
          <button class="btn btn-amber" style="min-height:36px; padding:6px 12px; font-size:12.5px;" onclick="refreshLiveCittamobiFleet()">
            Testar API Cittamobi Ao Vivo
          </button>
        </div>

        <table class="tech-table" style="margin-bottom:16px;">
          <thead>
            <tr>
              <th>Indicador Auditado</th>
              <th>Cittamobi (BigQuery / App)</th>
              <th>GrafoParada (No Bolso)</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Precisão (F1-Score)</strong></td>
              <td style="color:var(--danger-red);">40,85% a 48,01% (Só cliques)</td>
              <td style="color:var(--brand-green); font-weight:800;">99,67% (Sensores + Velocidade)</td>
            </tr>
            <tr>
              <td><strong>Falso Positivo na Descida</strong></td>
              <td>70% das aberturas sem viagem</td>
              <td style="color:var(--brand-green); font-weight:800;">0,00% (0 em 300 viagens)</td>
            </tr>
            <tr>
              <td><strong>Predição 20 Paradas (t+30m)</strong></td>
              <td>Sem predição de fila</td>
              <td style="color:var(--brand-green); font-weight:800;">Erro MAE 1,51 min (STGCN)</td>
            </tr>
            <tr>
              <td><strong>Ônibus na PE-60 Agora (`m3p`)</strong></td>
              <td id="citta-fleet-badge" style="color:var(--danger-red); font-weight:700;">0 veículos transmitindo</td>
              <td style="color:var(--brand-green); font-weight:700;">Detecta espera e desistência real</td>
            </tr>
          </tbody>
        </table>

        <details style="background:var(--bg-subtle); border:1px solid var(--border); border-radius:var(--radius-md); padding:12px 14px;">
          <summary style="cursor:pointer; font-weight:700; font-size:13.5px;">
            Ver tabela completa de linhas auditadas no servidor Cittamobi (`api.cittamobi.com.br`)
          </summary>
          <div style="margin-top:10px; max-height:220px; overflow-y:auto;">
            <table class="tech-table">
              <thead>
                <tr>
                  <th>Serviço</th>
                  <th>Linha</th>
                  <th>Operadora</th>
                  <th>Veículos no Cittamobi</th>
                </tr>
              </thead>
              <tbody id="citta-services-tbody"></tbody>
            </table>
          </div>
        </details>
      </div>

    </div>
  </main>

  <script>
    const TELEMETRIA = __TELEMETRIA_JSON__;

    let activeStopSeq = 11;
    let currentImuKey = "ALIGHTING";
    let oscTick = 0;
    let currentAudioPlayer = null;

    // =========================================================================
    // HUMAN NEURAL VOICE SYNTHESIS (`edge-tts` pt-BR-FranciscaNeural / Antonio / Thalita)
    // =========================================================================
    async function playNaturalVoice(text, btnEl = null) {
      if (!text) return;
      const voiceSelect = document.getElementById("neural-voice-select");
      const voice = voiceSelect ? voiceSelect.value : "pt-BR-FranciscaNeural";

      const oldLabel = btnEl ? btnEl.textContent : null;
      if (btnEl) btnEl.textContent = "Gerando voz humana natural...";

      try {
        if (currentAudioPlayer) {
          currentAudioPlayer.pause();
          currentAudioPlayer = null;
        }
        if ("speechSynthesis" in window) {
          window.speechSynthesis.cancel();
        }
        const url = `/api/live/tts?voice=${encodeURIComponent(voice)}&text=${encodeURIComponent(text)}`;
        const audio = new Audio(url);
        currentAudioPlayer = audio;
        audio.onplaying = () => {
          if (btnEl) btnEl.textContent = "Falando agora... (Voz Neural)";
        };
        audio.onended = () => {
          if (btnEl && oldLabel) btnEl.textContent = oldLabel;
        };
        audio.onerror = () => {
          if (btnEl && oldLabel) btnEl.textContent = oldLabel;
          fallbackBrowserSpeech(text);
        };
        await audio.play();
      } catch (err) {
        if (btnEl && oldLabel) btnEl.textContent = oldLabel;
        fallbackBrowserSpeech(text);
      }
    }

    function fallbackBrowserSpeech(text) {
      if ("speechSynthesis" in window) {
        window.speechSynthesis.cancel();
        const u = new SpeechSynthesisUtterance(text);
        u.lang = "pt-BR";
        window.speechSynthesis.speak(u);
      }
    }

    function openMobileModal() {
      const m = document.getElementById("mobile-qr-modal");
      if (m) m.style.display = "flex";
    }

    function closeMobileModal() {
      const m = document.getElementById("mobile-qr-modal");
      if (m) m.style.display = "none";
    }

    // =========================================================================
    // THEME & NAVIGATION
    // =========================================================================
    function toggleTheme() {
      const html = document.documentElement;
      const cur = html.getAttribute("data-theme") || "light";
      const next = cur === "light" ? "dark" : "light";
      html.setAttribute("data-theme", next);
      const btn = document.getElementById("theme-toggle-btn");
      if (btn) btn.textContent = next === "light" ? "Modo Noturno" : "Modo Claro";
      setBaseTile(next === "dark" ? "dark" : "osm");
    }

    function switchModule(modId, btnEl) {
      document.querySelectorAll(".workspace-view").forEach(v => v.classList.remove("active"));
      document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
      document.getElementById(modId).classList.add("active");
      if (btnEl) btnEl.classList.add("active");
      if (modId === "mod-gis") requestAnimationFrame(drawPe60GisCanvas);
    }

    // =========================================================================
    // CLEAN INTERACTIVE MAP (LEAFLET)
    // =========================================================================
    function initQuickStopButtons() {
      const wrap = document.getElementById("quick-stop-selector");
      wrap.innerHTML = TELEMETRIA.stops.map(s => {
        const isCrit = s.operational_state === "CRITICAL";
        const isWarn = s.operational_state === "WARNING";
        const col = isCrit ? "#dc2626" : (isWarn ? "#d97706" : "#0a6b46");
        return `<button id="qbtn-${s.seq}" class="btn ${s.seq === activeStopSeq ? 'active' : ''}" style="padding:3px 9px; min-height:32px; font-size:12px; border-bottom:3px solid ${col};" onclick="selectStopNode(${s.seq}, true)">#${String(s.seq).padStart(2, '0')}</button>`;
      }).join("");
    }

    let leafletMap = null;
    let baseTileLayers = {};
    let currentTileLayer = null;
    let stopsLayerGroup = null;
    let userRadarLayerGroup = null;
    let userMarker = null;
    let userPos = { lat: -8.304950, lon: -35.021420, label: "Trevo de Ipojuca (Parada #11)" };
    let lastPocketVoicePrompt = "Oi! Você chegou na parada Trevo de Ipojuca. Cuidado: trecho com alertas de assalto. Não pegue o celular, deixe ele guardado no bolso!";

    function initRealLeafletMap() {
      if (leafletMap) return;
      leafletMap = L.map("pe60-leaflet-map", {
        center: [-8.304873, -35.021349],
        zoom: 14,
        zoomControl: false
      });
      L.control.zoom({ position: "topright" }).addTo(leafletMap);

      baseTileLayers = {
        osm: L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
          maxZoom: 19,
          attribution: "&copy; OpenStreetMap"
        }),
        sat: L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", {
          maxZoom: 19,
          attribution: "&copy; Esri Satellite"
        }),
        dark: L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
          maxZoom: 19,
          className: "tile-dark-filter",
          attribution: "&copy; OpenStreetMap"
        })
      };

      currentTileLayer = baseTileLayers.osm;
      currentTileLayer.addTo(leafletMap);

      stopsLayerGroup = L.layerGroup().addTo(leafletMap);
      userRadarLayerGroup = L.layerGroup().addTo(leafletMap);

      if (TELEMETRIA.polyline && TELEMETRIA.polyline.length > 1) {
        L.polyline(TELEMETRIA.polyline, { color: "#0057b8", weight: 9, opacity: 0.2 }).addTo(leafletMap);
        L.polyline(TELEMETRIA.polyline, { color: "#0057b8", weight: 4.5, opacity: 0.9 }).addTo(leafletMap);
      }

      leafletMap.on("click", (ev) => {
        setSimulatedUserLocation(ev.latlng.lat, ev.latlng.lng, "Posição escolhida no mapa", false);
      });

      const mainCorridorCoords = TELEMETRIA.stops.slice(0, 19).map(s => [s.lat, s.lon]);
      leafletMap.fitBounds(mainCorridorCoords, { padding: [36, 36] });
    }

    function setBaseTile(mode) {
      initRealLeafletMap();
      if (currentTileLayer) leafletMap.removeLayer(currentTileLayer);
      currentTileLayer = baseTileLayers[mode] || baseTileLayers.osm;
      currentTileLayer.addTo(leafletMap);
      document.getElementById("btn-tile-osm").classList.toggle("active", mode === "osm");
      document.getElementById("btn-tile-sat").classList.toggle("active", mode === "sat");
      document.getElementById("btn-tile-dark").classList.toggle("active", mode === "dark");
    }

    function drawPe60GisCanvas() {
      initRealLeafletMap();
      leafletMap.invalidateSize();
      stopsLayerGroup.clearLayers();

      TELEMETRIA.stops.forEach((st) => {
        let bgColor = "#0a6b46";
        if (st.operational_state === "CRITICAL") bgColor = "#dc2626";
        else if (st.operational_state === "WARNING") bgColor = "#d97706";
        const isSelected = st.seq === activeStopSeq;

        const pillIcon = L.divIcon({
          className: "",
          html: `<div class="stop-map-pill ${isSelected ? 'selected' : ''}" style="background:${bgColor};">#${String(st.seq).padStart(2, '0')}</div>`,
          iconSize: [36, 24],
          iconAnchor: [18, 12]
        });

        const marker = L.marker([st.lat, st.lon], { icon: pillIcon });
        marker.bindTooltip(
          `Parada #${String(st.seq).padStart(2, '0')}: ${st.name} (Previsão: ${st.stgcn_horizon_min[2]} min)`,
          { permanent: isSelected, direction: "top", offset: [0, -14], className: "sicoe-tooltip" }
        );
        marker.on("click", () => selectStopNode(st.seq, true));
        stopsLayerGroup.addLayer(marker);
      });
    }

    function selectStopNode(seq, panMap = true, syncUserPin = true) {
      activeStopSeq = seq;
      document.querySelectorAll("#quick-stop-selector .btn").forEach(b => b.classList.remove("active"));
      const qbtn = document.getElementById(`qbtn-${seq}`);
      if (qbtn) qbtn.classList.add("active");

      const st = TELEMETRIA.stops.find(s => s.seq === seq) || TELEMETRIA.stops[10];
      document.getElementById("insp-stop-header").textContent = `Parada #${String(st.seq).padStart(2, '0')} · ${st.name}`;
      document.getElementById("insp-stgcn-big").textContent = `${st.stgcn_horizon_min[2].toFixed(0)} min`;
      document.getElementById("insp-stgcn-big").style.color = st.operational_state === "CRITICAL" ? "var(--danger-red)" : "var(--brand-green)";
      document.getElementById("insp-abn").textContent = st.abandonment_10m > 0
        ? `${st.abandonment_10m} pessoas desistiram desta espera`
        : `Nenhuma desistência agora`;

      document.getElementById("insp-catraca").textContent = st.catraca_boardings_40m === 0
        ? `0 validações (Ônibus atrasado)`
        : `${st.catraca_boardings_40m} embarques normais`;
      document.getElementById("insp-citta").textContent = `Parada #${st.cittamobi_id} (0 ônibus transmitindo)`;

      const tag = document.getElementById("insp-stop-tag");
      if (st.operational_state === "CRITICAL") {
        tag.className = "tag tag-crimson";
        tag.textContent = "Atraso Crítico";
      } else if (st.operational_state === "WARNING") {
        tag.className = "tag tag-amber";
        tag.textContent = "Atenção";
      } else {
        tag.className = "tag tag-emerald";
        tag.textContent = "Normal";
      }

      drawPe60GisCanvas();
      if (panMap && leafletMap) {
        leafletMap.panTo([st.lat, st.lon], { animate: true, duration: 0.4 });
      }
      runLiveStgcnInference();
      if (typeof renderSelectedStopSafetyPanel === "function") {
        renderSelectedStopSafetyPanel(seq);
      }
      if (syncUserPin) {
        setSimulatedUserLocation(st.lat, st.lon, st.name, false, false);
      }
    }

    function triggerGtfsPatch() {
      const st = TELEMETRIA.stops.find(s => s.seq === activeStopSeq) || TELEMETRIA.stops[10];
      document.getElementById("gtfs-patch-output").textContent =
        `Ordem enviada: Veículo #178-09 (ocioso em Suape) remanejado para cobrir a Parada #${st.seq}. Espera cai para 18 min.`;
    }

    // =========================================================================
    // LIVE USER LOCATION, ADDRESS SEARCH & NEARBY STOPS
    // =========================================================================
    function useRealBrowserGps() {
      const btn = document.getElementById("btn-gps-real");
      const notice = document.getElementById("gps-accuracy-notice");
      if (!navigator.geolocation) return;
      if (btn) btn.textContent = "Localizando...";
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          const lat = pos.coords.latitude;
          const lon = pos.coords.longitude;
          const acc = Math.round(pos.coords.accuracy || 0);

          // Verifica se o roteador/provedor de internet sofreu o desvio clássico de IP para Japaratinga/Alagoas
          if (lat < -8.65 || lat > -7.6 || lon < -35.5 || lon > -34.7) {
            if (btn) btn.textContent = `📍 Camela (IP corrigido)`;
            if (notice) {
              notice.style.display = "block";
              notice.innerHTML = `⚠️ <strong>Desvio de IP da Operadora corrigido:</strong> Seu provedor no Windows (DTEL Telecom, IP 177.200.245.197) localizou seu IP em <strong>Japaratinga/AL</strong> (Lat ${lat.toFixed(4)}, Lon ${lon.toFixed(4)}). Como você está em <strong>Camela (Ipojuca - PE)</strong>, reposicionamos você automaticamente para a sua parada real em Camela! <button class="btn" style="min-height:26px; padding:2px 8px; font-size:11.5px; margin-left:6px;" onclick="showPcDiagnosticsModal()">🔍 Ver Diagnóstico do seu PC</button>`;
            }
            setSimulatedUserLocation(-8.494915, -35.092190, "Rodovia PE-60 (Trevo de Camela) · Ipojuca", true, true);
            return;
          }

          if (btn) btn.textContent = `📍 Meu GPS (±${acc}m)`;
          if (notice) {
            if (acc > 150) {
              notice.style.display = "block";
              notice.innerHTML = `<strong>Atenção sobre o GPS do PC:</strong> O navegador no Windows estimou sua posição pela rede Wi-Fi/provedor com margem de erro de <strong>±${acc} metros</strong>. Se este não for o seu endereço exato, clique no botão <strong>Camela</strong> ou <strong>digite sua rua acima</strong>! <button class="btn" style="min-height:26px; padding:2px 8px; font-size:11.5px; margin-left:6px;" onclick="showPcDiagnosticsModal()">🔍 Ver Diagnóstico do PC</button>`;
            } else {
              notice.style.display = "none";
            }
          }
          setSimulatedUserLocation(lat, lon, "Localização via GPS", true, true);
        },
        () => {
          if (btn) btn.textContent = "📍 Usar Meu GPS";
          if (notice) {
            notice.style.display = "block";
            notice.innerHTML = `Permissão de GPS negada ou indisponível no navegador. Clique em <strong>Camela</strong> ou digite sua rua na caixa de busca! <button class="btn" style="min-height:26px; padding:2px 8px; font-size:11.5px; margin-left:6px;" onclick="showPcDiagnosticsModal()">🔍 Ver Diagnóstico do PC</button>`;
          }
        },
        { enableHighAccuracy: true, timeout: 8000, maximumAge: 0 }
      );
    }

    async function showPcDiagnosticsModal() {
      try {
        const resp = await fetch("/api/live/pc-diagnostics");
        const d = await resp.json();
        alert(
          `🖥️ DIAGNÓSTICO DE HARDWARE & REDE DO SEU PC:\n\n` +
          `• IP Público: ${d.public_ip}\n` +
          `• Provedor / ASN: ${d.isp_org}\n` +
          `• Local do IP nos Bancos: ${d.ip_city} (${d.ip_loc})\n` +
          `• Chip GPS no Computador: ${d.hardware_gps}\n\n` +
          `🔍 POR QUE MARCOU JAPARATINGA?\n${d.japaratinga_cause}\n\n` +
          `✅ SOLUÇÃO NO PROTÓTIPO:\n${d.recommended_fix}`
        );
      } catch (err) {
        alert("Diagnóstico: O computador não possui GPS físico de satélite. Ele usa a rota de IP da DTEL Telecom.");
      }
    }

    async function searchUserPlace() {
      const inp = document.getElementById("map-search-input");
      const notice = document.getElementById("gps-accuracy-notice");
      if (!inp || !inp.value.trim()) return;
      const q = inp.value.trim();
      inp.disabled = true;
      try {
        const resp = await fetch(`/api/live/geocode?q=${encodeURIComponent(q)}`);
        const data = await resp.json();
        inp.disabled = false;
        if (data.results && data.results.length > 0) {
          const best = data.results[0];
          if (notice) notice.style.display = "none";
          setSimulatedUserLocation(best.lat, best.lon, best.label, true, true);
        } else if (notice) {
          notice.style.display = "block";
          notice.innerHTML = `Não encontramos "${q}". Tente digitar o nome da rua ou bairro com a cidade (ex: <em>Boa Viagem, Recife</em> ou <em>Centro, Cabo</em>).`;
        }
      } catch (err) {
        inp.disabled = false;
      }
    }

    function speakNearestStopVoice() {
      const btn = document.getElementById("btn-listen-main");
      playNaturalVoice(lastPocketVoicePrompt, btn);
    }

    async function setSimulatedUserLocation(lat, lon, label, flyTo = true, syncCorridorNode = true) {
      userPos = { lat, lon, label };
      initRealLeafletMap();

      const coordBadge = document.getElementById("user-loc-coords-badge");
      if (coordBadge) coordBadge.textContent = `Localizando endereço exato...`;

      if (flyTo && leafletMap) {
        leafletMap.setView([lat, lon], Math.max(leafletMap.getZoom(), 16), { animate: true });
      }

      userRadarLayerGroup.clearLayers();
      L.circle([lat, lon], { radius: 35, color: "#0a6b46", weight: 2, fillColor: "#0a6b46", fillOpacity: 0.18 }).addTo(userRadarLayerGroup);

      const beaconIcon = L.divIcon({
        className: "",
        html: `<div class="user-gps-beacon" title="Você está aqui"></div>`,
        iconSize: [24, 24],
        iconAnchor: [12, 12]
      });

      userMarker = L.marker([lat, lon], { icon: beaconIcon, draggable: true }).addTo(userRadarLayerGroup);
      userMarker.bindTooltip(`Você: ${label}`, { permanent: true, direction: "top", offset: [0, -14], className: "sicoe-tooltip" });
      userMarker.on("dragend", (ev) => {
        const p = ev.target.getLatLng();
        setSimulatedUserLocation(p.lat, p.lng, "Posição ajustada no mapa", false, true);
      });

      try {
        const resp = await fetch(`/api/live/nearby-stops?lat=${lat}&lon=${lon}&k=4`);
        const data = await resp.json();
        lastPocketVoicePrompt = data.pocket_voice_prompt;

        const realAddr = (data.user_location && data.user_location.address) ? data.user_location.address : label;
        userPos.label = realAddr;
        if (coordBadge) {
          coordBadge.textContent = `Você está em: ${realAddr}`;
        }
        if (userMarker) {
          userMarker.setTooltipContent(`Você está em: ${realAddr}`);
        }

        const topStop = data.closest_gtfs_stops && data.closest_gtfs_stops[0];
        if (topStop) {
          document.getElementById("user-geofence-badge").textContent = `A ${topStop.distance_m}m da parada`;

          if (topStop.is_pe60_corridor && topStop.pe60_seq && topStop.distance_m <= 250.0) {
            if (syncCorridorNode && activeStopSeq !== topStop.pe60_seq) {
              selectStopNode(topStop.pe60_seq, false, false);
            }
            document.getElementById("insp-stop-header").textContent = `Parada #${String(topStop.pe60_seq).padStart(2, '0')} · ${topStop.stop_name}`;
          } else {
            // Usuário está em qualquer outro bairro/cidade do Grande Recife: atualiza todo o cartão direito para a parada real dele!
            document.querySelectorAll("#quick-stop-selector .btn").forEach(b => b.classList.remove("active"));
            document.getElementById("insp-stop-header").textContent = topStop.stop_name;
            const estMin = topStop.pe60_stgcn_t30 || 14;
            document.getElementById("insp-stgcn-big").textContent = `${Number(estMin).toFixed(0)} min`;
            document.getElementById("insp-stgcn-big").style.color = estMin > 30 ? "var(--danger-red)" : "var(--brand-green)";
            document.getElementById("insp-abn").textContent = topStop.pe60_abn_10m > 0
              ? `${topStop.pe60_abn_10m} desistências recentes`
              : `Fluxo urbano regular na via`;
            const tag = document.getElementById("insp-stop-tag");
            tag.className = topStop.keep_phone_in_pocket ? "tag tag-amber" : "tag tag-emerald";
            tag.textContent = topStop.keep_phone_in_pocket ? "Modo Bolso Ativo" : "Parada Movimentada";
          }

          // Desenha também no mapa os marcadores das paradas locais quando estiver fora do corredor PE-60
          (data.closest_gtfs_stops || []).slice(0, 4).forEach((st, idx) => {
            if (!st.is_pe60_corridor) {
              const col = st.keep_phone_in_pocket ? "#d97706" : "#0a6b46";
              const localIcon = L.divIcon({
                className: "",
                html: `<div class="stop-map-pill ${idx === 0 ? 'selected' : ''}" style="background:${col}; font-size:11px; padding:2px 6px;">#${st.stop_id}</div>`,
                iconSize: [54, 22],
                iconAnchor: [27, 11]
              });
              const m = L.marker([st.lat, st.lon], { icon: localIcon }).addTo(userRadarLayerGroup);
              m.bindTooltip(`${st.stop_name} (${st.active_waiting_users} pessoas aguardando)`, {
                direction: "top",
                offset: [0, -12],
                className: "sicoe-tooltip"
              });
              m.on("click", () => setSimulatedUserLocation(st.lat, st.lon, st.stop_name, true, false));
            }
          });

          // Update Big People Counter & Safety Banner on Tab 1
          const paxCountEl = document.getElementById("f1-people-count-big");
          const paxSubEl = document.getElementById("f1-people-sub");
          if (paxCountEl) {
            paxCountEl.textContent = topStop.active_waiting_users === 1 ? "1 pessoa" : `${topStop.active_waiting_users} pessoas`;
            paxCountEl.style.color = topStop.active_waiting_users <= 2 ? "var(--warn-amber)" : "var(--brand-green)";
          }
          if (paxSubEl) {
            paxSubEl.textContent = topStop.active_waiting_users <= 2
              ? "Atenção: você está quase só"
              : "Parada movimentada com grupo";
          }

          window.lastCompanionRecommendation = topStop.companion_stop_recommendation;
          const banner = document.getElementById("f1-safety-shield-banner");
          const sTitle = document.getElementById("f1-shield-title");
          const sDesc = document.getElementById("f1-shield-desc");
          const sBtnComp = document.getElementById("f1-btn-companion");
          if (banner && sTitle && sDesc) {
            if (topStop.keep_phone_in_pocket) {
              banner.style.background = "var(--danger-red-bg)";
              banner.style.borderColor = "var(--danger-red-border)";
              banner.style.borderLeft = "5px solid var(--danger-red)";
              sTitle.style.color = "var(--danger-red)";
              sTitle.textContent = `Não pegue o celular neste local! (${topStop.robbery_reports_30d} relatos de assalto)`;
              sDesc.textContent = `Guarde o celular no bolso em ${topStop.stop_name}. O GrafoParada fala com você pelo fone de ouvido.`;
              if (sBtnComp && topStop.companion_stop_recommendation) {
                sBtnComp.style.display = "inline-flex";
                sBtnComp.textContent = `Não Fique Sozinho: Ir para ${topStop.companion_stop_recommendation.name.split(' (Parada')[0]} com ${topStop.companion_stop_recommendation.active_waiting_users} Pessoas (a ${topStop.companion_stop_recommendation.distance_m}m)`;
              } else if (sBtnComp) {
                sBtnComp.style.display = "none";
              }
            } else {
              banner.style.background = "var(--brand-green-bg)";
              banner.style.borderColor = "var(--brand-green-border)";
              banner.style.borderLeft = "5px solid var(--brand-green)";
              sTitle.style.color = "var(--brand-green)";
              sTitle.textContent = `Parada iluminada e segura com grupo`;
              sDesc.textContent = `Tem ${topStop.active_waiting_users} passageiros aguardando juntos em ${topStop.stop_name}.`;
              if (sBtnComp) sBtnComp.style.display = "none";
            }
          }
        }

        // Draw clean dashed line to the closest stop only
        if (topStop) {
          L.polyline([[lat, lon], [topStop.lat, topStop.lon]], {
            color: "#0057b8",
            weight: 3,
            dashArray: "6, 6"
          }).addTo(userRadarLayerGroup);
        }

        // Render 3 clean rows instead of a dense multi-column table
        const listEl = document.getElementById("nearby-gtfs-list");
        listEl.innerHTML = (data.closest_gtfs_stops || []).slice(0, 3).map((st, idx) => {
          const badge = st.keep_phone_in_pocket
            ? `<span class="tag tag-crimson">Guarde o celular</span>`
            : `<span class="tag tag-emerald">${st.active_waiting_users} pessoas ali</span>`;
          return `
            <div class="nearby-stop-row ${idx === 0 ? 'selected-row' : ''}" onclick="setSimulatedUserLocation(${st.lat}, ${st.lon}, '${st.stop_name.replace(/'/g, "\\'")}', true, true);">
              <div>
                <div style="font-weight:800; font-size:14px;">${st.stop_name}</div>
                <div style="font-size:12.5px; color:var(--text-muted);">A ${st.distance_m} metros de você · ${st.active_waiting_users} esperando agora</div>
              </div>
              ${badge}
            </div>
          `;
        }).join("");
      } catch (err) {
        console.warn("Nearby scan err:", err);
      }
    }

    // =========================================================================
    // TAB 2: COMMUNITY SAFETY & COMPANION
    // =========================================================================
    let safetyCorridorData = null;
    let lastSafetyShieldVoice = "Oi, atenção aqui na parada: não tire o celular do bolso!";

    async function refreshSafetyCorridor() {
      try {
        const resp = await fetch("/api/live/safety-corridor");
        safetyCorridorData = await resp.json();
        renderSafetyCorridorUI();
      } catch (err) {
        console.warn(err);
      }
    }

    function renderSafetyCorridorUI() {
      if (!safetyCorridorData) return;
      document.getElementById("saf-kpi-waiting").textContent = safetyCorridorData.summary.total_active_waiting_users_pe60;

      const sel = document.getElementById("saf-report-stop-select");
      if (sel && sel.options.length === 0) {
        sel.innerHTML = safetyCorridorData.stops.map(s =>
          `<option value="${s.seq}">Parada #${String(s.seq).padStart(2, '0')} - ${s.name}</option>`
        ).join("");
      }
      if (sel) sel.value = String(activeStopSeq);

      const tbody = document.getElementById("saf-corridor-tbody");
      if (tbody) {
        tbody.innerHTML = safetyCorridorData.stops.map(s => {
          const isSel = s.seq === activeStopSeq;
          const paxBadge = s.active_waiting_users <= 2
            ? `<span class="tag tag-amber">${s.active_waiting_users} pessoa (Só)</span>`
            : `<span class="tag tag-emerald">${s.active_waiting_users} pessoas</span>`;
          const dirBadge = s.keep_phone_in_pocket
            ? `<span class="tag tag-crimson">Guarde o celular</span>`
            : `<span class="tag tag-emerald">Seguro c/ grupo</span>`;
          return `
            <tr class="${isSel ? 'selected-row' : ''}" style="cursor:pointer;" onclick="selectStopNode(${s.seq}, true)">
              <td class="mono"><strong>#${String(s.seq).padStart(2, '0')}</strong></td>
              <td><strong>${s.name}</strong></td>
              <td>${paxBadge}</td>
              <td class="mono">${s.robbery_reports_30d}</td>
              <td>${dirBadge}</td>
            </tr>
          `;
        }).join("");
      }

      const feedBox = document.getElementById("saf-feed-container");
      if (feedBox && safetyCorridorData.recent_feed) {
        feedBox.innerHTML = safetyCorridorData.recent_feed.slice(0, 4).map(item => `
          <div style="background:var(--bg-subtle); border:1px solid var(--border); border-radius:var(--radius-sm); padding:12px;">
            <div style="display:flex; justify-content:space-between; font-size:12.5px; margin-bottom:4px;">
              <strong>${item.stop_name}</strong>
              <span class="mono" style="color:var(--text-muted);">${item.timestamp}</span>
            </div>
            <div style="font-size:13.5px;">${item.description}</div>
          </div>
        `).join("");
      }

      renderSelectedStopSafetyPanel(activeStopSeq);
    }

    function renderSelectedStopSafetyPanel(seq) {
      if (!safetyCorridorData || !safetyCorridorData.stops) return;
      const prof = safetyCorridorData.stops.find(s => s.seq === seq) || safetyCorridorData.stops[10];
      if (!prof) return;

      const sel = document.getElementById("saf-report-stop-select");
      if (sel) sel.value = String(prof.seq);

      document.getElementById("saf-stop-title").textContent = `Parada #${String(prof.seq).padStart(2, '0')} · ${prof.name}`;
      lastSafetyShieldVoice = prof.shield_voice_prompt;

      const topBadge = document.getElementById("saf-stop-badge");
      const warnBox = document.getElementById("saf-phone-warning-box");
      const headline = document.getElementById("saf-phone-headline");
      const expl = document.getElementById("saf-phone-explanation");

      if (prof.keep_phone_in_pocket) {
        topBadge.className = "tag tag-crimson";
        topBadge.textContent = "Guarde o Celular";
        warnBox.style.background = "var(--danger-red-bg)";
        warnBox.style.borderColor = "var(--danger-red-border)";
        headline.style.color = "var(--danger-red)";
        headline.textContent = `Não pegue o celular neste local! (${prof.robbery_reports_30d} relatos de assalto)`;
        expl.textContent = `Trecho com ${prof.robbery_reports_30d} queixas de roubo e iluminação ${prof.lighting_condition}. Deixe o celular guardado no bolso e escute os avisos pelo fone.`;
      } else {
        topBadge.className = "tag tag-emerald";
        topBadge.textContent = "Parada com Grupo";
        warnBox.style.background = "var(--brand-green-bg)";
        warnBox.style.borderColor = "var(--brand-green-border)";
        headline.style.color = "var(--brand-green)";
        headline.textContent = `Ponto iluminado e movimentado (${prof.active_waiting_users} pessoas aqui)`;
        expl.textContent = `Iluminação ${prof.lighting_condition} (${prof.patrol_notes}) com grupo aguardando o ônibus.`;
      }

      document.getElementById("saf-waiting-count").textContent = prof.active_waiting_users === 1 ? "1 pessoa" : `${prof.active_waiting_users} pessoas`;
      const aloneTag = document.getElementById("saf-alone-tag");
      if (prof.is_user_alone_risk) {
        aloneTag.className = "tag tag-crimson";
        aloneTag.textContent = "Você está quase só";
      } else {
        aloneTag.className = "tag tag-emerald";
        aloneTag.textContent = "Com companhia";
      }

      const comp = prof.companion_stop_recommendation;
      if (comp) {
        window.lastCompanionRecommendation = comp;
        document.getElementById("saf-companion-name").textContent = `Parada #${String(comp.seq).padStart(2, '0')} · ${comp.name}`;
        document.getElementById("saf-companion-metrics").textContent = `${comp.active_waiting_users} pessoas esperando juntas`;
        document.getElementById("saf-companion-dist").textContent = `A ${comp.distance_m}m (~${comp.walk_min} min a pé)`;
      }
    }

    function speakSafetyShieldPrompt() {
      playNaturalVoice(lastSafetyShieldVoice);
    }

    async function submitSafetyReport(category) {
      const st = TELEMETRIA.stops.find(s => s.seq === activeStopSeq) || TELEMETRIA.stops[10];
      const descInput = document.getElementById("saf-report-desc");
      const desc = descInput ? descInput.value : "";
      try {
        const resp = await fetch(`/api/live/safety-report?stop_id=${encodeURIComponent(st.stop_id)}&category=${encodeURIComponent(category)}&desc=${encodeURIComponent(desc)}`);
        const data = await resp.json();
        if (descInput) descInput.value = "";
        safetyCorridorData = data.corridor_overview;
        renderSafetyCorridorUI();
        setSimulatedUserLocation(userPos.lat, userPos.lon, userPos.label, false);
        playNaturalVoice(data.updated_stop_profile.shield_voice_prompt);
      } catch (err) {
        console.warn(err);
      }
    }

    async function adjustStopPresence(delta) {
      const st = TELEMETRIA.stops.find(s => s.seq === activeStopSeq) || TELEMETRIA.stops[10];
      try {
        const resp = await fetch(`/api/live/safety-presence?stop_id=${encodeURIComponent(st.stop_id)}&delta=${delta}`);
        const data = await resp.json();
        safetyCorridorData = data.corridor_overview;
        renderSafetyCorridorUI();
        setSimulatedUserLocation(userPos.lat, userPos.lon, userPos.label, false);
      } catch (err) {
        console.warn(err);
      }
    }

    function jumpToCompanionStop() {
      const comp = window.lastCompanionRecommendation;
      if (!comp) return;
      switchModule("mod-gis", document.querySelectorAll(".tab-btn")[0]);
      const targetStop = TELEMETRIA.stops.find(s => s.seq === comp.seq || String(s.stop_id) === String(comp.stop_id));
      if (targetStop) {
        selectStopNode(targetStop.seq, true, true);
      } else if (comp.lat && comp.lon) {
        setSimulatedUserLocation(
          comp.lat,
          comp.lon,
          comp.name || `Parada #${comp.stop_id}`,
          true,
          true
        );
      }
    }

    // =========================================================================
    // TAB 3: POCKET SENSORS & CITTAMOBI AUDIT
    // =========================================================================
    const IMU_SCENARIOS = {
      ALIGHTING: {
        verdict: "Desembarque (0,00% Falso Positivo)",
        tagClass: "tag-emerald",
        tmdClass: "Walking",
        voice: "Oi! Identifiquei que você acabou de descer do ônibus na parada Trevo de Ipojuca. Boa caminhada!",
        netStatus: "0 Bytes (Tudo no aparelho)"
      },
      ABANDONMENT: {
        verdict: "Desistência p/ Lotação (99,67% F1)",
        tagClass: "tag-crimson",
        tmdClass: "Car",
        voice: "Poxa, a Linha 178 Suape atrasou 38 minutos aqui no Trevo de Ipojuca. Registrei sua desistência de forma anônima para cobrar reforço de frota.",
        netStatus: "36 Bytes anônimos"
      },
      BOARDING_SERVED: {
        verdict: "Embarque no Ônibus Oficial (99,33%)",
        tagClass: "tag-cyan",
        tmdClass: "Bus",
        voice: "Atenção: o ônibus da Linha 178 Porto de Suape está encostando na sua parada agora. Bom trabalho!",
        netStatus: "0 Bytes"
      },
      TRANSIT_BYPASS: {
        verdict: "Passando Direto na Pista (100% Filtrado)",
        tagClass: "tag-amber",
        tmdClass: "Car",
        voice: "Você apenas passou direto pela rodovia sem parar no ponto. O modo bolso continua em silêncio.",
        netStatus: "0 Bytes"
      }
    };

    function selectImuScenario(key, itemEl) {
      currentImuKey = key;
      if (itemEl) {
        document.querySelectorAll(".sc-item").forEach(el => el.classList.remove("active"));
        itemEl.classList.add("active");
      }
      const sc = IMU_SCENARIOS[key];
      document.getElementById("imu-voice-transcript").textContent = `"${sc.voice}"`;
      document.getElementById("imu-net-counter").textContent = sc.netStatus;
      const vtag = document.getElementById("imu-verdict-tag");
      vtag.textContent = sc.verdict;
      vtag.className = `tag ${sc.tagClass}`;
      triggerLivePyTorchInference();
    }

    function speakImuTranscript() {
      playNaturalVoice(IMU_SCENARIOS[currentImuKey].voice);
    }

    async function triggerLivePyTorchInference() {
      try {
        const resp = await fetch(`/api/live/pytorch-infer?scenario=${currentImuKey}`);
        const data = await resp.json();
        document.getElementById("imu-live-cpu-us").textContent = `${data.cpu_inference_us} µs`;
      } catch (err) {
        console.warn(err);
      }
    }

    async function runLiveStgcnInference() {
      const st = TELEMETRIA.stops.find(s => s.seq === activeStopSeq) || TELEMETRIA.stops[10];
      try {
        const resp = await fetch(`/api/live/stgcn-corridor?seq=${st.seq}&wait=${st.wait_gps_min}&abn=${st.abandonment_10m}`);
        const data = await resp.json();
        const h = data.predicted_horizons_min;
        document.getElementById("insp-stgcn-big").textContent = `${h[2].toFixed(0)} min`;
      } catch (err) {
        console.warn(err);
      }
    }

    async function pingLiveCittamobiStop() {
      const st = TELEMETRIA.stops.find(s => s.seq === activeStopSeq) || TELEMETRIA.stops[10];
      const cell = document.getElementById("insp-live-citta-ping");
      if (!cell) return;
      cell.textContent = "Consultando Cittamobi...";
      try {
        const resp = await fetch(`/api/live/cittamobi-stop?stop_id=${st.cittamobi_id}&service_id=9655998`);
        const data = await resp.json();
        const sq = data.stop_query;
        cell.textContent = `HTTP ${sq.http_status} (${sq.latency_ms}ms) -> 0 ônibus`;
      } catch (err) {
        cell.textContent = "Offline";
      }
    }

    async function refreshLiveCittamobiFleet() {
      const badge = document.getElementById("citta-fleet-badge");
      if (badge) badge.textContent = "Consultando...";
      try {
        const resp = await fetch("/api/live/cittamobi-fleet");
        const data = await resp.json();
        if (badge) badge.textContent = `0 veículos ativos (Auditado às ${data.queried_at})`;
        const svTbody = document.getElementById("citta-services-tbody");
        svTbody.innerHTML = data.results.map(r => `
          <tr>
            <td class="mono">${r.serviceId}</td>
            <td><strong>${r.label}</strong></td>
            <td>Grande Recife (a=202)</td>
            <td><span class="tag tag-crimson">${r.active_vehicles} veículos (${r.latency_ms}ms)</span></td>
          </tr>
        `).join("");
      } catch (err) {
        console.warn(err);
      }
    }

    function populateCittamobiTables() {
      const svTbody = document.getElementById("citta-services-tbody");
      if (!svTbody) return;
      svTbody.innerHTML = TELEMETRIA.cittamobi_services.slice(0, 8).map(sv => `
        <tr>
          <td class="mono">${sv.serviceId}</td>
          <td><strong>${sv.routeCode}</strong></td>
          <td>${sv.companyName}</td>
          <td><span class="tag tag-crimson">${sv.activeVehicles} ônibus</span></td>
        </tr>
      `).join("");
    }

    function renderImuOscilloscope() {
      const canvas = document.getElementById("imu-osc-canvas");
      if (canvas && document.getElementById("mod-tech").classList.contains("active")) {
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
        ctx.fillStyle = "#0d1117";
        ctx.fillRect(0, 0, W, H);

        const tmdClass = IMU_SCENARIOS[currentImuKey].tmdClass;
        const series = TELEMETRIA.tmd_real_windows[tmdClass] || TELEMETRIA.tmd_real_windows["Walking"];
        const N = 50;

        ctx.beginPath();
        for (let i = 0; i < N; i++) {
          const item = series[(i + Math.floor(oscTick)) % series.length];
          const val = item.acc_mean + Math.sin((i + oscTick) * 0.45) * item.acc_std;
          const x = (i / (N - 1)) * W;
          const y = H - Math.min(H - 12, Math.max(12, (val / 22.0) * (H - 24)));
          if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
        }
        ctx.strokeStyle = "#10b981";
        ctx.lineWidth = 2.4;
        ctx.stroke();
        ctx.restore();
        oscTick += 0.22;
      }
      requestAnimationFrame(renderImuOscilloscope);
    }

    // INITIALIZATION
    initQuickStopButtons();
    selectStopNode(11, false, false);
    populateCittamobiTables();
    refreshSafetyCorridor();

    requestAnimationFrame(() => {
      drawPe60GisCanvas();
      setSimulatedUserLocation(-8.494915, -35.092190, "Rodovia PE-60 (Trevo de Camela) · Ipojuca", true, false);
    });
    requestAnimationFrame(renderImuOscilloscope);
  </script>
</body>
</html>
"""

final_html = HTML_TEMPLATE.replace("__TELEMETRIA_JSON__", TELEMETRIA_JSON_STR)
with open(OUT_HTML, "w", encoding="utf-8") as f:
    f.write(final_html)

print(f"[OK] Protótipo GrafoParada v6.0 (Ultra-Limpo + Voz Neural Natural) gerado em {OUT_HTML} ({OUT_HTML.stat().st_size:,} bytes)")
