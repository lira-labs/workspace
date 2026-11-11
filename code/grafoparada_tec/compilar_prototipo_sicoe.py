# -*- coding: utf-8 -*-
import json
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

base_dir = Path("code/grafoparada_tec")
data_dir = base_dir / "data"

with open(data_dir / "telemetria_199_camela_cabo.json", "r", encoding="utf-8") as f:
    t199 = json.load(f)

with open(data_dir / "telemetria_real_pe60.json", "r", encoding="utf-8") as f:
    t178 = json.load(f)

with open(data_dir / "terminais_integrados_sei.json", "r", encoding="utf-8") as f:
    sei_terminals = json.load(f)

with open(data_dir / "gtfs_full_catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

routes = catalog["routes"]

# Group terminals by municipality for easy navigation
terminals_by_mun = {}
for t in sei_terminals:
    mun = t.get("municipio", "Grande Recife")
    if mun not in terminals_by_mun:
        terminals_by_mun[mun] = []
    terminals_by_mun[mun].append(t)

# Build options for Home (SEI terminals + Camela + Ipojuca)
home_opts = []
home_opts.append('<optgroup label="⭐ Sua Residência (Região Sul · PE-60)">')
home_opts.append('  <option value="Camela · Centro (Rua do Comércio / Linha 199)" data-lat="-8.514931" data-lon="-35.123469" selected>🏠 Camela · Centro (Rua do Comércio / Linha 199)</option>')
home_opts.append('  <option value="Camela · Rodovia PE-60 (Trevo PE-051)" data-lat="-8.494915" data-lon="-35.092190">🏠 Camela · Rodovia PE-60 (Trevo PE-051)</option>')
home_opts.append('  <option value="Ipojuca · Centro (Praça / UPA PE-60)" data-lat="-8.398512" data-lon="-35.064120">🏠 Ipojuca · Centro (Praça / UPA PE-60)</option>')
home_opts.append('</optgroup>')

for mun, t_list in terminals_by_mun.items():
    home_opts.append(f'<optgroup label="🏛️ Terminais Integrados do SEI · {mun}">')
    for t in t_list:
        home_opts.append(f'  <option value="{t["ti_name"]} ({mun})" data-lat="{t["lat"]}" data-lon="{t["lon"]}">🏛️ {t["ti_name"]} ({t.get("bairro", mun)})</option>')
    home_opts.append('</optgroup>')
home_opts_html = "\n".join(home_opts)

# Build options for Work (SEI terminals + Suape + Universities)
work_opts = []
work_opts.append('<optgroup label="💼 Principais Polos de Trabalho / Estudo">')
work_opts.append('  <option value="TI Cabo (Terminal Integrado do Cabo)" data-lat="-8.285065" data-lon="-35.032398" selected>💼 TI Cabo (Terminal Integrado · Conexão Metrô/RMR)</option>')
work_opts.append('  <option value="Complexo Industrial e Portuário de Suape" data-lat="-8.396500" data-lon="-34.980500">💼 Complexo Industrial de Suape (Porto / Refinaria)</option>')
work_opts.append('  <option value="UFRPE (Universidade Rural · Dois Irmãos)" data-lat="-8.016200" data-lon="-34.944800">💼 UFRPE (Universidade Rural · Dois Irmãos)</option>')
work_opts.append('  <option value="UFPE (Campus Recife / TI CDU)" data-lat="-8.038834" data-lon="-34.942996">💼 UFPE (Campus Recife / TI CDU)</option>')
work_opts.append('  <option value="Recife Centro (TI Joana Bezerra / TI Recife)" data-lat="-8.072129" data-lon="-34.895763">💼 Recife Centro (TI Joana Bezerra / TI Recife)</option>')
work_opts.append('  <option value="TI Aeroporto (Boa Viagem / Polo Empresarial)" data-lat="-8.134136" data-lon="-34.915124">💼 TI Aeroporto (Boa Viagem / Polo Empresarial)</option>')
work_opts.append('</optgroup>')

for mun, t_list in terminals_by_mun.items():
    work_opts.append(f'<optgroup label="🏛️ Terminais Integrados · {mun}">')
    for t in t_list:
        work_opts.append(f'  <option value="{t["ti_name"]} ({mun})" data-lat="{t["lat"]}" data-lon="{t["lon"]}">🏛️ {t["ti_name"]} ({t.get("bairro", mun)})</option>')
    work_opts.append('</optgroup>')
work_opts_html = "\n".join(work_opts)

# Build options for Routes (199 first, then priority, then all)
priority_codes = ["199", "178", "191", "195", "198", "197", "119"]
pe60_r = [r for r in routes if r["code"] in priority_codes]
pe60_r.sort(key=lambda r: priority_codes.index(r["code"]))
other_r = [r for r in routes if r["code"] not in priority_codes]

route_opts = []
route_opts.append('<optgroup label="⭐ Linhas Principais da Sua Região">')
for r in pe60_r:
    sel = ' selected' if r["code"] == "199" else ''
    route_opts.append(f'  <option value="{r["code"]}"{sel}>🚌 Linha {r["label"]}</option>')
route_opts.append('</optgroup>')
route_opts.append('<optgroup label="📋 Todas as Linhas do Grande Recife (SEI / CTM)">')
for r in other_r[:80]:
    route_opts.append(f'  <option value="{r["code"]}">🚌 Linha {r["label"]}</option>')
route_opts.append('</optgroup>')
route_opts_html = "\n".join(route_opts)

template = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover" />
  <title>GrafoParada · Ônibus Seguro no Grande Recife</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=JetBrains+Mono:wght@600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

  <style>
    :root {
      --brand-green: #059669;
      --brand-green-dark: #047857;
      --brand-green-bg: #ecfdf5;
      --brand-green-border: #a7f3d0;

      --blue-accent: #0284c7;
      --blue-bg: #f0f9ff;
      --blue-border: #bae6fd;

      --warning-amber: #d97706;
      --warning-bg: #fffbeb;
      --warning-border: #fde68a;

      --danger-red: #dc2626;
      --danger-bg: #fef2f2;
      --danger-border: #fecaca;

      --bg-surface: #ffffff;
      --bg-page: #f8fafc;
      --text-main: #0f172a;
      --text-secondary: #475569;
      --text-muted: #94a3b8;
      --border-color: #e2e8f0;
      --shadow-sheet: 0 -10px 30px rgba(0, 0, 0, 0.12);
      --shadow-floating: 0 4px 20px rgba(0, 0, 0, 0.14);
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-tap-highlight-color: transparent;
    }

    body {
      width: 100vw;
      height: 100dvh;
      overflow: hidden;
      background: #0f172a;
      background-image: radial-gradient(circle at 50% 10%, #1e293b 0%, #0b0f19 100%);
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      color: var(--text-main);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
    }

    /* DESKTOP TOP BAR (OUTSIDE PHONE) */
    .desktop-outer-bar {
      display: none;
      width: 100%;
      max-width: 900px;
      padding: 10px 20px;
      margin-bottom: 12px;
      justify-content: space-between;
      align-items: center;
      color: #e2e8f0;
      font-size: 13.5px;
      z-index: 1000;
    }

    .desktop-outer-bar .badge-title {
      font-weight: 800;
      display: flex;
      align-items: center;
      gap: 8px;
      letter-spacing: -0.01em;
    }

    .desktop-outer-bar .btn-desktop-action {
      background: rgba(255, 255, 255, 0.12);
      border: 1px solid rgba(255, 255, 255, 0.2);
      color: #ffffff;
      border-radius: 999px;
      padding: 6px 14px;
      font-size: 12.5px;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: background 0.2s;
    }

    .desktop-outer-bar .btn-desktop-action:hover {
      background: rgba(255, 255, 255, 0.25);
    }

    /* PHONE FRAME CONTAINER */
    .phone-simulator-frame {
      position: relative;
      width: 100%;
      height: 100%;
      background: #f8fafc;
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }

    /* DESKTOP MEDIA QUERY: ELEGANT SMARTPHONE FRAME */
    @media (min-width: 601px) {
      .desktop-outer-bar {
        display: flex;
      }
      .phone-simulator-frame {
        width: 412px;
        height: min(870px, 92vh);
        border-radius: 46px;
        border: 8px solid #1e293b;
        box-shadow: 0 25px 70px rgba(0, 0, 0, 0.4), 0 0 0 2px rgba(255, 255, 255, 0.1);
      }
      .phone-notch-island {
        display: flex;
      }
      .phone-home-indicator {
        display: block;
      }
    }

    /* FULLSCREEN TOGGLE ON DESKTOP */
    body.is-fullscreen .phone-simulator-frame {
      width: 100vw !important;
      height: 100dvh !important;
      border-radius: 0 !important;
      border: none !important;
      box-shadow: none !important;
    }
    body.is-fullscreen .desktop-outer-bar {
      display: none !important;
    }

    /* DYNAMIC ISLAND NOTCH ON DESKTOP */
    .phone-notch-island {
      position: absolute;
      top: 10px;
      left: 50%;
      transform: translateX(-50%);
      width: 110px;
      height: 24px;
      background: #000000;
      border-radius: 999px;
      z-index: 2000;
      display: none;
      align-items: center;
      justify-content: center;
      gap: 6px;
      pointer-events: none;
    }
    .phone-notch-cam {
      width: 9px;
      height: 9px;
      border-radius: 50%;
      background: #111827;
      border: 1px solid #1f2937;
    }

    /* HOME INDICATOR AT BOTTOM OF PHONE FRAME */
    .phone-home-indicator {
      position: absolute;
      bottom: 6px;
      left: 50%;
      transform: translateX(-50%);
      width: 130px;
      height: 4.5px;
      background: #0f172a;
      border-radius: 999px;
      z-index: 2000;
      display: none;
      pointer-events: none;
    }

    /* FULLSCREEN LEAFLET MAP INSIDE PHONE FRAME */
    #mobile-map {
      width: 100%;
      height: 100%;
      position: absolute;
      inset: 0;
      z-index: 1;
      background: #e2e8f0;
    }

    /* FLOATING TOP BAR (SLEEK PILL) */
    .top-floating-bar {
      position: absolute;
      top: 40px;
      left: 14px;
      right: 14px;
      z-index: 1000;
      display: flex;
      flex-direction: column;
      gap: 8px;
      pointer-events: none;
    }

    .top-pills-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
    }

    .top-pill {
      pointer-events: auto;
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(12px);
      border: 1.5px solid var(--border-color);
      border-radius: 999px;
      padding: 7px 12px;
      display: flex;
      align-items: center;
      gap: 6px;
      box-shadow: var(--shadow-floating);
      font-size: 13px;
      font-weight: 700;
      color: var(--text-main);
      cursor: pointer;
      user-select: none;
    }

    .status-badge-pill {
      pointer-events: auto;
      background: var(--brand-green-bg);
      border: 1.5px solid var(--brand-green-border);
      color: var(--brand-green-dark);
      border-radius: 999px;
      padding: 7px 12px;
      font-size: 12px;
      font-weight: 800;
      display: flex;
      align-items: center;
      gap: 6px;
      box-shadow: var(--shadow-floating);
      cursor: pointer;
    }

    /* SEARCH BAR (MELHORIA 1: AUTOCOMPLETE RÁPIDO) */
    .search-pill-wrapper {
      pointer-events: auto;
      position: relative;
      width: 100%;
    }

    .search-pill {
      background: rgba(255, 255, 255, 0.97);
      backdrop-filter: blur(12px);
      border: 1.5px solid var(--border-color);
      border-radius: 14px;
      padding: 8px 14px;
      display: flex;
      align-items: center;
      gap: 8px;
      box-shadow: var(--shadow-floating);
    }

    .search-input {
      border: none;
      background: transparent;
      outline: none;
      font-size: 13.5px;
      font-family: inherit;
      color: var(--text-main);
      width: 100%;
    }

    .search-dropdown {
      position: absolute;
      top: 44px;
      left: 0;
      right: 0;
      background: #ffffff;
      border: 1.5px solid var(--border-color);
      border-radius: 14px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.18);
      max-height: 220px;
      overflow-y: auto;
      display: none;
      z-index: 2000;
      flex-direction: column;
    }

    .search-item {
      padding: 9px 12px;
      border-bottom: 1px solid var(--border-color);
      cursor: pointer;
      font-size: 13px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .search-item:hover {
      background: var(--bg-page);
    }

    .pulse-dot {
      width: 8px;
      height: 8px;
      background: var(--brand-green);
      border-radius: 50%;
      box-shadow: 0 0 0 0 rgba(5, 150, 105, 0.7);
      animation: pulseGreen 2s infinite;
    }

    @keyframes pulseGreen {
      0% { box-shadow: 0 0 0 0 rgba(5, 150, 105, 0.7); }
      70% { box-shadow: 0 0 0 8px rgba(5, 150, 105, 0); }
      100% { box-shadow: 0 0 0 0 rgba(5, 150, 105, 0); }
    }

    /* FLOATING ACTION BUTTON (GPS RECENTER) */
    .fab-gps {
      position: absolute;
      bottom: 240px;
      right: 14px;
      z-index: 999;
      width: 48px;
      height: 48px;
      border-radius: 50%;
      background: var(--bg-surface);
      border: 2px solid var(--border-color);
      box-shadow: var(--shadow-floating);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      color: var(--blue-accent);
      transition: transform 0.15s ease, background 0.2s ease;
    }
    .fab-gps:active {
      transform: scale(0.92);
      background: var(--blue-bg);
    }

    /* BOTTOM SHEET (MOBILE-FIRST RIDE-HAILING CARD) */
    .mobile-bottom-sheet {
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      z-index: 1000;
      background: var(--bg-surface);
      border-radius: 24px 24px 0 0;
      box-shadow: var(--shadow-sheet);
      border-top: 1px solid var(--border-color);
      transition: max-height 0.35s cubic-bezier(0.16, 1, 0.3, 1);
      max-height: 232px;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }

    .mobile-bottom-sheet.expanded {
      max-height: calc(100% - 75px);
    }

    .sheet-handle-zone {
      padding: 10px 0 4px;
      display: flex;
      flex-direction: column;
      align-items: center;
      cursor: pointer;
    }

    .sheet-handle-pill {
      width: 40px;
      height: 4.5px;
      background: #cbd5e1;
      border-radius: 999px;
    }

    .sheet-body {
      padding: 6px 16px 24px;
      overflow-y: auto;
      -webkit-overflow-scrolling: touch;
      flex: 1;
    }

    /* 1-TAP TRAVEL CARDS */
    .travel-cards-row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      margin: 10px 0 10px;
    }

    .travel-card {
      background: var(--bg-page);
      border: 2px solid var(--border-color);
      border-radius: 16px;
      padding: 12px 12px;
      text-align: left;
      cursor: pointer;
      transition: all 0.15s ease;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      min-height: 72px;
    }

    .travel-card:active {
      transform: scale(0.97);
    }

    .travel-card.active-home {
      background: var(--brand-green-bg);
      border-color: var(--brand-green);
    }

    .travel-card.active-work {
      background: var(--blue-bg);
      border-color: var(--blue-accent);
    }

    .travel-card-title {
      font-size: 13px;
      font-weight: 800;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .travel-card-subtitle {
      font-size: 11.5px;
      font-weight: 600;
      color: var(--text-secondary);
      margin-top: 3px;
    }

    /* EMERGENCY HELPER CARD */
    .lost-help-card {
      background: var(--danger-bg);
      border: 1.5px solid var(--danger-border);
      border-radius: 14px;
      padding: 10px 14px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      cursor: pointer;
      margin-bottom: 8px;
    }

    .lost-help-card:active {
      transform: scale(0.98);
    }

    /* ACTIVE ROUTE / BIG NUMBER VIEW */
    .active-trip-view {
      display: none;
    }

    .active-trip-view.visible {
      display: block;
    }

    .hero-eta-box {
      background: var(--bg-page);
      border: 2px solid var(--border-color);
      border-radius: 18px;
      padding: 14px 18px;
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 14px;
    }

    .hero-eta-big {
      font-family: JetBrains Mono, monospace;
      font-size: 42px;
      font-weight: 800;
      line-height: 1;
      color: var(--brand-green-dark);
      letter-spacing: -0.03em;
    }

    .hero-btn-pocket {
      width: 100%;
      min-height: 50px;
      background: var(--brand-green);
      color: #ffffff;
      border: none;
      border-radius: 16px;
      font-size: 14px;
      font-weight: 800;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      cursor: pointer;
      box-shadow: 0 4px 16px rgba(5, 150, 105, 0.35);
      transition: all 0.15s ease;
      margin-bottom: 8px;
    }

    .hero-btn-pocket:active {
      transform: scale(0.98);
      background: var(--brand-green-dark);
    }

    /* BUTTON TO DEMO THE SLIDE 3 FAILURE REAL */
    .btn-demo-failure {
      width: 100%;
      min-height: 38px;
      background: var(--warning-bg);
      color: var(--warning-amber);
      border: 1.5px dashed var(--warning-border);
      border-radius: 12px;
      font-size: 12px;
      font-weight: 800;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      cursor: pointer;
      margin-bottom: 10px;
    }

    /* OLED BLACK SCREEN SHIELD */
    #pocket-shield-screen {
      position: absolute;
      inset: 0;
      z-index: 99999;
      background: #000000;
      color: #ffffff;
      display: none;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      padding: 24px;
      cursor: pointer;
    }

    /* MODAL BASE */
    .modal-overlay {
      position: absolute;
      inset: 0;
      z-index: 10000;
      background: rgba(15, 23, 42, 0.7);
      backdrop-filter: blur(8px);
      display: none;
      align-items: center;
      justify-content: center;
      padding: 16px;
    }

    .modal-card {
      background: var(--bg-surface);
      border-radius: 22px;
      width: 100%;
      max-width: 380px;
      max-height: 90%;
      overflow-y: auto;
      padding: 20px;
      box-shadow: 0 20px 40px rgba(0,0,0,0.25);
      border: 1px solid var(--border-color);
    }

    /* SCHEMATIC TERMINAL DIAGRAM (MELHORIA 2) */
    .terminal-schematic {
      background: #0f172a;
      border-radius: 14px;
      padding: 12px;
      color: #ffffff;
      margin-bottom: 14px;
      border: 1px solid #334155;
    }

    .schematic-bay {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 6px 10px;
      border-radius: 8px;
      margin-bottom: 6px;
      font-size: 11.5px;
      background: #1e293b;
      border: 1px solid #334155;
    }

    .schematic-bay.highlight-bay {
      background: rgba(5, 150, 105, 0.25);
      border: 1.5px solid var(--brand-green);
      color: #34d399;
      font-weight: 800;
    }

    /* FORM ELEMENTS */
    .field-group {
      margin-bottom: 12px;
      text-align: left;
    }

    .field-label {
      display: block;
      font-size: 12.5px;
      font-weight: 700;
      margin-bottom: 5px;
      color: var(--text-main);
    }

    .field-input, .field-select {
      width: 100%;
      min-height: 46px;
      padding: 10px 12px;
      font-size: 14px;
      border: 1.5px solid var(--border-color);
      border-radius: 12px;
      background: var(--bg-surface);
      color: var(--text-main);
      font-family: inherit;
    }

    .field-input:focus, .field-select:focus {
      border-color: var(--brand-green);
      outline: none;
      box-shadow: 0 0 0 3px var(--brand-green-bg);
    }

    .btn-primary {
      width: 100%;
      min-height: 48px;
      background: var(--brand-green);
      color: #ffffff;
      border: none;
      border-radius: 14px;
      font-size: 15px;
      font-weight: 800;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      box-shadow: 0 4px 16px rgba(5, 150, 105, 0.3);
    }

    .btn-secondary {
      width: 100%;
      min-height: 42px;
      background: transparent;
      color: var(--text-secondary);
      border: 1.5px solid var(--border-color);
      border-radius: 14px;
      font-size: 13.5px;
      font-weight: 700;
      cursor: pointer;
      margin-top: 8px;
    }

    /* STOP NODE ON MAP */
    .stop-marker-pill {
      background: var(--brand-green);
      color: #ffffff;
      font-family: JetBrains Mono, monospace;
      font-size: 11px;
      font-weight: 800;
      padding: 3px 6px;
      border-radius: 999px;
      border: 2px solid #ffffff;
      box-shadow: 0 2px 8px rgba(0,0,0,0.3);
      white-space: nowrap;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .stop-marker-pill.selected {
      background: var(--danger-red);
      transform: scale(1.15);
    }

    /* MOVING BUS MARKER */
    .bus-marker-pulse {
      background: #0284c7;
      color: #ffffff;
      border: 2px solid #ffffff;
      border-radius: 999px;
      padding: 4px 8px;
      font-size: 11px;
      font-weight: 800;
      box-shadow: 0 4px 12px rgba(2, 132, 199, 0.45);
      display: flex;
      align-items: center;
      gap: 4px;
      white-space: nowrap;
    }
  </style>
</head>
<body>

  <!-- DESKTOP TOP BAR (OUTSIDE SMARTPHONE FRAME) -->
  <div class="desktop-outer-bar">
    <div class="badge-title">
      <span>📱</span>
      <span>Simulador Mobile · GrafoParada Grande Recife</span>
      <span style="font-size:11px; background:rgba(5,150,105,0.25); color:#34d399; padding:2px 8px; border-radius:999px; border:1px solid rgba(5,150,105,0.4);">Seminário 2 Live</span>
    </div>
    <div style="display:flex; gap:8px;">
      <button class="btn-desktop-action" onclick="logoutAndRestart()">
        <span>🔄</span> Testar do Zero
      </button>
      <button class="btn-desktop-action" onclick="toggleFullscreenDesktop()">
        <span>⛶</span> Alternar Tela
      </button>
    </div>
  </div>

  <!-- SMARTPHONE SHELL FRAME -->
  <div class="phone-simulator-frame">
    <!-- HARDWARE NOTCH ISLAND -->
    <div class="phone-notch-island">
      <div class="phone-notch-cam"></div>
    </div>

    <!-- 1. FULLSCREEN LEAFLET MAP -->
    <div id="mobile-map"></div>

    <!-- 2. MINIMALIST FLOATING TOP BAR -->
    <div class="top-floating-bar">
      <div class="top-pills-row">
        <div class="top-pill" onclick="openProfileModal()">
          <span style="font-size:15px;">👤</span>
          <span id="top-user-name">Cauã</span>
        </div>

        <div class="status-badge-pill" id="top-line-badge" onclick="switchLineQuick()">
          <div class="pulse-dot"></div>
          <span id="top-line-label">199 · Camela / Cabo</span>
        </div>
      </div>

      <!-- SEARCH BAR AUTOCOMPLETE (MELHORIA 1) -->
      <div class="search-pill-wrapper">
        <div class="search-pill">
          <span style="font-size:14px; color:var(--text-muted);">🔍</span>
          <input type="text" id="quick-search-input" class="search-input" placeholder="Buscar linha (ex: 199, 178) ou Terminal..." oninput="handleQuickSearch(this.value)" onfocus="handleQuickSearch(this.value)" />
          <button id="search-clear-btn" onclick="clearQuickSearch()" style="display:none; border:none; background:none; color:var(--text-muted); cursor:pointer;">✕</button>
        </div>
        <div id="search-results-dropdown" class="search-dropdown"></div>
      </div>
    </div>

    <!-- 3. FLOATING ACTION BUTTON (GPS RECENTER) -->
    <button class="fab-gps" onclick="recenterGpsTarget()" title="Localizar meu GPS">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="9"></circle>
        <line x1="12" y1="1" x2="12" y2="4"></line>
        <line x1="12" y1="20" x2="12" y2="23"></line>
        <line x1="1" y1="12" x2="4" y2="12"></line>
        <line x1="20" y1="12" x2="23" y2="12"></line>
        <circle cx="12" cy="12" r="3" fill="currentColor"></circle>
      </svg>
    </button>

    <!-- 4. BOTTOM SHEET (RIDE-HAILING / TRANSIT EXPERIENCE) -->
    <div class="mobile-bottom-sheet" id="main-bottom-sheet">
      <div class="sheet-handle-zone" onclick="toggleSheetExpansion()">
        <div class="sheet-handle-pill"></div>
      </div>

      <div class="sheet-body">
        <!-- STATE A: DEFAULT / QUICK CHOICE VIEW -->
        <div id="view-sheet-resting">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
            <div style="display:flex; align-items:center; gap:6px;">
              <span style="font-size:11.5px; font-weight:700; color:var(--text-muted); text-transform:uppercase;">📍 Sua Parada Atual</span>
              <button id="btn-fav-star" onclick="toggleFavoriteCurrentStop()" style="border:none; background:none; cursor:pointer; font-size:14px;" title="Favoritar parada">⭐</button>
            </div>
            <button style="border:none; background:none; color:var(--blue-accent); font-weight:700; font-size:12px; cursor:pointer;" onclick="toggleSheetExpansion()">Ver Paradas ▲</button>
          </div>
          <div style="font-size:15.5px; font-weight:800; margin-bottom:10px; color:var(--text-main);" id="current-stop-name">
            Parada 030613 · Terminal de Camela
          </div>

          <!-- 2 GIANT 1-TAP CARDS -->
          <div class="travel-cards-row">
            <button class="travel-card active-home" onclick="triggerTripAction('home')">
              <div class="travel-card-title"><span>🏠</span> Vou pra Casa</div>
              <div class="travel-card-subtitle" id="home-card-sub">Camela · 4 min</div>
            </button>

            <button class="travel-card active-work" onclick="triggerTripAction('work')">
              <div class="travel-card-title"><span>💼</span> Vou pro Destino</div>
              <div class="travel-card-subtitle" id="work-card-sub">TI Cabo · 32 min</div>
            </button>
          </div>

          <!-- LOST PERSON ASSISTANCE BUTTON -->
          <div class="lost-help-card" onclick="openLostHelpModal()">
            <div style="display:flex; align-items:center; gap:8px;">
              <span style="font-size:20px;">🧭</span>
              <div>
                <div style="font-size:12.5px; font-weight:800; color:var(--danger-red);">Primeira vez aqui ou perdido?</div>
                <div style="font-size:11px; color:var(--text-secondary);">Guia anti-pânico de plataforma e segurança</div>
              </div>
            </div>
            <span style="font-size:14px; font-weight:800; color:var(--danger-red);">➔</span>
          </div>
        </div>

        <!-- STATE B: ACTIVE ROUTE / BUS WAITING VIEW -->
        <div id="view-sheet-active" class="active-trip-view">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <div style="font-size:13px; font-weight:800; color:var(--brand-green-dark);" id="active-trip-header">
              🚌 Linha 199 · Camela / TI Cabo
            </div>
            <button style="border:none; background:none; color:var(--text-muted); font-size:12.5px; font-weight:700; cursor:pointer;" onclick="closeActiveTripView()">✕ Voltar</button>
          </div>

          <!-- HERO ETA CARD -->
          <div class="hero-eta-box">
            <div>
              <div style="font-size:11.5px; font-weight:700; color:var(--text-secondary); text-transform:uppercase;">Primeiro Ônibus</div>
              <div class="hero-eta-big"><span id="live-eta-num">4</span> <span style="font-size:20px; font-weight:700;">min</span></div>
              <div style="font-size:11.5px; font-weight:700; color:var(--text-secondary); margin-top:2px;" id="live-eta-sub">Encosta às 06:14 · Plataforma 04</div>
            </div>
            <div style="text-align:right;">
              <div style="font-size:11.5px; font-weight:700; color:var(--text-secondary); text-transform:uppercase;">Viagem Total</div>
              <div style="font-size:23px; font-weight:800; color:var(--text-main);" id="live-total-trip">38 min</div>
              <span style="font-size:10.5px; font-weight:700; background:var(--brand-green-bg); color:var(--brand-green-dark); padding:2px 8px; border-radius:999px;">Assento Livre</span>
            </div>
          </div>

          <!-- TRUST BADGES -->
          <div style="display:flex; flex-direction:column; gap:6px; margin-bottom:10px;">
            <div id="badge-gps-status" style="font-size:11.5px; background:var(--brand-green-bg); color:var(--brand-green-dark); padding:6px 10px; border-radius:10px; font-weight:700; display:flex; align-items:center; gap:6px;">
              <span>🛰️</span> GPS Satélite Ativo · 42 km/h na PE-60 (Zero Ônibus Fantasma)
            </div>
            <div style="font-size:11.5px; background:var(--blue-bg); color:var(--blue-accent); padding:6px 10px; border-radius:10px; font-weight:700; display:flex; align-items:center; gap:6px;">
              <span>💺</span> 14 assentos livres · Embarque Sentado Garantido
            </div>
          </div>

          <!-- BUTTON TO SIMULATE THE SLIDE 3 FAILURE REAL -->
          <button class="btn-demo-failure" onclick="simulateSlide3Failure()">
            <span>🧪</span> Simular Interdição PE-60 (Demonstração da Falha · Sem2)
          </button>

          <!-- HERO ACTION: POCKET MODE AUDIO -->
          <button class="hero-btn-pocket" onclick="activatePocketShield()">
            <span>🎧</span> ATIVAR MODO CELULAR NO BOLSO
          </button>
        </div>

        <!-- STOPS LIST ACCORDION (VISIBLE WHEN EXPANDED) -->
        <div id="sheet-stops-list" style="margin-top:14px; border-top:1px solid var(--border-color); padding-top:14px;">
          <div style="font-size:12.5px; font-weight:800; margin-bottom:10px; color:var(--text-secondary); text-transform:uppercase;">
            Paradas Físicas do Trajeto (<span id="stops-count-label">43</span>):
          </div>
          <div id="stops-container" style="display:flex; flex-direction:column; gap:8px;"></div>
        </div>
      </div>
    </div>

    <!-- 5. OLED BLACK SCREEN POCKET SHIELD (ANTI-THEFT) -->
    <div id="pocket-shield-screen" onclick="deactivatePocketShield()">
      <div style="font-size:48px; margin-bottom:14px;">🛡️</div>
      <h2 style="font-size:21px; font-weight:800; margin-bottom:8px;">Modo Seguro Ativo</h2>
      <p style="font-size:13.5px; color:#94a3b8; max-width:260px; line-height:1.45; margin-bottom:24px;">
        Celular no bolso com a tela escura. Avisaremos pelo fone quando seu ônibus estiver chegando.
      </p>
      <div style="font-size:11.5px; color:#64748b; border:1px solid #334155; padding:8px 16px; border-radius:999px;">
        Toque na tela para voltar
      </div>
    </div>

    <!-- 6. MODAL: "ESTOU PERDIDO / PRIMEIRA VEZ AQUI" COM MAPA ESQUEMÁTICO DO T.I. -->
    <div id="modal-lost" class="modal-overlay">
      <div class="modal-card" style="border:2px solid var(--brand-green);">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
          <div style="display:flex; align-items:center; gap:8px;">
            <span style="font-size:26px;">🧭</span>
            <div>
              <h3 style="font-size:17px; font-weight:800; color:var(--brand-green-dark); margin:0;">Você está seguro</h3>
              <span style="font-size:11.5px; color:var(--text-secondary);">Guia anti-pânico com mapa de plataformas</span>
            </div>
          </div>
          <button style="border:none; background:none; font-size:20px; font-weight:800; color:var(--text-muted); cursor:pointer;" onclick="closeLostModal()">✕</button>
        </div>

        <!-- ESQUEMA VISUAL DO TERMINAL INTEGRADO DO CABO (MELHORIA 2) -->
        <div class="terminal-schematic">
          <div style="display:flex; justify-content:space-between; font-size:11px; font-weight:800; color:#94a3b8; margin-bottom:8px; text-transform:uppercase;">
            <span>🏛️ Terminal Integrado do Cabo</span>
            <span>Área Interna</span>
          </div>

          <div class="schematic-bay">
            <span>Plat. 01 / 02 · Linhas de Bairro (Centro)</span>
            <span style="color:#94a3b8;">Baia A</span>
          </div>
          <div class="schematic-bay">
            <span>Plat. 03 · Linha 178 (Porto de Suape)</span>
            <span style="color:#94a3b8;">Baia B</span>
          </div>
          <div class="schematic-bay highlight-bay">
            <span>📍 Plat. 04 · LINHA 199 (CAMELA / SJT)</span>
            <span>SEU EMBARQUE</span>
          </div>
          <div class="schematic-bay">
            <span>Plat. 05 / 06 · Troncais Recife / Conexão Metrô</span>
            <span style="color:#94a3b8;">Baia C</span>
          </div>

          <div style="display:flex; justify-content:space-between; margin-top:8px; font-size:10.5px; color:#cbd5e1; border-top:1px dashed #334155; padding-top:6px;">
            <span>👮 Cabine Fiscal CTM: 15m à frente</span>
            <span>💡 Iluminação 100%</span>
          </div>
        </div>

        <div style="display:flex; flex-direction:column; gap:8px; margin-bottom:14px;">
          <div style="background:var(--bg-page); border:1px solid var(--border-color); border-radius:12px; padding:10px;">
            <div style="font-size:11px; font-weight:800; color:var(--brand-green); text-transform:uppercase;">🚶 Instrução de Caminhada:</div>
            <div style="font-size:13px; font-weight:800; margin-top:2px;">Caminhe 20 passos até a Plataforma 04 (Lado Sul).</div>
            <div style="font-size:11px; color:var(--text-secondary); margin-top:2px;">Ônibus azul da São Judas Tadeu (SJT). Embarque coberto e seguro.</div>
          </div>

          <div style="background:var(--bg-page); border:1px solid var(--border-color); border-radius:12px; padding:10px;">
            <div style="font-size:11px; font-weight:800; color:var(--blue-accent); text-transform:uppercase;">🚌 Horário Previsto:</div>
            <div style="font-size:13px; font-weight:800; margin-top:2px;">Chega em 4 minutos (às 06:14)</div>
            <div style="font-size:11px; color:var(--text-secondary); margin-top:2px;">14 assentos livres. Fique perto da fila organizada.</div>
          </div>
        </div>

        <button class="btn-primary" onclick="playLostVoiceAudio()" style="margin-bottom:8px;">
          <span>🎧</span> Ouvir Instruções Calmas no Fone
        </button>

        <button class="btn-secondary" onclick="closeLostModal()">
          👍 Entendido, já estou na plataforma
        </button>
      </div>
    </div>

    <!-- 7. MODAL: PROFILE & LOGOUT -->
    <div id="modal-profile" class="modal-overlay">
      <div class="modal-card">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
          <h3 style="font-size:17px; font-weight:800;">👤 Minha Conta</h3>
          <button style="border:none; background:none; font-size:20px; font-weight:800; color:var(--text-muted); cursor:pointer;" onclick="closeProfileModal()">✕</button>
        </div>

        <div style="background:var(--bg-page); border-radius:14px; padding:12px; margin-bottom:14px; font-size:13px; line-height:1.6;">
          <div><strong>Nome:</strong> <span id="prof-name">Cauã Cunha</span></div>
          <div><strong>CPF:</strong> <span id="prof-cpf">084.721.904-12</span></div>
          <div><strong>Celular:</strong> <span id="prof-phone">(81) 98888-7766</span></div>
          <div><strong>Casa:</strong> <span id="prof-home">Camela (Rua do Comércio)</span></div>
          <div><strong>Destino:</strong> <span id="prof-work">TI Cabo</span></div>
          <div><strong>Linha:</strong> <span id="prof-line">199 · Camela / TI Cabo</span></div>
        </div>

        <button class="btn-primary" onclick="testNeuralVoice()" style="margin-bottom:8px;">
          <span>🔊</span> Testar Voz Humana no Fone
        </button>

        <button class="btn-secondary" style="color:var(--danger-red); border-color:var(--danger-border);" onclick="logoutAndRestart()">
          🚪 Sair da Conta / Reiniciar Teste do Zero
        </button>
      </div>
    </div>

    <!-- 8. ONBOARDING & CADASTRO MODAL -->
    <div id="modal-onboarding" class="modal-overlay" style="background:#0f172a; z-index:99999;">
      <!-- STEP 1: SPLASH SCREEN -->
      <div id="onboarding-step-splash" class="modal-card" style="max-width:360px; padding:24px; text-align:center;">
        <div style="font-size:42px; margin-bottom:10px;">🚌</div>
        <h2 style="font-size:22px; font-weight:800; margin-bottom:4px; letter-spacing:-0.02em;">GrafoParada</h2>
        <div style="font-size:12px; font-weight:700; color:var(--brand-green); margin-bottom:14px;">Grande Recife · Inteligência Artificial CTM</div>

        <p style="font-size:13px; color:var(--text-secondary); line-height:1.5; margin-bottom:18px;">
          Chega de esperar ônibus fantasma. Previsão real de chegada, assento livre garantido e proteção no bolso.
        </p>

        <div style="display:flex; flex-direction:column; gap:8px; text-align:left; margin-bottom:20px; font-size:12px;">
          <div style="background:var(--bg-page); padding:8px 12px; border-radius:10px; display:flex; gap:8px; align-items:center;">
            <span>🛰️</span> <strong>Zero Ônibus Fantasma:</strong> Telemetria e ST-GCN real.
          </div>
          <div style="background:var(--bg-page); padding:8px 12px; border-radius:10px; display:flex; gap:8px; align-items:center;">
            <span>💺</span> <strong>Sentado Garantido:</strong> Lotação antes de embarcar.
          </div>
          <div style="background:var(--bg-page); padding:8px 12px; border-radius:10px; display:flex; gap:8px; align-items:center;">
            <span>🛡️</span> <strong>Modo Bolso:</strong> Não tire o celular na parada.
          </div>
        </div>

        <button class="btn-primary" onclick="showOnboardingRegistration()" style="margin-bottom:8px;">
          🚀 Criar Minha Conta (Primeiro Acesso)
        </button>

        <button class="btn-secondary" onclick="enterAsQuickGuest()">
          ⚡ Entrar Rápido (Demonstração Cauã)
        </button>
      </div>

      <!-- STEP 2: CADASTRO COMPLETO DO PASSAGEIRO -->
      <div id="onboarding-step-form" class="modal-card" style="max-width:370px; padding:20px; display:none;">
        <div style="display:flex; align-items:center; gap:8px; margin-bottom:12px;">
          <button style="border:none; background:none; font-size:18px; cursor:pointer;" onclick="showOnboardingSplash()">←</button>
          <h3 style="font-size:17px; font-weight:800;">Cadastro do Passageiro</h3>
        </div>

        <form onsubmit="handleOnboardingSubmit(event)">
          <div class="field-group">
            <label class="field-label">Nome Completo:</label>
            <input type="text" id="inp-name" class="field-input" placeholder="Seu nome" value="Cauã Cunha" required />
          </div>

          <div class="field-group">
            <label class="field-label">CPF (Validação CTM / VEM):</label>
            <input type="tel" inputmode="numeric" id="inp-cpf" class="field-input" maxlength="14" oninput="formatCpf(this)" value="084.721.904-12" required />
          </div>

          <div class="field-group">
            <label class="field-label">🏠 Onde você mora (Casa / Partida Habitual):</label>
            <select id="inp-home" class="field-select">
__HOME_OPTIONS__
            </select>
          </div>

          <div class="field-group">
            <label class="field-label">💼 Destino Habitual (Trabalho / Estudo):</label>
            <select id="inp-work" class="field-select">
__WORK_OPTIONS__
            </select>
          </div>

          <div class="field-group">
            <label class="field-label">🚌 Linha Habitual de Ônibus:</label>
            <select id="inp-line" class="field-select">
__ROUTE_OPTIONS__
            </select>
          </div>

          <button type="submit" class="btn-primary" style="margin-top:10px;">
            Finalizar Cadastro e Entrar no App ➔
          </button>
        </form>
      </div>
    </div>

    <!-- HOME INDICATOR -->
    <div class="phone-home-indicator"></div>
  </div>

  <script>
    // DATASETS
    const TELEMETRIA_199 = __TELEMETRIA_199__;
    const TELEMETRIA_178 = __TELEMETRIA_178__;
    const SEI_TERMINALS = __SEI_TERMINALS__;

    let activeRouteCode = "199";
    let TELEMETRIA = TELEMETRIA_199;
    let activeStopSeq = 1;

    let leafletMap = null;
    let routePolylineLayer = null;
    let stopsMarkersLayer = null;
    let busMarker = null;
    let userMarker = null;
    let currentAudioPlayer = null;
    let busAnimIndex = 0;
    let isSlide3FailureActive = false;

    // INIT APP ON LOAD
    window.addEventListener("DOMContentLoaded", function() {
      initMap();
      checkAuthStatus();
      startBusAnimation();
    });

    function checkAuthStatus() {
      const isLogged = localStorage.getItem("grafoparada_logged");
      if (isLogged === "true") {
        loadUserData();
        document.getElementById("modal-onboarding").style.display = "none";
      } else {
        document.getElementById("modal-onboarding").style.display = "flex";
        showOnboardingSplash();
      }
    }

    function showOnboardingSplash() {
      document.getElementById("onboarding-step-splash").style.display = "block";
      document.getElementById("onboarding-step-form").style.display = "none";
    }

    function showOnboardingRegistration() {
      document.getElementById("onboarding-step-splash").style.display = "none";
      document.getElementById("onboarding-step-form").style.display = "block";
    }

    function initMap() {
      try {
        leafletMap = L.map("mobile-map", {
          center: [-8.514931, -35.123469],
          zoom: 14,
          zoomControl: false,
          attributionControl: false
        });

        // Universal OpenStreetMap tiles
        L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
          maxZoom: 19
        }).addTo(leafletMap);

        routePolylineLayer = L.layerGroup().addTo(leafletMap);
        stopsMarkersLayer = L.layerGroup().addTo(leafletMap);

        drawRoute(TELEMETRIA);
        selectStop(1, false);

        setTimeout(function() { if (leafletMap) leafletMap.invalidateSize(); }, 150);
        setTimeout(function() { if (leafletMap) leafletMap.invalidateSize(); }, 500);
      } catch (err) {
        console.error("Leaflet map init error:", err);
      }
    }

    function drawRoute(telemetria) {
      if (!leafletMap) return;
      routePolylineLayer.clearLayers();
      stopsMarkersLayer.clearLayers();

      if (telemetria.polyline && telemetria.polyline.length > 1) {
        L.polyline(telemetria.polyline, { color: "#0284c7", weight: 8, opacity: 0.25 }).addTo(routePolylineLayer);
        L.polyline(telemetria.polyline, { color: "#0284c7", weight: 4.5, opacity: 0.95 }).addTo(routePolylineLayer);
      }

      telemetria.stops.forEach(function(st) {
        const isSel = st.seq === activeStopSeq;
        const icon = L.divIcon({
          className: "",
          html: '<div class="stop-marker-pill ' + (isSel ? 'selected' : '') + '">#' + String(st.seq).padStart(2, '0') + '</div>',
          iconSize: [32, 22],
          iconAnchor: [16, 11]
        });

        const m = L.marker([st.lat, st.lon], { icon: icon });
        m.on("click", function() { selectStop(st.seq, true); });
        stopsMarkersLayer.addLayer(m);
      });

      renderStopsAccordion(telemetria);
    }

    function selectStop(seq, pan) {
      activeStopSeq = seq;
      const st = TELEMETRIA.stops.find(function(s) { return s.seq === seq; }) || TELEMETRIA.stops[0];

      // Update current stop name
      const nameEl = document.getElementById("current-stop-name");
      if (nameEl) nameEl.textContent = "Parada #" + String(st.seq).padStart(2, '0') + " · " + st.name;

      // Update ETA
      const etaNum = document.getElementById("live-eta-num");
      const etaVal = st.stgcn_horizon_min[1].toFixed(0);
      if (etaNum) etaNum.textContent = etaVal;

      // Trigger Haptic and audio if <= 2 min
      if (parseInt(etaVal) <= 2) {
        triggerArrivalAlert();
      }

      if (pan && leafletMap) {
        leafletMap.panTo([st.lat, st.lon], { animate: true, duration: 0.4 });
      }
    }

    function renderStopsAccordion(telemetria) {
      const container = document.getElementById("stops-container");
      const labelCount = document.getElementById("stops-count-label");
      if (labelCount) labelCount.textContent = telemetria.stops.length;
      if (!container) return;

      let html = "";
      telemetria.stops.forEach(function(st) {
        html += '<div style="background:var(--bg-page); border:1px solid var(--border-color); border-radius:12px; padding:10px 12px; display:flex; justify-content:space-between; align-items:center; cursor:pointer;" onclick="selectStop(' + st.seq + ', true)">' +
          '<div>' +
            '<div style="font-size:13px; font-weight:800;">#' + String(st.seq).padStart(2, '0') + ' · ' + st.name + '</div>' +
            '<div style="font-size:11.5px; color:var(--text-secondary); margin-top:2px;">' + (st.crowd_status || 'Sentado Garantido') + '</div>' +
          '</div>' +
          '<div style="font-family:JetBrains Mono,monospace; font-size:15px; font-weight:800; color:var(--brand-green-dark);">' + st.stgcn_horizon_min[1].toFixed(0) + ' min</div>' +
        '</div>';
      });
      container.innerHTML = html;
    }

    // SIMULATED MOVING REAL-TIME BUS
    function startBusAnimation() {
      if (!TELEMETRIA || !TELEMETRIA.polyline || TELEMETRIA.polyline.length === 0) return;
      setInterval(function() {
        if (!leafletMap) return;
        busAnimIndex = (busAnimIndex + 2) % TELEMETRIA.polyline.length;
        const pt = TELEMETRIA.polyline[busAnimIndex];
        if (!pt) return;

        const busHtml = '<div class="bus-marker-pulse">🚌 199 · 42 km/h</div>';
        const busIcon = L.divIcon({
          className: "",
          html: busHtml,
          iconSize: [110, 26],
          iconAnchor: [55, 13]
        });

        if (!busMarker) {
          busMarker = L.marker([pt[0], pt[1]], { icon: busIcon, zIndexOffset: 1000 }).addTo(leafletMap);
        } else {
          busMarker.setLatLng([pt[0], pt[1]]);
        }
      }, 3000);
    }

    // SEARCH AUTOCOMPLETE LOGIC (MELHORIA 1)
    function handleQuickSearch(query) {
      const q = (query || "").trim().toLowerCase();
      const drop = document.getElementById("search-results-dropdown");
      const clearBtn = document.getElementById("search-clear-btn");

      if (!q) {
        drop.style.display = "none";
        clearBtn.style.display = "none";
        return;
      }

      clearBtn.style.display = "block";
      const results = [];

      // 1. Check terminals
      SEI_TERMINALS.forEach(function(t) {
        if (t.ti_name.toLowerCase().includes(q) || t.municipio.toLowerCase().includes(q)) {
          results.push({ type: "terminal", title: t.ti_name, sub: t.municipio, lat: t.lat, lon: t.lon });
        }
      });

      // 2. Check lines
      if (q.includes("199") || "camela".includes(q) || "cabo".includes(q)) {
        results.push({ type: "route", title: "Linha 199", sub: "Camela / TI Cabo (via PE-60)", code: "199" });
      }
      if (q.includes("178") || "suape".includes(q)) {
        results.push({ type: "route", title: "Linha 178", sub: "Porto de Suape / TI Cabo", code: "178" });
      }
      if (q.includes("191") || "galinhas".includes(q)) {
        results.push({ type: "route", title: "Linha 191", sub: "Recife / Porto de Galinhas", code: "191" });
      }

      if (results.length === 0) {
        drop.innerHTML = '<div style="padding:10px; font-size:12px; color:var(--text-muted); text-align:center;">Nenhum terminal ou linha prioritária encontrado.</div>';
        drop.style.display = "flex";
        return;
      }

      let html = "";
      results.slice(0, 6).forEach(function(r) {
        if (r.type === "terminal") {
          html += '<div class="search-item" onclick="selectSearchedTerminal(' + r.lat + ', ' + r.lon + ', \\'' + r.title + '\\')">' +
            '<div><strong>🏛️ ' + r.title + '</strong><div style="font-size:11px; color:var(--text-muted);">' + r.sub + '</div></div>' +
            '<span style="font-size:12px; color:var(--blue-accent);">Ver ➔</span>' +
          '</div>';
        } else {
          html += '<div class="search-item" onclick="selectSearchedRoute(\\'' + r.code + '\\')">' +
            '<div><strong>🚌 ' + r.title + '</strong><div style="font-size:11px; color:var(--text-muted);">' + r.sub + '</div></div>' +
            '<span style="font-size:12px; color:var(--brand-green);">Ativar ➔</span>' +
          '</div>';
        }
      });

      drop.innerHTML = html;
      drop.style.display = "flex";
    }

    function clearQuickSearch() {
      const inp = document.getElementById("quick-search-input");
      if (inp) inp.value = "";
      document.getElementById("search-results-dropdown").style.display = "none";
      document.getElementById("search-clear-btn").style.display = "none";
    }

    function selectSearchedTerminal(lat, lon, title) {
      clearQuickSearch();
      if (leafletMap) {
        leafletMap.flyTo([lat, lon], 16, { animate: true });
        L.popup().setLatLng([lat, lon]).setContent("<strong>🏛️ " + title + "</strong><br>Terminal Integrado do SEI").openOn(leafletMap);
      }
    }

    function selectSearchedRoute(code) {
      clearQuickSearch();
      if (code === "178") {
        activeRouteCode = "178";
        TELEMETRIA = TELEMETRIA_178;
        document.getElementById("top-line-label").textContent = "178 · Suape / Cabo";
        drawRoute(TELEMETRIA);
        selectStop(1, true);
        playNaturalVoice("Linha 178 Suape ativada.");
      } else {
        activeRouteCode = "199";
        TELEMETRIA = TELEMETRIA_199;
        document.getElementById("top-line-label").textContent = "199 · Camela / Cabo";
        drawRoute(TELEMETRIA);
        selectStop(1, true);
        playNaturalVoice("Linha 199 Camela Cabo ativada.");
      }
    }

    // FAVORITES (MELHORIA 2)
    function toggleFavoriteCurrentStop() {
      const btn = document.getElementById("btn-fav-star");
      const isFav = localStorage.getItem("grafoparada_fav_stop") === String(activeStopSeq);
      if (isFav) {
        localStorage.removeItem("grafoparada_fav_stop");
        btn.textContent = "☆";
        playNaturalVoice("Parada removida dos favoritos.");
      } else {
        localStorage.setItem("grafoparada_fav_stop", String(activeStopSeq));
        btn.textContent = "⭐";
        playNaturalVoice("Parada salva como favorita.");
      }
    }

    // HAPTIC & ARRIVAL CHIME (MELHORIA 1)
    function triggerArrivalAlert() {
      if ("vibrate" in navigator) {
        try { navigator.vibrate([200, 100, 200, 100, 400]); } catch(e){}
      }
      playSimpleChime();
    }

    function playSimpleChime() {
      try {
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.frequency.setValueAtTime(587.33, ctx.currentTime); // D5
        osc.frequency.setValueAtTime(880.00, ctx.currentTime + 0.15); // A5
        gain.gain.setValueAtTime(0.2, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.5);
        osc.start();
        osc.stop(ctx.currentTime + 0.5);
      } catch(e){}
    }

    // SIMULATE SLIDE 3 FAILURE REAL (DEMO DO SEMINÁRIO 2)
    function simulateSlide3Failure() {
      isSlide3FailureActive = !isSlide3FailureActive;
      const etaNum = document.getElementById("live-eta-num");
      const badgeGps = document.getElementById("badge-gps-status");

      if (isSlide3FailureActive) {
        etaNum.innerHTML = '<span style="color:var(--danger-red);">18*</span>';
        badgeGps.style.background = "var(--warning-bg)";
        badgeGps.style.color = "var(--warning-amber)";
        badgeGps.innerHTML = '<span>⚠️</span> <strong>ALERTA DE FALHA (Slide 3):</strong> STGCN suavizou para 18 min · GPS Bruto = 45 min (Bloqueio Trevo Ipojuca)';

        playNaturalVoice("Atenção: Demonstração da falha do Seminário 2 ativa. A rede neural STGCN suavizou o atraso para 18 minutos devido à difusão espacial, mas o GPS bruto detectou bloqueio na PE-60 com 45 minutos. O GrafoParada alerta a divergência na tela para proteger o passageiro.");
      } else {
        etaNum.textContent = "4";
        badgeGps.style.background = "var(--brand-green-bg)";
        badgeGps.style.color = "var(--brand-green-dark)";
        badgeGps.innerHTML = '<span>🛰️</span> GPS Satélite Ativo · 42 km/h na PE-60 (Zero Ônibus Fantasma)';
        playNaturalVoice("Simulação finalizada. Retornando ao fluxo padrão da Linha 199.");
      }
    }

    // TRIP ACTIONS (1-TAP)
    function triggerTripAction(target) {
      const isHome = target === "home";
      const u = getUserData();

      if (activeRouteCode !== "199") {
        activeRouteCode = "199";
        TELEMETRIA = TELEMETRIA_199;
        drawRoute(TELEMETRIA);
      }

      document.getElementById("view-sheet-resting").style.display = "none";
      const activeView = document.getElementById("view-sheet-active");
      activeView.classList.add("visible");

      const sheet = document.getElementById("main-bottom-sheet");
      sheet.style.maxHeight = "360px";

      const headerEl = document.getElementById("active-trip-header");
      if (headerEl) headerEl.textContent = isHome ? "🏠 Rota para Casa · Camela" : "💼 Rota para Destino · TI Cabo";

      const totalEl = document.getElementById("live-total-trip");
      if (totalEl) totalEl.textContent = isHome ? "38 min" : "32 min";

      const etaSub = document.getElementById("live-eta-sub");
      if (etaSub) etaSub.textContent = isHome ? "Encosta às 06:14 · Plataforma 04" : "Encosta às 06:14 · Terminal Camela";

      const voiceMsg = isHome
        ? "Traçando rota para sua Casa em Camela. Primeiro ônibus da Linha 199 chegando em 4 minutos na Plataforma 04. Viagem estimada em 38 minutos com assento garantido."
        : "Traçando rota para seu destino no TI Cabo. Primeiro ônibus da Linha 199 passando em 4 minutos. Tempo previsto de 32 minutos.";

      playNaturalVoice(voiceMsg);

      if (leafletMap && TELEMETRIA.polyline) {
        leafletMap.fitBounds(TELEMETRIA.polyline, { padding: [40, 40] });
      }
    }

    function closeActiveTripView() {
      document.getElementById("view-sheet-active").classList.remove("visible");
      document.getElementById("view-sheet-resting").style.display = "block";
      const sheet = document.getElementById("main-bottom-sheet");
      sheet.style.maxHeight = "232px";
    }

    function toggleSheetExpansion() {
      const sheet = document.getElementById("main-bottom-sheet");
      sheet.classList.toggle("expanded");
    }

    // POCKET SHIELD
    function activatePocketShield() {
      document.getElementById("pocket-shield-screen").style.display = "flex";
      playNaturalVoice("GrafoParada ativo no bolso. Celular seguro. Avisaremos você no fone quando o ônibus encostar.");
    }

    function deactivatePocketShield() {
      document.getElementById("pocket-shield-screen").style.display = "none";
    }

    // MODALS
    function openLostHelpModal() {
      document.getElementById("modal-lost").style.display = "flex";
      playLostVoiceAudio();
    }

    function closeLostModal() {
      document.getElementById("modal-lost").style.display = "none";
    }

    function playLostVoiceAudio() {
      const u = getUserData();
      const name = (u.name || "passageiro").split(" ")[0];
      const msg = "Fique calmo, " + name + "! Deixe o celular guardado no bolso. Você está no Terminal Integrado do Cabo, dentro da área iluminada. Para ir para casa em Camela, basta caminhar até a Plataforma 04 e aguardar a Linha 199. O primeiro ônibus chega em 4 minutos com 14 assentos livres. Fique perto dos outros passageiros. Eu te aviso no fone assim que o ônibus encostar.";
      playNaturalVoice(msg);
    }

    function openProfileModal() {
      const u = getUserData();
      document.getElementById("prof-name").textContent = u.name || "Cauã Cunha";
      document.getElementById("prof-cpf").textContent = u.cpf || "084.721.904-12";
      document.getElementById("prof-phone").textContent = u.phone || "(81) 98888-7766";
      document.getElementById("prof-home").textContent = (u.home || "Camela").split("·")[0];
      document.getElementById("prof-work").textContent = (u.work || "TI Cabo").split("·")[0];
      document.getElementById("prof-line").textContent = u.line || "199 · Camela / TI Cabo";
      document.getElementById("modal-profile").style.display = "flex";
    }

    function closeProfileModal() {
      document.getElementById("modal-profile").style.display = "none";
    }

    function testNeuralVoice() {
      playNaturalVoice("Olá, Cauã! A voz neural do GrafoParada está funcionando perfeitamente em português do Brasil.");
    }

    // ONBOARDING & STORAGE
    function formatCpf(input) {
      let v = input.value.replace(/[^0-9]/g, "");
      if (v.length > 11) v = v.substring(0, 11);
      if (v.length > 9) {
        v = v.replace(/^([0-9]{3})([0-9]{3})([0-9]{3})([0-9]{1,2})$/, "$1.$2.$3-$4");
      } else if (v.length > 6) {
        v = v.replace(/^([0-9]{3})([0-9]{3})([0-9]{1,3})$/, "$1.$2.$3");
      } else if (v.length > 3) {
        v = v.replace(/^([0-9]{3})([0-9]{1,3})$/, "$1.$2");
      }
      input.value = v;
    }

    function handleOnboardingSubmit(e) {
      e.preventDefault();
      const name = document.getElementById("inp-name").value.trim() || "Cauã Cunha";
      const cpf = document.getElementById("inp-cpf").value.trim() || "084.721.904-12";
      const home = document.getElementById("inp-home").value;
      const work = document.getElementById("inp-work").value;
      const line = document.getElementById("inp-line").value;

      const userData = { name: name, cpf: cpf, phone: "(81) 98888-7766", home: home, work: work, line: line };
      saveUserData(userData);
    }

    function enterAsQuickGuest() {
      const userData = {
        name: "Cauã Cunha",
        cpf: "084.721.904-12",
        phone: "(81) 98888-7766",
        home: "Camela · Centro (Rua do Comércio / Linha 199)",
        work: "TI Cabo (Terminal Integrado do Cabo)",
        line: "199"
      };
      saveUserData(userData);
    }

    function saveUserData(userData) {
      localStorage.setItem("grafoparada_logged", "true");
      localStorage.setItem("grafoparada_user_data", JSON.stringify(userData));
      document.getElementById("modal-onboarding").style.display = "none";
      loadUserData();
      playNaturalVoice("Olá, " + userData.name.split(' ')[0] + "! Bem-vindo ao GrafoParada. Monitorando a Linha 199 em Camela com proteção inteligente.");
      if (leafletMap) {
        setTimeout(function() { leafletMap.invalidateSize(); }, 200);
      }
    }

    function loadUserData() {
      const u = getUserData();
      const topName = document.getElementById("top-user-name");
      if (topName) topName.textContent = (u.name || "Cauã").split(" ")[0];

      const homeSub = document.getElementById("home-card-sub");
      if (homeSub) homeSub.textContent = (u.home || 'Camela').split('·')[0].replace('🏠','').trim() + " · 4 min";

      const workSub = document.getElementById("work-card-sub");
      if (workSub) workSub.textContent = (u.work || 'TI Cabo').split('·')[0].replace('💼','').replace('🏛️','').trim() + " · 32 min";

      const lineBadge = document.getElementById("top-line-label");
      if (lineBadge && u.line) {
        lineBadge.textContent = u.line === "199" ? "199 · Camela / Cabo" : "Linha " + u.line;
      }
    }

    function getUserData() {
      try {
        return JSON.parse(localStorage.getItem("grafoparada_user_data") || "{}");
      } catch (e) {
        return {};
      }
    }

    function logoutAndRestart() {
      localStorage.removeItem("grafoparada_logged");
      localStorage.removeItem("grafoparada_user_data");
      closeProfileModal();
      document.getElementById("modal-onboarding").style.display = "flex";
      showOnboardingSplash();
    }

    function toggleFullscreenDesktop() {
      document.body.classList.toggle("is-fullscreen");
      setTimeout(function() {
        if (leafletMap) leafletMap.invalidateSize();
      }, 300);
    }

    function switchLineQuick() {
      if (activeRouteCode === "199") {
        activeRouteCode = "178";
        TELEMETRIA = TELEMETRIA_178;
        document.getElementById("top-line-label").textContent = "178 · Suape / Cabo";
        drawRoute(TELEMETRIA);
        selectStop(1, true);
        playNaturalVoice("Linha 178 Suape alternada.");
      } else {
        activeRouteCode = "199";
        TELEMETRIA = TELEMETRIA_199;
        document.getElementById("top-line-label").textContent = "199 · Camela / Cabo";
        drawRoute(TELEMETRIA);
        selectStop(1, true);
        playNaturalVoice("Linha 199 Camela Cabo alternada.");
      }
    }

    // RECENTER GPS TARGET
    function recenterGpsTarget() {
      if (!navigator.geolocation) {
        selectStop(1, true);
        return;
      }
      navigator.geolocation.getCurrentPosition(
        function(pos) {
          const lat = pos.coords.latitude;
          const lon = pos.coords.longitude;
          if (leafletMap) {
            leafletMap.flyTo([lat, lon], 16, { animate: true });
            if (userMarker) leafletMap.removeLayer(userMarker);
            userMarker = L.circleMarker([lat, lon], {
              radius: 9,
              fillColor: "#0284c7",
              color: "#ffffff",
              weight: 3,
              opacity: 1,
              fillOpacity: 1
            }).addTo(leafletMap);
          }
        },
        function() {
          selectStop(1, true);
        },
        { enableHighAccuracy: true, timeout: 8000 }
      );
    }

    // NEURAL TTS
    function playNaturalVoice(text) {
      if (!text) return;
      try {
        if (currentAudioPlayer) {
          currentAudioPlayer.pause();
          currentAudioPlayer = null;
        }
        const url = "/api/live/tts?voice=pt-BR-FranciscaNeural&text=" + encodeURIComponent(text);
        const audio = new Audio(url);
        currentAudioPlayer = audio;
        audio.play().catch(function(e) {
          if ('speechSynthesis' in window) {
            const utter = new SpeechSynthesisUtterance(text);
            utter.lang = 'pt-BR';
            utter.rate = 1.05;
            window.speechSynthesis.speak(utter);
          }
        });
      } catch (e) {
        console.warn(e);
      }
    }
  </script>
</body>
</html>
"""

# Inject data cleanly
final_html = template.replace("__HOME_OPTIONS__", home_opts_html)
final_html = final_html.replace("__WORK_OPTIONS__", work_opts_html)
final_html = final_html.replace("__ROUTE_OPTIONS__", route_opts_html)
final_html = final_html.replace("__TELEMETRIA_199__", json.dumps(t199, ensure_ascii=False))
final_html = final_html.replace("__TELEMETRIA_178__", json.dumps(t178, ensure_ascii=False))
final_html = final_html.replace("__SEI_TERMINALS__", json.dumps(sei_terminals, ensure_ascii=False))

out_html = base_dir / "prototipo_grafoparada.html"
with open(out_html, "w", encoding="utf-8") as f:
    f.write(final_html)

print(f"[OK] prototipo_grafoparada.html compilado com sucesso ({out_html.stat().st_size:,} bytes)!")
