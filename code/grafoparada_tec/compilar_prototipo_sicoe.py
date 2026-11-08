"""
Gerador do Protótipo GrafoParada v5.0 — Interface Limpa, Map-First e Altamente Acessível (WCAG AAA)
Referências de Design: Transit App 6.0, Citymapper, Gov.br/Grande Recife Consórcio.
Zero "AI Slop" (sem siglas robóticas, sem jargão de terminal hacker, tipografia Plus Jakarta Sans + JetBrains Mono,
Modo Claro Solar por padrão + Modo Escuro Noturno, botões grandes de 44px+, foco em Mapa, Segurança e Companhia).
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
  <title>GrafoParada · Grande Recife — Mapa ao Vivo, Segurança e Companhia na Parada (PE-60 / Suape)</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <style>
    /* =========================================================================
       DESIGN TOKENS: CLEAN DAYLIGHT DEFAULT + HIGH-CONTRAST NIGHT MODE (WCAG AAA)
       ========================================================================= */
    :root, [data-theme="light"] {
      --bg-page: #f5f5f2;
      --bg-surface: #ffffff;
      --bg-subtle: #ededeb;
      --bg-muted: #e2e2de;
      --border: #d4d4ce;
      --border-strong: #a8a89e;
      --text-main: #141413;
      --text-secondary: #454540;
      --text-muted: #6e6e66;

      --brand-green: #0a6b46;
      --brand-green-bg: #e3f5ec;
      --brand-green-border: #8fd4b4;

      --warn-amber: #9e5800;
      --warn-amber-bg: #fff3db;
      --warn-amber-border: #f0c36d;

      --danger-red: #b91c1c;
      --danger-red-bg: #fde8e8;
      --danger-red-border: #f5a3a3;

      --user-blue: #0057b8;
      --user-blue-bg: #e6f0fa;
      --user-blue-border: #90bef2;

      --shadow-sm: 0 1px 3px rgba(20, 20, 19, 0.06);
      --shadow-md: 0 6px 20px rgba(20, 20, 19, 0.09);
      --radius-sm: 8px;
      --radius-md: 12px;
      --radius-lg: 16px;
    }

    [data-theme="dark"] {
      --bg-page: #0f1115;
      --bg-surface: #171a21;
      --bg-subtle: #20242d;
      --bg-muted: #292e3a;
      --border: #2e3442;
      --border-strong: #454e63;
      --text-main: #f3f4f6;
      --text-secondary: #c4c9d4;
      --text-muted: #8b93a6;

      --brand-green: #22c55e;
      --brand-green-bg: rgba(34, 197, 94, 0.14);
      --brand-green-border: rgba(34, 197, 94, 0.45);

      --warn-amber: #fbbf24;
      --warn-amber-bg: rgba(251, 191, 36, 0.14);
      --warn-amber-border: rgba(251, 191, 36, 0.45);

      --danger-red: #f87171;
      --danger-red-bg: rgba(248, 113, 113, 0.15);
      --danger-red-border: rgba(248, 113, 113, 0.5);

      --user-blue: #38bdf8;
      --user-blue-bg: rgba(56, 189, 248, 0.14);
      --user-blue-border: rgba(56, 189, 248, 0.45);

      --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.35);
      --shadow-md: 0 8px 24px rgba(0, 0, 0, 0.5);
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
      font-size: 15px;
      line-height: 1.5;
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
       TOP HEADER NAVIGATION (CLEAN, HUMAN, ACCESSIBLE)
       ========================================================================= */
    .app-header {
      background: var(--bg-surface);
      border-bottom: 1px solid var(--border);
      padding: 0 20px;
      min-height: 62px;
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
      font-size: 13px;
      padding: 6px 11px;
      border-radius: var(--radius-sm);
      letter-spacing: 0.01em;
    }

    [data-theme="dark"] .brand-badge {
      color: #062112;
    }

    .brand-title {
      font-size: 16px;
      font-weight: 800;
      color: var(--text-main);
      letter-spacing: -0.02em;
    }

    .brand-subtitle {
      font-size: 12.5px;
      color: var(--text-muted);
      font-weight: 500;
    }

    .main-tabs {
      display: flex;
      align-items: center;
      gap: 6px;
      flex-wrap: wrap;
    }

    .tab-btn {
      background: transparent;
      border: 1px solid transparent;
      color: var(--text-secondary);
      font-size: 13.5px;
      font-weight: 700;
      padding: 9px 14px;
      border-radius: var(--radius-sm);
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: background 0.15s, color 0.15s, border-color 0.15s;
      min-height: 42px;
    }

    .tab-btn:hover {
      background: var(--bg-subtle);
      color: var(--text-main);
    }

    .tab-btn.active {
      background: var(--brand-green-bg);
      color: var(--brand-green);
      border-color: var(--brand-green-border);
    }

    .tab-num {
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      background: var(--bg-subtle);
      color: var(--text-secondary);
      padding: 2px 6px;
      border-radius: 5px;
    }

    .tab-btn.active .tab-num {
      background: var(--brand-green);
      color: #ffffff;
    }

    [data-theme="dark"] .tab-btn.active .tab-num {
      color: #062112;
    }

    .header-actions {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .live-pill {
      display: inline-flex;
      align-items: center;
      gap: 7px;
      font-size: 12px;
      font-weight: 700;
      padding: 6px 11px;
      border-radius: 999px;
      background: var(--brand-green-bg);
      color: var(--brand-green);
      border: 1px solid var(--brand-green-border);
    }

    .live-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--brand-green);
    }

    .theme-btn {
      background: var(--bg-subtle);
      border: 1px solid var(--border);
      color: var(--text-main);
      font-size: 13px;
      font-weight: 700;
      padding: 8px 12px;
      border-radius: var(--radius-sm);
      cursor: pointer;
      min-height: 40px;
    }

    .theme-btn:hover {
      background: var(--bg-muted);
    }

    /* =========================================================================
       BUTTONS & BADGES (ACCESSIBLE 42px+ TARGETS)
       ========================================================================= */
    .btn {
      background: var(--bg-surface);
      border: 1px solid var(--border-strong);
      color: var(--text-main);
      font-size: 13px;
      font-weight: 700;
      padding: 8px 13px;
      border-radius: var(--radius-sm);
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      min-height: 38px;
      transition: all 0.14s ease;
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

    .btn-primary:hover {
      opacity: 0.92;
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
      font-size: 11.5px;
      font-weight: 700;
      padding: 3px 9px;
      border-radius: 999px;
      border: 1px solid var(--border);
      background: var(--bg-subtle);
      color: var(--text-secondary);
      white-space: nowrap;
    }

    .tag-emerald {
      background: var(--brand-green-bg);
      color: var(--brand-green);
      border-color: var(--brand-green-border);
    }

    .tag-amber {
      background: var(--warn-amber-bg);
      color: var(--warn-amber);
      border-color: var(--warn-amber-border);
    }

    .tag-crimson {
      background: var(--danger-red-bg);
      color: var(--danger-red);
      border-color: var(--danger-red-border);
    }

    .tag-cyan {
      background: var(--user-blue-bg);
      color: var(--user-blue);
      border-color: var(--user-blue-border);
    }

    /* =========================================================================
       WORKSPACE VIEWS & MAP-FIRST SPLIT LAYOUT
       ========================================================================= */
    .workspace-view {
      display: none;
      padding: 18px 20px 28px;
      max-width: 1680px;
      margin: 0 auto;
    }

    .workspace-view.active {
      display: block;
    }

    /* TAB 1: MAP-FIRST WORKSPACE */
    .map-first-layout {
      display: grid;
      grid-template-columns: 1.55fr 1fr;
      gap: 18px;
      align-items: start;
    }

    .map-stage-card {
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      overflow: hidden;
      box-shadow: var(--shadow-md);
      display: flex;
      flex-direction: column;
    }

    .map-toolbar {
      padding: 12px 16px;
      border-bottom: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 10px;
      background: var(--bg-surface);
    }

    .map-container-box {
      position: relative;
      width: 100%;
      height: 550px;
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

    /* Clean Floating Pill on Map */
    .map-floating-status {
      position: absolute;
      top: 12px;
      left: 12px;
      z-index: 500;
      background: var(--bg-surface);
      border: 1px solid var(--border-strong);
      border-radius: var(--radius-md);
      padding: 10px 14px;
      box-shadow: var(--shadow-md);
      max-width: 440px;
      pointer-events: none;
    }

    .map-floating-legend {
      position: absolute;
      bottom: 12px;
      left: 12px;
      z-index: 500;
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      padding: 7px 12px;
      box-shadow: var(--shadow-sm);
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      font-size: 12px;
      font-weight: 600;
      color: var(--text-secondary);
    }

    .legend-dot {
      display: inline-block;
      width: 10px;
      height: 10px;
      border-radius: 50%;
      margin-right: 5px;
      vertical-align: middle;
    }

    /* Custom Stop Pill Markers on Map */
    .stop-map-pill {
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-weight: 800;
      font-size: 11px;
      color: #ffffff;
      border: 2px solid #ffffff;
      border-radius: 999px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.35);
      padding: 2px 6px;
      white-space: nowrap;
      transition: transform 0.12s ease;
    }

    .stop-map-pill.selected {
      transform: scale(1.22);
      border-width: 3px;
      z-index: 900 !important;
      box-shadow: 0 0 0 4px rgba(0, 87, 184, 0.35), 0 4px 10px rgba(0,0,0,0.45);
    }

    @keyframes pulseUserBeacon {
      0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 87, 184, 0.75); }
      70% { transform: scale(1.08); box-shadow: 0 0 0 16px rgba(0, 87, 184, 0); }
      100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 87, 184, 0); }
    }

    .user-gps-beacon {
      width: 22px;
      height: 22px;
      background: #0057b8;
      border: 3px solid #ffffff;
      border-radius: 50%;
      animation: pulseUserBeacon 1.8s infinite;
      cursor: grab;
      box-shadow: 0 2px 8px rgba(0,0,0,0.4);
    }

    .sicoe-tooltip {
      background: var(--bg-surface) !important;
      border: 1px solid var(--border-strong) !important;
      border-radius: 8px !important;
      color: var(--text-main) !important;
      font-family: 'Plus Jakarta Sans', sans-serif !important;
      font-size: 12px !important;
      font-weight: 600 !important;
      padding: 6px 10px !important;
      box-shadow: var(--shadow-md) !important;
    }

    /* Quick Location Presets Bar under Map */
    .location-bar {
      padding: 12px 16px;
      background: var(--bg-subtle);
      border-top: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 10px;
    }

    .corridor-strip {
      padding: 10px 16px;
      background: var(--bg-surface);
      border-top: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 8px;
    }

    /* =========================================================================
       CARDS, PANELS & TABLES
       ========================================================================= */
    .panel {
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-lg);
      box-shadow: var(--shadow-sm);
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }

    .panel-head {
      padding: 14px 18px;
      background: var(--bg-subtle);
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      font-size: 14px;
      font-weight: 800;
      color: var(--text-main);
    }

    .panel-body {
      padding: 16px 18px;
    }

    .tech-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 13.5px;
    }

    .tech-table th, .tech-table td {
      padding: 10px 12px;
      border-bottom: 1px solid var(--border);
      text-align: left;
      vertical-align: middle;
    }

    .tech-table th {
      font-size: 11.5px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      color: var(--text-muted);
      background: var(--bg-subtle);
    }

    .tech-table tr:hover td {
      background: var(--bg-subtle);
    }

    .tech-table tr.selected-row td {
      background: var(--brand-green-bg);
    }

    /* =========================================================================
       LAYOUT GRIDS FOR OTHER TABS
       ========================================================================= */
    .gis-grid, .split-2 {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 18px;
    }

    .imu-grid {
      display: grid;
      grid-template-columns: 400px 1fr;
      gap: 18px;
    }

    .kpi-grid-4 {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 14px;
      margin-bottom: 18px;
    }

    .kpi-card {
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 14px 16px;
      box-shadow: var(--shadow-sm);
    }

    .kpi-label {
      font-size: 12px;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.03em;
    }

    .kpi-val {
      font-size: 24px;
      font-weight: 800;
      margin: 4px 0;
      color: var(--text-main);
    }

    .kpi-sub {
      font-size: 12.5px;
      color: var(--text-secondary);
    }

    @media (max-width: 1220px) {
      .map-first-layout, .gis-grid, .imu-grid, .split-2 {
        grid-template-columns: 1fr;
      }
      .kpi-grid-4 {
        grid-template-columns: repeat(2, 1fr);
      }
    }

    /* MODULE 3 (IMU) SPECIFIC */
    .sc-item {
      background: var(--bg-surface);
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      padding: 12px 14px;
      cursor: pointer;
      margin-bottom: 8px;
      transition: all 0.14s;
    }

    .sc-item:hover {
      background: var(--bg-subtle);
    }

    .sc-item.active {
      border: 2px solid var(--brand-green);
      background: var(--brand-green-bg);
    }

    .sc-item-head {
      display: flex;
      justify-content: space-between;
      font-weight: 800;
      font-size: 14px;
      margin-bottom: 4px;
    }

    .sc-item-desc {
      font-size: 13px;
      color: var(--text-secondary);
    }

    .tts-box {
      background: var(--warn-amber-bg);
      border: 1px solid var(--warn-amber-border);
      border-radius: var(--radius-md);
      padding: 14px;
      margin: 14px 0;
    }

    .osc-wrap {
      background: #0d1117;
      border: 1px solid var(--border);
      border-radius: var(--radius-md);
      height: 185px;
      width: 100%;
      overflow: hidden;
      margin-bottom: 14px;
    }

    .osc-wrap canvas {
      width: 100%;
      height: 100%;
      display: block;
    }

    .prob-strip {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 10px;
      margin-bottom: 14px;
    }

    .prob-cell {
      background: var(--bg-subtle);
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      padding: 10px 12px;
    }

    .prob-bar-track {
      height: 8px;
      background: var(--bg-muted);
      border-radius: 999px;
      margin-top: 8px;
      overflow: hidden;
    }

    .prob-bar-fill {
      height: 100%;
      background: var(--user-blue);
      border-radius: 999px;
      transition: width 0.25s ease;
    }

    .code-box {
      background: #12151c;
      color: #34d399;
      border-radius: var(--radius-md);
      padding: 12px 14px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 12px;
      white-space: pre-wrap;
      line-height: 1.55;
    }

    input[type="range"] {
      width: 100%;
      accent-color: var(--brand-green);
      cursor: pointer;
    }
  </style>
</head>
<body>

  <!-- ======================================================================= -->
  <!-- CLEAN HUMAN HEADER                                                      -->
  <!-- ======================================================================= -->
  <header class="app-header">
    <div class="brand-block">
      <span class="brand-badge">GrafoParada</span>
      <div>
        <div class="brand-title">Grande Recife · Corredor PE-60 &amp; Suape</div>
        <div class="brand-subtitle">Previsão em Tempo Real, Modo Bolso Sem Tela e Companhia na Parada</div>
      </div>
    </div>

    <nav class="main-tabs" aria-label="Navegação Principal">
      <button class="tab-btn active" onclick="switchModule('mod-gis', this)">
        <span class="tab-num">1</span> Mapa ao Vivo &amp; Sua Parada
      </button>
      <button class="tab-btn" onclick="switchModule('mod-safety', this)">
        <span class="tab-num">2</span> Segurança &amp; Companhia
      </button>
      <button class="tab-btn" onclick="switchModule('mod-imu', this)">
        <span class="tab-num">3</span> Modo Bolso (Sensores &amp; Voz)
      </button>
      <button class="tab-btn" onclick="switchModule('mod-citta', this)">
        <span class="tab-num">4</span> Auditoria Cittamobi
      </button>
      <button class="tab-btn" onclick="switchModule('mod-bench', this)">
        <span class="tab-num">5</span> Resultados &amp; Privacidade
      </button>
    </nav>

    <div class="header-actions">
      <span class="live-pill" title="Conectado ao motor PyTorch e ao servidor Cittamobi em tempo real">
        <i class="live-dot"></i> Tempo Real Ativo · <span id="live-clock" class="mono">05:42:18</span>
      </span>
      <button id="theme-toggle-btn" class="theme-btn" onclick="toggleTheme()" aria-label="Alternar entre Modo Claro e Modo Noturno">
        Modo Noturno
      </button>
    </div>
  </header>

  <!-- ======================================================================= -->
  <!-- TAB 1: MAPA AO VIVO & SUA PARADA (MAP-FIRST, CLEAN & ACCESSIBLE)        -->
  <!-- ======================================================================= -->
  <main id="mod-gis" class="workspace-view active">
    <div class="map-first-layout">

      <!-- LEFT: REAL INTERACTIVE CARTOGRAPHIC MAP -->
      <div class="map-stage-card">
        <div class="map-toolbar">
          <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
            <strong style="font-size:14px;">Visualização do Mapa:</strong>
            <button id="btn-tile-osm" class="btn active" onclick="setBaseTile('osm')">Mapa Claro (Ruas)</button>
            <button id="btn-tile-dark" class="btn" onclick="setBaseTile('dark')">Mapa Noturno</button>
            <button id="btn-tile-sat" class="btn" onclick="setBaseTile('sat')">Satélite Real</button>
          </div>
          <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
            <button id="btn-layer-gp" class="btn active" onclick="setGisLayer('grafoparada')">Visão GrafoParada</button>
            <button id="btn-layer-catraca" class="btn" onclick="setGisLayer('catraca')">Visão Só Catraca</button>
            <button id="btn-layer-citta" class="btn" onclick="toggleCittamobi534()">534 Paradas Cittamobi: <span id="lbl-citta-toggle">OFF</span></button>
          </div>
        </div>

        <div class="map-container-box">
          <div id="pe60-leaflet-map" role="region" aria-label="Mapa interativo das paradas de ônibus"></div>

          <div class="map-floating-status">
            <div style="font-weight:800; font-size:13.5px; color:var(--user-blue); margin-bottom:2px;">
              Corredor Linha 178/191: TI Cabo &rarr; Rodovia PE-60 &rarr; Suape
            </div>
            <div id="map-hover-readout" style="font-size:12.5px; color:var(--text-secondary);">
              Clique em qualquer rua do mapa para posicionar você ou clique em uma parada numerada (#01 a #20).
            </div>
          </div>

          <div class="map-floating-legend">
            <span><i class="legend-dot" style="background:#0057b8; border:2px solid #fff;"></i>Sua Localização</span>
            <span><i class="legend-dot" style="background:#0a6b46;"></i>Normal (&le;35 min)</span>
            <span><i class="legend-dot" style="background:#d97706;"></i>Atenção (35–40 min)</span>
            <span><i class="legend-dot" style="background:#dc2626;"></i>Crítica (Desistência / Atraso)</span>
          </div>
        </div>

        <!-- EASY LOCATION BAR -->
        <div class="location-bar">
          <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
            <strong style="font-size:13px; color:var(--user-blue);">Onde você está agora?</strong>
            <button id="btn-gps-real" class="btn btn-blue" onclick="useRealBrowserGps()">
              Usar Meu GPS Real (Navegador)
            </button>
            <button class="btn" onclick="setSimulatedUserLocation(-8.304950, -35.021420, 'Na Parada #11 (PE-60 · Trevo Ipojuca)', true)">
              Simular no Trevo Ipojuca (#11)
            </button>
            <button class="btn" onclick="setSimulatedUserLocation(-8.285150, -35.032290, 'No Terminal Integrado do Cabo (#01)', true)">
              Simular no TI Cabo (#01)
            </button>
            <button class="btn" onclick="setSimulatedUserLocation(-8.062850, -34.878950, 'No Centro do Recife (Av. Conde da Boa Vista)', true)">
              Simular no Centro do Recife
            </button>
          </div>
          <span style="font-size:12.5px; color:var(--text-muted);">
            Dica: Você também pode clicar em qualquer ponto do mapa ou arrastar o pino azul!
          </span>
        </div>

        <!-- QUICK STOP SELECTOR (#01 to #20) -->
        <div class="corridor-strip">
          <span style="font-size:12.5px; font-weight:700; color:var(--text-secondary);">Ir direto para a parada da PE-60:</span>
          <div id="quick-stop-selector" style="display:flex; gap:4px; flex-wrap:wrap;"></div>
        </div>
      </div>

      <!-- RIGHT: HUMAN-CENTERED COMPANION CARDS (SAFETY + NEARBY STOPS + SELECTED STOP) -->
      <div style="display:flex; flex-direction:column; gap:16px;">

        <!-- CARD 1: YOUR LOCATION, SAFETY ALERT ("DO NOT TAKE PHONE OUT") & COMPANION FINDER -->
        <div class="panel">
          <div class="panel-head">
            <div>
              <span>Seu Radar de Paradas Próximas &amp; Proteção Pessoal</span>
              <div id="user-loc-coords-badge" class="mono" style="font-size:11.5px; font-weight:500; color:var(--text-muted); margin-top:2px;">
                Na Parada #11 (PE-60 · Trevo Ipojuca)
              </div>
            </div>
            <span id="user-geofence-badge" class="tag tag-emerald">Você está na parada (11,6m)</span>
          </div>

          <div class="panel-body">
            <!-- Big Accessible Safety Banner -->
            <div id="f1-safety-shield-banner" style="background:var(--danger-red-bg); border:1px solid var(--danger-red-border); border-left:5px solid var(--danger-red); border-radius:var(--radius-md); padding:12px 14px; margin-bottom:12px;">
              <div style="font-weight:800; font-size:14px; color:var(--danger-red); margin-bottom:4px;" id="f1-shield-title">
                Atenção: Local com relatos de assalto — Não pegue o celular na parada!
              </div>
              <p id="f1-shield-desc" style="font-size:13px; color:var(--text-main); margin-bottom:10px;">
                Esta parada possui 19 relatos de roubo e apenas 1 pessoa aguardando agora. Mantenha o celular guardado no bolso: o GrafoParada avisa pelo fone de ouvido quando o ônibus estiver chegando.
              </p>
              <div style="display:flex; gap:8px; flex-wrap:wrap;">
                <button id="f1-btn-companion" class="btn btn-primary" onclick="jumpToCompanionStop()">
                  Ir para Parada Segura com Companhia (12 pessoas a 480m)
                </button>
                <button class="btn btn-amber" onclick="speakNearestStopVoice()">
                  Ouvir Aviso de Voz no Fone
                </button>
                <button class="btn" onclick="switchModule('mod-safety', document.querySelectorAll('.tab-btn')[1])">
                  Relatar Roubo ou Ver Segurança
                </button>
              </div>
            </div>

            <!-- Voice Transcript Preview -->
            <div id="user-pocket-voice-bar" style="background:var(--bg-subtle); border:1px solid var(--border); border-radius:var(--radius-sm); padding:9px 12px; font-size:12.5px; color:var(--text-secondary); margin-bottom:12px;">
              Carregando radar de paradas próximas...
            </div>

            <!-- Nearby Official Stops Table -->
            <div style="font-size:12px; font-weight:700; color:var(--text-muted); text-transform:uppercase; margin-bottom:6px;">
              Paradas Oficiais Mais Próximas de Você (7.238 paradas do Grande Recife):
            </div>
            <div style="overflow-x:auto;">
              <table class="tech-table">
                <thead>
                  <tr>
                    <th>Código</th>
                    <th>Parada</th>
                    <th>Distância</th>
                    <th>Pessoas Esperando</th>
                    <th>Recomendação de Segurança</th>
                  </tr>
                </thead>
                <tbody id="nearby-gtfs-tbody"></tbody>
              </table>
            </div>

            <!-- Collapsible Cittamobi Live Viewport Comparison -->
            <details style="margin-top:10px; background:var(--bg-subtle); border:1px solid var(--border); border-radius:var(--radius-sm); padding:8px 12px;">
              <summary style="cursor:pointer; font-size:12.5px; font-weight:700; color:var(--text-secondary);">
                Ver paradas retornadas ao vivo pelo servidor Cittamobi neste raio (<span id="nearby-citta-meta">Consultando...</span>)
              </summary>
              <div style="margin-top:8px; overflow-x:auto;">
                <table class="tech-table">
                  <thead>
                    <tr>
                      <th>ID Cittamobi</th>
                      <th>Endereço no Cittamobi</th>
                      <th>Distância</th>
                      <th>Ônibus no App</th>
                    </tr>
                  </thead>
                  <tbody id="nearby-citta-tbody"></tbody>
                </table>
              </div>
            </details>
          </div>
        </div>

        <!-- CARD 2: SELECTED STOP DETAILS & FLEET DISPATCH -->
        <div class="panel">
          <div class="panel-head">
            <span id="insp-stop-header">Parada #11 · PE-60 km 17 (Trevo Ipojuca / Camela)</span>
            <span id="insp-stop-tag" class="tag tag-crimson">Crítica · 14 Desistências</span>
          </div>
          <div class="panel-body">
            <table class="tech-table" style="margin-bottom:12px;">
              <tbody>
                <tr>
                  <td style="color:var(--text-secondary); width:40%;">Previsão de Espera (IA STGCN)</td>
                  <td class="mono" id="insp-stgcn">Em 10m: 38,4 min | Em 20m: 43,8 min | <strong>Em 30m: 47,2 min</strong></td>
                </tr>
                <tr>
                  <td style="color:var(--text-secondary);">Passageiros Desistindo (Últimos 10 min)</td>
                  <td id="insp-abn" style="color:var(--danger-red); font-weight:700;">14 pessoas desistiram e pegaram transporte alternativo</td>
                </tr>
                <tr>
                  <td style="color:var(--text-secondary);">O que a Catraca Eletrônica VEM vê?</td>
                  <td id="insp-catraca">0 validações (Como o ônibus atrasou, a catraca acha que a parada está vazia)</td>
                </tr>
                <tr>
                  <td style="color:var(--text-secondary);">O que o App Cittamobi mostra agora?</td>
                  <td id="insp-citta">Parada #2966773 ("Rodovia Armínio Cuil Hi Rme" · 0 veículos na linha)</td>
                </tr>
                <tr>
                  <td style="color:var(--text-secondary);">Consulta ao Vivo (`api.cittamobi.com.br`)</td>
                  <td class="mono" id="insp-live-citta-ping" style="font-size:12px;">Consultando servidor...</td>
                </tr>
                <tr>
                  <td style="color:var(--text-secondary);">Coordenadas Oficiais (GTFS)</td>
                  <td class="mono" id="insp-coords" style="font-size:12px;">-8.304873, -35.021349</td>
                </tr>
              </tbody>
            </table>

            <div style="display:flex; gap:8px; flex-wrap:wrap; margin-bottom:12px;">
              <button class="btn btn-primary" onclick="runLiveStgcnInference()">
                Recalcular Previsão na Rede Neural (PyTorch)
              </button>
              <button class="btn" onclick="pingLiveCittamobiStop()">
                Testar Resposta do Cittamobi Agora
              </button>
            </div>

            <!-- Human-in-the-loop Dispatch Box -->
            <div style="background:var(--bg-subtle); border:1px solid var(--border); border-radius:var(--radius-md); padding:12px;">
              <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                <strong style="font-size:13px;">Ação do Controlador CTM: Remanejar Ônibus Ocioso ("Frota no Vazio")</strong>
                <span class="tag tag-amber" id="insp-audit-flag">Conferir GPS Anterior</span>
              </div>
              <p style="font-size:12.5px; color:var(--text-secondary); margin-bottom:10px;">
                Enquanto 14 trabalhadores desistem no Trevo de Ipojuca (#11), o veículo <strong>#178-09</strong> está voltando quase vazio (&lt;8% de ocupação) da Rotatória Administrativa de Suape (#19). O despachante autoriza o remanejamento sem custo extra de frota:
              </p>
              <div style="display:flex; gap:8px; flex-wrap:wrap; margin-bottom:8px;">
                <button class="btn btn-primary" onclick="triggerGtfsPatch()">
                  Autorizar Partida Expressa para Cobrir Esta Parada
                </button>
                <button class="btn" onclick="selectStopNode(19, true)">
                  Ver Ônibus Ocioso na Parada #19 (Suape)
                </button>
              </div>
              <div id="gtfs-patch-output" class="code-box" style="font-size:11.5px;">Clique em "Autorizar Partida Expressa" para gerar a ordem operacional no GTFS...</div>
            </div>
          </div>
        </div>

      </div>

    </div>
  </main>

  <!-- ======================================================================= -->
  <!-- TAB 2: SEGURANÇA COMUNITÁRIA & COMPANHIA NA PARADA ("NÃO FIQUE SÓ")     -->
  <!-- ======================================================================= -->
  <main id="mod-safety" class="workspace-view">
    <div class="kpi-grid-4">
      <div class="kpi-card" style="border-left:4px solid var(--brand-green);">
        <div class="kpi-label">Pessoas Esperando Agora (PE-60)</div>
        <div class="kpi-val" id="saf-kpi-waiting" style="color:var(--brand-green);">123 pessoas</div>
        <div class="kpi-sub">Contagem anônima via presença na parada (Zero dados pessoais)</div>
      </div>
      <div class="kpi-card" style="border-left:4px solid var(--danger-red);">
        <div class="kpi-label">Paradas com Alerta "Guarde o Celular"</div>
        <div class="kpi-val" id="saf-kpi-nophone" style="color:var(--danger-red);">5 paradas</div>
        <div class="kpi-sub">Aviso automático por voz no fone a 180 metros de distância</div>
      </div>
      <div class="kpi-card" style="border-left:4px solid var(--warn-amber);">
        <div class="kpi-label">Paradas Solitárias (&le; 2 Pessoas)</div>
        <div class="kpi-val" id="saf-kpi-lonely" style="color:var(--warn-amber);">6 paradas</div>
        <div class="kpi-sub">Sistema indica a parada iluminada com grupo mais próxima</div>
      </div>
      <div class="kpi-card" style="border-left:4px solid var(--user-blue);">
        <div class="kpi-label">Relatos da Comunidade (30 dias)</div>
        <div class="kpi-val" id="saf-kpi-reports" style="color:var(--user-blue);">132 relatos</div>
        <div class="kpi-sub">Colaboração entre trabalhadores do turno da madrugada</div>
      </div>
    </div>

    <div class="gis-grid">

      <!-- Left: Stop Safety Shield, Presence Counter & Report Form -->
      <div style="display:flex; flex-direction:column; gap:16px;">
        <div class="panel">
          <div class="panel-head">
            <span id="saf-stop-title">Segurança na Parada #11 · PE-60 km 17 (Trevo Ipojuca)</span>
            <span id="saf-stop-badge" class="tag tag-crimson">Perigo Elevado · Guarde o Celular</span>
          </div>
          <div class="panel-body">

            <div id="saf-phone-warning-box" style="background:var(--danger-red-bg); border:1px solid var(--danger-red-border); border-radius:var(--radius-md); padding:14px; margin-bottom:14px;">
              <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px; gap:8px; flex-wrap:wrap;">
                <strong id="saf-phone-headline" style="color:var(--danger-red); font-size:15px;">
                  Não pegue o celular neste local! (19 relatos de assalto)
                </strong>
                <span class="tag tag-crimson" id="saf-risk-score-tag">Risco: 99/100</span>
              </div>
              <p id="saf-phone-explanation" style="font-size:13.5px; color:var(--text-main); margin-bottom:10px;">
                Passageiros relataram abordagens rápidas de motocicleta para roubo de celulares com tela acesa neste trecho. Mantenha o aparelho no bolso: o GrafoParada funciona 100% por voz.
              </p>
              <div style="display:flex; gap:8px; flex-wrap:wrap;">
                <button class="btn btn-amber" onclick="speakSafetyShieldPrompt()">
                  Ouvir Aviso de Segurança no Fone
                </button>
                <button class="btn" onclick="switchModule('mod-gis', document.querySelectorAll('.tab-btn')[0]); selectStopNode(activeStopSeq, true);">
                  Ver Esta Parada no Mapa
                </button>
              </div>
            </div>

            <!-- Presence & Companion Grid -->
            <div class="split-2" style="margin-bottom:14px;">
              <div style="background:var(--bg-subtle); border:1px solid var(--border); border-radius:var(--radius-md); padding:14px;">
                <div style="font-size:12px; font-weight:700; color:var(--text-muted); text-transform:uppercase;">
                  Quantas pessoas estão esperando aqui agora?
                </div>
                <div style="display:flex; align-items:baseline; gap:10px; margin:8px 0;">
                  <span id="saf-waiting-count" style="font-size:28px; font-weight:800; color:var(--warn-amber);">1 pessoa</span>
                  <span id="saf-alone-tag" class="tag tag-crimson">Alerta: Você está quase só</span>
                </div>
                <div id="saf-lighting-info" style="font-size:12.5px; color:var(--text-secondary); margin-bottom:10px;">
                  Iluminação: Crítica (Trevo Escuro)
                </div>
                <div style="display:flex; gap:8px; flex-wrap:wrap;">
                  <button class="btn btn-primary" onclick="adjustStopPresence(1)">
                    +1 Simular Chegada de Passageiro
                  </button>
                  <button class="btn" onclick="adjustStopPresence(-1)">
                    -1 Saída
                  </button>
                </div>
              </div>

              <div style="background:var(--brand-green-bg); border:1px solid var(--brand-green-border); border-radius:var(--radius-md); padding:14px;">
                <div style="font-size:12px; font-weight:800; color:var(--brand-green); text-transform:uppercase;">
                  Para você não ficar sozinho (Parada Amiga):
                </div>
                <div id="saf-companion-name" style="font-size:15px; font-weight:800; color:var(--text-main); margin-top:6px;">
                  Parada #12 · PE-60 km 18 (Posto 24h)
                </div>
                <div id="saf-companion-metrics" style="font-size:13px; font-weight:700; color:var(--brand-green); margin:4px 0;">
                  12 passageiros esperando juntos · Iluminação Boa
                </div>
                <div id="saf-companion-dist" style="font-size:12.5px; color:var(--text-secondary); margin-bottom:10px;">
                  Distância: 480m (~6 min de caminhada)
                </div>
                <button class="btn btn-primary" style="width:100%; justify-content:center;" onclick="jumpToCompanionStop()">
                  Caminhar até Esta Parada com Grupo no Mapa
                </button>
              </div>
            </div>

            <!-- Easy Report Box -->
            <div style="background:var(--bg-subtle); border:1px solid var(--border); border-radius:var(--radius-md); padding:14px;">
              <div style="font-weight:800; font-size:13.5px; margin-bottom:8px;">
                Contribuir com a Comunidade: Informar situação desta parada (100% Anônimo)
              </div>
              <div class="split-2" style="margin-bottom:10px;">
                <div>
                  <label for="saf-report-stop-select" style="font-size:12px; font-weight:700; color:var(--text-secondary); display:block; margin-bottom:4px;">Qual parada?</label>
                  <select id="saf-report-stop-select" style="width:100%; padding:8px 10px; border-radius:var(--radius-sm); border:1px solid var(--border-strong); background:var(--bg-surface); color:var(--text-main);" onchange="selectStopNode(parseInt(this.value, 10), false)"></select>
                </div>
                <div>
                  <label for="saf-report-desc" style="font-size:12px; font-weight:700; color:var(--text-secondary); display:block; margin-bottom:4px;">O que está acontecendo? (Opcional)</label>
                  <input id="saf-report-desc" type="text" placeholder="Ex: Assalto de moto / Poste apagado / Tem bastante gente aqui..." style="width:100%; padding:8px 10px; border-radius:var(--radius-sm); border:1px solid var(--border-strong); background:var(--bg-surface); color:var(--text-main);" />
                </div>
              </div>
              <div style="display:grid; grid-template-columns:repeat(2, 1fr); gap:8px;">
                <button class="btn btn-danger" style="justify-content:center;" onclick="submitSafetyReport('ROUBO_CELULAR')">
                  Alertar Roubo / Assalto Aqui
                </button>
                <button class="btn btn-amber" style="justify-content:center;" onclick="submitSafetyReport('ILUMINACAO_PRECARIA')">
                  Informar Local Escuro
                </button>
                <button class="btn" style="justify-content:center;" onclick="submitSafetyReport('PARADA_SOLITARIA')">
                  Estou Esperando Sozinho(a)
                </button>
                <button class="btn btn-primary" style="justify-content:center;" onclick="submitSafetyReport('LOCAL_SEGURO_GRUPO')">
                  Confirmar Grupo Seguro Aqui
                </button>
              </div>
            </div>

          </div>
        </div>

        <!-- Community Feed -->
        <div class="panel">
          <div class="panel-head">
            <span>Últimos Alertas Enviados pelos Passageiros na PE-60</span>
            <span class="tag tag-cyan">Tempo Real</span>
          </div>
          <div class="panel-body" id="saf-feed-container" style="display:flex; flex-direction:column; gap:10px; max-height:260px; overflow-y:auto;"></div>
        </div>
      </div>

      <!-- Right: Full 20-stop Table -->
      <div class="panel">
        <div class="panel-head">
          <span>Situação das 20 Paradas da PE-60 (Clique em qualquer parada para inspecionar)</span>
          <span class="tag tag-emerald">Rede de Companhia</span>
        </div>
        <div class="panel-body" style="max-height:740px; overflow-y:auto;">
          <table class="tech-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Parada</th>
                <th>Pessoas Agora</th>
                <th>Relatos Roubo</th>
                <th>Iluminação</th>
                <th>Orientação ao Passageiro</th>
              </tr>
            </thead>
            <tbody id="saf-corridor-tbody"></tbody>
          </table>
        </div>
      </div>

    </div>
  </main>

  <!-- ======================================================================= -->
  <!-- TAB 3: MODO BOLSO (SENSORES INERCIAIS & VOZ SEM TIRAR DO BOLSO)         -->
  <!-- ======================================================================= -->
  <main id="mod-imu" class="workspace-view">
    <div class="imu-grid">

      <!-- Left: Scenario Selector & Voice Test -->
      <div class="panel">
        <div class="panel-head">
          <span>Como o Celular Detecta Tudo Dentro do Bolso?</span>
          <span class="tag tag-emerald">14,29 µs na CPU</span>
        </div>
        <div class="panel-body">
          <p style="font-size:13.5px; color:var(--text-secondary); margin-bottom:12px;">
            Sem precisar abrir tela ou clicar em botões, a rede neural <code>ResSensorNetV2</code> lê os sensores físicos do celular (acelerômetro, giroscópio, barômetro e som ambiente) + a velocidade de saída da parada:
          </p>

          <div class="sc-item active" onclick="selectImuScenario('ALIGHTING', this)">
            <div class="sc-item-head">
              <span>1. Desembarque do Ônibus (Descida)</span>
              <span class="tag tag-emerald">0,00% Falso Positivo</span>
            </div>
            <div class="sc-item-desc">Chega a 36 km/h no ônibus, para por 30s no ponto e sai caminhando a pé (4,6 km/h). Nunca é confundido com desistência.</div>
          </div>

          <div class="sc-item" onclick="selectImuScenario('ABANDONMENT', this)">
            <div class="sc-item-head">
              <span>2. Desistência para Lotação / Ligeirinho</span>
              <span class="tag tag-crimson">99,67% Precisão</span>
            </div>
            <div class="sc-item-desc">Chega a pé, espera 38 min na parada sem ônibus oficial passar e entra em carro/van a 52 km/h sem parar no próximo ponto.</div>
          </div>

          <div class="sc-item" onclick="selectImuScenario('BOARDING_SERVED', this)">
            <div class="sc-item-head">
              <span>3. Embarque no Ônibus Oficial (Linha 178)</span>
              <span class="tag tag-cyan">99,33% Recall</span>
            </div>
            <div class="sc-item-desc">Espera na parada e embarca em sincronia com o GPS do ônibus oficial + vibração característica de motor diesel.</div>
          </div>

          <div class="sc-item" onclick="selectImuScenario('TRANSIT_BYPASS', this)">
            <div class="sc-item-head">
              <span>4. Apenas Passando Direto na Rodovia</span>
              <span class="tag tag-amber">100% Ignorado</span>
            </div>
            <div class="sc-item-desc">Passa em frente à parada a 65 km/h (permanência de apenas 15s). O filtro ignora imediatamente na borda.</div>
          </div>

          <div class="tts-box">
            <div style="font-size:11.5px; font-weight:800; color:var(--warn-amber); text-transform:uppercase; margin-bottom:4px;">
              O que o usuário escuta no fone de ouvido (Tela Apagada):
            </div>
            <div id="imu-voice-transcript" style="font-size:13.5px; font-weight:600; color:var(--text-main); margin-bottom:10px;">
              "GrafoParada Modo Bolso: Desembarque detectado na Parada Trevo de Ipojuca. Boa caminhada."
            </div>
            <button class="btn btn-amber" style="width:100%; justify-content:center;" onclick="speakImuTranscript()">
              Ouvir Áudio em Português Agora
            </button>
          </div>

          <button class="btn btn-primary" style="width:100%; justify-content:center; margin-bottom:10px;" onclick="triggerLivePyTorchInference()">
            Sortear Novas Amostras Reais (TMD) &amp; Rodar PyTorch Agora
          </button>

          <div style="font-size:12.5px; color:var(--text-secondary); display:flex; flex-direction:column; gap:4px;">
            <div>Tempo de resposta da IA na CPU: <strong id="imu-live-cpu-us" class="mono" style="color:var(--user-blue);">14,29 µs</strong></div>
            <div>Memória gasta para aprender sua rotina (4º dia): <strong>166 Bytes locais</strong></div>
            <div>Dados enviados para a internet: <strong id="imu-net-counter" style="color:var(--brand-green);">0 Bytes (Silêncio Total)</strong></div>
          </div>
        </div>
      </div>

      <!-- Right: Live Oscilloscope + Probabilities + Step Table -->
      <div class="panel">
        <div class="panel-head">
          <span>Leitura dos Sensores em Tempo Real (Dataset TMD) &amp; Decisão da Máquina de Estados</span>
          <span id="imu-verdict-tag" class="tag tag-emerald">Veredito: Desembarque</span>
        </div>
        <div class="panel-body">
          <div style="display:flex; justify-content:space-between; flex-wrap:wrap; gap:8px; font-size:12.5px; color:var(--text-secondary); margin-bottom:6px;">
            <span>Ondas físicas: <strong style="color:#10b981;">Acelerômetro (m/s²)</strong> · <strong style="color:#38bdf8;">Giroscópio (rad/s)</strong> · <strong style="color:#f59e0b;">Ruído Acústico (dB)</strong></span>
            <strong id="osc-phase-label">Fase Pós-Parada: Caminhando a Pé (4,6 km/h)</strong>
          </div>

          <div class="osc-wrap">
            <canvas id="imu-osc-canvas"></canvas>
          </div>

          <div style="font-size:12px; font-weight:700; color:var(--text-muted); text-transform:uppercase; margin-bottom:6px;">
            Certeza da Rede Neural por Modal (Soft-Voting nas 26 variáveis físicas):
          </div>
          <div class="prob-strip">
            <div class="prob-cell">
              <div style="display:flex; justify-content:space-between; font-size:13px; font-weight:700;">
                <span>Parado (Still)</span><span id="p-val-still" class="mono">2,0%</span>
              </div>
              <div class="prob-bar-track"><div id="p-bar-still" class="prob-bar-fill" style="width:2%;"></div></div>
            </div>
            <div class="prob-cell">
              <div style="display:flex; justify-content:space-between; font-size:13px; font-weight:700;">
                <span>A Pé (Walking)</span><span id="p-val-walk" class="mono" style="color:var(--brand-green);">95,0%</span>
              </div>
              <div class="prob-bar-track"><div id="p-bar-walk" class="prob-bar-fill" style="width:95%; background:var(--brand-green);"></div></div>
            </div>
            <div class="prob-cell">
              <div style="display:flex; justify-content:space-between; font-size:13px; font-weight:700;">
                <span>Ônibus (Bus)</span><span id="p-val-bus" class="mono">2,0%</span>
              </div>
              <div class="prob-bar-track"><div id="p-bar-bus" class="prob-bar-fill" style="width:2%;"></div></div>
            </div>
            <div class="prob-cell">
              <div style="display:flex; justify-content:space-between; font-size:13px; font-weight:700;">
                <span>Carro/Van (Car)</span><span id="p-val-car" class="mono" style="color:var(--danger-red);">1,0%</span>
              </div>
              <div class="prob-bar-track"><div id="p-bar-car" class="prob-bar-fill" style="width:1%; background:var(--danger-red);"></div></div>
            </div>
          </div>

          <div style="overflow-x:auto; margin-bottom:12px;">
            <table class="tech-table">
              <thead>
                <tr>
                  <th>Minuto</th>
                  <th>Etapa do Trajeto</th>
                  <th>Distância da Parada</th>
                  <th>Velocidade</th>
                  <th>Vibração / Giro</th>
                  <th>Som Ambiente</th>
                  <th>Classificação da IA</th>
                </tr>
              </thead>
              <tbody id="imu-frames-tbody"></tbody>
            </table>
          </div>

          <div id="imu-wire-box" class="code-box"></div>
        </div>
      </div>

    </div>
  </main>

  <!-- ======================================================================= -->
  <!-- TAB 4: AUDITORIA AO VIVO DO SERVIDOR CITTAMOBI (m3p API)                -->
  <!-- ======================================================================= -->
  <main id="mod-citta" class="workspace-view">
    <div class="split-2">

      <div class="panel">
        <div class="panel-head">
          <span>Auditoria ao Vivo: Servidor Cittamobi Grande Recife (`api.cittamobi.com.br`)</span>
          <div style="display:flex; gap:8px; align-items:center;">
            <button class="btn btn-amber" onclick="refreshLiveCittamobiFleet()">Consultar Frota Cittamobi Agora</button>
            <span id="citta-fleet-badge" class="tag tag-crimson">0 Ônibus Transmitindo</span>
          </div>
        </div>
        <div class="panel-body">
          <p style="font-size:13.5px; color:var(--text-secondary); margin-bottom:12px;">
            Consultando diretamente a API pública do Cittamobi para a Agência <code>a=202</code> (Grande Recife Consórcio) nas linhas operadas pela <strong>Expresso Vera Cruz</strong> e <strong>São Judas Tadeu</strong> ao longo da PE-60:
          </p>
          <div style="overflow-x:auto;">
            <table class="tech-table">
              <thead>
                <tr>
                  <th>ID Serviço</th>
                  <th>Linha</th>
                  <th>Nome no Cittamobi</th>
                  <th>Empresa</th>
                  <th>Resposta em Tempo Real</th>
                </tr>
              </thead>
              <tbody id="citta-services-tbody"></tbody>
            </table>
          </div>

          <div style="margin-top:14px; background:var(--warn-amber-bg); border:1px solid var(--warn-amber-border); border-radius:var(--radius-md); padding:12px;">
            <strong style="color:var(--warn-amber); font-size:13px;">Descoberta da Auditoria: Erro de OCR no Cadastro da PE-60</strong>
            <p style="font-size:13px; color:var(--text-main); margin-top:4px;">
              Entre o km 15 e o km 19 da PE-60 (paradas <code>2965548</code>, <code>2966773</code>, <code>2966472</code>), o banco de dados do Cittamobi registrou o nome da rodovia corrompido por leitura óptica como <strong>"Rodovia Armínio Cuil Hi Rme"</strong> (em vez de <em>Rodovia Armínio Guilherme / PE-060</em>) e retorna lista vazia (<code>services: []</code>) para quem espera no ponto.
            </p>
          </div>
        </div>
      </div>

      <div style="display:flex; flex-direction:column; gap:16px;">
        <div class="panel">
          <div class="panel-head">
            <span>Comparativo Técnico: Machine Learning do Cittamobi vs. GrafoParada</span>
            <span class="tag tag-emerald">+58,8 pontos de F1-Score</span>
          </div>
          <div class="panel-body">
            <p style="font-size:13.5px; color:var(--text-secondary); margin-bottom:10px;">
              O estudo aberto <code>Leonardo0liveira/ML-Cittamobi</code> tentou prever embarques usando apenas os cliques de tela salvos no Google BigQuery da Cittamobi. Veja por que a leitura física no bolso (GrafoParada) é muito mais precisa:
            </p>
            <table class="tech-table">
              <thead>
                <tr>
                  <th>Critério</th>
                  <th>Cittamobi (Cliques na Tela)</th>
                  <th>GrafoParada (Sensores no Bolso)</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>Como detecta o passageiro</strong></td>
                  <td>Exige abrir o celular na rua e clicar na parada</td>
                  <td style="color:var(--brand-green); font-weight:700;">Automático no bolso (26 sinais físicos + velocidade)</td>
                </tr>
                <tr>
                  <td><strong>Segurança pessoal na parada</strong></td>
                  <td style="color:var(--danger-red);">Expõe o usuário com tela acesa na rodovia</td>
                  <td style="color:var(--brand-green); font-weight:700;">Tela apagada + aviso por voz no fone de ouvido</td>
                </tr>
                <tr>
                  <td><strong>Precisão (F1-Score)</strong></td>
                  <td class="mono" style="color:var(--danger-red);">40,85% (Random Forest) / 48,01% (CatBoost)</td>
                  <td class="mono" style="color:var(--brand-green); font-weight:700;">99,67% (ResSensorNetV2 + Soft-Voting)</td>
                </tr>
                <tr>
                  <td><strong>Consumo de internet ao abrir</strong></td>
                  <td class="mono">142,4 KB (Cabo) a 274,5 KB (Recife) + pacotes a cada 15s</td>
                  <td class="mono" style="color:var(--brand-green); font-weight:700;">0 Bytes na rotina normal (36 Bytes se houver desistência)</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="panel">
          <div class="panel-head">
            <span>Correspondência das 20 Paradas: GTFS Oficial CTM &harr; IDs Cittamobi</span>
            <span class="tag tag-cyan">Desvio médio: 20,4m</span>
          </div>
          <div class="panel-body" style="max-height:280px; overflow-y:auto;">
            <table class="tech-table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>GTFS ID</th>
                  <th>Nome Oficial CTM</th>
                  <th>ID Cittamobi</th>
                  <th>Endereço no Cittamobi</th>
                  <th>Diferença</th>
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
  <!-- TAB 5: RESULTADOS CIENTÍFICOS (v1->v4) & PRIVACIDADE LGPD               -->
  <!-- ======================================================================= -->
  <main id="mod-bench" class="workspace-view">
    <div class="split-2">

      <div class="panel">
        <div class="panel-head">
          <span>Evolução dos Modelos (v1.0 &rarr; v4.0 em 1.200 Viagens na PE-60)</span>
          <span class="tag tag-emerald">Zero Falsos Positivos</span>
        </div>
        <div class="panel-body">
          <table class="tech-table" style="margin-bottom:16px;">
            <thead>
              <tr>
                <th>Versão</th>
                <th>O que evoluiu na arquitetura</th>
                <th>Acurácia Sensores</th>
                <th>Acurácia Global</th>
                <th>Acerto Descida</th>
                <th>Erro Descida (FP)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td class="mono"><strong>v1.0</strong></td>
                <td>Rede simples (12 variáveis) olhando apenas 1 janela isolada</td>
                <td class="mono">75,29%</td>
                <td class="mono">67,75%</td>
                <td class="mono">56,33%</td>
                <td class="mono" style="color:var(--brand-green);">0,00%</td>
              </tr>
              <tr>
                <td class="mono"><strong>v2.0</strong></td>
                <td>26 variáveis físicas + rede residual <code>ResSensorNetV2</code></td>
                <td class="mono">86,96%</td>
                <td class="mono">84,67%</td>
                <td class="mono">84,00%</td>
                <td class="mono" style="color:var(--brand-green);">0,00%</td>
              </tr>
              <tr class="selected-row">
                <td class="mono"><strong style="color:var(--brand-green);">v3.0 / v4.0</strong></td>
                <td><strong>Soft-Voting multi-janela + Velocidade (v = &Delta;d/&Delta;t) + GPS CTM</strong></td>
                <td class="mono" style="color:var(--brand-green); font-weight:800;">97,42%</td>
                <td class="mono" style="color:var(--brand-green); font-weight:800;">99,67%</td>
                <td class="mono" style="color:var(--brand-green); font-weight:800;">99,33%</td>
                <td class="mono" style="color:var(--brand-green); font-weight:800;">0,00% (0/300)</td>
              </tr>
            </tbody>
          </table>

          <div style="font-size:12px; font-weight:700; color:var(--text-muted); text-transform:uppercase; margin-bottom:6px;">
            Por que usar Grafo Espaço-Temporal (STGCN) no corredor inteiro de 20 paradas?
          </div>
          <table class="tech-table">
            <thead>
              <tr>
                <th>Tamanho da Malha</th>
                <th>Persistência</th>
                <th>Regressão Linear (Sem Grafo)</th>
                <th>STGCN (Grafo Laplaciano)</th>
                <th>Conclusão</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Recorte Curto (5 paradas)</strong></td>
                <td class="mono">14,91 min</td>
                <td class="mono" style="color:var(--brand-green); font-weight:700;">2,46 min</td>
                <td class="mono">4,42 min</td>
                <td>Em trecho curto, o modelo linear simples é suficiente</td>
              </tr>
              <tr class="selected-row">
                <td><strong>Corredor PE-60 Completo (20 paradas)</strong></td>
                <td class="mono">7,13 min</td>
                <td class="mono">1,93 min</td>
                <td class="mono" style="color:var(--brand-green); font-weight:800;">1,51 min (-21,8% erro)</td>
                <td>No corredor completo, o Grafo STGCN vence com folga</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="panel">
        <div class="panel-head">
          <span>Economia de Dados Móveis &amp; Proteção Total de Privacidade (LGPD)</span>
          <span class="tag tag-cyan">Zero Dados Pessoais</span>
        </div>
        <div class="panel-body">
          <div style="background:var(--bg-subtle); border:1px solid var(--border); border-radius:var(--radius-md); padding:14px; margin-bottom:14px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
              <span style="font-weight:700; font-size:13.5px;">Simular quantidade de passageiros usando por dia no Grande Recife:</span>
              <strong id="sim-pax-label" class="mono" style="color:var(--brand-green); font-size:16px;">50.000 passageiros/dia</strong>
            </div>
            <input type="range" id="sim-pax-slider" min="5000" max="500000" step="5000" value="50000" oninput="updateCostSimulator(this.value)" />
          </div>

          <table class="tech-table" style="margin-bottom:14px;">
            <thead>
              <tr>
                <th>Indicador Mensal (30 dias)</th>
                <th>Modelo Tradicional (Polling Cittamobi)</th>
                <th>GrafoParada (Processamento no Bolso)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Chamadas ao Servidor por Mês</strong></td>
                <td class="mono" id="sim-citta-reqs" style="color:var(--danger-red);">150.000.000 reqs/mês</td>
                <td class="mono" id="sim-gp-reqs" style="color:var(--brand-green); font-weight:800;">225.000 reqs/mês</td>
              </tr>
              <tr>
                <td><strong>Tráfego Total de Internet</strong></td>
                <td class="mono" id="sim-citta-gb" style="color:var(--danger-red);">811,61 GB / mês</td>
                <td class="mono" id="sim-gp-gb" style="color:var(--brand-green); font-weight:800;">0,0077 GB / mês (7,9 MB)</td>
              </tr>
              <tr>
                <td><strong>Dados Pessoais Rastreados</strong></td>
                <td>ID do Aparelho, Conta, IP e Histórico de Rotas</td>
                <td style="color:var(--brand-green); font-weight:700;">Nenhum (Fila anônima apagada a cada 10 min · k&ge;3)</td>
              </tr>
            </tbody>
          </table>

          <div style="font-size:12px; font-weight:700; color:var(--text-muted); text-transform:uppercase; margin-bottom:6px;">
            Aprendizado da Rotina no Próprio Aparelho (Ativa o aviso de voz sozinho no 4º dia útil):
          </div>
          <div style="display:grid; grid-template-columns:repeat(7, 1fr); gap:6px; text-align:center; font-size:12px;">
            <div style="background:var(--bg-subtle); border:1px solid var(--border); border-radius:var(--radius-sm); padding:8px;"><strong>Dia 1</strong><br>Score 0.28<br><span style="color:var(--text-muted);">Observando</span></div>
            <div style="background:var(--bg-subtle); border:1px solid var(--border); border-radius:var(--radius-sm); padding:8px;"><strong>Dia 2</strong><br>Score 0.54<br><span style="color:var(--text-muted);">Observando</span></div>
            <div style="background:var(--warn-amber-bg); border:1px solid var(--warn-amber-border); border-radius:var(--radius-sm); padding:8px;"><strong>Dia 3</strong><br>Score 0.76<br><span style="color:var(--warn-amber);">Quase lá</span></div>
            <div style="background:var(--brand-green-bg); border:1px solid var(--brand-green-border); border-radius:var(--radius-sm); padding:8px;"><strong>Dia 4</strong><br><strong style="color:var(--brand-green);">Score 0.95</strong><br><span style="color:var(--brand-green); font-weight:700;">Voz Ativa!</span></div>
            <div style="background:var(--brand-green-bg); border:1px solid var(--brand-green-border); border-radius:var(--radius-sm); padding:8px;"><strong>Dia 5</strong><br><strong style="color:var(--brand-green);">Score 1.00</strong><br><span style="color:var(--brand-green); font-weight:700;">100% Recall</span></div>
            <div style="background:var(--bg-subtle); border:1px dashed var(--border); border-radius:var(--radius-sm); padding:8px;"><strong>Sábado</strong><br>Folga<br><span style="color:var(--text-muted);">0% Alarme Falso</span></div>
            <div style="background:var(--bg-subtle); border:1px dashed var(--border); border-radius:var(--radius-sm); padding:8px;"><strong>Domingo</strong><br>Folga<br><span style="color:var(--text-muted);">0% Alarme Falso</span></div>
          </div>
        </div>
      </div>

    </div>
  </main>

  <script>
    const TELEMETRIA = __TELEMETRIA_JSON__;

    let activeStopSeq = 11;
    let gisLayerMode = "grafoparada";
    let showCittamobi534 = false; // Default OFF so the map is super clean & readable!

    // =========================================================================
    // THEME TOGGLE (DAYLIGHT CLEAN DEFAULT vs. NIGHT MODE)
    // =========================================================================
    function toggleTheme() {
      const html = document.documentElement;
      const cur = html.getAttribute("data-theme") || "light";
      const next = cur === "light" ? "dark" : "light";
      html.setAttribute("data-theme", next);
      const btn = document.getElementById("theme-toggle-btn");
      if (btn) btn.textContent = next === "light" ? "Modo Noturno" : "Modo Claro Solar";
      setBaseTile(next === "dark" ? "dark" : "osm");
    }

    // =========================================================================
    // NAVIGATION & CLOCK
    // =========================================================================
    function switchModule(modId, btnEl) {
      document.querySelectorAll(".workspace-view").forEach(v => v.classList.remove("active"));
      document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
      document.getElementById(modId).classList.add("active");
      if (btnEl) btnEl.classList.add("active");
      if (modId === "mod-gis") requestAnimationFrame(drawPe60GisCanvas);
    }

    window.addEventListener("keydown", (e) => {
      const btns = document.querySelectorAll(".tab-btn");
      if (e.key === "F1") { e.preventDefault(); switchModule("mod-gis", btns[0]); }
      if (e.key === "F2") { e.preventDefault(); switchModule("mod-safety", btns[1]); }
      if (e.key === "F3") { e.preventDefault(); switchModule("mod-imu", btns[2]); }
      if (e.key === "F4") { e.preventDefault(); switchModule("mod-citta", btns[3]); }
      if (e.key === "F5") { e.preventDefault(); switchModule("mod-bench", btns[4]); }
    });

    setInterval(() => {
      const now = new Date();
      document.getElementById("live-clock").textContent = now.toTimeString().slice(0, 8);
    }, 1000);

    // =========================================================================
    // MODULE 01: CLEAN INTERACTIVE MAP OF PE-60 (LEAFLET)
    // =========================================================================
    function initQuickStopButtons() {
      const wrap = document.getElementById("quick-stop-selector");
      wrap.innerHTML = TELEMETRIA.stops.map(s => {
        const isCrit = s.operational_state === "CRITICAL";
        const isWarn = s.operational_state === "WARNING";
        const col = isCrit ? "#dc2626" : (isWarn ? "#d97706" : "#0a6b46");
        return `<button id="qbtn-${s.seq}" class="btn ${s.seq === activeStopSeq ? 'active' : ''}" style="padding:4px 9px; min-height:32px; font-size:12px; border-bottom:3px solid ${col};" onclick="selectStopNode(${s.seq}, true)">#${String(s.seq).padStart(2, '0')}</button>`;
      }).join("");
    }

    function setGisLayer(mode) {
      gisLayerMode = mode;
      document.getElementById("btn-layer-gp").classList.toggle("active", mode === "grafoparada");
      document.getElementById("btn-layer-catraca").classList.toggle("active", mode === "catraca");
      drawPe60GisCanvas();
    }

    function toggleCittamobi534() {
      showCittamobi534 = !showCittamobi534;
      document.getElementById("lbl-citta-toggle").textContent = showCittamobi534 ? "ON" : "OFF";
      document.getElementById("btn-layer-citta").classList.toggle("active", showCittamobi534);
      drawPe60GisCanvas();
    }

    let leafletMap = null;
    let baseTileLayers = {};
    let currentTileLayer = null;
    let cittaLayerGroup = null;
    let corridorPolylineLayer = null;
    let corridorGlowLayer = null;
    let stopsLayerGroup = null;
    let userRadarLayerGroup = null;
    let userMarker = null;
    let userPos = { lat: -8.304950, lon: -35.021420, label: "Na Parada #11 (PE-60 · Trevo Ipojuca)" };
    let lastPocketVoicePrompt = "GrafoParada Modo Bolso ativo.";

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
          attribution: "&copy; OpenStreetMap contributors"
        }),
        dark: L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
          maxZoom: 19,
          className: "tile-dark-filter",
          attribution: "&copy; OpenStreetMap contributors"
        }),
        sat: L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", {
          maxZoom: 19,
          attribution: "&copy; Esri World Imagery"
        })
      };

      currentTileLayer = baseTileLayers.osm;
      currentTileLayer.addTo(leafletMap);

      cittaLayerGroup = L.layerGroup().addTo(leafletMap);
      stopsLayerGroup = L.layerGroup().addTo(leafletMap);
      userRadarLayerGroup = L.layerGroup().addTo(leafletMap);

      if (TELEMETRIA.polyline && TELEMETRIA.polyline.length > 1) {
        corridorGlowLayer = L.polyline(TELEMETRIA.polyline, {
          color: "#0057b8",
          weight: 10,
          opacity: 0.22
        }).addTo(leafletMap);

        corridorPolylineLayer = L.polyline(TELEMETRIA.polyline, {
          color: "#0057b8",
          weight: 4.5,
          opacity: 0.90
        }).addTo(leafletMap);
      }

      leafletMap.on("click", (ev) => {
        setSimulatedUserLocation(
          ev.latlng.lat,
          ev.latlng.lng,
          "Posição escolhida por clique no mapa",
          false
        );
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
      document.getElementById("btn-tile-dark").classList.toggle("active", mode === "dark");
      document.getElementById("btn-tile-sat").classList.toggle("active", mode === "sat");
    }

    function drawPe60GisCanvas() {
      initRealLeafletMap();
      leafletMap.invalidateSize();

      cittaLayerGroup.clearLayers();
      if (showCittamobi534 && TELEMETRIA.cittamobi_viewport_534_stops) {
        TELEMETRIA.cittamobi_viewport_534_stops.forEach((cs) => {
          const cm = L.circleMarker([cs.lat, cs.lon], {
            radius: 3.5,
            color: "#475569",
            weight: 1,
            fillColor: "#94a3b8",
            fillOpacity: 0.7
          });
          cm.bindTooltip(
            `Parada Cittamobi #${cs.id}: ${cs.mnemonic || 'Sem nome'} (Veículos ativos: ${cs.active_services})`,
            { className: "sicoe-tooltip", direction: "top" }
          );
          cittaLayerGroup.addLayer(cm);
        });
      }

      // Render numbered pill markers (#01..#20) without cluttering the map with overlapping boxes
      stopsLayerGroup.clearLayers();
      TELEMETRIA.stops.forEach((st) => {
        const isCatraca = gisLayerMode === "catraca";
        let bgColor = "#0a6b46";
        if (!isCatraca) {
          if (st.operational_state === "CRITICAL") bgColor = "#dc2626";
          else if (st.operational_state === "WARNING") bgColor = "#d97706";
        }
        const isSelected = st.seq === activeStopSeq;

        const pillIcon = L.divIcon({
          className: "",
          html: `<div class="stop-map-pill ${isSelected ? 'selected' : ''}" style="background:${bgColor};">#${String(st.seq).padStart(2, '0')}</div>`,
          iconSize: [34, 22],
          iconAnchor: [17, 11]
        });

        const marker = L.marker([st.lat, st.lon], { icon: pillIcon });
        const ttText = `Parada #${String(st.seq).padStart(2, '0')}: ${st.name} | Espera prevista: ${st.stgcn_horizon_min[2]} min | Desistências: ${st.abandonment_10m}`;
        marker.bindTooltip(ttText, {
          permanent: isSelected,
          direction: "top",
          offset: [0, -12],
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
      document.getElementById("insp-stop-header").textContent = `Parada #${String(st.seq).padStart(2, '0')} · ${st.name} (Código ${st.stop_id})`;
      document.getElementById("insp-coords").textContent = `${st.lat.toFixed(6)}, ${st.lon.toFixed(6)} (Horário tabela: ${st.scheduled_time})`;

      const hasOcrBug = st.cittamobi_mnemonic.includes("Cuil Hi Rme");
      document.getElementById("insp-citta").innerHTML =
        `ID #${st.cittamobi_id} · "${st.cittamobi_mnemonic}" ` +
        (hasOcrBug ? `<span class="tag tag-amber">Erro de OCR no Cittamobi</span> ` : ``) +
        `(0 ônibus ativos)`;

      document.getElementById("insp-catraca").textContent =
        st.catraca_boardings_40m === 0
          ? `0 passageiros na catraca nos últimos 40 min (Como o ônibus atrasou, a catraca acha que não há demanda)`
          : `${st.catraca_boardings_40m} embarques registrados normalmente na catraca`;

      document.getElementById("insp-abn").textContent =
        st.k_anonymity_unlocked
          ? `${st.abandonment_10m} trabalhadores desistiram nos últimos 10 min e embarcaram em transporte alternativo`
          : `${st.abandonment_10m} eventos (Ocultado por privacidade LGPD porque é menor que 3 pessoas)`;

      const h = st.stgcn_horizon_min;
      document.getElementById("insp-stgcn").innerHTML =
        `Em 10m: ${h[0].toFixed(1)} min | Em 20m: ${h[1].toFixed(1)} min | <strong>Em 30m: ${h[2].toFixed(1)} min</strong>`;

      const tag = document.getElementById("insp-stop-tag");
      if (st.operational_state === "CRITICAL") {
        tag.className = "tag tag-crimson";
        tag.textContent = `Crítica · ${st.abandonment_10m} Desistências`;
      } else if (st.operational_state === "WARNING") {
        tag.className = "tag tag-amber";
        tag.textContent = `Atenção (Espera 35–40 min)`;
      } else {
        tag.className = "tag tag-emerald";
        tag.textContent = `Operação Normal`;
      }

      drawPe60GisCanvas();
      if (panMap && leafletMap) {
        leafletMap.panTo([st.lat, st.lon], { animate: true, duration: 0.4 });
      }
      pingLiveCittamobiStop();
      runLiveStgcnInference();
      if (typeof renderSelectedStopSafetyPanel === "function") {
        renderSelectedStopSafetyPanel(seq);
      }
    }

    function triggerGtfsPatch() {
      const st = TELEMETRIA.stops.find(s => s.seq === activeStopSeq) || TELEMETRIA.stops[10];
      const out = document.getElementById("gtfs-patch-output");
      out.textContent =
`[ORDEM DE REMANEJAMENTO EMITIDA PELO CONTROLADOR CTM]
Veículo Remanejado: Prefixo #178-09 (Estava ocioso na Parada #19 Rotatória Suape com <8% ocupação)
Nova Partida Expressa: Atendimento direto à Parada #${String(st.seq).padStart(2, '0')} (${st.name} - GTFS ${st.stop_id})
Impacto Estimado: Tempo de espera cai de ${st.stgcn_horizon_min[2].toFixed(1)} min para 18,5 min (Custo adicional: R$ 0,00).`;
    }

    // =========================================================================
    // MODULE 03: REAL-TIME IMU OSCILLOSCOPE & KINEMATIC FSM
    // =========================================================================
    const IMU_SCENARIOS = {
      ALIGHTING: {
        verdict: "Veredito: Desembarque Detectado (0,00% Falso Positivo)",
        tagClass: "tag-emerald",
        phaseLabel: "Fase Pós-Parada: Caminhando a Pé (4,6 km/h)",
        tmdClass: "Walking",
        voice: "GrafoParada Modo Bolso: Desembarque detectado na Parada Trevo de Ipojuca. Boa caminhada.",
        netStatus: "0 Bytes (Processado 100% no aparelho)",
        probs: { still: 2.0, walk: 95.0, bus: 2.0, car: 1.0 },
        wire: `[PRIVACIDADE LGPD] -> Nenhum pacote enviado pela internet (0 Bytes).\nExplicação: Você chegou a 36 km/h no ônibus, ficou 30s na parada e saiu caminhando a 4,6 km/h (95% certeza de caminhada). Classificado como Desembarque normal.`,
        frames: [
          { t: "0,0 min", stage: "Chegando no Ônibus (PE-60)", dist: "650 m", v: "36,0 km/h", imu: "1,42 m/s² | 0,09 rad/s", db: "78,4 dB", cls: "Ônibus (94%)" },
          { t: "1,5 min", stage: "Parou no Ponto (Raio 35m)", dist: "6 m", v: "0,0 km/h", imu: "0,04 m/s² | 0,01 rad/s", db: "68,2 dB", cls: "Parado (91%)" },
          { t: "2,0 min", stage: "Descendo os Degraus (30s)", dist: "8 m", v: "1,8 km/h", imu: "0,35 m/s² | 0,03 rad/s", db: "66,0 dB", cls: "Descendo" },
          { t: "3,0 min", stage: "Caminhando na Calçada", dist: "85 m", v: "4,6 km/h", imu: "3,85 m/s² | 0,41 rad/s", db: "62,1 dB", cls: "A Pé (96%)" },
          { t: "4,2 min", stage: "Seguindo a Pé para Casa/Trabalho", dist: "180 m", v: "4,8 km/h", imu: "4,12 m/s² | 0,44 rad/s", db: "60,5 dB", cls: "A Pé (97%)" }
        ]
      },
      ABANDONMENT: {
        verdict: "Veredito: Desistência para Transporte Alternativo (99,67% F1)",
        tagClass: "tag-crimson",
        phaseLabel: "Fase Pós-Parada: Embarcou em Carro/Lotação (52,4 km/h)",
        tmdClass: "Car",
        voice: "GrafoParada Modo Bolso: Aviso na Parada Trevo de Ipojuca. Linha 178 Suape atrasada há 38 minutos. Registrando desistência anônima para reforço de frota.",
        netStatus: "1 Alerta Anônimo (36 Bytes)",
        probs: { still: 1.0, walk: 1.0, bus: 3.0, car: 95.0 },
        wire: `[PACOTE ANÔNIMO DE 36 BYTES ENVIADO AO CTM] -> {"s":"030192","e":"ABN","t":378}\nSem nome, sem CPF, sem ID do celular. O servidor só libera para o painel se pelo menos 3 pessoas desistirem juntas (k-anonimato >= 3).`,
        frames: [
          { t: "0,0 min", stage: "Chegou Caminhando na Parada", dist: "65 m", v: "4,5 km/h", imu: "3,70 m/s² | 0,38 rad/s", db: "64,0 dB", cls: "A Pé (93%)" },
          { t: "18,0 min", stage: "Esperando na Parada", dist: "4 m", v: "0,0 km/h", imu: "0,03 m/s² | 0,01 rad/s", db: "73,5 dB", cls: "Parado (99%)" },
          { t: "38,0 min", stage: "Espera Crítica (Sem Ônibus Oficial)", dist: "5 m", v: "0,4 km/h", imu: "0,08 m/s² | 0,02 rad/s", db: "75,0 dB", cls: "Parado (97%)" },
          { t: "38,5 min", stage: "Entrou em Lotação / Ligeirinho", dist: "240 m", v: "46,8 km/h", imu: "1,85 m/s² | 0,19 rad/s", db: "88,4 dB", cls: "Carro/Van (94%)" },
          { t: "39,2 min", stage: "Passou Direto pela Parada Seguinte", dist: "890 m", v: "55,2 km/h", imu: "1,92 m/s² | 0,22 rad/s", db: "89,1 dB", cls: "Carro/Van (96%)" }
        ]
      },
      BOARDING_SERVED: {
        verdict: "Veredito: Embarque no Ônibus Oficial CTM (99,33%)",
        tagClass: "tag-cyan",
        phaseLabel: "Fase Pós-Parada: Viajando no Ônibus Oficial (29,8 km/h)",
        tmdClass: "Bus",
        voice: "GrafoParada Modo Bolso: O ônibus da Linha 178 Porto de Suape está encostando na parada agora.",
        netStatus: "0 Bytes (Viagem Normal Atendida)",
        probs: { still: 2.0, walk: 1.0, bus: 94.0, car: 3.0 },
        wire: `[PRIVACIDADE LGPD] -> Nenhum pacote enviado (0 Bytes).\nExplicação: Você embarcou em sincronia com o GPS do ônibus oficial da Linha 178 e parou normalmente no ponto seguinte da rota.`,
        frames: [
          { t: "0,0 min", stage: "Chegou a Pé na Parada", dist: "80 m", v: "4,4 km/h", imu: "3,62 m/s² | 0,36 rad/s", db: "63,5 dB", cls: "A Pé (94%)" },
          { t: "14,5 min", stage: "Ônibus Linha 178 Encostou", dist: "5 m", v: "1,2 km/h", imu: "0,65 m/s² | 0,05 rad/s", db: "81,2 dB", cls: "Subindo" },
          { t: "15,2 min", stage: "Partida no Ônibus Oficial", dist: "210 m", v: "31,5 km/h", imu: "1,34 m/s² | 0,07 rad/s", db: "79,5 dB", cls: "Ônibus (93%)" },
          { t: "16,0 min", stage: "Parou na Parada Seguinte da Linha", dist: "520 m", v: "28,4 km/h", imu: "1,29 m/s² | 0,06 rad/s", db: "78,8 dB", cls: "Ônibus (95%)" }
        ]
      },
      TRANSIT_BYPASS: {
        verdict: "Veredito: Passagem Direta na Rodovia (100% Ignorado)",
        tagClass: "tag-amber",
        phaseLabel: "Fase Contínua: Passando pela Rodovia PE-60 (65,2 km/h)",
        tmdClass: "Car",
        voice: "Modo Bolso em silêncio: Usuário apenas passando pela rodovia PE-60 sem parar no ponto.",
        netStatus: "0 Bytes (Ignorado na Borda)",
        probs: { still: 0.0, walk: 0.0, bus: 12.0, car: 88.0 },
        wire: `[FILTRO DE BORDA] -> Descartado imediatamente (0 Bytes).\nExplicação: Cruzou o raio de 35m da parada em apenas 15 segundos a 65 km/h. Não estava esperando ônibus.`,
        frames: [
          { t: "0,00 min", stage: "Trafegando na PE-60 (Antes)", dist: "450 m", v: "64,0 km/h", imu: "1,65 m/s² | 0,14 rad/s", db: "86,2 dB", cls: "Carro (89%)" },
          { t: "0,25 min", stage: "Cruzou Raio de 35m (Apenas 15s)", dist: "15 m", v: "65,2 km/h", imu: "1,61 m/s² | 0,13 rad/s", db: "87,0 dB", cls: "Carro (88%)" },
          { t: "0,55 min", stage: "Trafegando na PE-60 (Depois)", dist: "480 m", v: "66,0 km/h", imu: "1,70 m/s² | 0,15 rad/s", db: "86,8 dB", cls: "Carro (90%)" }
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
      document.getElementById("imu-net-counter").style.color = key === "ABANDONMENT" ? "var(--warn-amber)" : "var(--brand-green)";

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
          <td class="mono" style="font-weight:700;">${f.cls}</td>
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

        ctx.fillStyle = "#0d1117";
        ctx.fillRect(0, 0, W, H);

        ctx.strokeStyle = "#1f2937";
        ctx.lineWidth = 1;
        for (let x = 0; x < W; x += 40) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke(); }
        for (let y = 0; y < H; y += 35) { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke(); }

        const tmdClass = IMU_SCENARIOS[currentImuKey].tmdClass;
        const series = TELEMETRIA.tmd_real_windows[tmdClass] || TELEMETRIA.tmd_real_windows["Walking"];
        const N = 60;

        ctx.beginPath();
        for (let i = 0; i < N; i++) {
          const item = series[(i + Math.floor(oscTick)) % series.length];
          const val = item.acc_mean + Math.sin((i + oscTick) * 0.45) * item.acc_std;
          const x = (i / (N - 1)) * W;
          const y = H - Math.min(H - 12, Math.max(12, (val / 22.0) * (H - 24)));
          if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
        }
        ctx.strokeStyle = "#10b981";
        ctx.lineWidth = 2.2;
        ctx.stroke();

        ctx.beginPath();
        for (let i = 0; i < N; i++) {
          const item = series[(i + Math.floor(oscTick)) % series.length];
          const val = item.gyro_mean * 18.0 + Math.cos((i + oscTick) * 0.6) * item.gyro_std * 15.0;
          const x = (i / (N - 1)) * W;
          const y = H * 0.72 - Math.min(H * 0.6, Math.max(-30, val * 12));
          if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
        }
        ctx.strokeStyle = "#38bdf8";
        ctx.lineWidth = 1.8;
        ctx.stroke();

        ctx.beginPath();
        for (let i = 0; i < N; i++) {
          const item = series[(i + Math.floor(oscTick)) % series.length];
          const x = (i / (N - 1)) * W;
          const y = H - ((item.sound_db - 40) / 60.0) * (H - 30);
          if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
        }
        ctx.strokeStyle = "#f59e0b";
        ctx.lineWidth = 1.4;
        ctx.stroke();

        ctx.restore();
        oscTick += 0.25;
      }
      requestAnimationFrame(renderImuOscilloscope);
    }

    // =========================================================================
    // MODULE 04 & 05: CITTAMOBI TABLES & PRIVACY CALCULATOR
    // =========================================================================
    function populateCittamobiTables() {
      const svTbody = document.getElementById("citta-services-tbody");
      svTbody.innerHTML = TELEMETRIA.cittamobi_services.slice(0, 10).map(sv => `
        <tr>
          <td class="mono">${sv.serviceId}</td>
          <td class="mono"><strong>${sv.routeCode}</strong> (${sv.direction === 'OUTWARD' ? 'Ida' : 'Volta'})</td>
          <td>${sv.serviceMnemonic}</td>
          <td>${sv.companyName}</td>
          <td><span class="tag tag-crimson">${sv.activeVehicles} ônibus (${sv.latencyMs}ms)</span></td>
        </tr>
      `).join("");

      const mapTbody = document.getElementById("citta-mapping-tbody");
      mapTbody.innerHTML = TELEMETRIA.stops.map(s => `
        <tr onclick="switchModule('mod-gis', document.querySelectorAll('.tab-btn')[0]); selectStopNode(${s.seq}, true);" style="cursor:pointer;">
          <td class="mono"><strong>#${String(s.seq).padStart(2, '0')}</strong></td>
          <td class="mono">${s.stop_id}</td>
          <td>${s.name}</td>
          <td class="mono">#${s.cittamobi_id}</td>
          <td>${s.cittamobi_mnemonic}</td>
          <td class="mono">${s.cittamobi_dist_m}m</td>
        </tr>
      `).join("");
    }

    function updateCostSimulator(val) {
      const pax = parseInt(val, 10);
      document.getElementById("sim-pax-label").textContent = `${pax.toLocaleString("pt-BR")} passageiros/dia`;

      const cittaReqs = pax * 100 * 30;
      const cittaBytes = pax * 567363 * 30;
      const cittaGb = cittaBytes / (1024 ** 3);

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
    // LIVE BACKEND HOOKS (CITTAMOBI PROXY + PYTORCH CPU INFERENCE)
    // =========================================================================
    async function pingLiveCittamobiStop() {
      const st = TELEMETRIA.stops.find(s => s.seq === activeStopSeq) || TELEMETRIA.stops[10];
      const cell = document.getElementById("insp-live-citta-ping");
      if (!cell) return;
      cell.innerHTML = `<span style="color:var(--warn-amber);">Consultando api.cittamobi.com.br para a parada #${st.cittamobi_id}...</span>`;
      try {
        const resp = await fetch(`/api/live/cittamobi-stop?stop_id=${st.cittamobi_id}&service_id=9655998`);
        const data = await resp.json();
        const sq = data.stop_query;
        const vq = data.service_vehicles_query;
        const svLen = (sq.response && sq.response.services) ? sq.response.services.length : 0;
        const vehLen = Array.isArray(vq.response) ? vq.response.length : 0;
        cell.innerHTML = `<strong style="color:var(--brand-green);">[Ao Vivo às ${sq.queried_at}]</strong> HTTP ${sq.http_status} (${sq.latency_ms}ms) &rarr; Previsões retornadas: <strong>${svLen}</strong> | Linha 0178: <strong>${vehLen} veículos</strong>`;
      } catch (err) {
        cell.innerHTML = `<span style="color:var(--text-muted);">Modo Demonstração Local</span>`;
      }
    }

    async function runLiveStgcnInference() {
      const st = TELEMETRIA.stops.find(s => s.seq === activeStopSeq) || TELEMETRIA.stops[10];
      const cell = document.getElementById("insp-stgcn");
      try {
        const resp = await fetch(`/api/live/stgcn-corridor?seq=${st.seq}&wait=${st.wait_gps_min}&abn=${st.abandonment_10m}`);
        const data = await resp.json();
        const h = data.predicted_horizons_min;
        cell.innerHTML = `Em 10m: ${h[0].toFixed(1)} min | Em 20m: ${h[1].toFixed(1)} min | <strong style="color:var(--brand-green);">Em 30m: ${h[2].toFixed(1)} min</strong> <span class="tag tag-emerald">Calculado agora (${data.cpu_stgcn_ms}ms)</span>`;
      } catch (err) {
        console.warn("Live STGCN fallback:", err);
      }
    }

    async function triggerLivePyTorchInference() {
      try {
        const resp = await fetch(`/api/live/pytorch-infer?scenario=${currentImuKey}`);
        const data = await resp.json();
        document.getElementById("imu-live-cpu-us").textContent = `${data.cpu_inference_us} µs (às ${data.timestamp})`;
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
            <td class="mono" style="font-weight:700;">${f.cls}</td>
          </tr>
        `).join("");

        const vtag = document.getElementById("imu-verdict-tag");
        vtag.textContent = `PyTorch ao Vivo (${data.timestamp}): ${data.fsm_verdict} (${data.cpu_inference_us} µs)`;
      } catch (err) {
        console.warn("Live PyTorch fallback:", err);
      }
    }

    async function refreshLiveCittamobiFleet() {
      const badge = document.getElementById("citta-fleet-badge");
      if (badge) badge.textContent = "Consultando api.cittamobi.com.br...";
      try {
        const resp = await fetch("/api/live/cittamobi-fleet");
        const data = await resp.json();
        if (badge) badge.textContent = `Auditado às ${data.queried_at} · 0 Ônibus Ativos`;
        const svTbody = document.getElementById("citta-services-tbody");
        svTbody.innerHTML = data.results.map(r => `
          <tr>
            <td class="mono">${r.serviceId}</td>
            <td class="mono"><strong>${r.label}</strong></td>
            <td>Consulta ao vivo às ${data.queried_at}</td>
            <td>Grande Recife (a=202)</td>
            <td><span class="tag tag-crimson">HTTP ${r.http_status} · ${r.active_vehicles} veículos (${r.latency_ms}ms)</span></td>
          </tr>
        `).join("");
      } catch (err) {
        console.warn("Fleet scan err:", err);
      }
    }

    // =========================================================================
    // MODULE 02: COMMUNITY SAFETY SHIELD ("NO PHONE") & COMPANION PRESENCE
    // =========================================================================
    let safetyCorridorData = null;
    let lastSafetyShieldVoice = "Alerta de Segurança GrafoParada: Não tire o celular do bolso neste ponto.";

    async function refreshSafetyCorridor() {
      try {
        const resp = await fetch("/api/live/safety-corridor");
        safetyCorridorData = await resp.json();
        renderSafetyCorridorUI();
      } catch (err) {
        console.warn("Safety corridor fallback:", err);
      }
    }

    function renderSafetyCorridorUI() {
      if (!safetyCorridorData) return;
      const sum = safetyCorridorData.summary;
      document.getElementById("saf-kpi-waiting").textContent = `${sum.total_active_waiting_users_pe60} pessoas`;
      document.getElementById("saf-kpi-nophone").textContent = `${sum.high_risk_no_phone_stops} paradas`;
      document.getElementById("saf-kpi-lonely").textContent = `${sum.lonely_stops_le_2_pax} paradas`;
      document.getElementById("saf-kpi-reports").textContent = `${sum.total_robbery_reports_30d} relatos`;

      const sel = document.getElementById("saf-report-stop-select");
      if (sel && sel.options.length === 0) {
        sel.innerHTML = safetyCorridorData.stops.map(s =>
          `<option value="${s.seq}">Parada #${String(s.seq).padStart(2, '0')} - ${s.name} (${s.stop_id})</option>`
        ).join("");
      }
      if (sel) sel.value = String(activeStopSeq);

      const tbody = document.getElementById("saf-corridor-tbody");
      if (tbody) {
        tbody.innerHTML = safetyCorridorData.stops.map(s => {
          const isSel = s.seq === activeStopSeq;
          const paxBadge = s.active_waiting_users <= 2
            ? `<span class="tag tag-amber">${s.active_waiting_users} pessoa(s) · Quase só</span>`
            : `<span class="tag tag-emerald">${s.active_waiting_users} pessoas · Com grupo</span>`;
          const dirBadge = s.risk_level === "HIGH_RISK"
            ? `<span class="tag tag-crimson">Não pegue o celular!</span>`
            : (s.risk_level === "MODERATE_RISK"
                ? `<span class="tag tag-amber">Usar áudio no bolso</span>`
                : `<span class="tag tag-emerald">Local seguro c/ grupo</span>`);
          return `
            <tr class="${isSel ? 'selected-row' : ''}" style="cursor:pointer;" onclick="selectStopNode(${s.seq}, true)">
              <td class="mono"><strong>#${String(s.seq).padStart(2, '0')}</strong></td>
              <td><strong>${s.name}</strong> <span class="mono" style="color:var(--text-muted); font-size:12px;">(${s.stop_id})</span></td>
              <td>${paxBadge}</td>
              <td class="mono" style="color:${s.robbery_reports_30d >= 10 ? 'var(--danger-red)' : 'var(--text-main)'}; font-weight:700;">${s.robbery_reports_30d} relatos</td>
              <td style="font-size:12.5px; color:var(--text-secondary);">${s.lighting_condition}</td>
              <td>${dirBadge}</td>
            </tr>
          `;
        }).join("");
      }

      const feedBox = document.getElementById("saf-feed-container");
      if (feedBox && safetyCorridorData.recent_feed) {
        feedBox.innerHTML = safetyCorridorData.recent_feed.map(item => {
          const isDanger = item.category === "ROUBO_CELULAR";
          const isSafe = item.category === "LOCAL_SEGURO_GRUPO";
          const borderCol = isDanger ? "var(--danger-red)" : (isSafe ? "var(--brand-green)" : "var(--warn-amber)");
          const labelMap = {
            ROUBO_CELULAR: "Alerta de Roubo / Assalto",
            ILUMINACAO_PRECARIA: "Local Escuro",
            PARADA_SOLITARIA: "Parada Solitária",
            LOCAL_SEGURO_GRUPO: "Grupo Seguro Confirmado"
          };
          return `
            <div style="background:var(--bg-subtle); border:1px solid var(--border); border-left:4px solid ${borderCol}; border-radius:var(--radius-sm); padding:10px 12px;">
              <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:4px;">
                <strong style="color:${borderCol};">${labelMap[item.category] || item.category} · ${item.stop_name}</strong>
                <span class="mono" style="color:var(--text-muted);">${item.timestamp}</span>
              </div>
              <div style="font-size:13px; color:var(--text-main); margin-bottom:4px;">${item.description}</div>
              <div style="font-size:12px; font-weight:600; color:var(--user-blue);">&rarr; ${item.action_taken}</div>
            </div>
          `;
        }).join("");
      }

      renderSelectedStopSafetyPanel(activeStopSeq);
    }

    function renderSelectedStopSafetyPanel(seq) {
      if (!safetyCorridorData || !safetyCorridorData.stops) return;
      const prof = safetyCorridorData.stops.find(s => s.seq === seq) || safetyCorridorData.stops[10];
      if (!prof) return;

      const sel = document.getElementById("saf-report-stop-select");
      if (sel) sel.value = String(prof.seq);

      document.getElementById("saf-stop-title").textContent =
        `Segurança na Parada #${String(prof.seq).padStart(2, '0')} · ${prof.name}`;

      const topBadge = document.getElementById("saf-stop-badge");
      const warnBox = document.getElementById("saf-phone-warning-box");
      const headline = document.getElementById("saf-phone-headline");
      const expl = document.getElementById("saf-phone-explanation");
      const scoreTag = document.getElementById("saf-risk-score-tag");

      scoreTag.textContent = `Risco: ${prof.risk_score_100}/100`;
      lastSafetyShieldVoice = prof.shield_voice_prompt;

      if (prof.keep_phone_in_pocket) {
        topBadge.className = "tag tag-crimson";
        topBadge.textContent = "Guarde o Celular no Bolso";
        warnBox.style.background = "var(--danger-red-bg)";
        warnBox.style.borderColor = "var(--danger-red-border)";
        headline.style.color = "var(--danger-red)";
        headline.textContent = `Atenção: Não pegue o celular neste local! (${prof.robbery_reports_30d} relatos de roubo)`;
        expl.innerHTML =
          `Passageiros registraram <strong>${prof.robbery_reports_30d} alertas de assalto/furto de celular</strong> e <strong>${prof.dark_spot_reports_30d} relatos de escuridão</strong> nesta parada (${prof.patrol_notes}). ` +
          `Mantenha o celular guardado no bolso: o GrafoParada avisa pelo fone quando o seu ônibus estiver chegando.`;
      } else {
        topBadge.className = "tag tag-emerald";
        topBadge.textContent = "Parada Segura com Companhia";
        warnBox.style.background = "var(--brand-green-bg)";
        warnBox.style.borderColor = "var(--brand-green-border)";
        headline.style.color = "var(--brand-green)";
        headline.textContent = `Parada iluminada e com grupo (${prof.active_waiting_users} pessoas esperando agora)`;
        expl.innerHTML =
          `Este ponto possui <strong>${prof.safe_confirmations_30d} confirmações de segurança</strong>, iluminação <strong>${prof.lighting_condition}</strong> (${prof.patrol_notes}) e grupo ativo aguardando o ônibus.`;
      }

      const waitCountEl = document.getElementById("saf-waiting-count");
      const aloneTag = document.getElementById("saf-alone-tag");
      waitCountEl.textContent = prof.active_waiting_users === 1 ? "1 pessoa" : `${prof.active_waiting_users} pessoas`;
      if (prof.is_user_alone_risk) {
        waitCountEl.style.color = "var(--warn-amber)";
        aloneTag.className = "tag tag-crimson";
        aloneTag.textContent = "Você está quase sozinho(a)";
      } else {
        waitCountEl.style.color = "var(--brand-green)";
        aloneTag.className = "tag tag-emerald";
        aloneTag.textContent = "Companhia ativa no ponto";
      }

      document.getElementById("saf-lighting-info").textContent =
        `Iluminação: ${prof.lighting_condition} · ${prof.patrol_notes}`;

      const comp = prof.companion_stop_recommendation;
      if (comp) {
        window.lastCompanionRecommendation = comp;
        document.getElementById("saf-companion-name").textContent =
          `Parada #${String(comp.seq).padStart(2, '0')} · ${comp.name}`;
        document.getElementById("saf-companion-metrics").textContent =
          `${comp.active_waiting_users} pessoas esperando juntas · Iluminação ${comp.lighting_condition}`;
        document.getElementById("saf-companion-dist").textContent =
          `Distância: ${comp.distance_m}m (~${comp.walk_min} min a pé) · Apenas ${comp.robbery_reports_30d} relatos.`;
      }
    }

    function speakSafetyShieldPrompt() {
      if ("speechSynthesis" in window && lastSafetyShieldVoice) {
        window.speechSynthesis.cancel();
        const u = new SpeechSynthesisUtterance(lastSafetyShieldVoice);
        u.lang = "pt-BR";
        u.rate = 1.03;
        window.speechSynthesis.speak(u);
      }
    }

    async function submitSafetyReport(category) {
      const st = TELEMETRIA.stops.find(s => s.seq === activeStopSeq) || TELEMETRIA.stops[10];
      const descInput = document.getElementById("saf-report-desc");
      const desc = descInput ? descInput.value : "";
      try {
        const url = `/api/live/safety-report?stop_id=${encodeURIComponent(st.stop_id)}&category=${encodeURIComponent(category)}&desc=${encodeURIComponent(desc)}`;
        const resp = await fetch(url);
        const data = await resp.json();
        if (descInput) descInput.value = "";
        safetyCorridorData = data.corridor_overview;
        renderSafetyCorridorUI();
        setSimulatedUserLocation(userPos.lat, userPos.lon, userPos.label, false);
        speakSafetyShieldPrompt();
      } catch (err) {
        console.warn("Report error:", err);
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
        console.warn("Presence update error:", err);
      }
    }

    function jumpToCompanionStop() {
      const comp = window.lastCompanionRecommendation;
      if (!comp) return;
      const targetStop = TELEMETRIA.stops.find(s => s.seq === comp.seq || String(s.stop_id) === String(comp.stop_id));
      if (targetStop) {
        switchModule("mod-gis", document.querySelectorAll(".tab-btn")[0]);
        selectStopNode(targetStop.seq, true);
        setSimulatedUserLocation(
          targetStop.lat + 0.00006,
          targetStop.lon + 0.00006,
          `Junto ao grupo na Parada Segura #${targetStop.seq} (${comp.active_waiting_users} pessoas esperando)`,
          true
        );
      }
    }

    // =========================================================================
    // LIVE USER LOCATION & NEARBY STOPS RADAR
    // =========================================================================
    function haversineLocalM(lat1, lon1, lat2, lon2) {
      const R = 6371000.0;
      const toRad = d => (d * Math.PI) / 180.0;
      const dLat = toRad(lat2 - lat1);
      const dLon = toRad(lon2 - lon1);
      const a =
        Math.sin(dLat / 2) ** 2 +
        Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLon / 2) ** 2;
      return 2 * R * Math.atan2(Math.sqrt(a), Math.sqrt(Math.max(0, 1 - a)));
    }

    function useRealBrowserGps() {
      const btn = document.getElementById("btn-gps-real");
      if (!navigator.geolocation) {
        alert("Este navegador não suporta geolocalização.");
        return;
      }
      if (btn) btn.textContent = "Obtendo seu GPS...";
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          if (btn) btn.textContent = "Meu GPS Real Ativo";
          setSimulatedUserLocation(
            pos.coords.latitude,
            pos.coords.longitude,
            `Sua localização real via GPS (±${Math.round(pos.coords.accuracy || 15)}m)`,
            true
          );
        },
        (err) => {
          if (btn) btn.textContent = "Usar Meu GPS Real (Navegador)";
          document.getElementById("user-pocket-voice-bar").innerHTML =
            `<strong style="color:var(--warn-amber);">Permissão de GPS não concedida pelo navegador (${err.message}).</strong> Clique em qualquer rua do mapa ao lado para posicionar seu marcador manualmente!`;
        },
        { enableHighAccuracy: true, timeout: 8000, maximumAge: 0 }
      );
    }

    function speakNearestStopVoice() {
      if ("speechSynthesis" in window && lastPocketVoicePrompt) {
        window.speechSynthesis.cancel();
        const u = new SpeechSynthesisUtterance(lastPocketVoicePrompt);
        u.lang = "pt-BR";
        u.rate = 1.03;
        window.speechSynthesis.speak(u);
      }
    }

    async function setSimulatedUserLocation(lat, lon, label, flyTo = true) {
      userPos = { lat, lon, label };
      initRealLeafletMap();

      const coordBadge = document.getElementById("user-loc-coords-badge");
      if (coordBadge) {
        coordBadge.textContent = `${label} · (${lat.toFixed(5)}, ${lon.toFixed(5)})`;
      }

      if (flyTo && leafletMap) {
        leafletMap.setView([lat, lon], Math.max(leafletMap.getZoom(), 16), { animate: true });
      }

      userRadarLayerGroup.clearLayers();

      L.circle([lat, lon], {
        radius: 180,
        color: "#0057b8",
        weight: 1.5,
        dashArray: "5, 6",
        fillColor: "#0057b8",
        fillOpacity: 0.05
      }).addTo(userRadarLayerGroup);

      L.circle([lat, lon], {
        radius: 35,
        color: "#0a6b46",
        weight: 2,
        fillColor: "#0a6b46",
        fillOpacity: 0.18
      }).addTo(userRadarLayerGroup);

      const beaconIcon = L.divIcon({
        className: "",
        html: `<div class="user-gps-beacon" title="Você está aqui (Arraste para mover)"></div>`,
        iconSize: [22, 22],
        iconAnchor: [11, 11]
      });

      userMarker = L.marker([lat, lon], { icon: beaconIcon, draggable: true }).addTo(userRadarLayerGroup);
      userMarker.bindTooltip(
        `Você está aqui: ${label}`,
        { permanent: true, direction: "top", offset: [0, -12], className: "sicoe-tooltip" }
      );

      userMarker.on("dragend", (ev) => {
        const p = ev.target.getLatLng();
        setSimulatedUserLocation(p.lat, p.lng, "Posição ajustada manualmente no mapa", false);
      });

      try {
        const resp = await fetch(`/api/live/nearby-stops?lat=${lat}&lon=${lon}&k=5`);
        const data = await resp.json();

        lastPocketVoicePrompt = data.pocket_voice_prompt;
        document.getElementById("user-pocket-voice-bar").innerHTML =
          `<strong>Aviso automático no fone:</strong> "${data.pocket_voice_prompt}"`;

        const gfBadge = document.getElementById("user-geofence-badge");
        const topStop = data.closest_gtfs_stops && data.closest_gtfs_stops[0];
        if (topStop) {
          if (topStop.inside_geofence_35m) {
            gfBadge.className = "tag tag-emerald";
            gfBadge.textContent = `Na parada (${topStop.distance_m}m de #${topStop.stop_id})`;
          } else if (topStop.inside_pocket_radar_150m) {
            gfBadge.className = "tag tag-cyan";
            gfBadge.textContent = `Próximo à parada (${topStop.distance_m}m)`;
          } else {
            gfBadge.className = "tag tag-amber";
            gfBadge.textContent = `Parada mais próxima a ${topStop.distance_m}m`;
          }

          if (topStop.is_pe60_corridor && topStop.pe60_seq && topStop.distance_m <= 120.0) {
            if (activeStopSeq !== topStop.pe60_seq) {
              selectStopNode(topStop.pe60_seq, false);
            }
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
              sTitle.textContent = `Atenção em ${topStop.stop_name}: Não pegue o celular na parada!`;
              const compTxt = topStop.companion_stop_recommendation
                ? ` Como há apenas ${topStop.active_waiting_users} pessoa aqui, recomendamos caminhar até ${topStop.companion_stop_recommendation.name} (${topStop.companion_stop_recommendation.distance_m}m), onde há ${topStop.companion_stop_recommendation.active_waiting_users} pessoas esperando juntas.`
                : ``;
              sDesc.textContent = `Local com ${topStop.robbery_reports_30d} relatos de roubo. Deixe o celular no bolso com o áudio ligado.${compTxt}`;
              if (sBtnComp && topStop.companion_stop_recommendation) {
                sBtnComp.style.display = "inline-flex";
                sBtnComp.textContent = `Ir para Parada com Companhia (${topStop.companion_stop_recommendation.active_waiting_users} pessoas a ${topStop.companion_stop_recommendation.distance_m}m)`;
              }
            } else {
              banner.style.background = "var(--brand-green-bg)";
              banner.style.borderColor = "var(--brand-green-border)";
              banner.style.borderLeft = "5px solid var(--brand-green)";
              sTitle.style.color = "var(--brand-green)";
              sTitle.textContent = `Parada Segura com Companhia: ${topStop.stop_name}`;
              sDesc.textContent = `Há ${topStop.active_waiting_users} passageiros aguardando juntos neste ponto agora (${topStop.robbery_reports_30d} relatos recentes).`;
              if (sBtnComp) sBtnComp.style.display = "none";
            }
          }
        }

        (data.closest_gtfs_stops || []).slice(0, 3).forEach((st, idx) => {
          const lineCol = st.inside_geofence_35m ? "#0a6b46" : (idx === 0 ? "#0057b8" : "#d97706");
          L.polyline([[lat, lon], [st.lat, st.lon]], {
            color: lineCol,
            weight: idx === 0 ? 3 : 2,
            dashArray: "5, 5",
            opacity: 0.85
          }).addTo(userRadarLayerGroup);

          if (!st.is_pe60_corridor) {
            const rmrMarker = L.circleMarker([st.lat, st.lon], {
              radius: 7,
              color: "#ffffff",
              weight: 2,
              fillColor: "#0057b8",
              fillOpacity: 0.95
            }).addTo(userRadarLayerGroup);
            rmrMarker.bindTooltip(
              `Parada Oficial #${st.stop_id}: ${st.stop_name} (${st.distance_m}m)`,
              { permanent: idx === 0, direction: "bottom", className: "sicoe-tooltip" }
            );
          }
        });

        const gtfsTbody = document.getElementById("nearby-gtfs-tbody");
        gtfsTbody.innerHTML = (data.closest_gtfs_stops || []).map((st, idx) => {
          const paxCol = st.active_waiting_users <= 2 ? "var(--warn-amber)" : "var(--brand-green)";
          const paxTxt = st.active_waiting_users === 1 ? "1 pessoa (Só)" : `${st.active_waiting_users} pessoas`;
          const safetyBadge = st.keep_phone_in_pocket
            ? `<span class="tag tag-crimson">Guarde o celular (${st.robbery_reports_30d} relatos)</span>`
            : `<span class="tag tag-emerald">Grupo seguro (${st.active_waiting_users} ali)</span>`;
          return `
            <tr class="${idx === 0 ? 'selected-row' : ''}" style="cursor:pointer;" onclick="leafletMap.setView([${st.lat}, ${st.lon}], 17);">
              <td class="mono"><strong>${st.stop_id}</strong></td>
              <td><strong>${st.stop_name}</strong></td>
              <td class="mono" style="font-weight:700;">${st.distance_m} m</td>
              <td style="color:${paxCol}; font-weight:700;">${paxTxt}</td>
              <td>${safetyBadge}</td>
            </tr>
          `;
        }).join("");

        const cvp = data.cittamobi_viewport_live || {};
        document.getElementById("nearby-citta-meta").textContent =
          `${cvp.total_stops_in_bbox || 0} paradas encontradas em ${cvp.latency_ms || 0}ms`;

        const cittaTbody = document.getElementById("nearby-citta-tbody");
        const cList = cvp.closest_cittamobi_stops || [];
        if (cList.length === 0) {
          cittaTbody.innerHTML = `<tr><td colspan="4" style="color:var(--text-muted);">Nenhuma parada Cittamobi próxima.</td></tr>`;
        } else {
          cittaTbody.innerHTML = cList.map((cs) => `
            <tr style="cursor:pointer;" onclick="leafletMap.setView([${cs.lat}, ${cs.lon}], 17);">
              <td class="mono">#${cs.cittamobi_id}</td>
              <td>${cs.mnemonic}</td>
              <td class="mono"><strong>${cs.distance_m} m</strong></td>
              <td><span class="tag tag-crimson">${cs.active_services} linhas ativas</span></td>
            </tr>
          `).join("");
        }
      } catch (err) {
        console.warn("Nearby scan err:", err);
      }
    }

    // INITIALIZATION
    initQuickStopButtons();
    selectStopNode(11, false);
    selectImuScenario("ALIGHTING", document.querySelector(".sc-item"));
    populateCittamobiTables();
    updateCostSimulator(50000);
    refreshSafetyCorridor();

    const params = new URLSearchParams(window.location.search);
    const modParam = params.get("mod");
    if (modParam && document.getElementById(modParam)) {
      const idxMap = { "mod-gis": 0, "mod-safety": 1, "mod-imu": 2, "mod-citta": 3, "mod-bench": 4 };
      switchModule(modParam, document.querySelectorAll(".tab-btn")[idxMap[modParam] || 0]);
    }

    requestAnimationFrame(() => {
      drawPe60GisCanvas();
      setSimulatedUserLocation(
        -8.304950,
        -35.021420,
        "Na Parada #11 (PE-60 · Trevo Ipojuca)",
        false
      );
    });
    requestAnimationFrame(renderImuOscilloscope);
  </script>
</body>
</html>
"""

final_html = HTML_TEMPLATE.replace("__TELEMETRIA_JSON__", TELEMETRIA_JSON_STR)
with open(OUT_HTML, "w", encoding="utf-8") as f:
    f.write(final_html)

print(f"[OK] Protótipo GrafoParada v5.0 (Clean, Map-First & Accessible) gerado em {OUT_HTML} ({OUT_HTML.stat().st_size:,} bytes)")
