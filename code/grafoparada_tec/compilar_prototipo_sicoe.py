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

    .mobile-only {
      display: none !important;
    }
    .desktop-only {
      display: flex !important;
    }

    @media (max-width: 1180px) {
      .map-first-layout, .split-2 {
        grid-template-columns: 1fr;
      }
    }

    /* =========================================================================
       NATIVE MOBILE TRANSIT APP EXPERIENCE (@media max-width: 860px)
       Like Google Maps, Uber, Moovit, Citymapper
       ========================================================================= */
    @media (max-width: 860px) {
      .mobile-only {
        display: flex !important;
      }
      .desktop-only {
        display: none !important;
      }

      body {
        overflow: hidden !important;
        height: 100dvh !important;
        width: 100vw !important;
        position: fixed !important;
        margin: 0 !important;
        padding: 0 !important;
      }

      /* Native Compact App Header (52px) */
      .app-header {
        height: 52px !important;
        padding: 0 12px !important;
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        border-bottom: 1px solid var(--border) !important;
        background: var(--bg-surface) !important;
        z-index: 10000 !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
      }
      .app-header .brand-subtitle,
      .app-header .main-tabs,
      .app-header .header-actions .btn-emerald {
        display: none !important;
      }
      .brand-title {
        font-size: 13.5px !important;
        font-weight: 800 !important;
      }
      .brand-badge {
        font-size: 11.5px !important;
        padding: 4px 8px !important;
      }
      .voice-selector-wrap {
        padding: 3px 6px !important;
        font-size: 11px !important;
      }
      #theme-toggle-btn {
        min-height: 32px !important;
        padding: 4px 8px !important;
        font-size: 11px !important;
      }

      /* Views fit screen exactly between header (52px) and bottom nav (60px) */
      .workspace-view {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
        height: calc(100dvh - 52px - 60px) !important;
        overflow: hidden !important;
        position: relative !important;
      }

      #mod-safety.workspace-view,
      #mod-tech.workspace-view {
        overflow-y: auto !important;
        padding: 14px 14px 75px !important;
        -webkit-overflow-scrolling: touch !important;
      }

      /* TAB 1: Immersive Screen-Filling Map */
      .map-first-layout {
        display: flex !important;
        flex-direction: column !important;
        height: 100% !important;
        width: 100% !important;
        position: relative !important;
        overflow: hidden !important;
      }

      .map-card {
        border: none !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        height: 100% !important;
        width: 100% !important;
        position: absolute !important;
        inset: 0 !important;
        display: flex !important;
        flex-direction: column !important;
      }

      .map-canvas-holder {
        flex: 1 !important;
        height: 100% !important;
        width: 100% !important;
        position: relative !important;
      }

      #pe60-leaflet-map {
        height: 100% !important;
        width: 100% !important;
      }

      .map-legend-pill {
        top: 60px !important;
        bottom: auto !important;
        left: 10px !important;
        font-size: 10.5px !important;
        padding: 4px 10px !important;
        gap: 8px !important;
        background: rgba(255, 255, 255, 0.92) !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.15) !important;
        z-index: 450 !important;
      }
      [data-theme="dark"] .map-legend-pill {
        background: rgba(22, 27, 34, 0.92) !important;
      }

      /* Floating Overlay on Top of Map */
      .mobile-map-floating-bar {
        position: absolute !important;
        top: 10px !important;
        left: 10px !important;
        right: 10px !important;
        z-index: 500 !important;
        display: flex !important;
        align-items: center !important;
        gap: 6px !important;
      }

      .mobile-search-pill {
        flex: 1 !important;
        display: flex !important;
        align-items: center !important;
        gap: 6px !important;
        background: var(--bg-surface) !important;
        border: 1.5px solid var(--border-strong) !important;
        border-radius: 999px !important;
        padding: 7px 13px !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2) !important;
      }
      .mobile-search-pill input {
        border: none !important;
        background: transparent !important;
        outline: none !important;
        width: 100% !important;
        font-size: 13.5px !important;
        color: var(--text-main) !important;
        font-family: inherit !important;
      }

      .mobile-quick-chip {
        background: var(--brand-green-bg) !important;
        border: 2px solid var(--brand-green) !important;
        color: var(--brand-green) !important;
        font-weight: 800 !important;
        font-size: 13px !important;
        padding: 7px 13px !important;
        border-radius: 999px !important;
        cursor: pointer !important;
        white-space: nowrap !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2) !important;
        display: inline-flex !important;
        align-items: center !important;
      }

      /* Floating Action Button (FAB) for GPS recentering */
      .mobile-fab-gps {
        position: absolute !important;
        bottom: 215px !important;
        right: 14px !important;
        z-index: 550 !important;
        width: 48px !important;
        height: 48px !important;
        border-radius: 50% !important;
        background: var(--bg-surface) !important;
        border: 1.5px solid var(--border-strong) !important;
        color: var(--user-blue) !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.28) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        cursor: pointer !important;
        transition: transform 0.15s ease !important;
      }
      .mobile-fab-gps:active {
        transform: scale(0.9) !important;
      }

      /* Mobile Bottom Sheet (Draggable / Collapsible) */
      .companion-sheet {
        position: absolute !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        z-index: 700 !important;
        background: var(--bg-surface) !important;
        border-radius: 22px 22px 0 0 !important;
        border: 1px solid var(--border) !important;
        border-bottom: none !important;
        box-shadow: 0 -8px 30px rgba(0,0,0,0.28) !important;
        padding: 6px 16px 16px !important;
        transition: max-height 0.35s cubic-bezier(0.16, 1, 0.3, 1) !important;
        max-height: 200px !important;
        overflow: hidden !important;
      }

      .companion-sheet.sheet-expanded {
        max-height: calc(100dvh - 110px) !important;
        overflow-y: auto !important;
        -webkit-overflow-scrolling: touch !important;
      }

      .sheet-handle-bar {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        padding: 4px 0 8px !important;
        cursor: pointer !important;
        touch-action: pan-y !important;
      }

      .sheet-handle-pill {
        width: 44px !important;
        height: 4.5px !important;
        background: var(--border-strong) !important;
        border-radius: 999px !important;
      }

      .sheet-handle-hint {
        font-size: 10.5px !important;
        font-weight: 700 !important;
        color: var(--text-muted) !important;
        margin-top: 3px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.04em !important;
      }

      .eta-hero-box {
        margin: 8px 0 10px !important;
        gap: 8px !important;
      }
      .eta-stat {
        padding: 8px 12px !important;
      }
      .eta-stat-val {
        font-size: 21px !important;
      }

      /* Native Bottom Navigation Bar */
      .mobile-bottom-nav {
        display: flex !important;
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        height: 60px !important;
        background: var(--bg-surface) !important;
        border-top: 1px solid var(--border) !important;
        z-index: 9999 !important;
        box-shadow: 0 -2px 14px rgba(0,0,0,0.08) !important;
      }

      .mob-nav-item {
        flex: 1 !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 2px !important;
        background: transparent !important;
        border: none !important;
        color: var(--text-muted) !important;
        cursor: pointer !important;
        padding: 4px 0 !important;
        transition: color 0.15s ease !important;
      }

      .mob-nav-item.active {
        color: var(--brand-green) !important;
        font-weight: 800 !important;
      }

      .mob-nav-icon {
        font-size: 20px !important;
        line-height: 1 !important;
      }

      .mob-nav-label {
        font-size: 10.5px !important;
        letter-spacing: -0.01em !important;
      }

      /* Tab 2 & 3 responsive adjustments */
      .split-2 {
        display: flex !important;
        flex-direction: column !important;
        gap: 16px !important;
      }
    }
  </style>
</head>
<body>

  <!-- ======================================================================= -->
  <!-- FULLSCREEN USER AUTH & ONBOARDING EXPERIENCE (DO ZERO AO USO)          -->
  <!-- ======================================================================= -->
  <div id="auth-onboarding-screen" style="display:flex; position:fixed; inset:0; z-index:99999; background:var(--bg-page); overflow-y:auto; -webkit-overflow-scrolling:touch;">
    <div style="max-width:480px; width:100%; margin:auto; padding:24px 20px; min-height:100%; display:flex; flex-direction:column; justify-content:center;">

      <!-- STEP 1: WELCOME SPLASH SCREEN -->
      <div id="auth-step-welcome" style="display:block;">
        <div style="text-align:center; margin-bottom:24px;">
          <div style="display:inline-flex; align-items:center; gap:8px; background:var(--brand-green-bg); border:2px solid var(--brand-green); padding:8px 18px; border-radius:999px; margin-bottom:14px;">
            <span style="font-size:20px;">🚌🛡️</span>
            <span style="font-weight:800; font-size:15px; color:var(--brand-green);">GrafoParada · Grande Recife</span>
          </div>
          <h1 style="font-size:26px; font-weight:800; line-height:1.2; letter-spacing:-0.03em; margin-bottom:10px;">
            O ônibus no Grande Recife que você espera sem medo de assalto.
          </h1>
          <p style="font-size:14px; color:var(--text-secondary); line-height:1.5;">
            Primeira tecnologia com Companhia na Parada, Modo Celular no Bolso com voz natural e Remanejamento de frotas vazias na Rodovia PE-60.
          </p>
        </div>

        <!-- 3 Feature Pillars -->
        <div style="display:flex; flex-direction:column; gap:12px; margin-bottom:24px;">
          <div style="background:var(--bg-surface); border:1px solid var(--border); border-radius:14px; padding:14px; display:flex; gap:12px; align-items:center; box-shadow:var(--shadow-sm);">
            <div style="font-size:26px; background:var(--brand-green-bg); padding:10px; border-radius:12px;">🛡️</div>
            <div>
              <div style="font-weight:800; font-size:14px;">Companhia Coletiva na Parada</div>
              <div style="font-size:12.5px; color:var(--text-secondary);">Veja quantas pessoas estão esperando antes de sair de casa para nunca ficar só.</div>
            </div>
          </div>

          <div style="background:var(--bg-surface); border:1px solid var(--border); border-radius:14px; padding:14px; display:flex; gap:12px; align-items:center; box-shadow:var(--shadow-sm);">
            <div style="font-size:26px; background:var(--warn-amber-bg); padding:10px; border-radius:12px;">🎧</div>
            <div>
              <div style="font-weight:800; font-size:14px;">Modo Celular no Bolso</div>
              <div style="font-size:12.5px; color:var(--text-secondary);">A IA avisa com voz humana no seu fone de ouvido. Você não tira o celular da bolsa.</div>
            </div>
          </div>

          <div style="background:var(--bg-surface); border:1px solid var(--border); border-radius:14px; padding:14px; display:flex; gap:12px; align-items:center; box-shadow:var(--shadow-sm);">
            <div style="font-size:26px; background:var(--user-blue-bg); padding:10px; border-radius:12px;">🚌</div>
            <div>
              <div style="font-weight:800; font-size:14px;">Frota Inteligente na PE-60</div>
              <div style="font-size:12.5px; color:var(--text-secondary);">Ônibus ociosos de Suape são remanejados automaticamente para cobrir lotações.</div>
            </div>
          </div>
        </div>

        <button class="btn btn-primary" style="width:100%; min-height:52px; font-size:16px; font-weight:800; border-radius:14px; margin-bottom:10px;" onclick="goToAuthStep('signup')">
          🚀 Criar Minha Conta de Passageiro
        </button>
        <button class="btn" style="width:100%; min-height:46px; font-size:14px; font-weight:700; border-radius:14px;" onclick="goToAuthStep('login')">
          Já Tenho Conta · Entrar
        </button>

        <div style="text-align:center; margin-top:16px;">
          <a href="javascript:void(0)" onclick="quickTestUser('Cauã Cunha', 'Camela (PE-60)')" style="font-size:13px; color:var(--brand-green); font-weight:800; text-decoration:underline;">
            ⚡ Teste Rápido de 1 Toque: Entrar como Cauã em Camela
          </a>
        </div>
      </div>

      <!-- STEP 2: CADASTRO RÁPIDO -->
      <div id="auth-step-signup" style="display:none;">
        <div style="margin-bottom:20px;">
          <span class="tag tag-emerald" style="margin-bottom:8px;">Etapa 1 de 2 · Seus Dados</span>
          <h2 style="font-size:22px; font-weight:800; margin-top:4px;">Crie sua conta de passageiro</h2>
          <p style="font-size:13.5px; color:var(--text-secondary);">Leva menos de 1 minuto para proteger sua rotina de ônibus.</p>
        </div>

        <div style="display:flex; flex-direction:column; gap:14px; margin-bottom:20px;">
          <div>
            <label style="display:block; font-size:13px; font-weight:700; margin-bottom:6px;">Seu Nome Completo:</label>
            <input id="signup-name" type="text" placeholder="Ex: Cauã Cunha" value="Cauã Cunha"
              style="width:100%; min-height:48px; padding:10px 14px; font-size:14px; border:1.5px solid var(--border-strong); border-radius:12px; background:var(--bg-surface); color:var(--text-main);" />
          </div>

          <div>
            <label style="display:block; font-size:13px; font-weight:700; margin-bottom:6px;">Celular / WhatsApp:</label>
            <input id="signup-phone" type="tel" placeholder="(81) 98888-0000" value="(81) 98888-7766"
              style="width:100%; min-height:48px; padding:10px 14px; font-size:14px; border:1.5px solid var(--border-strong); border-radius:12px; background:var(--bg-surface); color:var(--text-main);" />
          </div>

          <div>
            <label style="display:block; font-size:13px; font-weight:700; margin-bottom:6px;">
              Sua Parada, Bairro ou Terminal Integrado (T.I.):
            </label>
            <input id="signup-place-search" type="text" placeholder="🔍 Filtrar T.I. ou cidade (ex: Camela, TI Joana, TI Macaxeira, TI Pelópidas, Cabo)..." oninput="filterPlaceOptions(this.value)"
              style="width:100%; min-height:42px; padding:8px 12px; font-size:13px; border:1.5px solid var(--border-strong); border-radius:10px; background:var(--bg-surface); color:var(--text-main); margin-bottom:6px;" />
            <select id="signup-place" size="6" style="width:100%; max-height:140px; padding:6px; font-size:13px; border:1.5px solid var(--border-strong); border-radius:10px; background:var(--bg-surface); color:var(--text-main); margin-bottom:14px;">
  <optgroup label="📍 Abreu e Lima">
    <option value="Ti Abreu E Lima" data-lat="-7.921296345462924" data-lon="-34.89528933864802">Ti Abreu E Lima</option>
  </optgroup>
  <optgroup label="📍 Cabo de Santo Agostinho">
    <option value="Ti Cabo" data-lat="-8.285064968083757" data-lon="-35.03239778768872">Ti Cabo</option>
  </optgroup>
  <optgroup label="📍 Camaragibe">
    <option value="Ti Camaragibe" data-lat="-8.02478969917935" data-lon="-34.99606368801693">Ti Camaragibe</option>
    <option value="Ti Cosme E Damião" data-lat="-8.036236471550168" data-lon="-34.988185865632055">Ti Cosme E Damião</option>
  </optgroup>
  <optgroup label="📍 Igarassu">
    <option value="Terminal Da Linha 1969 Ti Igarassu / Itapissuma" data-lat="-7.771441667468382" data-lon="-34.90325833329781">Terminal Da Linha 1969 Ti Igarassu / Itapissuma</option>
    <option value="Ti Igarassu" data-lat="-7.832827812755261" data-lon="-34.911922291263345">Ti Igarassu</option>
  </optgroup>
  <optgroup label="📍 Ipojuca">
    <option value="Ipojuca · Centro / Praça e UPA (PE-60)" data-lat="-8.398512" data-lon="-35.06412">Ipojuca · Centro / Praça e UPA (PE-60)</option>
    <option value="Porto de Galinhas · Terminal de Ônibus" data-lat="-8.505432" data-lon="-35.004121">Porto de Galinhas · Terminal de Ônibus</option>
  </optgroup>
  <optgroup label="📍 Ipojuca (Camela)">
    <option value="Camela · Centro (Rua do Comércio / Terminal)" data-lat="-8.514931" data-lon="-35.123469">Camela · Centro (Rua do Comércio / Terminal)</option>
    <option value="Camela · Trevo da Rodovia PE-60 (Ipojuca)" data-lat="-8.494915" data-lon="-35.09219" selected>Camela · Trevo da Rodovia PE-60 (Ipojuca)</option>
  </optgroup>
  <optgroup label="📍 Jaboatão dos Guararapes">
    <option value="Ponto De Retorno Muribeca/Ti Cajueiro Seco" data-lat="-8.149558336096304" data-lon="-34.97679999995839">Ponto De Retorno Muribeca/Ti Cajueiro Seco</option>
    <option value="Terminal Da Linha 290 Bonança/Ti Jaboatão" data-lat="-8.106150000906043" data-lon="-35.19478888880074">Terminal Da Linha 290 Bonança/Ti Jaboatão</option>
    <option value="Ti Cajueiro Seco" data-lat="-8.167989004420969" data-lon="-34.934533688542">Ti Cajueiro Seco</option>
    <option value="Ti Cavaleiro" data-lat="-8.094519891011108" data-lon="-34.97291415128109">Ti Cavaleiro</option>
    <option value="Ti Jaboatão" data-lat="-8.111632198453698" data-lon="-35.014398835403874">Ti Jaboatão</option>
    <option value="Ti Prazeres" data-lat="-8.161419696372274" data-lon="-34.92655824202219">Ti Prazeres</option>
  </optgroup>
  <optgroup label="📍 Olinda">
    <option value="Terminal Da Linha 895 Alto Do Sol Nascente/Ti Xamba" data-lat="-7.976716669262277" data-lon="-34.91052499996502">Terminal Da Linha 895 Alto Do Sol Nascente/Ti Xamba</option>
    <option value="Ti Pe-15" data-lat="-7.982723500007164" data-lon="-34.856319955857714">Ti Pe-15</option>
    <option value="Ti Rio Doce" data-lat="-7.9607209918352" data-lon="-34.85102855127083">Ti Rio Doce</option>
    <option value="Ti Xambá" data-lat="-8.001196661427809" data-lon="-34.892626605900084">Ti Xambá</option>
  </optgroup>
  <optgroup label="📍 Paulista">
    <option value="Ti Pelópidas" data-lat="-7.947072139974567" data-lon="-34.87797167910255">Ti Pelópidas</option>
    <option value="Ti Pelópidas Silveira" data-lat="-7.946769515773473" data-lon="-34.877856200512845">Ti Pelópidas Silveira</option>
    <option value="Ti Pelópidas- Desembarque 01" data-lat="-7.945576169910893" data-lon="-34.87759786383087">Ti Pelópidas- Desembarque 01</option>
    <option value="Ti Pelópidas- Embarque 17" data-lat="-7.946586597184459" data-lon="-34.87784604226094">Ti Pelópidas- Embarque 17</option>
  </optgroup>
  <optgroup label="📍 Recife">
    <option value="Terminal Da Linha 303 Ti Caxangá/Curado Ii (Br-232)" data-lat="-8.04768889155233" data-lon="-34.95956388884871">Terminal Da Linha 303 Ti Caxangá/Curado Ii (Br-232)</option>
    <option value="Terminal De Linha 302" data-lat="-8.031608334216045" data-lon="-34.95833611106901">Terminal De Linha 302</option>
    <option value="Terminal Nova Morada/Ti Caxangá" data-lat="-8.025455556436276" data-lon="-34.950294444403426">Terminal Nova Morada/Ti Caxangá</option>
    <option value="Ti Aeroporto" data-lat="-8.134136062005572" data-lon="-34.91512430325258">Ti Aeroporto</option>
    <option value="Ti Afogados" data-lat="-8.077302413073026" data-lon="-34.90679635435186">Ti Afogados</option>
    <option value="Ti Barro" data-lat="-8.08817445055669" data-lon="-34.94585759758854">Ti Barro</option>
    <option value="Ti Caxangá" data-lat="-8.031208942325296" data-lon="-34.954937843290075">Ti Caxangá</option>
    <option value="Ti Cdu" data-lat="-8.03883429543645" data-lon="-34.94299630962573">Ti Cdu</option>
    <option value="Ti Getulio Vargas" data-lat="-8.050618224769712" data-lon="-34.92200224898446">Ti Getulio Vargas</option>
    <option value="Ti Getúlio Vargas" data-lat="-8.050186111999881" data-lon="-34.92204444440719">Ti Getúlio Vargas</option>
    <option value="Ti Joana Bezarra" data-lat="-8.072163889784743" data-lon="-34.89523055552157">Ti Joana Bezarra</option>
    <option value="Ti Joana Bezerra" data-lat="-8.072128730179074" data-lon="-34.89576292232596">Ti Joana Bezerra</option>
    <option value="Ti Largo Da Paz" data-lat="-8.081244227400381" data-lon="-34.905061094793076">Ti Largo Da Paz</option>
    <option value="Ti Macaxeira" data-lat="-8.008235080134988" data-lon="-34.93832783476195">Ti Macaxeira</option>
    <option value="Ti Pe 15" data-lat="-7.983177157724002" data-lon="-34.85607007133678">Ti Pe 15</option>
    <option value="Ti Recife" data-lat="-8.068453118313338" data-lon="-34.88437609302074">Ti Recife</option>
    <option value="Ti Santa Luzia" data-lat="-8.084164824756378" data-lon="-34.93009157562516">Ti Santa Luzia</option>
    <option value="Ti Tancredo Neves" data-lat="-8.122014463888496" data-lon="-34.91246455096088">Ti Tancredo Neves</option>
  </optgroup>
  <optgroup label="📍 Recife / Várzea (TIP)">
    <option value="Ti Tip" data-lat="-8.064289307992048" data-lon="-34.98207327791133">Ti Tip</option>
  </optgroup>
  <optgroup label="📍 Suape / Ipojuca">
    <option value="Complexo Industrial e Portuário de Suape" data-lat="-8.3941" data-lon="-34.9812">Complexo Industrial e Portuário de Suape</option>
  </optgroup>
            </select>
          </div>

          <div>
            <label style="display:block; font-size:13px; font-weight:700; margin-bottom:6px;">
              Linha de Ônibus Habitual (Todas as 400 Linhas do Grande Recife):
            </label>
            <input id="signup-line-search" type="text" placeholder="🔍 Filtrar por número ou nome (ex: 178, 202, 026, 050, 914, Macaxeira, Camela, Caxangá)..." oninput="filterLineOptions(this.value)"
              style="width:100%; min-height:42px; padding:8px 12px; font-size:13px; border:1.5px solid var(--border-strong); border-radius:10px; background:var(--bg-surface); color:var(--text-main); margin-bottom:6px;" />
            <select id="signup-line" size="6" style="width:100%; max-height:150px; padding:6px; font-size:13px; border:1.5px solid var(--border-strong); border-radius:10px; background:var(--bg-surface); color:var(--text-main); margin-bottom:18px;">
  <optgroup label="⭐ Eixo Sul / PE-60 / Suape / Camela / Cabo">
    <option value="001">🚌 Linha 001 · Ponte Dos Carvalhos / Prazeres (Barra De Jangada)</option>
    <option value="034">🚌 Linha 034 · Curcurana / Ti Cajueiro Seco</option>
    <option value="037">🚌 Linha 037 · Comportas / Ti Cajueiro Seco</option>
    <option value="178" selected>🚌 Linha 178 · Porto De Suape / Ti Cabo</option>
    <option value="191">🚌 Linha 191 · Recife / Porto De Galinhas (N. Sra. Do Ó)</option>
    <option value="195">🚌 Linha 195 · Recife / Porto De Galinhas (Opcional)</option>
    <option value="198">🚌 Linha 198 · Ipojuca / Ti Cabo</option>
  </optgroup>
  <optgroup label="🔄 Linhas Interterminais / Perimetrais (T.I. a T.I.)">
    <option value="020">🚌 Linha 020 · Candeias / Ti Tancredo Neves</option>
    <option value="023">🚌 Linha 023 · Ti Tancredo Neves / Ti Aeroporto</option>
    <option value="024">🚌 Linha 024 · Ti Tancredo Neves (Circular Boa Viagem)</option>
    <option value="026">🚌 Linha 026 · Ti Aeroporto / Ti Joana Bezerra</option>
    <option value="030">🚌 Linha 030 · Ti Rio Doce / Barra De Jangada</option>
    <option value="050">🚌 Linha 050 · Ti Pe-15 / Boa Viagem</option>
    <option value="200">🚌 Linha 200 · Ti Jaboatão (Parador)</option>
    <option value="202">🚌 Linha 202 · Ti Barro / Ti Macaxeira (Várzea)</option>
    <option value="207">🚌 Linha 207 · Ti Barro / Ti Macaxeira (Br-101)</option>
    <option value="2490">🚌 Linha 2490 · Ti Camaragibe / Ti Macaxeira</option>
    <option value="860">🚌 Linha 860 · Ti Xambá (Príncipe)</option>
    <option value="914">🚌 Linha 914 · Ti Pe-15 / Ti Afogados</option>
  </optgroup>
  <optgroup label="📋 Todas as 400 Linhas do Grande Recife (001 a 2490)">
    <option value="001">🚌 Linha 001 · Ponte Dos Carvalhos / Prazeres (Barra De Jangada)</option>
    <option value="010">🚌 Linha 010 · Abdo Cabus (Conde Boa Vista)</option>
    <option value="011">🚌 Linha 011 · Piedade / Derby</option>
    <option value="013">🚌 Linha 013 · Jardim Beira Rio (Pina)</option>
    <option value="014">🚌 Linha 014 · Brasília (Cd. Boa Vista)</option>
    <option value="018">🚌 Linha 018 · Brasília Teimosa</option>
    <option value="020">🚌 Linha 020 · Candeias / Ti Tancredo Neves</option>
    <option value="021">🚌 Linha 021 · Ti Joana Bezerra / Shopping Riomar</option>
    <option value="023">🚌 Linha 023 · Ti Tancredo Neves / Ti Aeroporto</option>
    <option value="024">🚌 Linha 024 · Ti Tancredo Neves (Circular Boa Viagem)</option>
    <option value="026">🚌 Linha 026 · Ti Aeroporto / Ti Joana Bezerra</option>
    <option value="030">🚌 Linha 030 · Ti Rio Doce / Barra De Jangada</option>
    <option value="031">🚌 Linha 031 · Shopping Center (Ter. Res. Boa Viagem)</option>
    <option value="032">🚌 Linha 032 · Setúbal (Conde Da Boa Vista)</option>
    <option value="034">🚌 Linha 034 · Curcurana / Ti Cajueiro Seco</option>
    <option value="036">🚌 Linha 036 · Aeroporto (Bacurau)</option>
    <option value="037">🚌 Linha 037 · Comportas / Ti Cajueiro Seco</option>
    <option value="038">🚌 Linha 038 · Residencial Boa Viagem (Bacurau)</option>
    <option value="039">🚌 Linha 039 · Setúbal (Príncipe)</option>
    <option value="041">🚌 Linha 041 · Setúbal (Opcional)</option>
    <option value="043">🚌 Linha 043 · Aeroporto / Tacaruna (Derby)</option>
    <option value="044">🚌 Linha 044 · Massangana (Boa Vista)</option>
    <option value="049">🚌 Linha 049 · Ti Tip / Moreno (Br-232)</option>
    <option value="050">🚌 Linha 050 · Ti Pe-15 / Boa Viagem</option>
    <option value="061">🚌 Linha 061 · Piedade</option>
    <option value="062">🚌 Linha 062 · Jardim Piedade</option>
    <option value="063">🚌 Linha 063 · Jardim Piedade (Bacurau)</option>
    <option value="064">🚌 Linha 064 · Piedade (Opcional)</option>
    <option value="065">🚌 Linha 065 · Piedade / Ti Prazeres</option>
    <option value="069">🚌 Linha 069 · Conj. Catamarã</option>
    <option value="070">🚌 Linha 070 · Candeias / Shopping Riomar</option>
    <option value="071">🚌 Linha 071 · Candeias</option>
    <option value="072">🚌 Linha 072 · Candeias (Opcional)</option>
    <option value="073">🚌 Linha 073 · Candeias (Bacurau)</option>
    <option value="075">🚌 Linha 075 · Ti Prazeres / Curcurana</option>
    <option value="080">🚌 Linha 080 · Ti Joana Bezerra / Boa Viagem</option>
    <option value="101">🚌 Linha 101 · Ti Recife / Ti J. Bezerra (Boa Vista)</option>
    <option value="102">🚌 Linha 102 · Ti Santa Luzia / Ibura</option>
    <option value="103">🚌 Linha 103 · Ur-11 / Ti Barro</option>
    <option value="104">🚌 Linha 104 · Ti J. Bezerra / Ti Recife (Imip)</option>
    <option value="106">🚌 Linha 106 · Ti Santa Luzia / Parque Aeronáutica (Jiquiá)</option>
    <option value="1062">🚌 Linha 1062 · Ti Abreu E Lima (Pcr) (Parador)</option>
    <option value="107">🚌 Linha 107 · Ti Recife (Cabugá/Pcr)</option>
    <option value="1076">🚌 Linha 1076 · Ti Pelópidas (Pcr) (Parador)</option>
    <option value="108">🚌 Linha 108 · Ti Barro / Ceasa</option>
    <option value="110">🚌 Linha 110 · Ibura / Ti Prazeres</option>
    <option value="1100">🚌 Linha 1100 · Ti Pe-15 (Pcr) (Parador)</option>
    <option value="115">🚌 Linha 115 · Ti Aeroporto / Ti Afogados</option>
    <option value="116">🚌 Linha 116 · Ti Recife (Príncipe)</option>
    <option value="117">🚌 Linha 117 · Ti Recife (Pcr/Cabugá)</option>
    <option value="118">🚌 Linha 118 · Prazeres / Boa Viagem</option>
    <option value="120">🚌 Linha 120 · Alto Dois Carneiros / Shopping Recife</option>
    <option value="121">🚌 Linha 121 · Vila Da Sudene</option>
    <option value="122">🚌 Linha 122 · Vila Do Ipsep</option>
    <option value="125">🚌 Linha 125 · Córrego Da Gameleira (Vila Do Sesi) / Ti Tancredo Neves</option>
    <option value="126">🚌 Linha 126 · Ti Tancredo Neves / Ur-03</option>
    <option value="128">🚌 Linha 128 · Ti Barro / Ur-03 (Milagres)</option>
    <option value="129">🚌 Linha 129 · Paiva / Ti Cabo</option>
    <option value="131">🚌 Linha 131 · Ur-02 (Bacurau)</option>
    <option value="132">🚌 Linha 132 · Ti Tancredo Neves / Ur-02 (Ibura)</option>
    <option value="134">🚌 Linha 134 · Lagoa Encantada / Ti Tancredo Neves</option>
    <option value="135">🚌 Linha 135 · Ur-10 / Ti Tancredo Neves</option>
    <option value="136">🚌 Linha 136 · Ti Tancredo Neves / Ur-05</option>
    <option value="138">🚌 Linha 138 · Ti Tancredo Neves / Zumbi Do Pacheco</option>
    <option value="139">🚌 Linha 139 · Ti Cabo / Ti Cajueiro Seco</option>
    <option value="140">🚌 Linha 140 · Ti Cajueiro Seco / Shopping Recife</option>
    <option value="141">🚌 Linha 141 · Jardim Monte Verde / Ti Tancredo Neves</option>
    <option value="142">🚌 Linha 142 · Ti Tancredo Neves / Alto Dois Carneiros</option>
    <option value="143">🚌 Linha 143 · Ti Tancredo Neves / Ur-06</option>
    <option value="144">🚌 Linha 144 · Ur-04 / Ti Tancredo Neves</option>
    <option value="145">🚌 Linha 145 · Alto Dois Carneiros (Bacurau)</option>
    <option value="146">🚌 Linha 146 · Ur-11 (Bacurau)</option>
    <option value="149">🚌 Linha 149 · Ti Cavaleiro / Zumbi Do Pacheco</option>
    <option value="151">🚌 Linha 151 · Jardim Jordão / Ti Aeroporto</option>
    <option value="152">🚌 Linha 152 · Jordão Baixo / Ti Aeroporto</option>
    <option value="153">🚌 Linha 153 · Jordão Alto / Ti Aeroporto</option>
    <option value="154">🚌 Linha 154 · Jordão (Bacurau)</option>
    <option value="155">🚌 Linha 155 · Jordão Baixo / Boa Viagem</option>
    <option value="157">🚌 Linha 157 · Gaibu / Ti Cabo</option>
    <option value="158">🚌 Linha 158 · Garapu / Ti Cabo</option>
    <option value="159">🚌 Linha 159 · Charneca / Ti Cabo</option>
    <option value="160">🚌 Linha 160 · Gaibu / Barra De Jangada - Via Paiva (Opcional)</option>
    <option value="162">🚌 Linha 162 · Muribeca / Ti Cajueiro Seco</option>
    <option value="163">🚌 Linha 163 · Ti Cajueiro Seco (Circular)</option>
    <option value="164">🚌 Linha 164 · Marcos Freire / Ti Cajueiro Seco</option>
    <option value="165">🚌 Linha 165 · Muribeca Dos Guararapes / Ti Cajueiro Seco</option>
    <option value="166">🚌 Linha 166 · Ti Cajueiro Seco (Rua Do Sol)</option>
    <option value="167">🚌 Linha 167 · Ti Tancredo Neves (Imip)</option>
    <option value="168">🚌 Linha 168 · Ti Tancredo Neves (Cde. B. Vista)</option>
    <option value="170">🚌 Linha 170 · Muribeca Dos Guararapes (Bacurau)</option>
    <option value="171">🚌 Linha 171 · Lot. Integração / Ti Cajueiro Seco</option>
    <option value="172">🚌 Linha 172 · Marcos Freire (Bacurau)</option>
    <option value="178">🚌 Linha 178 · Porto De Suape / Ti Cabo</option>
    <option value="181">🚌 Linha 181 · Cabo (Cohab) / Ti Cajueiro Seco</option>
    <option value="183">🚌 Linha 183 · Pte. Dos Carvalhos / Ti Cajueiro Seco</option>
    <option value="184">🚌 Linha 184 · Cabo (Bacurau)</option>
    <option value="185">🚌 Linha 185 · Ti Cabo</option>
    <option value="1903">🚌 Linha 1903 · Araçoiaba / Ti Igarassu</option>
    <option value="1904">🚌 Linha 1904 · Ti Igarassu / Nova Cruz</option>
    <option value="1905">🚌 Linha 1905 · Ti Abreu E Lima / Ti Igarassu</option>
    <option value="1906">🚌 Linha 1906 · Ti Pelópidas / Ti Macaxeira</option>
    <option value="1907">🚌 Linha 1907 · Paulista / Rio Doce</option>
    <option value="1908">🚌 Linha 1908 · Ti Igarassu / Botafogo</option>
    <option value="1909">🚌 Linha 1909 · Ti Pelópidas / Ti Joana Bezerra</option>
    <option value="191">🚌 Linha 191 · Recife / Porto De Galinhas (N. Sra. Do Ó)</option>
    <option value="1911">🚌 Linha 1911 · Ouro Preto (Cohab)</option>
    <option value="1912">🚌 Linha 1912 · Caetés I / Ti Abreu E Lima</option>
    <option value="1913">🚌 Linha 1913 · Ti Pe-15 / Ti Joana Bezerra</option>
    <option value="1917">🚌 Linha 1917 · Caetés Ii / Ti Abreu E Lima</option>
    <option value="1918">🚌 Linha 1918 · Ti Igarassu (Circular)</option>
    <option value="1921">🚌 Linha 1921 · Ouro Preto / Ti Pe-15</option>
    <option value="1922">🚌 Linha 1922 · Pau Amarelo / Ti Pelópidas</option>
    <option value="1923">🚌 Linha 1923 · Cidade Tabajara / Ti Pe-15</option>
    <option value="1926">🚌 Linha 1926 · Ouro Preto (Jatobá Ii)</option>
    <option value="1927">🚌 Linha 1927 · Ouro Preto (Bacurau)</option>
    <option value="1928">🚌 Linha 1928 · Maranguape Ii (Bacurau)</option>
    <option value="1929">🚌 Linha 1929 · Alameda Paulista / Ti Rio Doce (Jaguarana)</option>
    <option value="1931">🚌 Linha 1931 · Jardim Paulista Baixo / Ti Pelópidas</option>
    <option value="1932">🚌 Linha 1932 · Jardim Paulista Alto / Ti Pelópidas</option>
    <option value="1933">🚌 Linha 1933 · Ti Pe-15 / Ti Abreu E Lima</option>
    <option value="1934">🚌 Linha 1934 · Arthur Lundgren I / Ti Pelópidas</option>
    <option value="1935">🚌 Linha 1935 · Paratibe / Ti Pelópidas</option>
    <option value="1936">🚌 Linha 1936 · Mirueira (Bacurau)</option>
    <option value="1937">🚌 Linha 1937 · Ti Abreu E Lima / Nova Aurora</option>
    <option value="1940">🚌 Linha 1940 · Ti Pe-15 (Circular)</option>
    <option value="1941">🚌 Linha 1941 · Arthur Lundgren Ii / Ti Pelópidas</option>
    <option value="1943">🚌 Linha 1943 · Mirueira / Ti Pelópidas</option>
    <option value="1944">🚌 Linha 1944 · Ti Pelópidas / Maria Farinha (Lot. Conceição)</option>
    <option value="1945">🚌 Linha 1945 · Jaguarana (Alameda) / Ti Pelópidas</option>
    <option value="1946">🚌 Linha 1946 · Ti Igarassu (Br-101)</option>
    <option value="1948">🚌 Linha 1948 · Ti Abreu E Lima / Ti Pelópidas (Circular)</option>
    <option value="195">🚌 Linha 195 · Recife / Porto De Galinhas (Opcional)</option>
    <option value="1950">🚌 Linha 1950 · Engenho Maranguape / Varadouro</option>
    <option value="1952">🚌 Linha 1952 · Ti Pelópidas / Ti Rio Doce</option>
    <option value="1953">🚌 Linha 1953 · Maranguape Ii / Ti Pelópidas</option>
    <option value="1955">🚌 Linha 1955 · Ti Pelópidas / Cj. Praia Do Janga (Eng. Maranguape)</option>
    <option value="1956">🚌 Linha 1956 · Igarassu (Bacurau)</option>
    <option value="1957">🚌 Linha 1957 · Caetés I (Bacurau)</option>
    <option value="1958">🚌 Linha 1958 · Costa Azul / Ti Pelópidas</option>
    <option value="196">🚌 Linha 196 · Ti Cabo / P. De Galinhas (N. Sra. Do Ó)</option>
    <option value="1960">🚌 Linha 1960 · Ti Rio Doce / Maria Farinha (Casa Caiada)</option>
    <option value="1963">🚌 Linha 1963 · Ti Pe-15 / Ti Igarassu (Sítio Histórico)</option>
    <option value="1964">🚌 Linha 1964 · Ti Igarassu / Ti Macaxeira</option>
    <option value="1966">🚌 Linha 1966 · Ti Rio Doce / Ti Pe-15 (Fragoso)</option>
    <option value="1967">🚌 Linha 1967 · Ti Igarassu (Sítio Histórico)</option>
    <option value="1968">🚌 Linha 1968 · Ilha De Itamaracá / Ti Igarassu</option>
    <option value="1969">🚌 Linha 1969 · Itapissuma / Ti Igarassu</option>
    <option value="1971">🚌 Linha 1971 · Amparo</option>
    <option value="1973">🚌 Linha 1973 · Casa Caiada (Conde Boa Vista)</option>
    <option value="1974">🚌 Linha 1974 · Jardim Atlântico</option>
    <option value="1975">🚌 Linha 1975 · Amparo (Bacurau)</option>
    <option value="1977">🚌 Linha 1977 · Ti Pelópidas (Conde Boa Vista)</option>
    <option value="1978">🚌 Linha 1978 · Loteamento Conceição / Ti Rio Doce (Pe-22)</option>
    <option value="198">🚌 Linha 198 · Ipojuca / Ti Cabo</option>
    <option value="1980">🚌 Linha 1980 · Igarassu / Cidade Tabajara</option>
    <option value="1981">🚌 Linha 1981 · Ti Rio Doce / Ti Joana Bezerra</option>
    <option value="1982">🚌 Linha 1982 · Conjunto Beira Mar / Derby</option>
    <option value="1983">🚌 Linha 1983 · Ti Rio Doce (Princesa Isabel)</option>
    <option value="1984">🚌 Linha 1984 · Lot. Bonfim / Ti Abreu E Lima</option>
    <option value="1985">🚌 Linha 1985 · Rio Doce (Bacurau)</option>
    <option value="1986">🚌 Linha 1986 · Ti Pe-15 / Ti Rio Doce</option>
    <option value="1987">🚌 Linha 1987 · Ti Rio Doce (Príncipe / Conde Boa Vista)</option>
    <option value="1988">🚌 Linha 1988 · Desterro / Ti Abreu E Lima</option>
    <option value="1989">🚌 Linha 1989 · Lot. Planalto / Ti Abreu E Lima</option>
    <option value="199">🚌 Linha 199 · Camela / Ti Cabo</option>
    <option value="1992">🚌 Linha 1992 · Pau Amarelo</option>
    <option value="1993">🚌 Linha 1993 · Conjunto Praia Do Janga</option>
    <option value="1994">🚌 Linha 1994 · Conjunto Beira Mar</option>
    <option value="1995">🚌 Linha 1995 · Pau Amarelo (Bacurau)</option>
    <option value="1996">🚌 Linha 1996 · Arthur Lundgren Ii / Rio Doce (Paratibe)</option>
    <option value="1998">🚌 Linha 1998 · Caetés Iii / Ti Abreu E Lima</option>
    <option value="200">🚌 Linha 200 · Ti Jaboatão (Parador)</option>
    <option value="201">🚌 Linha 201 · Moreno / Ti Jaboatão</option>
    <option value="202">🚌 Linha 202 · Ti Barro / Ti Macaxeira (Várzea)</option>
    <option value="203">🚌 Linha 203 · Ti Barro / Zumbi Do Pacheco (Lot.)</option>
    <option value="2040">🚌 Linha 2040 · Cdu / Boa Viagem / Caxangá</option>
    <option value="2043">🚌 Linha 2043 · Ti Cdu / Ti Joana Bezerra (Parador)</option>
    <option value="205">🚌 Linha 205 · Ti Barro / Ur-05 (Br-101)</option>
    <option value="206">🚌 Linha 206 · Ti Barro / Ti Prazeres (Jordão)</option>
    <option value="2060">🚌 Linha 2060 · Ti Tancredo Neves / Ti Macaxeira</option>
    <option value="207">🚌 Linha 207 · Ti Barro / Ti Macaxeira (Br-101)</option>
    <option value="208">🚌 Linha 208 · Nossa Senhora Da Conceição / Ti Jaboatão</option>
    <option value="209">🚌 Linha 209 · Ti Barro / Coqueiral</option>
    <option value="211">🚌 Linha 211 · Vila Tamandaré</option>
    <option value="212">🚌 Linha 212 · Jardim São Paulo</option>
    <option value="216">🚌 Linha 216 · Ti Barro / Ti Cajueiro Seco</option>
    <option value="219">🚌 Linha 219 · Ti Tip / Ti Jaboatão (Sancho)</option>
    <option value="220">🚌 Linha 220 · Ti Jaboatão / Ti Cavaleiro</option>
    <option value="221">🚌 Linha 221 · Vila Cardeal E Silva</option>
    <option value="222">🚌 Linha 222 · Jardim Uchôa</option>
    <option value="229">🚌 Linha 229 · Marcos Freire (Opcional)</option>
    <option value="232">🚌 Linha 232 · Cavaleiro</option>
    <option value="233">🚌 Linha 233 · Cavaleiro (Bacurau)</option>
    <option value="238">🚌 Linha 238 · Ti Jaboatão / Ti Barro</option>
    <option value="240">🚌 Linha 240 · Cavaleiro / Ceasa</option>
    <option value="2402">🚌 Linha 2402 · Parque Capibaribe / Caxangá</option>
    <option value="2410">🚌 Linha 2410 · Parque Capibaribe / Ti Tip</option>
    <option value="2416">🚌 Linha 2416 · Roda De Fogo / Ti Getúlio Vargas</option>
    <option value="2417">🚌 Linha 2417 · Nova Morada / Ti Caxangá</option>
    <option value="2419">🚌 Linha 2419 · Matriz Da Luz / Ti Camaragibe</option>
    <option value="242">🚌 Linha 242 · Pacheco (Floresta)</option>
    <option value="2420">🚌 Linha 2420 · Muribara / Ti Camaragibe</option>
    <option value="2421">🚌 Linha 2421 · Torrões / Ti Getúlio Vargas</option>
    <option value="2423">🚌 Linha 2423 · Engenho Do Meio / Ti Cdu</option>
    <option value="2427">🚌 Linha 2427 · Monsenhor Fabrício (Bacurau)</option>
    <option value="2429">🚌 Linha 2429 · Ti Getúlio Vargas / Ti Cdu</option>
    <option value="243">🚌 Linha 243 · Vila Dois Carneiros</option>
    <option value="2431">🚌 Linha 2431 · Ti Cdu / Ti Caxangá (Ufpe)</option>
    <option value="2433">🚌 Linha 2433 · Brasilit / Ti Cdu</option>
    <option value="2434">🚌 Linha 2434 · Ti Getúlio Vargas / Tamarineira</option>
    <option value="2437">🚌 Linha 2437 · Ti Caxangá (Conde Boa Vista)</option>
    <option value="244">🚌 Linha 244 · Alto Do Vento / Ti Cavaleiro</option>
    <option value="2441">🚌 Linha 2441 · Ti Cdu (Conde Boa Vista)</option>
    <option value="2442">🚌 Linha 2442 · Jd. Primavera (V. Pedreiras) / Ti Cdu</option>
    <option value="2444">🚌 Linha 2444 · Ti Getúlio Vargas (Conde Da Boa Vista)</option>
    <option value="2445">🚌 Linha 2445 · Tabatinga / Ti Caxangá</option>
    <option value="2446">🚌 Linha 2446 · Ur-07 (Várzea) / Ti Cdu</option>
    <option value="2448">🚌 Linha 2448 · Alto Santo Antônio / Ti Camaragibe</option>
    <option value="245">🚌 Linha 245 · Dois Carneiros / Ti Cavaleiro</option>
    <option value="2450">🚌 Linha 2450 · Ti Camaragibe (Conde Boa Vista)</option>
    <option value="2456">🚌 Linha 2456 · Viana / Ti Camaragibe</option>
    <option value="2457">🚌 Linha 2457 · São Lourenço (Bacurau)</option>
    <option value="2459">🚌 Linha 2459 · Ti Cosme E Damião / Ti Caxangá</option>
    <option value="2462">🚌 Linha 2462 · Lot. Santos Cosme Damião (Bacurau)</option>
    <option value="2463">🚌 Linha 2463 · Araçoiaba / Ti Camaragibe</option>
    <option value="2464">🚌 Linha 2464 · Jardim Teresópolis / Ti Caxangá</option>
    <option value="2466">🚌 Linha 2466 · Vera Cruz / Ti Camaragibe</option>
    <option value="2467">🚌 Linha 2467 · Chã De Cruz / Ti Camaragibe</option>
    <option value="2470">🚌 Linha 2470 · Circular Vila Da Fábrica/Santana (Via Bairro Dos Estados)</option>
    <option value="2473">🚌 Linha 2473 · João Paulo Ii / Ti Camaragibe</option>
    <option value="2475">🚌 Linha 2475 · Timbi / Ti Camaragibe</option>
    <option value="2476">🚌 Linha 2476 · Santa Mônica / Ti Camaragibe</option>
    <option value="2477">🚌 Linha 2477 · Santa Terezinha / Ti Camaragibe</option>
    <option value="2478">🚌 Linha 2478 · Santana / Ti Camaragibe</option>
    <option value="2481">🚌 Linha 2481 · Ti Camaragibe / Ti Tip</option>
    <option value="2483">🚌 Linha 2483 · Lot. S. João E S. Paulo / Ti Camaragibe</option>
    <option value="2486">🚌 Linha 2486 · Penedo / Ti Camaragibe</option>
    <option value="2487">🚌 Linha 2487 · Várzea Fria / Ti Camaragibe</option>
    <option value="2488">🚌 Linha 2488 · Vila Da Fábrica / Ti Caxangá</option>
    <option value="2490">🚌 Linha 2490 · Ti Camaragibe / Ti Macaxeira</option>
    <option value="2493">🚌 Linha 2493 · Tiúma / Ti Camaragibe</option>
    <option value="250">🚌 Linha 250 · Ti Jaboatão / Santo Aleixo (Luz)</option>
    <option value="2501">🚌 Linha 2501 · Circular Peroba / Oitenta / Borralho</option>
    <option value="2502">🚌 Linha 2502 · Circular Santa Mônica / Maranguape (V. Beira Rio)</option>
    <option value="2503">🚌 Linha 2503 · Circular Quadra 30 (V. Celeiro)</option>
    <option value="2504">🚌 Linha 2504 · Circular Vale Das Pedreiras (Shopping)</option>
    <option value="2505">🚌 Linha 2505 · Circular Tabatinga / São Jorge (Via Fábrica)</option>
    <option value="251">🚌 Linha 251 · Ti Jaboatão / Santo Aleixo (Rios)</option>
    <option value="252">🚌 Linha 252 · Vila Rica / Ti Jaboatão</option>
    <option value="254">🚌 Linha 254 · Jaboatão (Bacurau)</option>
    <option value="255">🚌 Linha 255 · Quitandinha / Ti Cavaleiro</option>
    <option value="256">🚌 Linha 256 · Ti Cavaleiro / Lot. Nova Esperança</option>
    <option value="258">🚌 Linha 258 · Moreno (Bacurau)</option>
    <option value="261">🚌 Linha 261 · Ti Jaboatão / Vila Piedade</option>
    <option value="262">🚌 Linha 262 · Ti Jaboatão / Malvinas</option>
    <option value="272">🚌 Linha 272 · Colônia / Ti Jaboatão</option>
    <option value="274">🚌 Linha 274 · Ti Jaboatão / Lote 56</option>
    <option value="290">🚌 Linha 290 · Ti Jaboatão / Bonança</option>
    <option value="291">🚌 Linha 291 · Ti Jaboatão / Moreno (Recife Outlet)</option>
    <option value="2920">🚌 Linha 2920 · Ti Rio Doce / Ti Cdu</option>
    <option value="2930">🚌 Linha 2930 · Ti Rio Doce / Dois Irmãos</option>
    <option value="302">🚌 Linha 302 · Caxangá / Ti Tip</option>
    <option value="303">🚌 Linha 303 · Caxangá / Curado Ii (Br-232)</option>
    <option value="311">🚌 Linha 311 · Bongi (Afogados)</option>
    <option value="312">🚌 Linha 312 · Mustardinha</option>
    <option value="313">🚌 Linha 313 · San Martin (A. De Carvalho)</option>
    <option value="314">🚌 Linha 314 · Mangueira</option>
    <option value="315">🚌 Linha 315 · Bongi</option>
    <option value="320">🚌 Linha 320 · Curado I / Ti Santa Luzia</option>
    <option value="321">🚌 Linha 321 · Jardim São Paulo (A. Carvalho)</option>
    <option value="322">🚌 Linha 322 · Jardim São Paulo (Bacurau)</option>
    <option value="324">🚌 Linha 324 · Jardim São Paulo (Piracicaba)</option>
    <option value="330">🚌 Linha 330 · Casa Amarela / Cdu (Av. Caxangá)</option>
    <option value="331">🚌 Linha 331 · Totó (Jardim Planalto)</option>
    <option value="332">🚌 Linha 332 · Totó (Abdias De Carvalho)</option>
    <option value="333">🚌 Linha 333 · Totó (Bacurau)</option>
    <option value="341">🚌 Linha 341 · Curado I</option>
    <option value="342">🚌 Linha 342 · Curados (Opcional)</option>
    <option value="346">🚌 Linha 346 · Ti Tip (Conde Boa Vista)</option>
    <option value="347">🚌 Linha 347 · Ti Tip / Joana Bezerra</option>
    <option value="348">🚌 Linha 348 · Ti Tip / Curado V</option>
    <option value="351">🚌 Linha 351 · Ti Tip / Curado Ii</option>
    <option value="352">🚌 Linha 352 · Curado Ii (Bacurau)</option>
    <option value="360">🚌 Linha 360 · Totó / Boa Viagem</option>
    <option value="361">🚌 Linha 361 · Ti Tip / Curado Iv (Rua 14)</option>
    <option value="362">🚌 Linha 362 · Curado Iv (Bacurau)</option>
    <option value="363">🚌 Linha 363 · Ti Tip / Curado Iv (Av. 01)</option>
    <option value="370">🚌 Linha 370 · Ti Tip / Ti Aeroporto</option>
    <option value="411">🚌 Linha 411 · Plaza Shopping (Conde Da Boa Vista)</option>
    <option value="412">🚌 Linha 412 · Ti Santa Luzia / Ti Getúlio Vargas</option>
    <option value="4123">🚌 Linha 4123 · Três Carneiros Baixo (Cais De Santa Rita)</option>
    <option value="4133">🚌 Linha 4133 · Três Carneiros (Cais De Santa Rita)</option>
    <option value="4137">🚌 Linha 4137 · Ur-11 (Cais De Santa Rita)</option>
    <option value="414">🚌 Linha 414 · Torre</option>
    <option value="418">🚌 Linha 418 · Tiúma / Camaragibe</option>
    <option value="424">🚌 Linha 424 · Cdu / Largo Da Paz (Via Torrões/San Martin)</option>
    <option value="440">🚌 Linha 440 · Cdu / Caxangá / Boa Viagem</option>
    <option value="510">🚌 Linha 510 · Nova Descoberta / Derby</option>
    <option value="511">🚌 Linha 511 · Ti Cdu / Casa Amarela / Alto Do Mandu</option>
    <option value="513">🚌 Linha 513 · Córrego Da Areia</option>
    <option value="514">🚌 Linha 514 · Nova Descoberta (Cór. Do Joaquim)</option>
    <option value="515">🚌 Linha 515 · Nova Descoberta (Bacurau)</option>
    <option value="516">🚌 Linha 516 · Casa Amarela / Torre / Cde. Boa Vista</option>
    <option value="517">🚌 Linha 517 · Córrego Do Inácio</option>
    <option value="520">🚌 Linha 520 · Ti Macaxeira / Parnamirim</option>
    <option value="521">🚌 Linha 521 · Alto Santa Isabel (Cde. Boa Vista)</option>
    <option value="522">🚌 Linha 522 · Dois Irmãos (Rui Barbosa E Príncipe)</option>
    <option value="523">🚌 Linha 523 · Dois Irmãos (Bacurau)</option>
    <option value="524">🚌 Linha 524 · Sítio Dos Pintos (Dois Irmãos)</option>
    <option value="532">🚌 Linha 532 · Dois Irmãos / Casa Amarela (Cruz Cabugá)</option>
    <option value="533">🚌 Linha 533 · Casa Amarela (Bacurau)</option>
    <option value="601">🚌 Linha 601 · Ti Macaxeira / P.R. Bola Na Rede</option>
    <option value="604">🚌 Linha 604 · Ti Macaxeira / Alto Do Burity</option>
    <option value="611">🚌 Linha 611 · Alto José Do Pinho (Cais De Santa Rita)</option>
    <option value="612">🚌 Linha 612 · Morro Da Conceição (Cruz Cabugá)</option>
    <option value="613">🚌 Linha 613 · Morro Da Conceição (Bacurau)</option>
    <option value="621">🚌 Linha 621 · Alto Treze De Maio (Príncipe)</option>
    <option value="622">🚌 Linha 622 · Vasco Da Gama (Cruz Cabugá)</option>
    <option value="623">🚌 Linha 623 · Vasco Da Gama (João De Barros)</option>
    <option value="624">🚌 Linha 624 · Brejo (Cde. Boa Vista)</option>
    <option value="626">🚌 Linha 626 · Brejo (Bacurau)</option>
    <option value="630">🚌 Linha 630 · Vasco Da Gama / Derby</option>
    <option value="631">🚌 Linha 631 · Nova Descoberta (Cabugá)</option>
    <option value="632">🚌 Linha 632 · Alto Do Refúgio (Cabugá)</option>
    <option value="640">🚌 Linha 640 · Guabiraba / Derby (Joana Bezerra)</option>
    <option value="641">🚌 Linha 641 · Ti Macaxeira / Encruzilhada</option>
    <option value="642">🚌 Linha 642 · Guabiraba (Córrego Do Jenipapo)</option>
    <option value="643">🚌 Linha 643 · Córrego Do Jenipapo (Bacurau)</option>
    <option value="644">🚌 Linha 644 · Largo Do Maracanã (Conde Da Boa Vista)</option>
    <option value="645">🚌 Linha 645 · Ti Macaxeira (Av. Norte)</option>
    <option value="650">🚌 Linha 650 · Ti Macaxeira / Ti Xambá</option>
    <option value="680">🚌 Linha 680 · Vasco Da Gama / Afogados</option>
    <option value="700">🚌 Linha 700 · Beberibe / Afogados</option>
    <option value="710">🚌 Linha 710 · Beberibe / Derby (Joana Bezerra)</option>
    <option value="711">🚌 Linha 711 · Alto Do Pascoal</option>
    <option value="712">🚌 Linha 712 · Alto Santa Terezinha</option>
    <option value="713">🚌 Linha 713 · Bomba Do Hemetério</option>
    <option value="714">🚌 Linha 714 · Alto José Bonifácio (Av. Norte)</option>
    <option value="715">🚌 Linha 715 · Alto Santa Terezinha (Bacurau)</option>
    <option value="717">🚌 Linha 717 · José Amarino Dos Reis</option>
    <option value="718">🚌 Linha 718 · Córrego Do Euclides / Derby</option>
    <option value="721">🚌 Linha 721 · Água Fria (Circular)</option>
    <option value="722">🚌 Linha 722 · Campina Do Barreto</option>
    <option value="723">🚌 Linha 723 · Cajueiro</option>
    <option value="724">🚌 Linha 724 · Chão De Estrelas</option>
    <option value="741">🚌 Linha 741 · Dois Unidos</option>
    <option value="742">🚌 Linha 742 · Linha Do Tiro</option>
    <option value="743">🚌 Linha 743 · Alto José Bonifácio (J. Barros)</option>
    <option value="744">🚌 Linha 744 · Dois Unidos (Bacurau)</option>
    <option value="745">🚌 Linha 745 · Alto José Bonifácio (Bacurau)</option>
    <option value="746">🚌 Linha 746 · Alto Do Capitão</option>
    <option value="760">🚌 Linha 760 · Dois Unidos / Derby</option>
    <option value="780">🚌 Linha 780 · Alto Santa Terezinha / Derby</option>
    <option value="800">🚌 Linha 800 · Dois Unidos / Afogados</option>
    <option value="810">🚌 Linha 810 · Ti Xambá / Encruzilhada</option>
    <option value="820">🚌 Linha 820 · Ti Xambá (Cabugá)</option>
    <option value="821">🚌 Linha 821 · Jardim Brasil I (Est. De Belém)</option>
    <option value="822">🚌 Linha 822 · Jardim Brasil I (Cruz Cabugá)</option>
    <option value="823">🚌 Linha 823 · Jardim Brasil Ii (Est. De Belém)</option>
    <option value="824">🚌 Linha 824 · Jardim Brasil Ii (Cruz Cabugá)</option>
    <option value="825">🚌 Linha 825 · Jardim Brasil / Ti Joana Bezerra</option>
    <option value="827">🚌 Linha 827 · Jardim Brasil (Bacurau)</option>
    <option value="831">🚌 Linha 831 · Aguazinha / Ti Xambá</option>
    <option value="841">🚌 Linha 841 · Nova Olinda / Ti Xambá</option>
    <option value="842">🚌 Linha 842 · Águas Compridas / Ti Xambá</option>
    <option value="843">🚌 Linha 843 · Alto Da Bondade / Ti Xambá</option>
    <option value="844">🚌 Linha 844 · Santa Casa / Ti Xambá</option>
    <option value="846">🚌 Linha 846 · Águas Compridas (Bacurau)</option>
    <option value="847">🚌 Linha 847 · Alto Nova Olinda / Ti Xambá</option>
    <option value="852">🚌 Linha 852 · Caixa D'Água / Ti Xambá</option>
    <option value="858">🚌 Linha 858 · Ti Joana Bezerra / Ti Afogados / Ti Barro</option>
    <option value="860">🚌 Linha 860 · Ti Xambá (Príncipe)</option>
    <option value="861">🚌 Linha 861 · Ti Joana Bezerra / Ti Xambá</option>
    <option value="870">🚌 Linha 870 · Ti Xambá / Ti Largo Da Paz</option>
    <option value="881">🚌 Linha 881 · Ti Xambá / Rio Doce (Av. Getúlio Vargas)</option>
    <option value="882">🚌 Linha 882 · Ti Xambá / Rio Doce (Carlos De Lima Cavalcanti)</option>
    <option value="883">🚌 Linha 883 · Ti Pe-15 / Ti Xambá</option>
    <option value="884">🚌 Linha 884 · Jardim Brasil / Rio Doce</option>
    <option value="885">🚌 Linha 885 · Sítio Novo / Rio Doce</option>
    <option value="886">🚌 Linha 886 · Ouro Preto / Rio Doce</option>
    <option value="892">🚌 Linha 892 · Alto Do Cajueiro / Ti Xambá</option>
    <option value="893">🚌 Linha 893 · Ti Pe-15 / Alto Da Conquista</option>
    <option value="894">🚌 Linha 894 · Ti Xambá / Córrego Do Abacaxi</option>
    <option value="895">🚌 Linha 895 · Alto Sol Nascente / Ti Xambá</option>
    <option value="901">🚌 Linha 901 · Ti Abreu E Lima / Ti Macaxeira</option>
    <option value="910">🚌 Linha 910 · Piedade / Ti Rio Doce</option>
    <option value="9104">🚌 Linha 9104 · Casseterita / Casa Amarela / Jaqueira</option>
    <option value="9105">🚌 Linha 9105 · Córrego Do Boleiro / Casa Amarela / Jaqueira</option>
    <option value="9108">🚌 Linha 9108 · Dois Unidos / Torre</option>
    <option value="9110">🚌 Linha 9110 · Campo Grande / Afogados</option>
    <option value="9112">🚌 Linha 9112 · Casa Amarela / Bomba Do Hemetério / Shopping Tacaruna</option>
    <option value="914">🚌 Linha 914 · Ti Pe-15 / Ti Afogados</option>
    <option value="916">🚌 Linha 916 · Ouro Preto / Joana Bezerra</option>
    <option value="9205">🚌 Linha 9205 · Jardim Uchôa / Boa Viagem</option>
    <option value="9301">🚌 Linha 9301 · San Martin / Lagoa Do Araçá / Boa Viagem</option>
    <option value="Centro 1">🚌 Linha Centro 1 · Recife - Camaragibe</option>
    <option value="Centro 2">🚌 Linha Centro 2 · Recife - Jaboatão</option>
    <option value="Sul">🚌 Linha Sul · Recife - Cajueiro Seco</option>
    <option value="VLT Cabo">🚌 Linha VLT Cabo · Cabo de Santo Agostinho - Cajueiro Seco</option>
    <option value="VLT Curado">🚌 Linha VLT Curado · Curado - Cajueiro Seco</option>
  </optgroup>
            </select>
          </div>
        </div>

        <button class="btn btn-primary" style="width:100%; min-height:50px; font-size:15.5px; font-weight:800; border-radius:14px; margin-bottom:10px;" onclick="goToAuthStep('preferences')">
          Avançar: Configurar Proteção no Fone →
        </button>
        <button class="btn" style="width:100%; min-height:42px; font-size:13.5px; border-radius:14px;" onclick="goToAuthStep('welcome')">
          ← Voltar
        </button>
      </div>

      <!-- STEP 3: PREFERÊNCIAS DE SEGURANÇA & FONE -->
      <div id="auth-step-preferences" style="display:none;">
        <div style="margin-bottom:20px;">
          <span class="tag tag-amber" style="margin-bottom:8px;">Etapa 2 de 2 · Modo Fone no Bolso</span>
          <h2 style="font-size:22px; font-weight:800; margin-top:4px;">Como o GrafoParada deve te proteger?</h2>
          <p style="font-size:13.5px; color:var(--text-secondary);">A inteligência artificial avisa você sem que você precise tirar o celular da bolsa ou bolso na pista.</p>
        </div>

        <div style="display:flex; flex-direction:column; gap:14px; margin-bottom:20px;">
          <div style="background:var(--bg-surface); border:2px solid var(--brand-green); border-radius:14px; padding:16px;">
            <div style="font-weight:800; font-size:15px; margin-bottom:4px; display:flex; align-items:center; gap:8px;">
              <span>🎧 Voz Humana Natural no Fone</span>
              <span class="tag tag-emerald" style="font-size:11px;">Recomendado</span>
            </div>
            <p style="font-size:13px; color:var(--text-secondary); margin-bottom:12px;">
              O app sussurra discretamente no seu fone quando o ônibus estiver chegando na curva da PE-60.
            </p>

            <div style="margin-bottom:10px;">
              <label style="display:block; font-size:12.5px; font-weight:700; margin-bottom:4px;">Escolha a voz do seu assistente:</label>
              <select id="pref-voice-select" style="width:100%; min-height:44px; padding:8px 12px; font-size:13.5px; border:1px solid var(--border-strong); border-radius:10px; background:var(--bg-subtle); color:var(--text-main); font-weight:700;">
                <option value="pt-BR-FranciscaNeural" selected>Francisca (Feminina Natural · PE-60)</option>
                <option value="pt-BR-AntonioNeural">Antônio (Masculino Natural)</option>
                <option value="pt-BR-ThalitaMultilingualNeural">Thalita (Jovem Expressiva)</option>
              </select>
            </div>

            <button class="btn btn-amber" style="width:100%; min-height:38px; font-size:13px; font-weight:800;" onclick="testPrefVoice()">
              ▶️ Testar Voz no Fone Agora
            </button>
          </div>

          <div style="background:var(--bg-surface); border:1px solid var(--border); border-radius:14px; padding:14px;">
            <label style="display:flex; gap:10px; align-items:flex-start; cursor:pointer;">
              <input type="checkbox" id="pref-opt-presence" checked style="width:20px; height:20px; margin-top:2px; accent-color:var(--brand-green);" />
              <div style="font-size:13px; line-height:1.45; color:var(--text-secondary);">
                <strong>Proteção Coletiva (Companhia Anônima):</strong> Contar minha presença anonimamente na parada para que outras pessoas saibam que há grupo seguro no ponto. Seus dados nunca são vendidos (100% LGPD).
              </div>
            </label>
          </div>
        </div>

        <button class="btn btn-emerald" style="width:100%; min-height:52px; font-size:16px; font-weight:800; border-radius:14px; border:2px solid var(--brand-green); margin-bottom:10px;" onclick="completeRegistration()">
          ✅ Concluir Cadastro &amp; Abrir Meu Mapa
        </button>
        <button class="btn" style="width:100%; min-height:42px; font-size:13.5px; border-radius:14px;" onclick="goToAuthStep('signup')">
          ← Voltar para Dados
        </button>
      </div>

      <!-- STEP 4: LOGIN RÁPIDO -->
      <div id="auth-step-login" style="display:none;">
        <div style="margin-bottom:20px;">
          <h2 style="font-size:22px; font-weight:800; margin-top:4px;">Entrar na sua conta</h2>
          <p style="font-size:13.5px; color:var(--text-secondary);">Acesse com seu celular ou nome cadastrado:</p>
        </div>

        <div style="display:flex; flex-direction:column; gap:14px; margin-bottom:20px;">
          <div>
            <label style="display:block; font-size:13px; font-weight:700; margin-bottom:6px;">Celular ou Nome:</label>
            <input id="login-phone" type="text" placeholder="Ex: Cauã Cunha ou (81) 98888-7766" value="Cauã Cunha"
              style="width:100%; min-height:48px; padding:10px 14px; font-size:14px; border:1.5px solid var(--border-strong); border-radius:12px; background:var(--bg-surface); color:var(--text-main);" />
          </div>

          <div>
            <label style="display:block; font-size:13px; font-weight:700; margin-bottom:6px;">PIN de Acesso:</label>
            <input id="login-pin" type="password" value="1234"
              style="width:100%; min-height:48px; padding:10px 14px; font-size:14px; border:1.5px solid var(--border-strong); border-radius:12px; background:var(--bg-surface); color:var(--text-main);" />
          </div>
        </div>

        <button class="btn btn-primary" style="width:100%; min-height:50px; font-size:15.5px; font-weight:800; border-radius:14px; margin-bottom:10px;" onclick="doLogin()">
          Entrar no GrafoParada
        </button>
        <button class="btn" style="width:100%; min-height:42px; font-size:13.5px; border-radius:14px;" onclick="goToAuthStep('welcome')">
          ← Voltar
        </button>
      </div>

    </div>
  </div>

  <!-- MODAL DE PERFIL DO USUÁRIO & REINICIAR TESTE -->
  <div id="user-profile-modal" style="display:none; position:fixed; inset:0; background:rgba(0,0,0,0.65); z-index:99999; justify-content:center; align-items:center; padding:16px;">
    <div style="background:var(--bg-surface); border:1px solid var(--border); border-radius:var(--radius-lg); max-width:440px; width:100%; padding:24px; box-shadow:0 12px 32px rgba(0,0,0,0.35);">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
        <h3 style="font-size:20px; font-weight:800;">👤 Meu Perfil de Passageiro</h3>
        <span class="tag tag-emerald">Ativo</span>
      </div>

      <div style="background:var(--bg-subtle); border:1px solid var(--border); border-radius:12px; padding:14px; margin-bottom:16px; line-height:1.5;">
        <div><strong>Nome:</strong> <span id="prof-modal-name">Cauã Cunha</span></div>
        <div><strong>Telefone:</strong> <span id="prof-modal-phone">(81) 98888-7766</span></div>
        <div><strong>Parada Principal:</strong> <span id="prof-modal-place">Camela (PE-60)</span></div>
        <div><strong>Linha Favorita:</strong> <span id="prof-modal-line">Linha 178</span></div>
        <div><strong>Voz Selecionada:</strong> <span id="prof-modal-voice">Francisca</span></div>
      </div>

      <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:18px;">
        <div style="background:var(--brand-green-bg); border:1px solid var(--brand-green-border); border-radius:10px; padding:10px; text-align:center;">
          <div style="font-size:22px; font-weight:800; color:var(--brand-green);">14</div>
          <div style="font-size:11.5px; color:var(--brand-green); font-weight:700;">Viagens Seguras</div>
        </div>
        <div style="background:var(--warn-amber-bg); border:1px solid var(--warn-amber-border); border-radius:10px; padding:10px; text-align:center;">
          <div style="font-size:22px; font-weight:800; color:var(--warn-amber);">0</div>
          <div style="font-size:11.5px; color:var(--warn-amber); font-weight:700;">Assaltos (No Bolso)</div>
        </div>
      </div>

      <button class="btn btn-danger" style="width:100%; min-height:46px; font-size:14px; font-weight:800; border-radius:12px; margin-bottom:10px;" onclick="logoutAndResetTest()">
        🚪 Sair da Conta / Recomeçar Teste do Zero
      </button>
      <button class="btn" style="width:100%; min-height:40px; font-size:13px; border-radius:12px;" onclick="closeUserProfileModal()">
        Fechar
      </button>
    </div>
  </div>

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
      <button id="btn-user-profile" class="btn btn-emerald" style="min-height:36px; padding:4px 10px; font-size:12.5px; font-weight:800; border:2px solid var(--brand-green);" onclick="openUserProfileModal()">
        👤 <span id="header-user-name">Minha Conta</span>
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
      <div style="font-size:12.5px; color:var(--text-muted); margin-bottom:12px; word-break:break-all;">
        Link direto: <a href="https://icy-oranges-think.loca.lt" target="_blank" style="color:var(--brand-green); font-weight:700;">https://icy-oranges-think.loca.lt</a>
      </div>
      <div style="font-size:12px; text-align:left; background:var(--bg-subtle); border:1px solid var(--border); border-radius:var(--radius-sm); padding:10px 12px; margin-bottom:16px; line-height:1.45; color:var(--text-secondary);">
        💡 <strong>Dicas importantes ao abrir no celular:</strong><br>
        1. Se o túnel de teste solicitar confirmação, digite o IP da sua rede: <strong style="color:var(--brand-green);">177.200.245.197</strong> e toque em <em>Continue</em>.<br>
        2. Quando o navegador perguntar <em>"Deseja permitir que o site use sua localização?"</em>, toque em <strong>Permitir</strong> (ou <em>Durante o uso do app</em>).
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
        <div class="map-bar-top desktop-only">
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
          <!-- FLOATING TOP BAR ON MOBILE -->
          <div class="mobile-map-floating-bar mobile-only">
            <div class="mobile-search-pill">
              <span style="font-size:14px;">🔍</span>
              <input type="text" id="mobile-search-input" placeholder="Buscar parada ou rua..." onkeydown="if(event.key==='Enter') searchUserPlaceMobile()" />
            </div>
            <button class="mobile-quick-chip" onclick="setSimulatedUserLocation(-8.494915, -35.092190, 'Camela (PE-60) · Ipojuca', true)">📍 Camela</button>
            <button class="mobile-quick-chip" onclick="openAllTisModal()" style="background:var(--user-blue-bg) !important; border-color:var(--user-blue) !important; color:var(--user-blue) !important;">🏛️ T.I.s</button>
          </div>

          <!-- FLOATING GPS TARGET BUTTON (FAB) -->
          <button class="mobile-fab-gps mobile-only" onclick="useRealBrowserGps()" title="Centralizar no meu GPS">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="9"></circle>
              <line x1="12" y1="1" x2="12" y2="4"></line>
              <line x1="12" y1="20" x2="12" y2="23"></line>
              <line x1="1" y1="12" x2="4" y2="12"></line>
              <line x1="20" y1="12" x2="23" y2="12"></line>
              <circle cx="12" cy="12" r="3" fill="currentColor"></circle>
            </svg>
          </button>

          <div id="pe60-leaflet-map" role="region" aria-label="Mapa interativo"></div>

          <div class="map-legend-pill">
            <span><i class="legend-dot" style="background:#0057b8;"></i>Você (Clique ou Arraste)</span>
            <span><i class="legend-dot" style="background:#0a6b46;"></i>Parada Normal</span>
            <span><i class="legend-dot" style="background:#d97706;"></i>Atenção</span>
            <span><i class="legend-dot" style="background:#dc2626;"></i>Parada Crítica</span>
          </div>
        </div>

        <div class="map-bar-bottom desktop-only">
          <span style="font-size:13px; font-weight:700; color:var(--text-secondary);">Paradas da Linha 178 (PE-60):</span>
          <div id="quick-stop-selector" style="display:flex; gap:4px; flex-wrap:wrap;"></div>
        </div>
      </div>

      <!-- RIGHT: SINGLE FOCUSED COMPANION CARD (BOTTOM SHEET ON MOBILE) -->
      <div class="card companion-sheet" id="companion-bottom-sheet">
        <!-- DRAG HANDLE FOR MOBILE BOTTOM SHEET -->
        <div class="sheet-handle-bar mobile-only" onclick="toggleMobileSheet()">
          <div class="sheet-handle-pill"></div>
          <span class="sheet-handle-hint" id="sheet-handle-text">▲ Puxe para ver paradas e rotas</span>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:10px; margin-bottom:4px;">
          <div>
            <span style="font-size:12.5px; font-weight:700; color:var(--user-blue); text-transform:uppercase;" id="user-loc-coords-badge">
              Sua Parada Atual
            </span>
            <h2 id="insp-stop-header" style="font-size:18px; font-weight:800; margin-top:2px;">
              Parada #11 · Trevo de Ipojuca (PE-60)
            </h2>
          </div>
          <span id="insp-stop-tag" class="tag tag-crimson">Atraso Crítico</span>
        </div>

        <!-- LINE BADGE & SWITCHER BUTTON -->
        <div style="display:flex; justify-content:space-between; align-items:center; background:var(--bg-subtle); border:1px solid var(--border); border-radius:10px; padding:6px 10px; margin:6px 0;">
          <div style="font-size:12.5px; font-weight:700; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">
            🚌 Linha: <strong id="active-line-badge" style="color:var(--brand-green);">178 · Dantas Barreto / Suape</strong>
          </div>
          <button class="btn btn-emerald" style="min-height:28px; padding:2px 8px; font-size:11.5px; font-weight:800; border:1.5px solid var(--brand-green); white-space:nowrap; margin-left:6px;" onclick="openLineSwitcherModal()">
            🔄 Trocar Linha (400)
          </button>
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

  <!-- NATIVE MOBILE BOTTOM NAVIGATION BAR -->
  <nav class="mobile-bottom-nav mobile-only" aria-label="Navegação Móvel">
    <button class="mob-nav-item active" onclick="switchModule('mod-gis', this)">
      <span class="mob-nav-icon">🗺️</span>
      <span class="mob-nav-label">Mapa & Ônibus</span>
    </button>
    <button class="mob-nav-item" onclick="switchModule('mod-safety', this)">
      <span class="mob-nav-icon">🛡️</span>
      <span class="mob-nav-label">Segurança</span>
    </button>
    <button class="mob-nav-item" onclick="switchModule('mod-tech', this)">
      <span class="mob-nav-icon">⚡</span>
      <span class="mob-nav-label">IA da Frota</span>
    </button>
  </nav>

  <!-- MODAL DE TROCA DE LINHA (TODAS AS 400 LINHAS DO GRANDE RECIFE) -->
  <div id="line-switcher-modal" style="display:none; position:fixed; inset:0; background:rgba(0,0,0,0.65); z-index:99999; justify-content:center; align-items:center; padding:16px;">
    <div style="background:var(--bg-surface); border:1px solid var(--border); border-radius:var(--radius-lg); max-width:480px; width:100%; padding:22px; box-shadow:0 12px 32px rgba(0,0,0,0.35);">
      <h3 style="font-size:18px; font-weight:800; margin-bottom:4px;">🔄 Trocar Linha de Ônibus</h3>
      <p style="font-size:13px; color:var(--text-secondary); margin-bottom:12px;">Selecione qualquer uma das 400 linhas do Grande Recife para monitorar:</p>
      <input id="switcher-line-search" type="text" placeholder="🔍 Digite número ou nome da linha..." oninput="filterSwitcherOptions(this.value)"
        style="width:100%; min-height:42px; padding:8px 12px; font-size:13px; border:1.5px solid var(--border-strong); border-radius:10px; background:var(--bg-surface); color:var(--text-main); margin-bottom:8px;" />
      <select id="switcher-line-select" size="8" style="width:100%; max-height:220px; padding:6px; font-size:13px; border:1.5px solid var(--border-strong); border-radius:10px; background:var(--bg-surface); color:var(--text-main); margin-bottom:16px;">
  <optgroup label="⭐ Eixo Sul / PE-60 / Suape / Camela / Cabo">
    <option value="001">🚌 Linha 001 · Ponte Dos Carvalhos / Prazeres (Barra De Jangada)</option>
    <option value="034">🚌 Linha 034 · Curcurana / Ti Cajueiro Seco</option>
    <option value="037">🚌 Linha 037 · Comportas / Ti Cajueiro Seco</option>
    <option value="178" selected>🚌 Linha 178 · Porto De Suape / Ti Cabo</option>
    <option value="191">🚌 Linha 191 · Recife / Porto De Galinhas (N. Sra. Do Ó)</option>
    <option value="195">🚌 Linha 195 · Recife / Porto De Galinhas (Opcional)</option>
    <option value="198">🚌 Linha 198 · Ipojuca / Ti Cabo</option>
  </optgroup>
  <optgroup label="🔄 Linhas Interterminais / Perimetrais (T.I. a T.I.)">
    <option value="020">🚌 Linha 020 · Candeias / Ti Tancredo Neves</option>
    <option value="023">🚌 Linha 023 · Ti Tancredo Neves / Ti Aeroporto</option>
    <option value="024">🚌 Linha 024 · Ti Tancredo Neves (Circular Boa Viagem)</option>
    <option value="026">🚌 Linha 026 · Ti Aeroporto / Ti Joana Bezerra</option>
    <option value="030">🚌 Linha 030 · Ti Rio Doce / Barra De Jangada</option>
    <option value="050">🚌 Linha 050 · Ti Pe-15 / Boa Viagem</option>
    <option value="200">🚌 Linha 200 · Ti Jaboatão (Parador)</option>
    <option value="202">🚌 Linha 202 · Ti Barro / Ti Macaxeira (Várzea)</option>
    <option value="207">🚌 Linha 207 · Ti Barro / Ti Macaxeira (Br-101)</option>
    <option value="2490">🚌 Linha 2490 · Ti Camaragibe / Ti Macaxeira</option>
    <option value="860">🚌 Linha 860 · Ti Xambá (Príncipe)</option>
    <option value="914">🚌 Linha 914 · Ti Pe-15 / Ti Afogados</option>
  </optgroup>
  <optgroup label="📋 Todas as 400 Linhas do Grande Recife (001 a 2490)">
    <option value="001">🚌 Linha 001 · Ponte Dos Carvalhos / Prazeres (Barra De Jangada)</option>
    <option value="010">🚌 Linha 010 · Abdo Cabus (Conde Boa Vista)</option>
    <option value="011">🚌 Linha 011 · Piedade / Derby</option>
    <option value="013">🚌 Linha 013 · Jardim Beira Rio (Pina)</option>
    <option value="014">🚌 Linha 014 · Brasília (Cd. Boa Vista)</option>
    <option value="018">🚌 Linha 018 · Brasília Teimosa</option>
    <option value="020">🚌 Linha 020 · Candeias / Ti Tancredo Neves</option>
    <option value="021">🚌 Linha 021 · Ti Joana Bezerra / Shopping Riomar</option>
    <option value="023">🚌 Linha 023 · Ti Tancredo Neves / Ti Aeroporto</option>
    <option value="024">🚌 Linha 024 · Ti Tancredo Neves (Circular Boa Viagem)</option>
    <option value="026">🚌 Linha 026 · Ti Aeroporto / Ti Joana Bezerra</option>
    <option value="030">🚌 Linha 030 · Ti Rio Doce / Barra De Jangada</option>
    <option value="031">🚌 Linha 031 · Shopping Center (Ter. Res. Boa Viagem)</option>
    <option value="032">🚌 Linha 032 · Setúbal (Conde Da Boa Vista)</option>
    <option value="034">🚌 Linha 034 · Curcurana / Ti Cajueiro Seco</option>
    <option value="036">🚌 Linha 036 · Aeroporto (Bacurau)</option>
    <option value="037">🚌 Linha 037 · Comportas / Ti Cajueiro Seco</option>
    <option value="038">🚌 Linha 038 · Residencial Boa Viagem (Bacurau)</option>
    <option value="039">🚌 Linha 039 · Setúbal (Príncipe)</option>
    <option value="041">🚌 Linha 041 · Setúbal (Opcional)</option>
    <option value="043">🚌 Linha 043 · Aeroporto / Tacaruna (Derby)</option>
    <option value="044">🚌 Linha 044 · Massangana (Boa Vista)</option>
    <option value="049">🚌 Linha 049 · Ti Tip / Moreno (Br-232)</option>
    <option value="050">🚌 Linha 050 · Ti Pe-15 / Boa Viagem</option>
    <option value="061">🚌 Linha 061 · Piedade</option>
    <option value="062">🚌 Linha 062 · Jardim Piedade</option>
    <option value="063">🚌 Linha 063 · Jardim Piedade (Bacurau)</option>
    <option value="064">🚌 Linha 064 · Piedade (Opcional)</option>
    <option value="065">🚌 Linha 065 · Piedade / Ti Prazeres</option>
    <option value="069">🚌 Linha 069 · Conj. Catamarã</option>
    <option value="070">🚌 Linha 070 · Candeias / Shopping Riomar</option>
    <option value="071">🚌 Linha 071 · Candeias</option>
    <option value="072">🚌 Linha 072 · Candeias (Opcional)</option>
    <option value="073">🚌 Linha 073 · Candeias (Bacurau)</option>
    <option value="075">🚌 Linha 075 · Ti Prazeres / Curcurana</option>
    <option value="080">🚌 Linha 080 · Ti Joana Bezerra / Boa Viagem</option>
    <option value="101">🚌 Linha 101 · Ti Recife / Ti J. Bezerra (Boa Vista)</option>
    <option value="102">🚌 Linha 102 · Ti Santa Luzia / Ibura</option>
    <option value="103">🚌 Linha 103 · Ur-11 / Ti Barro</option>
    <option value="104">🚌 Linha 104 · Ti J. Bezerra / Ti Recife (Imip)</option>
    <option value="106">🚌 Linha 106 · Ti Santa Luzia / Parque Aeronáutica (Jiquiá)</option>
    <option value="1062">🚌 Linha 1062 · Ti Abreu E Lima (Pcr) (Parador)</option>
    <option value="107">🚌 Linha 107 · Ti Recife (Cabugá/Pcr)</option>
    <option value="1076">🚌 Linha 1076 · Ti Pelópidas (Pcr) (Parador)</option>
    <option value="108">🚌 Linha 108 · Ti Barro / Ceasa</option>
    <option value="110">🚌 Linha 110 · Ibura / Ti Prazeres</option>
    <option value="1100">🚌 Linha 1100 · Ti Pe-15 (Pcr) (Parador)</option>
    <option value="115">🚌 Linha 115 · Ti Aeroporto / Ti Afogados</option>
    <option value="116">🚌 Linha 116 · Ti Recife (Príncipe)</option>
    <option value="117">🚌 Linha 117 · Ti Recife (Pcr/Cabugá)</option>
    <option value="118">🚌 Linha 118 · Prazeres / Boa Viagem</option>
    <option value="120">🚌 Linha 120 · Alto Dois Carneiros / Shopping Recife</option>
    <option value="121">🚌 Linha 121 · Vila Da Sudene</option>
    <option value="122">🚌 Linha 122 · Vila Do Ipsep</option>
    <option value="125">🚌 Linha 125 · Córrego Da Gameleira (Vila Do Sesi) / Ti Tancredo Neves</option>
    <option value="126">🚌 Linha 126 · Ti Tancredo Neves / Ur-03</option>
    <option value="128">🚌 Linha 128 · Ti Barro / Ur-03 (Milagres)</option>
    <option value="129">🚌 Linha 129 · Paiva / Ti Cabo</option>
    <option value="131">🚌 Linha 131 · Ur-02 (Bacurau)</option>
    <option value="132">🚌 Linha 132 · Ti Tancredo Neves / Ur-02 (Ibura)</option>
    <option value="134">🚌 Linha 134 · Lagoa Encantada / Ti Tancredo Neves</option>
    <option value="135">🚌 Linha 135 · Ur-10 / Ti Tancredo Neves</option>
    <option value="136">🚌 Linha 136 · Ti Tancredo Neves / Ur-05</option>
    <option value="138">🚌 Linha 138 · Ti Tancredo Neves / Zumbi Do Pacheco</option>
    <option value="139">🚌 Linha 139 · Ti Cabo / Ti Cajueiro Seco</option>
    <option value="140">🚌 Linha 140 · Ti Cajueiro Seco / Shopping Recife</option>
    <option value="141">🚌 Linha 141 · Jardim Monte Verde / Ti Tancredo Neves</option>
    <option value="142">🚌 Linha 142 · Ti Tancredo Neves / Alto Dois Carneiros</option>
    <option value="143">🚌 Linha 143 · Ti Tancredo Neves / Ur-06</option>
    <option value="144">🚌 Linha 144 · Ur-04 / Ti Tancredo Neves</option>
    <option value="145">🚌 Linha 145 · Alto Dois Carneiros (Bacurau)</option>
    <option value="146">🚌 Linha 146 · Ur-11 (Bacurau)</option>
    <option value="149">🚌 Linha 149 · Ti Cavaleiro / Zumbi Do Pacheco</option>
    <option value="151">🚌 Linha 151 · Jardim Jordão / Ti Aeroporto</option>
    <option value="152">🚌 Linha 152 · Jordão Baixo / Ti Aeroporto</option>
    <option value="153">🚌 Linha 153 · Jordão Alto / Ti Aeroporto</option>
    <option value="154">🚌 Linha 154 · Jordão (Bacurau)</option>
    <option value="155">🚌 Linha 155 · Jordão Baixo / Boa Viagem</option>
    <option value="157">🚌 Linha 157 · Gaibu / Ti Cabo</option>
    <option value="158">🚌 Linha 158 · Garapu / Ti Cabo</option>
    <option value="159">🚌 Linha 159 · Charneca / Ti Cabo</option>
    <option value="160">🚌 Linha 160 · Gaibu / Barra De Jangada - Via Paiva (Opcional)</option>
    <option value="162">🚌 Linha 162 · Muribeca / Ti Cajueiro Seco</option>
    <option value="163">🚌 Linha 163 · Ti Cajueiro Seco (Circular)</option>
    <option value="164">🚌 Linha 164 · Marcos Freire / Ti Cajueiro Seco</option>
    <option value="165">🚌 Linha 165 · Muribeca Dos Guararapes / Ti Cajueiro Seco</option>
    <option value="166">🚌 Linha 166 · Ti Cajueiro Seco (Rua Do Sol)</option>
    <option value="167">🚌 Linha 167 · Ti Tancredo Neves (Imip)</option>
    <option value="168">🚌 Linha 168 · Ti Tancredo Neves (Cde. B. Vista)</option>
    <option value="170">🚌 Linha 170 · Muribeca Dos Guararapes (Bacurau)</option>
    <option value="171">🚌 Linha 171 · Lot. Integração / Ti Cajueiro Seco</option>
    <option value="172">🚌 Linha 172 · Marcos Freire (Bacurau)</option>
    <option value="178">🚌 Linha 178 · Porto De Suape / Ti Cabo</option>
    <option value="181">🚌 Linha 181 · Cabo (Cohab) / Ti Cajueiro Seco</option>
    <option value="183">🚌 Linha 183 · Pte. Dos Carvalhos / Ti Cajueiro Seco</option>
    <option value="184">🚌 Linha 184 · Cabo (Bacurau)</option>
    <option value="185">🚌 Linha 185 · Ti Cabo</option>
    <option value="1903">🚌 Linha 1903 · Araçoiaba / Ti Igarassu</option>
    <option value="1904">🚌 Linha 1904 · Ti Igarassu / Nova Cruz</option>
    <option value="1905">🚌 Linha 1905 · Ti Abreu E Lima / Ti Igarassu</option>
    <option value="1906">🚌 Linha 1906 · Ti Pelópidas / Ti Macaxeira</option>
    <option value="1907">🚌 Linha 1907 · Paulista / Rio Doce</option>
    <option value="1908">🚌 Linha 1908 · Ti Igarassu / Botafogo</option>
    <option value="1909">🚌 Linha 1909 · Ti Pelópidas / Ti Joana Bezerra</option>
    <option value="191">🚌 Linha 191 · Recife / Porto De Galinhas (N. Sra. Do Ó)</option>
    <option value="1911">🚌 Linha 1911 · Ouro Preto (Cohab)</option>
    <option value="1912">🚌 Linha 1912 · Caetés I / Ti Abreu E Lima</option>
    <option value="1913">🚌 Linha 1913 · Ti Pe-15 / Ti Joana Bezerra</option>
    <option value="1917">🚌 Linha 1917 · Caetés Ii / Ti Abreu E Lima</option>
    <option value="1918">🚌 Linha 1918 · Ti Igarassu (Circular)</option>
    <option value="1921">🚌 Linha 1921 · Ouro Preto / Ti Pe-15</option>
    <option value="1922">🚌 Linha 1922 · Pau Amarelo / Ti Pelópidas</option>
    <option value="1923">🚌 Linha 1923 · Cidade Tabajara / Ti Pe-15</option>
    <option value="1926">🚌 Linha 1926 · Ouro Preto (Jatobá Ii)</option>
    <option value="1927">🚌 Linha 1927 · Ouro Preto (Bacurau)</option>
    <option value="1928">🚌 Linha 1928 · Maranguape Ii (Bacurau)</option>
    <option value="1929">🚌 Linha 1929 · Alameda Paulista / Ti Rio Doce (Jaguarana)</option>
    <option value="1931">🚌 Linha 1931 · Jardim Paulista Baixo / Ti Pelópidas</option>
    <option value="1932">🚌 Linha 1932 · Jardim Paulista Alto / Ti Pelópidas</option>
    <option value="1933">🚌 Linha 1933 · Ti Pe-15 / Ti Abreu E Lima</option>
    <option value="1934">🚌 Linha 1934 · Arthur Lundgren I / Ti Pelópidas</option>
    <option value="1935">🚌 Linha 1935 · Paratibe / Ti Pelópidas</option>
    <option value="1936">🚌 Linha 1936 · Mirueira (Bacurau)</option>
    <option value="1937">🚌 Linha 1937 · Ti Abreu E Lima / Nova Aurora</option>
    <option value="1940">🚌 Linha 1940 · Ti Pe-15 (Circular)</option>
    <option value="1941">🚌 Linha 1941 · Arthur Lundgren Ii / Ti Pelópidas</option>
    <option value="1943">🚌 Linha 1943 · Mirueira / Ti Pelópidas</option>
    <option value="1944">🚌 Linha 1944 · Ti Pelópidas / Maria Farinha (Lot. Conceição)</option>
    <option value="1945">🚌 Linha 1945 · Jaguarana (Alameda) / Ti Pelópidas</option>
    <option value="1946">🚌 Linha 1946 · Ti Igarassu (Br-101)</option>
    <option value="1948">🚌 Linha 1948 · Ti Abreu E Lima / Ti Pelópidas (Circular)</option>
    <option value="195">🚌 Linha 195 · Recife / Porto De Galinhas (Opcional)</option>
    <option value="1950">🚌 Linha 1950 · Engenho Maranguape / Varadouro</option>
    <option value="1952">🚌 Linha 1952 · Ti Pelópidas / Ti Rio Doce</option>
    <option value="1953">🚌 Linha 1953 · Maranguape Ii / Ti Pelópidas</option>
    <option value="1955">🚌 Linha 1955 · Ti Pelópidas / Cj. Praia Do Janga (Eng. Maranguape)</option>
    <option value="1956">🚌 Linha 1956 · Igarassu (Bacurau)</option>
    <option value="1957">🚌 Linha 1957 · Caetés I (Bacurau)</option>
    <option value="1958">🚌 Linha 1958 · Costa Azul / Ti Pelópidas</option>
    <option value="196">🚌 Linha 196 · Ti Cabo / P. De Galinhas (N. Sra. Do Ó)</option>
    <option value="1960">🚌 Linha 1960 · Ti Rio Doce / Maria Farinha (Casa Caiada)</option>
    <option value="1963">🚌 Linha 1963 · Ti Pe-15 / Ti Igarassu (Sítio Histórico)</option>
    <option value="1964">🚌 Linha 1964 · Ti Igarassu / Ti Macaxeira</option>
    <option value="1966">🚌 Linha 1966 · Ti Rio Doce / Ti Pe-15 (Fragoso)</option>
    <option value="1967">🚌 Linha 1967 · Ti Igarassu (Sítio Histórico)</option>
    <option value="1968">🚌 Linha 1968 · Ilha De Itamaracá / Ti Igarassu</option>
    <option value="1969">🚌 Linha 1969 · Itapissuma / Ti Igarassu</option>
    <option value="1971">🚌 Linha 1971 · Amparo</option>
    <option value="1973">🚌 Linha 1973 · Casa Caiada (Conde Boa Vista)</option>
    <option value="1974">🚌 Linha 1974 · Jardim Atlântico</option>
    <option value="1975">🚌 Linha 1975 · Amparo (Bacurau)</option>
    <option value="1977">🚌 Linha 1977 · Ti Pelópidas (Conde Boa Vista)</option>
    <option value="1978">🚌 Linha 1978 · Loteamento Conceição / Ti Rio Doce (Pe-22)</option>
    <option value="198">🚌 Linha 198 · Ipojuca / Ti Cabo</option>
    <option value="1980">🚌 Linha 1980 · Igarassu / Cidade Tabajara</option>
    <option value="1981">🚌 Linha 1981 · Ti Rio Doce / Ti Joana Bezerra</option>
    <option value="1982">🚌 Linha 1982 · Conjunto Beira Mar / Derby</option>
    <option value="1983">🚌 Linha 1983 · Ti Rio Doce (Princesa Isabel)</option>
    <option value="1984">🚌 Linha 1984 · Lot. Bonfim / Ti Abreu E Lima</option>
    <option value="1985">🚌 Linha 1985 · Rio Doce (Bacurau)</option>
    <option value="1986">🚌 Linha 1986 · Ti Pe-15 / Ti Rio Doce</option>
    <option value="1987">🚌 Linha 1987 · Ti Rio Doce (Príncipe / Conde Boa Vista)</option>
    <option value="1988">🚌 Linha 1988 · Desterro / Ti Abreu E Lima</option>
    <option value="1989">🚌 Linha 1989 · Lot. Planalto / Ti Abreu E Lima</option>
    <option value="199">🚌 Linha 199 · Camela / Ti Cabo</option>
    <option value="1992">🚌 Linha 1992 · Pau Amarelo</option>
    <option value="1993">🚌 Linha 1993 · Conjunto Praia Do Janga</option>
    <option value="1994">🚌 Linha 1994 · Conjunto Beira Mar</option>
    <option value="1995">🚌 Linha 1995 · Pau Amarelo (Bacurau)</option>
    <option value="1996">🚌 Linha 1996 · Arthur Lundgren Ii / Rio Doce (Paratibe)</option>
    <option value="1998">🚌 Linha 1998 · Caetés Iii / Ti Abreu E Lima</option>
    <option value="200">🚌 Linha 200 · Ti Jaboatão (Parador)</option>
    <option value="201">🚌 Linha 201 · Moreno / Ti Jaboatão</option>
    <option value="202">🚌 Linha 202 · Ti Barro / Ti Macaxeira (Várzea)</option>
    <option value="203">🚌 Linha 203 · Ti Barro / Zumbi Do Pacheco (Lot.)</option>
    <option value="2040">🚌 Linha 2040 · Cdu / Boa Viagem / Caxangá</option>
    <option value="2043">🚌 Linha 2043 · Ti Cdu / Ti Joana Bezerra (Parador)</option>
    <option value="205">🚌 Linha 205 · Ti Barro / Ur-05 (Br-101)</option>
    <option value="206">🚌 Linha 206 · Ti Barro / Ti Prazeres (Jordão)</option>
    <option value="2060">🚌 Linha 2060 · Ti Tancredo Neves / Ti Macaxeira</option>
    <option value="207">🚌 Linha 207 · Ti Barro / Ti Macaxeira (Br-101)</option>
    <option value="208">🚌 Linha 208 · Nossa Senhora Da Conceição / Ti Jaboatão</option>
    <option value="209">🚌 Linha 209 · Ti Barro / Coqueiral</option>
    <option value="211">🚌 Linha 211 · Vila Tamandaré</option>
    <option value="212">🚌 Linha 212 · Jardim São Paulo</option>
    <option value="216">🚌 Linha 216 · Ti Barro / Ti Cajueiro Seco</option>
    <option value="219">🚌 Linha 219 · Ti Tip / Ti Jaboatão (Sancho)</option>
    <option value="220">🚌 Linha 220 · Ti Jaboatão / Ti Cavaleiro</option>
    <option value="221">🚌 Linha 221 · Vila Cardeal E Silva</option>
    <option value="222">🚌 Linha 222 · Jardim Uchôa</option>
    <option value="229">🚌 Linha 229 · Marcos Freire (Opcional)</option>
    <option value="232">🚌 Linha 232 · Cavaleiro</option>
    <option value="233">🚌 Linha 233 · Cavaleiro (Bacurau)</option>
    <option value="238">🚌 Linha 238 · Ti Jaboatão / Ti Barro</option>
    <option value="240">🚌 Linha 240 · Cavaleiro / Ceasa</option>
    <option value="2402">🚌 Linha 2402 · Parque Capibaribe / Caxangá</option>
    <option value="2410">🚌 Linha 2410 · Parque Capibaribe / Ti Tip</option>
    <option value="2416">🚌 Linha 2416 · Roda De Fogo / Ti Getúlio Vargas</option>
    <option value="2417">🚌 Linha 2417 · Nova Morada / Ti Caxangá</option>
    <option value="2419">🚌 Linha 2419 · Matriz Da Luz / Ti Camaragibe</option>
    <option value="242">🚌 Linha 242 · Pacheco (Floresta)</option>
    <option value="2420">🚌 Linha 2420 · Muribara / Ti Camaragibe</option>
    <option value="2421">🚌 Linha 2421 · Torrões / Ti Getúlio Vargas</option>
    <option value="2423">🚌 Linha 2423 · Engenho Do Meio / Ti Cdu</option>
    <option value="2427">🚌 Linha 2427 · Monsenhor Fabrício (Bacurau)</option>
    <option value="2429">🚌 Linha 2429 · Ti Getúlio Vargas / Ti Cdu</option>
    <option value="243">🚌 Linha 243 · Vila Dois Carneiros</option>
    <option value="2431">🚌 Linha 2431 · Ti Cdu / Ti Caxangá (Ufpe)</option>
    <option value="2433">🚌 Linha 2433 · Brasilit / Ti Cdu</option>
    <option value="2434">🚌 Linha 2434 · Ti Getúlio Vargas / Tamarineira</option>
    <option value="2437">🚌 Linha 2437 · Ti Caxangá (Conde Boa Vista)</option>
    <option value="244">🚌 Linha 244 · Alto Do Vento / Ti Cavaleiro</option>
    <option value="2441">🚌 Linha 2441 · Ti Cdu (Conde Boa Vista)</option>
    <option value="2442">🚌 Linha 2442 · Jd. Primavera (V. Pedreiras) / Ti Cdu</option>
    <option value="2444">🚌 Linha 2444 · Ti Getúlio Vargas (Conde Da Boa Vista)</option>
    <option value="2445">🚌 Linha 2445 · Tabatinga / Ti Caxangá</option>
    <option value="2446">🚌 Linha 2446 · Ur-07 (Várzea) / Ti Cdu</option>
    <option value="2448">🚌 Linha 2448 · Alto Santo Antônio / Ti Camaragibe</option>
    <option value="245">🚌 Linha 245 · Dois Carneiros / Ti Cavaleiro</option>
    <option value="2450">🚌 Linha 2450 · Ti Camaragibe (Conde Boa Vista)</option>
    <option value="2456">🚌 Linha 2456 · Viana / Ti Camaragibe</option>
    <option value="2457">🚌 Linha 2457 · São Lourenço (Bacurau)</option>
    <option value="2459">🚌 Linha 2459 · Ti Cosme E Damião / Ti Caxangá</option>
    <option value="2462">🚌 Linha 2462 · Lot. Santos Cosme Damião (Bacurau)</option>
    <option value="2463">🚌 Linha 2463 · Araçoiaba / Ti Camaragibe</option>
    <option value="2464">🚌 Linha 2464 · Jardim Teresópolis / Ti Caxangá</option>
    <option value="2466">🚌 Linha 2466 · Vera Cruz / Ti Camaragibe</option>
    <option value="2467">🚌 Linha 2467 · Chã De Cruz / Ti Camaragibe</option>
    <option value="2470">🚌 Linha 2470 · Circular Vila Da Fábrica/Santana (Via Bairro Dos Estados)</option>
    <option value="2473">🚌 Linha 2473 · João Paulo Ii / Ti Camaragibe</option>
    <option value="2475">🚌 Linha 2475 · Timbi / Ti Camaragibe</option>
    <option value="2476">🚌 Linha 2476 · Santa Mônica / Ti Camaragibe</option>
    <option value="2477">🚌 Linha 2477 · Santa Terezinha / Ti Camaragibe</option>
    <option value="2478">🚌 Linha 2478 · Santana / Ti Camaragibe</option>
    <option value="2481">🚌 Linha 2481 · Ti Camaragibe / Ti Tip</option>
    <option value="2483">🚌 Linha 2483 · Lot. S. João E S. Paulo / Ti Camaragibe</option>
    <option value="2486">🚌 Linha 2486 · Penedo / Ti Camaragibe</option>
    <option value="2487">🚌 Linha 2487 · Várzea Fria / Ti Camaragibe</option>
    <option value="2488">🚌 Linha 2488 · Vila Da Fábrica / Ti Caxangá</option>
    <option value="2490">🚌 Linha 2490 · Ti Camaragibe / Ti Macaxeira</option>
    <option value="2493">🚌 Linha 2493 · Tiúma / Ti Camaragibe</option>
    <option value="250">🚌 Linha 250 · Ti Jaboatão / Santo Aleixo (Luz)</option>
    <option value="2501">🚌 Linha 2501 · Circular Peroba / Oitenta / Borralho</option>
    <option value="2502">🚌 Linha 2502 · Circular Santa Mônica / Maranguape (V. Beira Rio)</option>
    <option value="2503">🚌 Linha 2503 · Circular Quadra 30 (V. Celeiro)</option>
    <option value="2504">🚌 Linha 2504 · Circular Vale Das Pedreiras (Shopping)</option>
    <option value="2505">🚌 Linha 2505 · Circular Tabatinga / São Jorge (Via Fábrica)</option>
    <option value="251">🚌 Linha 251 · Ti Jaboatão / Santo Aleixo (Rios)</option>
    <option value="252">🚌 Linha 252 · Vila Rica / Ti Jaboatão</option>
    <option value="254">🚌 Linha 254 · Jaboatão (Bacurau)</option>
    <option value="255">🚌 Linha 255 · Quitandinha / Ti Cavaleiro</option>
    <option value="256">🚌 Linha 256 · Ti Cavaleiro / Lot. Nova Esperança</option>
    <option value="258">🚌 Linha 258 · Moreno (Bacurau)</option>
    <option value="261">🚌 Linha 261 · Ti Jaboatão / Vila Piedade</option>
    <option value="262">🚌 Linha 262 · Ti Jaboatão / Malvinas</option>
    <option value="272">🚌 Linha 272 · Colônia / Ti Jaboatão</option>
    <option value="274">🚌 Linha 274 · Ti Jaboatão / Lote 56</option>
    <option value="290">🚌 Linha 290 · Ti Jaboatão / Bonança</option>
    <option value="291">🚌 Linha 291 · Ti Jaboatão / Moreno (Recife Outlet)</option>
    <option value="2920">🚌 Linha 2920 · Ti Rio Doce / Ti Cdu</option>
    <option value="2930">🚌 Linha 2930 · Ti Rio Doce / Dois Irmãos</option>
    <option value="302">🚌 Linha 302 · Caxangá / Ti Tip</option>
    <option value="303">🚌 Linha 303 · Caxangá / Curado Ii (Br-232)</option>
    <option value="311">🚌 Linha 311 · Bongi (Afogados)</option>
    <option value="312">🚌 Linha 312 · Mustardinha</option>
    <option value="313">🚌 Linha 313 · San Martin (A. De Carvalho)</option>
    <option value="314">🚌 Linha 314 · Mangueira</option>
    <option value="315">🚌 Linha 315 · Bongi</option>
    <option value="320">🚌 Linha 320 · Curado I / Ti Santa Luzia</option>
    <option value="321">🚌 Linha 321 · Jardim São Paulo (A. Carvalho)</option>
    <option value="322">🚌 Linha 322 · Jardim São Paulo (Bacurau)</option>
    <option value="324">🚌 Linha 324 · Jardim São Paulo (Piracicaba)</option>
    <option value="330">🚌 Linha 330 · Casa Amarela / Cdu (Av. Caxangá)</option>
    <option value="331">🚌 Linha 331 · Totó (Jardim Planalto)</option>
    <option value="332">🚌 Linha 332 · Totó (Abdias De Carvalho)</option>
    <option value="333">🚌 Linha 333 · Totó (Bacurau)</option>
    <option value="341">🚌 Linha 341 · Curado I</option>
    <option value="342">🚌 Linha 342 · Curados (Opcional)</option>
    <option value="346">🚌 Linha 346 · Ti Tip (Conde Boa Vista)</option>
    <option value="347">🚌 Linha 347 · Ti Tip / Joana Bezerra</option>
    <option value="348">🚌 Linha 348 · Ti Tip / Curado V</option>
    <option value="351">🚌 Linha 351 · Ti Tip / Curado Ii</option>
    <option value="352">🚌 Linha 352 · Curado Ii (Bacurau)</option>
    <option value="360">🚌 Linha 360 · Totó / Boa Viagem</option>
    <option value="361">🚌 Linha 361 · Ti Tip / Curado Iv (Rua 14)</option>
    <option value="362">🚌 Linha 362 · Curado Iv (Bacurau)</option>
    <option value="363">🚌 Linha 363 · Ti Tip / Curado Iv (Av. 01)</option>
    <option value="370">🚌 Linha 370 · Ti Tip / Ti Aeroporto</option>
    <option value="411">🚌 Linha 411 · Plaza Shopping (Conde Da Boa Vista)</option>
    <option value="412">🚌 Linha 412 · Ti Santa Luzia / Ti Getúlio Vargas</option>
    <option value="4123">🚌 Linha 4123 · Três Carneiros Baixo (Cais De Santa Rita)</option>
    <option value="4133">🚌 Linha 4133 · Três Carneiros (Cais De Santa Rita)</option>
    <option value="4137">🚌 Linha 4137 · Ur-11 (Cais De Santa Rita)</option>
    <option value="414">🚌 Linha 414 · Torre</option>
    <option value="418">🚌 Linha 418 · Tiúma / Camaragibe</option>
    <option value="424">🚌 Linha 424 · Cdu / Largo Da Paz (Via Torrões/San Martin)</option>
    <option value="440">🚌 Linha 440 · Cdu / Caxangá / Boa Viagem</option>
    <option value="510">🚌 Linha 510 · Nova Descoberta / Derby</option>
    <option value="511">🚌 Linha 511 · Ti Cdu / Casa Amarela / Alto Do Mandu</option>
    <option value="513">🚌 Linha 513 · Córrego Da Areia</option>
    <option value="514">🚌 Linha 514 · Nova Descoberta (Cór. Do Joaquim)</option>
    <option value="515">🚌 Linha 515 · Nova Descoberta (Bacurau)</option>
    <option value="516">🚌 Linha 516 · Casa Amarela / Torre / Cde. Boa Vista</option>
    <option value="517">🚌 Linha 517 · Córrego Do Inácio</option>
    <option value="520">🚌 Linha 520 · Ti Macaxeira / Parnamirim</option>
    <option value="521">🚌 Linha 521 · Alto Santa Isabel (Cde. Boa Vista)</option>
    <option value="522">🚌 Linha 522 · Dois Irmãos (Rui Barbosa E Príncipe)</option>
    <option value="523">🚌 Linha 523 · Dois Irmãos (Bacurau)</option>
    <option value="524">🚌 Linha 524 · Sítio Dos Pintos (Dois Irmãos)</option>
    <option value="532">🚌 Linha 532 · Dois Irmãos / Casa Amarela (Cruz Cabugá)</option>
    <option value="533">🚌 Linha 533 · Casa Amarela (Bacurau)</option>
    <option value="601">🚌 Linha 601 · Ti Macaxeira / P.R. Bola Na Rede</option>
    <option value="604">🚌 Linha 604 · Ti Macaxeira / Alto Do Burity</option>
    <option value="611">🚌 Linha 611 · Alto José Do Pinho (Cais De Santa Rita)</option>
    <option value="612">🚌 Linha 612 · Morro Da Conceição (Cruz Cabugá)</option>
    <option value="613">🚌 Linha 613 · Morro Da Conceição (Bacurau)</option>
    <option value="621">🚌 Linha 621 · Alto Treze De Maio (Príncipe)</option>
    <option value="622">🚌 Linha 622 · Vasco Da Gama (Cruz Cabugá)</option>
    <option value="623">🚌 Linha 623 · Vasco Da Gama (João De Barros)</option>
    <option value="624">🚌 Linha 624 · Brejo (Cde. Boa Vista)</option>
    <option value="626">🚌 Linha 626 · Brejo (Bacurau)</option>
    <option value="630">🚌 Linha 630 · Vasco Da Gama / Derby</option>
    <option value="631">🚌 Linha 631 · Nova Descoberta (Cabugá)</option>
    <option value="632">🚌 Linha 632 · Alto Do Refúgio (Cabugá)</option>
    <option value="640">🚌 Linha 640 · Guabiraba / Derby (Joana Bezerra)</option>
    <option value="641">🚌 Linha 641 · Ti Macaxeira / Encruzilhada</option>
    <option value="642">🚌 Linha 642 · Guabiraba (Córrego Do Jenipapo)</option>
    <option value="643">🚌 Linha 643 · Córrego Do Jenipapo (Bacurau)</option>
    <option value="644">🚌 Linha 644 · Largo Do Maracanã (Conde Da Boa Vista)</option>
    <option value="645">🚌 Linha 645 · Ti Macaxeira (Av. Norte)</option>
    <option value="650">🚌 Linha 650 · Ti Macaxeira / Ti Xambá</option>
    <option value="680">🚌 Linha 680 · Vasco Da Gama / Afogados</option>
    <option value="700">🚌 Linha 700 · Beberibe / Afogados</option>
    <option value="710">🚌 Linha 710 · Beberibe / Derby (Joana Bezerra)</option>
    <option value="711">🚌 Linha 711 · Alto Do Pascoal</option>
    <option value="712">🚌 Linha 712 · Alto Santa Terezinha</option>
    <option value="713">🚌 Linha 713 · Bomba Do Hemetério</option>
    <option value="714">🚌 Linha 714 · Alto José Bonifácio (Av. Norte)</option>
    <option value="715">🚌 Linha 715 · Alto Santa Terezinha (Bacurau)</option>
    <option value="717">🚌 Linha 717 · José Amarino Dos Reis</option>
    <option value="718">🚌 Linha 718 · Córrego Do Euclides / Derby</option>
    <option value="721">🚌 Linha 721 · Água Fria (Circular)</option>
    <option value="722">🚌 Linha 722 · Campina Do Barreto</option>
    <option value="723">🚌 Linha 723 · Cajueiro</option>
    <option value="724">🚌 Linha 724 · Chão De Estrelas</option>
    <option value="741">🚌 Linha 741 · Dois Unidos</option>
    <option value="742">🚌 Linha 742 · Linha Do Tiro</option>
    <option value="743">🚌 Linha 743 · Alto José Bonifácio (J. Barros)</option>
    <option value="744">🚌 Linha 744 · Dois Unidos (Bacurau)</option>
    <option value="745">🚌 Linha 745 · Alto José Bonifácio (Bacurau)</option>
    <option value="746">🚌 Linha 746 · Alto Do Capitão</option>
    <option value="760">🚌 Linha 760 · Dois Unidos / Derby</option>
    <option value="780">🚌 Linha 780 · Alto Santa Terezinha / Derby</option>
    <option value="800">🚌 Linha 800 · Dois Unidos / Afogados</option>
    <option value="810">🚌 Linha 810 · Ti Xambá / Encruzilhada</option>
    <option value="820">🚌 Linha 820 · Ti Xambá (Cabugá)</option>
    <option value="821">🚌 Linha 821 · Jardim Brasil I (Est. De Belém)</option>
    <option value="822">🚌 Linha 822 · Jardim Brasil I (Cruz Cabugá)</option>
    <option value="823">🚌 Linha 823 · Jardim Brasil Ii (Est. De Belém)</option>
    <option value="824">🚌 Linha 824 · Jardim Brasil Ii (Cruz Cabugá)</option>
    <option value="825">🚌 Linha 825 · Jardim Brasil / Ti Joana Bezerra</option>
    <option value="827">🚌 Linha 827 · Jardim Brasil (Bacurau)</option>
    <option value="831">🚌 Linha 831 · Aguazinha / Ti Xambá</option>
    <option value="841">🚌 Linha 841 · Nova Olinda / Ti Xambá</option>
    <option value="842">🚌 Linha 842 · Águas Compridas / Ti Xambá</option>
    <option value="843">🚌 Linha 843 · Alto Da Bondade / Ti Xambá</option>
    <option value="844">🚌 Linha 844 · Santa Casa / Ti Xambá</option>
    <option value="846">🚌 Linha 846 · Águas Compridas (Bacurau)</option>
    <option value="847">🚌 Linha 847 · Alto Nova Olinda / Ti Xambá</option>
    <option value="852">🚌 Linha 852 · Caixa D'Água / Ti Xambá</option>
    <option value="858">🚌 Linha 858 · Ti Joana Bezerra / Ti Afogados / Ti Barro</option>
    <option value="860">🚌 Linha 860 · Ti Xambá (Príncipe)</option>
    <option value="861">🚌 Linha 861 · Ti Joana Bezerra / Ti Xambá</option>
    <option value="870">🚌 Linha 870 · Ti Xambá / Ti Largo Da Paz</option>
    <option value="881">🚌 Linha 881 · Ti Xambá / Rio Doce (Av. Getúlio Vargas)</option>
    <option value="882">🚌 Linha 882 · Ti Xambá / Rio Doce (Carlos De Lima Cavalcanti)</option>
    <option value="883">🚌 Linha 883 · Ti Pe-15 / Ti Xambá</option>
    <option value="884">🚌 Linha 884 · Jardim Brasil / Rio Doce</option>
    <option value="885">🚌 Linha 885 · Sítio Novo / Rio Doce</option>
    <option value="886">🚌 Linha 886 · Ouro Preto / Rio Doce</option>
    <option value="892">🚌 Linha 892 · Alto Do Cajueiro / Ti Xambá</option>
    <option value="893">🚌 Linha 893 · Ti Pe-15 / Alto Da Conquista</option>
    <option value="894">🚌 Linha 894 · Ti Xambá / Córrego Do Abacaxi</option>
    <option value="895">🚌 Linha 895 · Alto Sol Nascente / Ti Xambá</option>
    <option value="901">🚌 Linha 901 · Ti Abreu E Lima / Ti Macaxeira</option>
    <option value="910">🚌 Linha 910 · Piedade / Ti Rio Doce</option>
    <option value="9104">🚌 Linha 9104 · Casseterita / Casa Amarela / Jaqueira</option>
    <option value="9105">🚌 Linha 9105 · Córrego Do Boleiro / Casa Amarela / Jaqueira</option>
    <option value="9108">🚌 Linha 9108 · Dois Unidos / Torre</option>
    <option value="9110">🚌 Linha 9110 · Campo Grande / Afogados</option>
    <option value="9112">🚌 Linha 9112 · Casa Amarela / Bomba Do Hemetério / Shopping Tacaruna</option>
    <option value="914">🚌 Linha 914 · Ti Pe-15 / Ti Afogados</option>
    <option value="916">🚌 Linha 916 · Ouro Preto / Joana Bezerra</option>
    <option value="9205">🚌 Linha 9205 · Jardim Uchôa / Boa Viagem</option>
    <option value="9301">🚌 Linha 9301 · San Martin / Lagoa Do Araçá / Boa Viagem</option>
    <option value="Centro 1">🚌 Linha Centro 1 · Recife - Camaragibe</option>
    <option value="Centro 2">🚌 Linha Centro 2 · Recife - Jaboatão</option>
    <option value="Sul">🚌 Linha Sul · Recife - Cajueiro Seco</option>
    <option value="VLT Cabo">🚌 Linha VLT Cabo · Cabo de Santo Agostinho - Cajueiro Seco</option>
    <option value="VLT Curado">🚌 Linha VLT Curado · Curado - Cajueiro Seco</option>
  </optgroup>
      </select>
      <div style="display:flex; gap:8px;">
        <button class="btn btn-primary" style="flex:1; min-height:44px; font-weight:800;" onclick="confirmSwitchLine()">
          Confirmar Troca de Linha
        </button>
        <button class="btn" style="min-height:44px;" onclick="closeLineSwitcherModal()">
          Cancelar
        </button>
      </div>
    </div>
  </div>

  <!-- MODAL DE NAVEGAÇÃO DE TODOS OS TERMINAIS INTEGRADOS (T.I.) -->
  <div id="all-tis-modal" style="display:none; position:fixed; inset:0; background:rgba(0,0,0,0.65); z-index:99999; justify-content:center; align-items:center; padding:16px;">
    <div style="background:var(--bg-surface); border:1px solid var(--border); border-radius:var(--radius-lg); max-width:520px; width:100%; padding:22px; box-shadow:0 12px 32px rgba(0,0,0,0.35); max-height:85vh; display:flex; flex-direction:column;">
      <h3 style="font-size:18px; font-weight:800; margin-bottom:4px;">🏛️ Terminais Integrados (T.I.) da RMR</h3>
      <p style="font-size:13px; color:var(--text-secondary); margin-bottom:12px;">Selecione qualquer Terminal Integrado para teletransportar o mapa instantaneamente:</p>
      <input id="ti-search-filter" type="text" placeholder="🔍 Filtrar cidade ou T.I. (ex: Cabo, Camela, Macaxeira, Joana, Pelópidas)..." oninput="filterTiModalList(this.value)"
        style="width:100%; min-height:42px; padding:8px 12px; font-size:13px; border:1.5px solid var(--border-strong); border-radius:10px; background:var(--bg-surface); color:var(--text-main); margin-bottom:12px;" />
      <div id="ti-modal-items-container" style="flex:1; overflow-y:auto; display:flex; flex-direction:column; gap:8px; margin-bottom:14px;">
      </div>
      <button class="btn" style="width:100%; min-height:40px;" onclick="closeAllTisModal()">Fechar</button>
    </div>
  </div>

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

    function toggleMobileSheet() {
      const sheet = document.getElementById("companion-bottom-sheet");
      const hint = document.getElementById("sheet-handle-text");
      if (!sheet) return;
      sheet.classList.toggle("sheet-expanded");
      if (sheet.classList.contains("sheet-expanded")) {
        if (hint) hint.textContent = "▼ Toque para recolher";
      } else {
        if (hint) hint.textContent = "▲ Puxe para ver paradas e rotas";
      }
    }

    function searchUserPlaceMobile() {
      const inp = document.getElementById("mobile-search-input");
      if (!inp || !inp.value.trim()) return;
      const deskInp = document.getElementById("map-search-input");
      if (deskInp) deskInp.value = inp.value;
      searchUserPlace();
    }

    function switchModule(modId, btnEl) {
      document.querySelectorAll(".workspace-view").forEach(v => v.classList.remove("active"));
      document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
      document.querySelectorAll(".mob-nav-item").forEach(b => b.classList.remove("active"));
      const targetView = document.getElementById(modId);
      if (targetView) targetView.classList.add("active");

      // Synchronize desktop top tabs and mobile bottom nav
      const modIndex = modId === "mod-gis" ? 0 : (modId === "mod-safety" ? 1 : 2);
      const topTabs = document.querySelectorAll(".tab-btn");
      if (topTabs[modIndex]) topTabs[modIndex].classList.add("active");
      const mobTabs = document.querySelectorAll(".mob-nav-item");
      if (mobTabs[modIndex]) mobTabs[modIndex].classList.add("active");

      if (modId === "mod-gis") {
        if (leafletMap) {
          setTimeout(() => leafletMap.invalidateSize(), 150);
        }
        requestAnimationFrame(drawPe60GisCanvas);
      }
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
        const sheet = document.getElementById("companion-bottom-sheet");
        if (sheet && sheet.classList.contains("sheet-expanded")) {
          toggleMobileSheet();
        }
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
      if (!navigator.geolocation) {
        if (notice) {
          notice.style.display = "block";
          notice.innerHTML = `⚠️ Seu navegador não suporta geolocalização. Clique em <strong>Camela (PE-60)</strong> para ver os horários!`;
        }
        return;
      }

      // Verifica se está em contexto seguro (HTTPS ou localhost) exigido pelos navegadores para liberar o GPS
      const isSecure = window.isSecureContext || location.hostname === "localhost" || location.hostname === "127.0.0.1";
      if (!isSecure) {
        if (notice) {
          notice.style.display = "block";
          notice.innerHTML = `
            <div style="line-height:1.5;">
              ⚠️ <strong>Bloqueio de Segurança do Navegador (Requer HTTPS):</strong><br>
              Navegadores móveis bloqueiam o chip de satélite em endereços HTTP comuns (como <code>http://192.168...</code>).<br>
              • <strong>Acesso Seguro:</strong> Use <a href="https://icy-oranges-think.loca.lt" target="_blank" style="color:var(--brand-green); font-weight:800; text-decoration:underline;">https://icy-oranges-think.loca.lt</a><br>
              • <strong>Ou veja agora mesmo:</strong> Clique no botão verde <button class="btn btn-emerald" style="min-height:26px; padding:2px 8px; font-size:11.5px; font-weight:800; margin-left:4px;" onclick="setSimulatedUserLocation(-8.494915, -35.092190, 'Camela (PE-60) · Ipojuca', true)">📍 Camela (PE-60)</button> para carregar Camela instantaneamente!
            </div>
          `;
        }
        return;
      }

      if (btn) btn.textContent = "Buscando satélites...";

      function handleSuccess(pos) {
        const lat = pos.coords.latitude;
        const lon = pos.coords.longitude;
        const acc = Math.round(pos.coords.accuracy || 0);

        // Verifica se o roteador/provedor de internet sofreu o desvio clássico de IP para Japaratinga/Alagoas
        if (lat < -8.65 || lat > -7.6 || lon < -35.5 || lon > -34.7) {
          if (btn) btn.textContent = `📍 Camela (IP corrigido)`;
          if (notice) {
            notice.style.display = "block";
            notice.innerHTML = `⚠️ <strong>Desvio de IP da Operadora corrigido:</strong> Seu provedor (DTEL Telecom, IP 177.200.245.197) localizou seu IP em <strong>Japaratinga/AL</strong> (Lat ${lat.toFixed(4)}, Lon ${lon.toFixed(4)}). Como você está em <strong>Camela (Ipojuca - PE)</strong>, reposicionamos você automaticamente para a sua parada real em Camela! <button class="btn" style="min-height:26px; padding:2px 8px; font-size:11.5px; margin-left:6px;" onclick="showPcDiagnosticsModal()">🔍 Ver Diagnóstico do seu PC</button>`;
          }
          setSimulatedUserLocation(-8.494915, -35.092190, "Rodovia PE-60 (Trevo de Camela) · Ipojuca", true, true);
          return;
        }

        if (btn) btn.textContent = `📍 Meu GPS (±${acc}m)`;
        if (notice) {
          if (acc > 150) {
            notice.style.display = "block";
            notice.innerHTML = `<strong>Atenção sobre o GPS:</strong> Posição obtida com margem de <strong>±${acc} metros</strong>. Se você estiver num ponto diferente, clique em <strong>Camela (PE-60)</strong> ou busque sua rua acima!`;
          } else {
            notice.style.display = "none";
          }
        }
        setSimulatedUserLocation(lat, lon, `Minha Posição GPS (±${acc}m)`, true, true);
      }

      function handleError(err) {
        if (btn) btn.textContent = "📍 Usar Meu GPS";
        if (!notice) return;
        notice.style.display = "block";

        if (err && err.code === 1) { // PERMISSION_DENIED
          notice.innerHTML = `
            <div style="line-height:1.5;">
              ⚠️ <strong>Permissão de Localização Bloqueada no Navegador:</strong><br>
              Para liberar o GPS:<br>
              <strong>1.</strong> Toque no ícone de <strong>cadeado 🔒</strong> ou <strong>configurações do site 🎚️</strong> ao lado do endereço na barra do navegador.<br>
              <strong>2.</strong> Em <strong>Permissões</strong> (ou Localização), altere para <strong>"Permitir"</strong> e recarregue.<br>
              <strong>3.</strong> Certifique-se de que a <strong>Localização / GPS</strong> do aparelho está ligada.<br>
              👉 <em>Ou veja agora sem permissão:</em> Clique em <button class="btn btn-emerald" style="min-height:26px; padding:2px 8px; font-size:12px; font-weight:800; margin-left:4px;" onclick="setSimulatedUserLocation(-8.494915, -35.092190, 'Camela (PE-60) · Ipojuca', true)">📍 Usar Posição Camela (PE-60)</button>
            </div>
          `;
        } else if (err && err.code === 3) { // TIMEOUT
          if (btn) btn.textContent = "Tentando via rede...";
          navigator.geolocation.getCurrentPosition(
            handleSuccess,
            (err2) => {
              if (btn) btn.textContent = "📍 Usar Meu GPS";
              notice.innerHTML = `⚠️ Sinal de satélite fraco no momento (ambiente interno). Clique em <button class="btn btn-emerald" style="min-height:26px; padding:2px 8px; font-size:12px; font-weight:800; margin-left:4px;" onclick="setSimulatedUserLocation(-8.494915, -35.092190, 'Camela (PE-60) · Ipojuca', true)">📍 Camela (PE-60)</button> para carregar as paradas ao seu redor!`;
            },
            { enableHighAccuracy: false, timeout: 10000, maximumAge: 60000 }
          );
        } else {
          notice.innerHTML = `⚠️ <strong>GPS indisponível:</strong> ${err && err.message ? err.message : 'Sinal não capturado'}. Clique em <button class="btn btn-emerald" style="min-height:26px; padding:2px 8px; font-size:12px; font-weight:800; margin-left:4px;" onclick="setSimulatedUserLocation(-8.494915, -35.092190, 'Camela (PE-60) · Ipojuca', true)">📍 Camela (PE-60)</button> para ver as paradas da sua rua!`;
        }
      }

      navigator.geolocation.getCurrentPosition(
        handleSuccess,
        handleError,
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

    // =========================================================================
    // USER AUTH, ONBOARDING & PROFILE FLOW (TESTE DO ZERO)
    // =========================================================================
    function initAuthFlow() {
      const isLogged = localStorage.getItem("grafoparada_user_logged");
      const authScreen = document.getElementById("auth-onboarding-screen");
      if (!isLogged || isLogged !== "true") {
        if (authScreen) authScreen.style.display = "flex";
        goToAuthStep("welcome");
      } else {
        if (authScreen) authScreen.style.display = "none";
        try {
          const raw = localStorage.getItem("grafoparada_user_data");
          if (raw) {
            const data = JSON.parse(raw);
            applyUserData(data);
          }
        } catch (e) {
          console.warn("User data parse err:", e);
        }
      }
    }

    function goToAuthStep(stepName) {
      document.getElementById("auth-step-welcome").style.display = stepName === "welcome" ? "block" : "none";
      document.getElementById("auth-step-signup").style.display = stepName === "signup" ? "block" : "none";
      document.getElementById("auth-step-preferences").style.display = stepName === "preferences" ? "block" : "none";
      document.getElementById("auth-step-login").style.display = stepName === "login" ? "block" : "none";
      const scr = document.getElementById("auth-onboarding-screen");
      if (scr) scr.scrollTop = 0;
    }

    function quickTestUser(name, place) {
      const userData = {
        name: name || "Cauã Cunha",
        phone: "(81) 98888-7766",
        place: place || "Camela (PE-60)",
        line: "178",
        voice: "pt-BR-FranciscaNeural"
      };
      saveAndEnterApp(userData);
    }

    function completeRegistration() {
      const name = document.getElementById("signup-name").value.trim() || "Cauã Cunha";
      const phone = document.getElementById("signup-phone").value.trim() || "(81) 98888-7766";
      const place = document.getElementById("signup-place").value;
      const line = document.getElementById("signup-line").value;
      const voice = document.getElementById("pref-voice-select").value;

      const userData = { name, phone, place, line, voice };
      saveAndEnterApp(userData);
    }

    function doLogin() {
      const phoneOrName = document.getElementById("login-phone").value.trim() || "Cauã Cunha";
      const userData = {
        name: phoneOrName,
        phone: "(81) 98888-7766",
        place: "Camela (PE-60)",
        line: "178",
        voice: "pt-BR-FranciscaNeural"
      };
      saveAndEnterApp(userData);
    }

    function saveAndEnterApp(userData) {
      localStorage.setItem("grafoparada_user_logged", "true");
      localStorage.setItem("grafoparada_user_data", JSON.stringify(userData));
      applyUserData(userData);

      const authScreen = document.getElementById("auth-onboarding-screen");
      if (authScreen) authScreen.style.display = "none";

      // Atualiza o crachá da linha selecionada no app
      const lineBadge = document.getElementById("active-line-badge");
      if (lineBadge && userData.line) {
        lineBadge.textContent = `Linha ${userData.line}`;
      }
      const etaLabel = document.querySelector(".eta-stat-label");
      if (etaLabel && userData.line) {
        etaLabel.textContent = `Previsão Linha ${userData.line}`;
      }

      // Welcome voice message dinâmico com a linha e local escolhidos pelo usuário
      const placeShort = userData.place ? userData.place.split('·')[0].replace("📍", "").trim() : "Camela";
      const voiceText = `Olá, ${userData.name.split(' ')[0]}! Bem-vindo ao GrafoParada. Monitorando a Linha ${userData.line} em ${placeShort} com proteção de inteligência artificial.`;
      setTimeout(() => playNaturalVoice(voiceText, null), 800);

      // Posiciona o usuário dinamicamente em QUALQUER Terminal Integrado ou parada de Camela
      const matchedTerminal = ALL_TERMINALS_DATA.find(t => t.name === userData.place || (userData.place && userData.place.includes(t.name)) || (userData.place && t.name.includes(userData.place)));
      if (matchedTerminal) {
        setSimulatedUserLocation(matchedTerminal.lat, matchedTerminal.lon, matchedTerminal.name, true, true);
      } else if (userData.place && userData.place.includes("Camela")) {
        setSimulatedUserLocation(-8.494915, -35.092190, "Rodovia PE-60 (Trevo de Camela) · Ipojuca", true, true);
      } else {
        setSimulatedUserLocation(-8.494915, -35.092190, userData.place || "Camela (PE-60)", true, true);
      }
    }

    function applyUserData(userData) {
      if (!userData) return;
      const headerName = document.getElementById("header-user-name");
      if (headerName) headerName.textContent = userData.name.split(" ")[0];

      const pName = document.getElementById("prof-modal-name");
      const pPhone = document.getElementById("prof-modal-phone");
      const pPlace = document.getElementById("prof-modal-place");
      const pLine = document.getElementById("prof-modal-line");
      const pVoice = document.getElementById("prof-modal-voice");

      if (pName) pName.textContent = userData.name;
      if (pPhone) pPhone.textContent = userData.phone;
      if (pPlace) pPlace.textContent = userData.place;
      if (pLine) pLine.textContent = `Linha ${userData.line}`;
      if (pVoice) pVoice.textContent = userData.voice.includes("Francisca") ? "Francisca" : (userData.voice.includes("Antonio") ? "Antônio" : "Thalita");

      const voiceSel = document.getElementById("neural-voice-select");
      if (voiceSel && userData.voice) voiceSel.value = userData.voice;
    }

    function openUserProfileModal() {
      const m = document.getElementById("user-profile-modal");
      if (m) m.style.display = "flex";
    }

    function closeUserProfileModal() {
      const m = document.getElementById("user-profile-modal");
      if (m) m.style.display = "none";
    }

    function logoutAndResetTest() {
      if (confirm("Deseja sair da conta e reiniciar o teste do zero (boas-vindas, cadastro e telas)?")) {
        localStorage.removeItem("grafoparada_user_logged");
        localStorage.removeItem("grafoparada_user_data");
        closeUserProfileModal();
        initAuthFlow();
      }
    }

    // =========================================================================
    // SEARCH & FILTER FUNCTIONS FOR ALL 400 LINES & 44 TERMINALS
    // =========================================================================
    function filterLineOptions(query) {
      const sel = document.getElementById("signup-line");
      if (!sel) return;
      const q = query.toLowerCase().trim();
      const options = sel.querySelectorAll("option");
      options.forEach(opt => {
        const text = opt.textContent.toLowerCase();
        const val = opt.value.toLowerCase();
        if (!q || text.includes(q) || val.includes(q)) {
          opt.style.display = "";
        } else {
          opt.style.display = "none";
        }
      });
      const firstVis = Array.from(options).find(o => o.style.display !== "none");
      if (firstVis && (!sel.selectedOptions[0] || sel.selectedOptions[0].style.display === "none")) {
        firstVis.selected = true;
      }
    }

    function filterPlaceOptions(query) {
      const sel = document.getElementById("signup-place");
      if (!sel) return;
      const q = query.toLowerCase().trim();
      const options = sel.querySelectorAll("option");
      options.forEach(opt => {
        const text = opt.textContent.toLowerCase();
        if (!q || text.includes(q)) {
          opt.style.display = "";
        } else {
          opt.style.display = "none";
        }
      });
      const firstVis = Array.from(options).find(o => o.style.display !== "none");
      if (firstVis && (!sel.selectedOptions[0] || sel.selectedOptions[0].style.display === "none")) {
        firstVis.selected = true;
      }
    }

    function filterSwitcherOptions(query) {
      const sel = document.getElementById("switcher-line-select");
      if (!sel) return;
      const q = query.toLowerCase().trim();
      const options = sel.querySelectorAll("option");
      options.forEach(opt => {
        const text = opt.textContent.toLowerCase();
        const val = opt.value.toLowerCase();
        if (!q || text.includes(q) || val.includes(q)) {
          opt.style.display = "";
        } else {
          opt.style.display = "none";
        }
      });
      const firstVis = Array.from(options).find(o => o.style.display !== "none");
      if (firstVis && (!sel.selectedOptions[0] || sel.selectedOptions[0].style.display === "none")) {
        firstVis.selected = true;
      }
    }

    function openLineSwitcherModal() {
      const m = document.getElementById("line-switcher-modal");
      if (m) m.style.display = "flex";
    }

    function closeLineSwitcherModal() {
      const m = document.getElementById("line-switcher-modal");
      if (m) m.style.display = "none";
    }

    function confirmSwitchLine() {
      const sel = document.getElementById("switcher-line-select");
      if (!sel || !sel.selectedOptions[0]) return;
      const opt = sel.selectedOptions[0];
      const code = opt.value;
      const fullLabel = opt.textContent.replace("🚌 Linha ", "").trim();

      const badge = document.getElementById("active-line-badge");
      if (badge) badge.textContent = fullLabel;

      const etaLabel = document.querySelector(".eta-stat-label");
      if (etaLabel) etaLabel.textContent = `Previsão Linha ${code}`;

      closeLineSwitcherModal();

      // Audio feedback
      playNaturalVoice(`Linha alterada para ${fullLabel}. Monitorando chegadas na sua parada.`, null);
    }

    // TERMINAL INTEGRADOS (T.I.) MODAL LIST
    const ALL_TERMINALS_DATA = [{"id": "190890", "name": "Ti Abreu E Lima", "full_name": "Ti Abreu E Lima - 190890", "lat": -7.921296345462924, "lon": -34.89528933864802, "region": "Abreu e Lima"}, {"id": "030000", "name": "Ti Cabo", "full_name": "Ti Cabo - 030000", "lat": -8.285064968083757, "lon": -35.03239778768872, "region": "Cabo de Santo Agostinho"}, {"id": "090000", "name": "Ti Camaragibe", "full_name": "Ti Camaragibe - 090000", "lat": -8.02478969917935, "lon": -34.99606368801693, "region": "Camaragibe"}, {"id": "090848", "name": "Ti Cosme E Damião", "full_name": "Ti Cosme E Damião - 090848", "lat": -8.036236471550168, "lon": -34.988185865632055, "region": "Camaragibe"}, {"id": "150323", "name": "Terminal Da Linha 1969 Ti Igarassu / Itapissuma", "full_name": "Terminal Da Linha 1969 Ti Igarassu / Itapissuma - 150323", "lat": -7.771441667468382, "lon": -34.90325833329781, "region": "Igarassu"}, {"id": "150000", "name": "Ti Igarassu", "full_name": "Ti Igarassu - 150000", "lat": -7.832827812755261, "lon": -34.911922291263345, "region": "Igarassu"}, {"id": "IPOJUCA_CENTRO", "name": "Ipojuca · Centro / Praça e UPA (PE-60)", "full_name": "Rodovia PE-60 (Centro / Trevo de Ipojuca) · Ipojuca - PE", "lat": -8.398512, "lon": -35.06412, "region": "Ipojuca"}, {"id": "PORTO_GALINHAS", "name": "Porto de Galinhas · Terminal de Ônibus", "full_name": "Terminal de Porto de Galinhas · Ipojuca - PE", "lat": -8.505432, "lon": -35.004121, "region": "Ipojuca"}, {"id": "CAMELA_CENTRO", "name": "Camela · Centro (Rua do Comércio / Terminal)", "full_name": "Rua do Comércio / Terminal de Camela · Ipojuca - PE", "lat": -8.514931, "lon": -35.123469, "region": "Ipojuca (Camela)"}, {"id": "CAMELA_TREVO", "name": "Camela · Trevo da Rodovia PE-60 (Ipojuca)", "full_name": "Rodovia PE-60 (Entrada / Trevo de Camela) · Ipojuca - PE", "lat": -8.494915, "lon": -35.09219, "region": "Ipojuca (Camela)"}, {"id": "020471", "name": "Ponto De Retorno Muribeca/Ti Cajueiro Seco", "full_name": "Ponto De Retorno Muribeca/Ti Cajueiro Seco - 020471", "lat": -8.149558336096304, "lon": -34.97679999995839, "region": "Jaboatão dos Guararapes"}, {"id": "050490", "name": "Terminal Da Linha 290 Bonança/Ti Jaboatão", "full_name": "Terminal Da Linha 290 Bonança/Ti Jaboatão - 050490", "lat": -8.106150000906043, "lon": -35.19478888880074, "region": "Jaboatão dos Guararapes"}, {"id": "020002", "name": "Ti Cajueiro Seco", "full_name": "Ti Cajueiro Seco - 020002", "lat": -8.167989004420969, "lon": -34.934533688542, "region": "Jaboatão dos Guararapes"}, {"id": "040135", "name": "Ti Cavaleiro", "full_name": "Ti Cavaleiro - 040135", "lat": -8.094519891011108, "lon": -34.97291415128109, "region": "Jaboatão dos Guararapes"}, {"id": "050000", "name": "Ti Jaboatão", "full_name": "Ti Jaboatão - 050000", "lat": -8.111632198453698, "lon": -35.014398835403874, "region": "Jaboatão dos Guararapes"}, {"id": "020536", "name": "Ti Prazeres", "full_name": "Ti Prazeres - 020536", "lat": -8.161419696372274, "lon": -34.92655824202219, "region": "Jaboatão dos Guararapes"}, {"id": "130380", "name": "Terminal Da Linha 895 Alto Do Sol Nascente/Ti Xamba", "full_name": "Terminal Da Linha 895 Alto Do Sol Nascente/Ti Xamba - 130380", "lat": -7.976716669262277, "lon": -34.91052499996502, "region": "Olinda"}, {"id": "150002", "name": "Ti Pe-15", "full_name": "Ti Pe-15 - 150002", "lat": -7.982723500007164, "lon": -34.856319955857714, "region": "Olinda"}, {"id": "160000", "name": "Ti Rio Doce", "full_name": "Ti Rio Doce - 160000", "lat": -7.9607209918352, "lon": -34.85102855127083, "region": "Olinda"}, {"id": "130000", "name": "Ti Xambá", "full_name": "Ti Xambá - 130000", "lat": -8.001196661427809, "lon": -34.892626605900084, "region": "Olinda"}, {"id": "150936", "name": "Ti Pelópidas", "full_name": "Ti Pelópidas - Embarque 01- 150936", "lat": -7.947072139974567, "lon": -34.87797167910255, "region": "Paulista"}, {"id": "150001", "name": "Ti Pelópidas Silveira", "full_name": "Ti Pelópidas Silveira - 150001", "lat": -7.946769515773473, "lon": -34.877856200512845, "region": "Paulista"}, {"id": "150957", "name": "Ti Pelópidas- Desembarque 01", "full_name": "Ti Pelópidas- Desembarque 01 - 150957", "lat": -7.945576169910893, "lon": -34.87759786383087, "region": "Paulista"}, {"id": "150952", "name": "Ti Pelópidas- Embarque 17", "full_name": "Ti Pelópidas- Embarque 17 - 150952", "lat": -7.946586597184459, "lon": -34.87784604226094, "region": "Paulista"}, {"id": "080254", "name": "Terminal Da Linha 303 Ti Caxangá/Curado Ii (Br-232)", "full_name": "Terminal Da Linha 303 Ti Caxangá/Curado Ii (Br-232) - 080254", "lat": -8.04768889155233, "lon": -34.95956388884871, "region": "Recife"}, {"id": "090276", "name": "Terminal De Linha 302", "full_name": "Terminal De Linha 302 - Caxangá / Ti Tip - 090276", "lat": -8.031608334216045, "lon": -34.95833611106901, "region": "Recife"}, {"id": "080331", "name": "Terminal Nova Morada/Ti Caxangá", "full_name": "Terminal Nova Morada/Ti Caxangá - 080331", "lat": -8.025455556436276, "lon": -34.950294444403426, "region": "Recife"}, {"id": "020900", "name": "Ti Aeroporto", "full_name": "Ti Aeroporto - 020900", "lat": -8.134136062005572, "lon": -34.91512430325258, "region": "Recife"}, {"id": "180003", "name": "Ti Afogados", "full_name": "Ti Afogados - 180003", "lat": -8.077302413073026, "lon": -34.90679635435186, "region": "Recife"}, {"id": "040000", "name": "Ti Barro", "full_name": "Ti Barro - 040000", "lat": -8.08817445055669, "lon": -34.94585759758854, "region": "Recife"}, {"id": "080000", "name": "Ti Caxangá", "full_name": "Ti Caxangá - 080000", "lat": -8.031208942325296, "lon": -34.954937843290075, "region": "Recife"}, {"id": "080431", "name": "Ti Cdu", "full_name": "Ti Cdu - 080431", "lat": -8.03883429543645, "lon": -34.94299630962573, "region": "Recife"}, {"id": "080012", "name": "Ti Getulio Vargas", "full_name": "Ti Getulio Vargas - 080012", "lat": -8.050618224769712, "lon": -34.92200224898446, "region": "Recife"}, {"id": "080936", "name": "Ti Getúlio Vargas", "full_name": "Ti Getúlio Vargas - Embarque 01 - 080936", "lat": -8.050186111999881, "lon": -34.92204444440719, "region": "Recife"}, {"id": "180915", "name": "Ti Joana Bezarra", "full_name": "Ti Joana Bezarra - Embarque 05 - 180915", "lat": -8.072163889784743, "lon": -34.89523055552157, "region": "Recife"}, {"id": "180002", "name": "Ti Joana Bezerra", "full_name": "Ti Joana Bezerra - 180002", "lat": -8.072128730179074, "lon": -34.89576292232596, "region": "Recife"}, {"id": "180004", "name": "Ti Largo Da Paz", "full_name": "Ti Largo Da Paz - 180004", "lat": -8.081244227400381, "lon": -34.905061094793076, "region": "Recife"}, {"id": "110000", "name": "Ti Macaxeira", "full_name": "Ti Macaxeira - 110000", "lat": -8.008235080134988, "lon": -34.93832783476195, "region": "Recife"}, {"id": "150901", "name": "Ti Pe 15", "full_name": "Ti Pe 15 - Embarque 01 A - 150901", "lat": -7.983177157724002, "lon": -34.85607007133678, "region": "Recife"}, {"id": "180001", "name": "Ti Recife", "full_name": "Ti Recife - 180001", "lat": -8.068453118313338, "lon": -34.88437609302074, "region": "Recife"}, {"id": "040920", "name": "Ti Santa Luzia", "full_name": "Ti Santa Luzia - 040920", "lat": -8.084164824756378, "lon": -34.93009157562516, "region": "Recife"}, {"id": "020000", "name": "Ti Tancredo Neves", "full_name": "Ti Tancredo Neves - 020000", "lat": -8.122014463888496, "lon": -34.91246455096088, "region": "Recife"}, {"id": "070000", "name": "Ti Tip", "full_name": "Ti Tip - 070000", "lat": -8.064289307992048, "lon": -34.98207327791133, "region": "Recife / Várzea (TIP)"}, {"id": "SUAPE_PORTO", "name": "Complexo Industrial e Portuário de Suape", "full_name": "Porto de Suape · Rodovia PE-60 / TSuape · Ipojuca", "lat": -8.3941, "lon": -34.9812, "region": "Suape / Ipojuca"}];

    function openAllTisModal() {
      const m = document.getElementById("all-tis-modal");
      if (m) m.style.display = "flex";
      renderTiModalList("");
    }

    function closeAllTisModal() {
      const m = document.getElementById("all-tis-modal");
      if (m) m.style.display = "none";
    }

    function filterTiModalList(query) {
      renderTiModalList(query);
    }

    function renderTiModalList(query) {
      const container = document.getElementById("ti-modal-items-container");
      if (!container) return;
      const q = query.toLowerCase().trim();
      const filtered = ALL_TERMINALS_DATA.filter(t => !q || t.name.toLowerCase().includes(q) || t.region.toLowerCase().includes(q));

      container.innerHTML = filtered.map(t => `
        <div style="background:var(--bg-subtle); border:1px solid var(--border); border-radius:10px; padding:10px 12px; display:flex; justify-content:space-between; align-items:center; cursor:pointer;"
          onclick="selectTerminalFromModal('${t.name.replace(/'/g, "\'")}', ${t.lat}, ${t.lon})">
          <div>
            <div style="font-weight:800; font-size:13.5px;">${t.name}</div>
            <div style="font-size:11.5px; color:var(--text-muted);">Região: ${t.region}</div>
          </div>
          <span class="tag tag-emerald" style="font-size:11px;">Ir ao T.I. →</span>
        </div>
      `).join("");
    }

    function selectTerminalFromModal(name, lat, lon) {
      closeAllTisModal();
      setSimulatedUserLocation(lat, lon, name, true, true);
    }

    function testPrefVoice() {
      const sel = document.getElementById("pref-voice-select");
      const v = sel ? sel.value : "pt-BR-FranciscaNeural";
      playNaturalVoice("Oi! Esta é a voz que vai te avisar discretamente no fone quando o ônibus estiver chegando na PE-60.", null);
    }

    // INITIALIZATION
    initAuthFlow();
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
