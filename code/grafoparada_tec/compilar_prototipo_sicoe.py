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

    /* DESKTOP MEDIA QUERY: ELEGANT RESPONSIVE SMARTPHONE FRAME */
    @media (min-width: 601px) {
      .desktop-outer-bar {
        display: flex;
      }
      .phone-simulator-frame {
        width: 100%;
        max-width: 440px;
        height: 100%;
        max-height: min(880px, 94vh);
        border-radius: 36px;
        border: 6px solid #1e293b;
        box-shadow: 0 25px 70px rgba(0, 0, 0, 0.4), 0 0 0 2px rgba(255, 255, 255, 0.1);
      }
      .phone-notch-island {
        display: flex;
      }
      .phone-home-indicator {
        display: block;
      }
    }

    /* SHORT SCREENS (e.g. laptop 480px-700px height): adapt cleanly without clipping */
    @media (min-width: 601px) and (max-height: 720px) {
      .desktop-outer-bar {
        display: none !important;
      }
      .phone-simulator-frame {
        max-height: 100dvh !important;
        border-radius: 0 !important;
        border: none !important;
        box-shadow: none !important;
      }
      .phone-notch-island {
        display: none !important;
      }
    }

    /* FULLSCREEN TOGGLE ON DESKTOP */
    body.is-fullscreen .phone-simulator-frame {
      width: 100vw !important;
      max-width: 100vw !important;
      height: 100dvh !important;
      max-height: 100dvh !important;
      border-radius: 0 !important;
      border: none !important;
      box-shadow: none !important;
    }
    body.is-fullscreen .desktop-outer-bar {
      display: none !important;
    }
    body.is-fullscreen .phone-notch-island {
      display: none !important;
    }
    body.is-fullscreen .top-floating-bar,
    body.is-fullscreen .mobile-bottom-sheet {
      max-width: 460px;
      margin-left: auto;
      margin-right: auto;
      left: 0;
      right: 0;
    }
    body.is-fullscreen .fab-gps {
      right: calc(50% - 215px);
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
      top: 14px;
      left: 12px;
      right: 12px;
      z-index: 1000;
      display: flex;
      flex-direction: column;
      gap: 6px;
      pointer-events: none;
    }

    .top-pills-row {
      display: flex;
      align-items: center;
      gap: 6px;
      overflow-x: auto;
      scrollbar-width: none;
      -webkit-overflow-scrolling: touch;
      padding-bottom: 2px;
    }
    .top-pills-row::-webkit-scrollbar {
      display: none;
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

    /* ==============================================================
       MODO FÁCIL / SÊNIOR (ACESSIBILIDADE UNIVERSAL PARA IDOSOS)
       WCAG 2.1 AAA - Alto contraste, letras grandes, toque facilitado
       ============================================================== */
    body.mode-senior {
      --bg-page: #ffffff !important;
      --bg-surface: #ffffff !important;
      --text-main: #000000 !important;
      --text-secondary: #111111 !important;
      --border-color: #000000 !important;
    }
    body.mode-senior #current-stop-name {
      font-size: 20px !important;
      font-weight: 800 !important;
      color: #000000 !important;
    }
    body.mode-senior .travel-cards-row {
      flex-direction: column !important;
      gap: 12px !important;
    }
    body.mode-senior .travel-card {
      min-height: 72px !important;
      border: 3px solid #000000 !important;
      padding: 14px 18px !important;
    }
    body.mode-senior .travel-card-title {
      font-size: 19px !important;
      font-weight: 800 !important;
      color: #000000 !important;
    }
    body.mode-senior .travel-card-subtitle {
      font-size: 15px !important;
      font-weight: 700 !important;
      color: #111111 !important;
    }
    body.mode-senior .hero-eta-big {
      font-size: 58px !important;
      font-weight: 900 !important;
      color: #000000 !important;
    }
    body.mode-senior .hero-eta-box {
      border: 3px solid #000000 !important;
      background: #ffffff !important;
      padding: 16px !important;
    }
    body.mode-senior .top-pill {
      font-size: 14px !important;
      font-weight: 800 !important;
      border: 2px solid #000000 !important;
      padding: 8px 14px !important;
    }
    body.mode-senior .status-badge-pill {
      font-size: 14px !important;
      border: 2px solid #000000 !important;
    }
    body.mode-senior .lost-help-card {
      border: 3px solid #dc2626 !important;
      background: #ffffff !important;
      min-height: 60px !important;
    }
    .btn-senior-voice {
      display: none;
      align-items: center;
      justify-content: center;
      gap: 10px;
      width: 100%;
      min-height: 56px;
      background: #000000;
      color: #ffffff;
      font-size: 15px;
      font-weight: 800;
      border-radius: 16px;
      border: none;
      cursor: pointer;
      margin-top: 10px;
      box-shadow: 0 4px 14px rgba(0,0,0,0.3);
    }
    .btn-senior-voice:active {
      background: #333333;
    }

    /* CTM FLEET REALLOCATION BANNER */
    .reallocation-banner {
      display: none;
      background: #047857;
      color: #ffffff;
      padding: 12px 14px;
      border-radius: 14px;
      font-size: 12.5px;
      font-weight: 700;
      line-height: 1.4;
      margin-bottom: 12px;
      border: 1.5px solid #34d399;
      box-shadow: 0 4px 16px rgba(4, 120, 87, 0.4);
      animation: pulseGreenGlow 2s infinite;
    }
    @keyframes pulseGreenGlow {
      0% { box-shadow: 0 0 0 0 rgba(4, 120, 87, 0.6); }
      70% { box-shadow: 0 0 0 10px rgba(4, 120, 87, 0); }
      100% { box-shadow: 0 0 0 0 rgba(4, 120, 87, 0); }
    }


    /* FAROL NOTURNO DE EMBARQUE (SINAL LUMINOSO CONTRA QUEIMA DE PARADA) */
    #night-beacon-screen {
      position: absolute;
      inset: 0;
      z-index: 100000;
      background: #facc15;
      color: #000000;
      display: none;
      flex-direction: column;
      align-items: center;
      justify-content: space-between;
      padding: 40px 20px 48px;
      cursor: pointer;
      text-align: center;
      animation: strobeYellowWhite 0.8s infinite alternate;
    }
    @keyframes strobeYellowWhite {
      0% { background: #facc15; }
      100% { background: #ffffff; }
    }
    .beacon-line-big {
      font-size: 76px;
      font-weight: 900;
      line-height: 1;
      font-family: 'JetBrains Mono', monospace;
      letter-spacing: -0.04em;
    }
    .beacon-hand-pulse {
      font-size: 86px;
      animation: bounceHand 0.75s infinite alternate;
    }
    @keyframes bounceHand {
      0% { transform: translateY(0); }
      100% { transform: translateY(-20px); }
    }
    .btn-night-beacon {
      width: 100%;
      min-height: 42px;
      background: #fef08a;
      color: #854d0e;
      border: 1.5px solid #facc15;
      border-radius: 12px;
      font-size: 12.5px;
      font-weight: 800;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      cursor: pointer;
      margin-top: 6px;
      transition: background 0.15s;
    }
    .btn-night-beacon:active {
      background: #fde047;
    }

    /* CARD GUARDIÃO DA INTEGRAÇÃO TEMPORAL (VEM) */
    .vem-guard-card {
      background: #f0f9ff;
      border: 1.5px solid #bae6fd;
      border-radius: 14px;
      padding: 10px 12px;
      margin-bottom: 10px;
    }

    /* BOTAO SIMULAR QUEIMA DE PARADA */
    .btn-demo-queima {
      width: 100%;
      min-height: 38px;
      background: #fff1f2;
      color: #e11d48;
      border: 1.5px dashed #fda4af;
      border-radius: 12px;
      font-size: 11.5px;
      font-weight: 800;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      cursor: pointer;
      margin-top: 6px;
    }


    /* BOTOES DE DESEMBARQUE SEGURO E ALAGAMENTO */
    .btn-safe-disembark {
      width: 100%;
      min-height: 40px;
      background: #fdf4ff;
      color: #9333ea;
      border: 1.5px solid #f0abfc;
      border-radius: 12px;
      font-size: 12px;
      font-weight: 800;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      cursor: pointer;
      margin-top: 6px;
      transition: background 0.15s;
    }
    .btn-safe-disembark:active {
      background: #fae8ff;
    }

    .btn-flood-radar {
      width: 100%;
      min-height: 38px;
      background: #ecfeff;
      color: #0891b2;
      border: 1.5px solid #a5f3fc;
      border-radius: 12px;
      font-size: 11.5px;
      font-weight: 800;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      cursor: pointer;
      margin-top: 6px;
    }

    /* BANNER ALAGAMENTO */
    .flood-alert-banner {
      display: none;
      background: #0891b2;
      color: #ffffff;
      padding: 10px 14px;
      border-radius: 12px;
      font-size: 12px;
      font-weight: 700;
      line-height: 1.35;
      margin-bottom: 10px;
      border: 1.5px solid #67e8f9;
      animation: pulseCyan 2s infinite;
    }
    @keyframes pulseCyan {
      0% { box-shadow: 0 0 0 0 rgba(8, 145, 178, 0.6); }
      70% { box-shadow: 0 0 0 8px rgba(8, 145, 178, 0); }
      100% { box-shadow: 0 0 0 0 rgba(8, 145, 178, 0); }
    }


    /* CARD ROTINA PENDULAR INTELIGENTE */
    .routine-commute-card {
      background: #f0fdf4;
      border: 1.5px solid #bbf7d0;
      border-radius: 14px;
      padding: 10px 14px;
      margin-bottom: 10px;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .routine-commute-card:active {
      transform: scale(0.98);
      background: #dcfce7;
    }

    /* LETREIRO DE LED FRONTAL DO COLETIVO (ACESSIBILIDADE SÊNIOR) */
    .bus-led-sign-box {
      background: #000000;
      border: 2px solid #334155;
      border-radius: 14px;
      padding: 10px 14px;
      margin-bottom: 10px;
      text-align: center;
      cursor: pointer;
    }
    .bus-led-sign-header {
      font-size: 10px;
      font-weight: 800;
      color: #94a3b8;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 4px;
    }
    .bus-led-sign-display {
      font-family: 'JetBrains Mono', monospace;
      color: #f59e0b;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
      text-shadow: 0 0 8px rgba(245, 158, 11, 0.6);
    }
    .led-line-number {
      font-size: 24px;
      font-weight: 900;
      background: rgba(245, 158, 11, 0.15);
      border: 1px solid #f59e0b;
      padding: 2px 8px;
      border-radius: 6px;
    }
    .led-line-dest {
      font-size: 13.5px;
      font-weight: 800;
      letter-spacing: 0.05em;
    }
    .bus-led-sign-hint {
      font-size: 10.5px;
      color: #cbd5e1;
      margin-top: 5px;
    }

    .btn-senior-voice-big {
      width: 100%;
      min-height: 48px;
      background: #0f172a;
      color: #f8fafc;
      border: 2px solid #334155;
      border-radius: 14px;
      font-size: 13.5px;
      font-weight: 800;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      cursor: pointer;
      margin-bottom: 10px;
      transition: background 0.15s;
    }
    .btn-senior-voice-big:active {
      background: #1e293b;
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
            <button class="btn-desktop-action" onclick="openRoutineModal()" style="background:rgba(5,150,105,0.25); border-color:#34d399; color:#a7f3d0;">
        <span>📅</span> Minha Rotina (Turnos)
      </button>
      <button class="btn-desktop-action" onclick="openSeiTerminalsModal()" style="background:rgba(2,132,199,0.25); border-color:#38bdf8; color:#bae6fd;">
        <span>🏛️</span> 26 Terminais do SEI
      </button>
<button class="btn-desktop-action" onclick="openDispatchModal()" style="background:rgba(2,132,199,0.25); border-color:#38bdf8;">
        <span>🏛️</span> Central CTM (Realocação de Frota)
      </button>
      <button class="btn-desktop-action" onclick="openAuditModal()" style="background:rgba(16,185,129,0.25); border-color:#34d399;">
        <span>🧪</span> Auditoria (Idosos vs Jovens)
      </button>
      <button class="btn-desktop-action" onclick="activateNightBeacon()" style="background:rgba(250,204,21,0.2); border-color:#facc15; color:#fef08a;">
        <span>💡</span> Farol Noturno (Anti-Queima)
      </button>
      <button class="btn-desktop-action" onclick="openVemModal()" style="background:rgba(14,165,233,0.2); border-color:#38bdf8;">
        <span>⏱️</span> Integração VEM (2h)
      </button>
      <button class="btn-desktop-action" onclick="openSafeDisembarkModal()" style="background:rgba(168,85,247,0.2); border-color:#c084fc; color:#f3e8ff;">
        <span>🌙</span> Lei Parada Segura (22h)
      </button>
      <button class="btn-desktop-action" onclick="toggleFloodAlertSimulation()" style="background:rgba(6,182,212,0.2); border-color:#67e8f9; color:#cffafe;">
        <span>🌊</span> Radar Alagamento & Desvios
      </button>
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

                <div class="top-pill" id="routine-pill-btn" onclick="openRoutineModal()" title="Configurar Minha Rotina Pendular" style="color:#059669; font-weight:800;">
          <span style="font-size:14px;">📅</span>
          <span id="label-routine-pill">Rotina: 05h45</span>
        </div>

<div class="top-pill" id="senior-pill-btn" onclick="toggleSeniorMode()" title="Ativar Modo Fácil / Letras Grandes para Idosos" style="font-weight:800;">
          <span style="font-size:14px;">👁️</span>
          <span id="label-senior-pill">Aa Fácil</span>
        </div>

        <div class="top-pill" onclick="openDispatchModal()" title="Central CTM de Realocação de Frota" style="color:var(--blue-accent); font-weight:800;">
          <span style="font-size:14px;">🏛️</span>
          <span>CTM Frota</span>
        </div>

        <div class="status-badge-pill" id="top-line-badge" onclick="switchLineQuick()">
          <div class="pulse-dot"></div>
          <span id="top-line-label">199</span>
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
        <!-- REAL-TIME FLEET REALLOCATION BANNER -->
        <div id="resting-reallocation-banner" class="reallocation-banner"></div>

        <!-- STATE A: DEFAULT / QUICK CHOICE VIEW -->
        <div id="view-sheet-resting">
          <!-- PARADA ATUAL DETALHADA COM CÓDIGO CTM E MUNICÍPIO -->
          <div style="background:var(--bg-page); border:1.5px solid var(--border-color); border-radius:14px; padding:10px 12px; margin-bottom:10px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
              <div style="display:flex; align-items:center; gap:6px;">
                <span style="font-size:11px; font-weight:800; color:var(--text-muted); text-transform:uppercase;">📍 Sua Parada Atual:</span>
                <button id="btn-fav-star" onclick="toggleFavoriteCurrentStop()" style="border:none; background:none; cursor:pointer; font-size:14px;" title="Favoritar parada">⭐</button>
              </div>
              <button style="border:none; background:none; color:var(--blue-accent); font-weight:800; font-size:12px; cursor:pointer;" onclick="toggleSheetExpansion()">Ver Todas (43) ▲</button>
            </div>
            <div id="current-stop-name" style="color:var(--text-main);">
              <div style="display:flex; align-items:center; gap:6px;">
                <span style="font-size:10.5px; font-weight:800; background:#f1f5f9; color:#475569; padding:2px 6px; border-radius:6px; border:1px solid #cbd5e1;">CÓD 030613</span>
                <span style="font-size:11px; font-weight:800; color:#047857;">📍 Ipojuca · Camela</span>
                <span style="font-size:10px; background:#dcfce7; color:#15803d; padding:1px 5px; border-radius:4px; font-weight:700;">🏠 Abrigo Coberto</span>
              </div>
              <div style="font-size:14.5px; font-weight:800; color:var(--text-main); margin-top:3px;">
                Praça Pedro Serafim (Terminal de Camela)
              </div>
              <div style="font-size:11px; color:var(--text-secondary); margin-top:2px;">
                Ref: Igreja Matriz de Santo Antônio / Mercado Público · Sentido TI Cabo
              </div>
            </div>

            <!-- LIVE ARRIVAL AT CURRENT STOP (ETA IMEDIATO & VOZ) -->
            <div style="background:#ecfdf5; border:1.5px solid #a7f3d0; border-radius:10px; padding:8px 10px; margin-top:8px; display:flex; justify-content:space-between; align-items:center;">
              <div>
                <div style="font-size:10.5px; font-weight:800; color:#047857; text-transform:uppercase; letter-spacing:0.02em;">
                  🚌 Próximo Ônibus Linha 199:
                </div>
                <div style="font-size:14.5px; font-weight:800; color:#065f46; margin-top:1px;">
                  Chega em <span id="resting-eta-val">4</span> min <span style="font-size:11px; font-weight:600; color:#047857;">(06:14)</span>
                </div>
              </div>
              <div style="display:flex; gap:6px; align-items:center;">
                <button onclick="speakCurrentArrival()" style="background:#ffffff; border:1.5px solid #a7f3d0; border-radius:8px; padding:6px 9px; font-size:11.5px; font-weight:800; color:#047857; cursor:pointer;" title="Ouvir previsão por voz">
                  🔊 Ouvir
                </button>
                <button onclick="triggerTripAction('work')" style="background:#059669; border:none; border-radius:8px; padding:6px 11px; font-size:11.5px; font-weight:800; color:#ffffff; cursor:pointer;">
                  Acompanhar ➔
                </button>
              </div>
            </div>
          </div>

                    <!-- CARD ROTINA PENDULAR INTELIGENTE -->
          <div class="routine-commute-card" onclick="openRoutineModal()">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <div style="display:flex; align-items:center; gap:6px;">
                <span style="font-size:15px;">📅</span>
                <span style="font-size:11.5px; font-weight:800; color:#047857; text-transform:uppercase;">Minha Rotina Pendular</span>
              </div>
              <span style="font-size:10.5px; font-weight:800; background:#dcfce7; color:#15803d; padding:2px 8px; border-radius:999px;" id="routine-tag-pill">Turno Ativo · 05h45</span>
            </div>
            <div style="font-size:12.5px; font-weight:800; color:#0f172a; margin-top:5px;" id="routine-title-desc">
              Indústria Suape (Camela ➔ TI Cabo) · Entrada 07h00
            </div>
            <div style="font-size:11px; color:#475569; margin-top:3px; line-height:1.35;" id="routine-advice-desc">
              💡 <strong>Janela de Saída:</strong> Caminhada de 6 min. Saia de casa às <strong>06:08</strong> para pegar o 199 das 06:14 sem mofar no ponto.
            </div>
            <div style="font-size:10.5px; color:#059669; font-weight:700; margin-top:4px;">
              👥 48 trabalhadores nesta rota · Demanda alimenta a Central CTM.
            </div>
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
          <div id="active-reallocation-banner" class="reallocation-banner"></div>
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

          <!-- GUARDIÃO DA INTEGRAÇÃO TEMPORAL (VEM) -->
          <div class="vem-guard-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <div style="display:flex; align-items:center; gap:6px;">
                <span style="font-size:16px;">⏱️</span>
                <span style="font-weight:800; font-size:11.5px; color:#0369a1; text-transform:uppercase;">Integração Temporal VEM (2h)</span>
              </div>
              <span style="font-size:11.5px; font-weight:800; background:#e0f2fe; color:#0369a1; padding:2px 8px; border-radius:999px;" id="vem-countdown">1h 14m restantes</span>
            </div>
            <div style="font-size:11px; color:#334155; margin-top:5px; line-height:1.35;" id="vem-status-desc">
              ✅ <strong>Gratuidade Assegurada:</strong> Com o 199 chegando em 4 min, você desembarcará no TI Cabo com <strong>38 min de folga</strong> no cartão VEM. Tarifa na catraca: <strong>R$ 0,00</strong>.
            </div>
          </div>

                    <!-- LETREIRO AMIGO IDENTICO AO ÔNIBUS (ACESSIBILIDADE SÊNIOR) -->
          <div class="bus-led-sign-box" onclick="speakSeniorDirections()">
            <div class="bus-led-sign-header">LETREIRO FRONTAL DO COLETIVO:</div>
            <div class="bus-led-sign-display">
              <span class="led-line-number">199</span>
              <span class="led-line-dest">CAMELA / TI CABO VIA PE-60</span>
            </div>
            <div class="bus-led-sign-hint">
              👁️ Compare este visor com o letreiro do ônibus chegando na pista.
            </div>
          </div>

          <!-- BOTÃO GIGANTE DE CONFIRMAÇÃO POR VOZ PARA IDOSOS -->
          <button class="btn-senior-voice-big" onclick="speakSeniorDirections()">
            <span>🔊</span> OUVIR EM VOZ ALTA (CONFIRMAR EMBARQUE)
          </button>

          <!-- BANNER MODO OFFLINE INERCIAL -->
          <div id="offline-inertial-banner" style="display:none; background:#fffbeb; border:1px solid #fde68a; border-radius:12px; padding:10px; margin-bottom:8px; font-size:11.5px; color:#92400e; line-height:1.4;">
            📶 <strong>MODO OFFLINE INERCIAL ATIVO:</strong> Sem cobertura 4G no Km 12 (Engenho Mercês). Estimativa mantida pelo histórico local do grafo (STGCN).
          </div>

          <!-- BOTÃO SIMULAR OFFLINE NA PE-60 -->
          <button class="btn-demo-failure" onclick="toggleOfflineInertialSimulation()" style="background:#fffbeb; color:#b45309; border-color:#fde68a;">
            <span>📶</span> Simular Queda de Sinal 4G (Modo Offline Inercial)
          </button>

          <!-- BOTÃO FAROL NOTURNO DE EMBARQUE (ANTI-QUEIMA DE PARADA) -->
          <button class="btn-night-beacon" onclick="activateNightBeacon()">
            <span>💡</span> ATIVAR FAROL NOTURNO (SINAL PRO MOTORISTA)
          </button>

          <!-- BOTÃO SIMULAR QUEIMA DE PARADA -->
          <button class="btn-demo-queima" onclick="simulateQueimaDeParada()">
            <span>🚨</span> Simular Queima de Parada (Motorista Passou Direto)
          </button>

          <!-- BANNER DE ALAGAMENTO PE-60 -->
          <div id="flood-alert-banner" class="flood-alert-banner"></div>

          <!-- BOTÃO DESEMBARQUE SEGURO NOTURNO (LEI ESTADUAL 15.878) -->
          <button class="btn-safe-disembark" onclick="openSafeDisembarkModal()">
            <span>🌙</span> Desembarque Noturno (Lei Estadual nº 15.878)
          </button>

          <!-- BOTÃO RADAR DE ALAGAMENTO & DESVIOS PE-60 -->
          <button class="btn-flood-radar" onclick="toggleFloodAlertSimulation()">
            <span>🌊</span> Radar Alagamento & Pane (Desvios na Rodovia)
          </button>

          <!-- BUTTON TO SIMULATE THE SLIDE 3 FAILURE REAL -->
          <button class="btn-demo-failure" onclick="simulateSlide3Failure()">
            <span>🧪</span> Simular Interdição PE-60 (Demonstração da Falha · Sem2)
          </button>

          <!-- HERO ACTION: POCKET MODE AUDIO -->
          <button class="hero-btn-pocket" onclick="activatePocketShield()">
            <span>🎧</span> ATIVAR MODO CELULAR NO BOLSO
          </button>

          <!-- VOICE READING FOR SENIOR MODE -->
          <button class="btn-senior-voice" id="btn-senior-voice-action" onclick="speakSeniorDirections()">
            <span>🔊</span> OUVIR EM VOZ ALTA (LEITURA CLARA)
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


    <!-- 14. MODAL: MINHA ROTINA PENDULAR (MAPEADOR DE TURNO SEM BUROCRACIA) -->
    <div id="modal-routine" class="modal-overlay">
      <div class="modal-card" style="border:2px solid #059669; max-width:400px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
          <div style="display:flex; align-items:center; gap:8px;">
            <span style="font-size:22px;">📅</span>
            <div>
              <h3 style="font-size:16px; font-weight:800; color:#059669; margin:0;">Minha Rotina Pendular</h3>
              <span style="font-size:11px; color:var(--text-secondary);">Mapeador de Turno com Zero Burocracia</span>
            </div>
          </div>
          <button style="border:none; background:none; font-size:20px; font-weight:800; color:var(--text-muted); cursor:pointer;" onclick="closeRoutineModal()">✕</button>
        </div>

        <p style="font-size:12px; color:#475569; margin-bottom:12px; line-height:1.4;">
          Escolha seu turno habitual com 1 toque. O GrafoParada calcula quando sair de casa e comunica sua demanda anonimamente à Central CTM:
        </p>

        <!-- 4 BOTOES DE TURNO -->
        <div style="display:flex; flex-direction:column; gap:8px; margin-bottom:14px;">
          <button class="routine-choice-btn" id="btn-routine-suape" onclick="selectRoutinePreset('suape')" style="background:#ecfdf5; border:1.5px solid #059669; border-radius:12px; padding:10px 12px; text-align:left; cursor:pointer;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <strong style="font-size:13px; color:#065f46;">🏭 Turno Indústria Suape</strong>
              <span style="font-size:11px; font-weight:800; background:#059669; color:#ffffff; padding:2px 8px; border-radius:999px;">05h45</span>
            </div>
            <div style="font-size:11px; color:#475569; margin-top:2px;">Camela ➔ TI Cabo / Suape · Entrada no posto às 07h00. 48 passageiros.</div>
          </button>

          <button class="routine-choice-btn" id="btn-routine-comercio" onclick="selectRoutinePreset('comercio')" style="background:#f8fafc; border:1.5px solid #e2e8f0; border-radius:12px; padding:10px 12px; text-align:left; cursor:pointer;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <strong style="font-size:13px; color:#0f172a;">🛍️ Turno Comércio / Centro</strong>
              <span style="font-size:11px; font-weight:800; background:#64748b; color:#ffffff; padding:2px 8px; border-radius:999px;">07h30</span>
            </div>
            <div style="font-size:11px; color:#475569; margin-top:2px;">Camela ➔ Centro do Cabo / Shopping Costa Dourada · Entrada às 08h30.</div>
          </button>

          <button class="routine-choice-btn" id="btn-routine-noturno" onclick="selectRoutinePreset('noturno')" style="background:#f8fafc; border:1.5px solid #e2e8f0; border-radius:12px; padding:10px 12px; text-align:left; cursor:pointer;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <strong style="font-size:13px; color:#0f172a;">🎓 Estudante Universitário / Noite</strong>
              <span style="font-size:11px; font-weight:800; background:#64748b; color:#ffffff; padding:2px 8px; border-radius:999px;">17h40</span>
            </div>
            <div style="font-size:11px; color:#475569; margin-top:2px;">Camela ➔ TI Cabo / Fachuca / UFRPE · Volta às 22h30.</div>
          </button>

          <button class="routine-choice-btn" id="btn-routine-saude" onclick="selectRoutinePreset('saude')" style="background:#f8fafc; border:1.5px solid #e2e8f0; border-radius:12px; padding:10px 12px; text-align:left; cursor:pointer;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <strong style="font-size:13px; color:#0f172a;">🏥 Turno Plantão Saúde (12x36)</strong>
              <span style="font-size:11px; font-weight:800; background:#64748b; color:#ffffff; padding:2px 8px; border-radius:999px;">06h30</span>
            </div>
            <div style="font-size:11px; color:#475569; margin-top:2px;">Camela ➔ UPA Ipojuca / Hosp. Mendo Sampaio · Plantão das 07h às 19h.</div>
          </button>
        </div>

        <div style="background:#f0f9ff; border:1px solid #bae6fd; border-radius:12px; padding:10px; margin-bottom:12px; font-size:11.5px; color:#0369a1; line-height:1.4;">
          ⚡ <strong>Previsão de Demanda para a Central CTM:</strong> Ao salvar seu turno, a Central sabe exatamente quantas pessoas precisam embarcar na sua parada sem você precisar abrir o app com antecedência!
        </div>

        <button class="btn-primary" onclick="confirmRoutineChoice()" style="background:#059669; margin-bottom:8px;">
          Salvar Minha Rotina
        </button>
        <button class="btn-secondary" onclick="closeRoutineModal()">Cancelar</button>
      </div>
    </div>

    <!-- 15. MODAL: GUIA DOS 26 TERMINAIS INTEGRADOS DO SEI (GRANDE RECIFE) -->
    <div id="modal-sei-terminals" class="modal-overlay">
      <div class="modal-card" style="border:2px solid #0284c7; max-width:440px; max-height:85vh; display:flex; flex-direction:column;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
          <div style="display:flex; align-items:center; gap:8px;">
            <span style="font-size:24px;">🏛️</span>
            <div>
              <h3 style="font-size:16px; font-weight:800; color:#0284c7; margin:0;">26 Terminais Integrados (SEI)</h3>
              <span style="font-size:11px; color:var(--text-secondary);">Sistema Estrutural Integrado · CTM Grande Recife</span>
            </div>
          </div>
          <button style="border:none; background:none; font-size:20px; font-weight:800; color:var(--text-muted); cursor:pointer;" onclick="closeSeiTerminalsModal()">✕</button>
        </div>

        <div style="background:#f0f9ff; border:1px solid #bae6fd; border-radius:12px; padding:10px; margin-bottom:10px; font-size:11.5px; color:#0369a1; line-height:1.4;">
          💳 <strong>Integração Temporal VEM:</strong> Permite baldeação gratuita em até 120 minutos entre ônibus e Metrô/VLT com a tarifa única de <strong>R$ 4,10</strong>.
        </div>

        <!-- FILTROS POR REGIÃO -->
        <div style="display:flex; gap:6px; margin-bottom:10px; overflow-x:auto; padding-bottom:4px;">
          <button class="ti-filter-btn active" id="btn-ti-filter-all" onclick="filterTerminalsByRegion('all')" style="background:#0284c7; color:#fff; border:none; padding:4px 10px; border-radius:999px; font-size:11.5px; font-weight:700; cursor:pointer; white-space:nowrap;">Todos (26)</button>
          <button class="ti-filter-btn" id="btn-ti-filter-sul" onclick="filterTerminalsByRegion('sul')" style="background:#f1f5f9; color:#475569; border:1px solid #cbd5e1; padding:4px 10px; border-radius:999px; font-size:11.5px; font-weight:700; cursor:pointer; white-space:nowrap;">Cabo & Sul</button>
          <button class="ti-filter-btn" id="btn-ti-filter-recife" onclick="filterTerminalsByRegion('recife')" style="background:#f1f5f9; color:#475569; border:1px solid #cbd5e1; padding:4px 10px; border-radius:999px; font-size:11.5px; font-weight:700; cursor:pointer; white-space:nowrap;">Recife (12)</button>
          <button class="ti-filter-btn" id="btn-ti-filter-norte" onclick="filterTerminalsByRegion('norte')" style="background:#f1f5f9; color:#475569; border:1px solid #cbd5e1; padding:4px 10px; border-radius:999px; font-size:11.5px; font-weight:700; cursor:pointer; white-space:nowrap;">Olinda & Norte</button>
          <button class="ti-filter-btn" id="btn-ti-filter-oeste" onclick="filterTerminalsByRegion('oeste')" style="background:#f1f5f9; color:#475569; border:1px solid #cbd5e1; padding:4px 10px; border-radius:999px; font-size:11.5px; font-weight:700; cursor:pointer; white-space:nowrap;">Oeste & Jaboatão</button>
        </div>

        <!-- LISTA ROLÁVEL DE TERMINAIS -->
        <div id="sei-terminals-list-box" style="flex:1; overflow-y:auto; display:flex; flex-direction:column; gap:8px; padding-right:2px;"></div>

        <button class="btn-secondary" onclick="closeSeiTerminalsModal()" style="margin-top:10px;">Fechar</button>
      </div>
    </div>

    <!-- 8. MODAL: CENTRAL CTM DE REALOCAÇÃO DE FROTA NO VAZIO -->
    <div id="modal-dispatch" class="modal-overlay">
      <div class="modal-card" style="border:2px solid #0284c7; max-width:400px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
          <div style="display:flex; align-items:center; gap:8px;">
            <span style="font-size:22px;">🏛️</span>
            <div>
              <h3 style="font-size:16px; font-weight:800; color:#0284c7; margin:0;">Central CTM · Realocação</h3>
              <span style="font-size:11px; color:var(--text-secondary);">Balanceamento da Frota no Vazio (PE-60)</span>
            </div>
          </div>
          <button style="border:none; background:none; font-size:20px; font-weight:800; color:var(--text-muted); cursor:pointer;" onclick="closeDispatchModal()">✕</button>
        </div>

        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:8px; margin-bottom:12px;">
          <div style="background:#fef2f2; border:1px solid #fecaca; border-radius:12px; padding:10px;">
            <div style="font-size:10.5px; font-weight:800; color:#dc2626; text-transform:uppercase;">Linha 178 Suape</div>
            <div style="font-size:18px; font-weight:800; color:#dc2626; margin:3px 0;">3 passageiros</div>
            <div style="font-size:11px; color:#475569; line-height:1.3;">6% ocupação (No Vazio). 14 L de diesel/h desperdiçados.</div>
          </div>

          <div style="background:#ecfdf5; border:1px solid #a7f3d0; border-radius:12px; padding:10px;">
            <div style="font-size:10.5px; font-weight:800; color:#059669; text-transform:uppercase;">Linha 199 Camela</div>
            <div style="font-size:18px; font-weight:800; color:#059669; margin:3px 0;">38 aguardando</div>
            <div style="font-size:11px; color:#475569; line-height:1.3;">Demanda reprimida na PE-60. Risco de fuga para ligeirinho.</div>
          </div>
        </div>

        <div style="background:#f0f9ff; border:1.5px solid #bae6fd; border-radius:12px; padding:12px; margin-bottom:14px;">
          <div style="font-size:11px; font-weight:800; color:#0284c7; text-transform:uppercase; margin-bottom:4px;">
            ⚡ Decisão Algorítmica STGCN:
          </div>
          <div style="font-size:12.5px; font-weight:700; color:#0f172a; line-height:1.4;">
            Transferir coletivo ocioso 178-04 para a Linha 199 e antecipar partida no TI Cabo em 10 minutos.
          </div>
        </div>

        <button class="btn-primary" onclick="executeFleetReallocation()" style="margin-bottom:8px; background:#0284c7;">
          ⚡ Executar Realocação de Frota Agora
        </button>
        <button class="btn-secondary" onclick="closeDispatchModal()">Fechar</button>
      </div>
    </div>

    <!-- 9. MODAL: AUDITORIA DE USABILIDADE & RETESTES (PERSONAS REAIS) -->
    <div id="modal-audit" class="modal-overlay">
      <div class="modal-card" style="border:2px solid #059669; max-width:410px; max-height:85vh; overflow-y:auto;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
          <div style="display:flex; align-items:center; gap:8px;">
            <span style="font-size:22px;">🧪</span>
            <div>
              <h3 style="font-size:16px; font-weight:800; color:#059669; margin:0;">Auditoria de Usabilidade</h3>
              <span style="font-size:11px; color:var(--text-secondary);">Retestes de Campo · Todas as Idades</span>
            </div>
          </div>
          <button style="border:none; background:none; font-size:20px; font-weight:800; color:var(--text-muted); cursor:pointer;" onclick="closeAuditModal()">✕</button>
        </div>

        <!-- PERSONA 1 -->
        <div style="background:var(--bg-page); border:1px solid var(--border-color); border-radius:12px; padding:12px; margin-bottom:10px;">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <strong style="font-size:13px; color:#0f172a;">👵 Dona Severina (68 anos · Camela)</strong>
            <span style="font-size:10.5px; font-weight:800; background:#dcfce7; color:#15803d; padding:2px 8px; border-radius:999px;">Aprovado</span>
          </div>
          <div style="font-size:11.5px; color:#475569; margin-top:4px; line-height:1.4;">
            • <strong>Desafio:</strong> Baixa visão e tremor nos dedos no ponto.<br>
            • <strong>Resultado no GrafoParada:</strong> Modo Fácil ativado. Contraste 9.2:1 (WCAG AAA), toque em botão gigante de 72px, instrução falada alta no fone em 1.8s. Zero necessidade de dar zoom no mapa.
          </div>
        </div>

        <!-- PERSONA 2 -->
        <div style="background:var(--bg-page); border:1px solid var(--border-color); border-radius:12px; padding:12px; margin-bottom:10px;">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <strong style="font-size:13px; color:#0f172a;">🧑‍🦱 Lucas (21 anos · Suape)</strong>
            <span style="font-size:10.5px; font-weight:800; background:#dcfce7; color:#15803d; padding:2px 8px; border-radius:999px;">Aprovado</span>
          </div>
          <div style="font-size:11.5px; color:#475569; margin-top:4px; line-height:1.4;">
            • <strong>Desafio:</strong> Parada escura na PE-60 às 22h40 (medo de assalto).<br>
            • <strong>Resultado no GrafoParada:</strong> Modo Bolso com tela 100% preta (0 nits), alerta tátil por vibração (< 2 min), voz discreta no fone. Proteção máxima sem expor o aparelho.
          </div>
        </div>

        <!-- PERSONA 3 -->
        <div style="background:var(--bg-page); border:1px solid var(--border-color); border-radius:12px; padding:12px; margin-bottom:12px;">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <strong style="font-size:13px; color:#0f172a;">👮 Fiscal Severino (54 anos · TI Cabo)</strong>
            <span style="font-size:10.5px; font-weight:800; background:#dcfce7; color:#15803d; padding:2px 8px; border-radius:999px;">Aprovado</span>
          </div>
          <div style="font-size:11.5px; color:#475569; margin-top:4px; line-height:1.4;">
            • <strong>Desafio:</strong> Ônibus rodando vazio enquanto linhas suburbanas superlotam.<br>
            • <strong>Resultado no GrafoParada:</strong> STGCN detecta 38 passageiros reprimidos vs Linha 178 vazia. Ordem de despacho emitida em 12 segundos. Economia de 14 L de diesel por viagem.
          </div>
        </div>

        <button class="btn-primary" onclick="closeAuditModal()" style="background:#059669;">Concluir Inspeção</button>
      </div>
    </div>


    <!-- 10. SCREEN: FAROL NOTURNO DE EMBARQUE (SINAL LUMINOSO PARA O MOTORISTA) -->
    <div id="night-beacon-screen" onclick="deactivateNightBeacon()">
      <div>
        <div style="font-size:14px; font-weight:800; text-transform:uppercase; letter-spacing:0.1em; color:#713f12; margin-bottom:6px;">
          Sinal Luminoso Noturno · Aponte para a Rodovia
        </div>
        <div class="beacon-line-big">199</div>
        <div style="font-size:20px; font-weight:800; color:#000000; letter-spacing:-0.02em;">
          CAMELA / TI CABO
        </div>
      </div>

      <div class="beacon-hand-pulse">✋</div>

      <div>
        <div style="font-size:16px; font-weight:800; color:#000000; margin-bottom:4px;">
          SÃO JUDAS TADEU (SJT)
        </div>
        <div style="font-size:12.5px; font-weight:700; color:#713f12; background:rgba(0,0,0,0.08); padding:6px 14px; border-radius:999px; display:inline-block;">
          Toque em qualquer lugar da tela para fechar
        </div>
      </div>
    </div>

    <!-- 11. MODAL: AUDITORIA FORENSE DE QUEIMA DE PARADA -->
    <div id="modal-queima-parada" class="modal-overlay">
      <div class="modal-card" style="border:2px solid #e11d48; max-width:400px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
          <div style="display:flex; align-items:center; gap:8px;">
            <span style="font-size:24px;">🚨</span>
            <div>
              <h3 style="font-size:16px; font-weight:800; color:#e11d48; margin:0;">Queima de Parada Detectada!</h3>
              <span style="font-size:11px; color:var(--text-secondary);">Telemetria Forense com Prova de GPS</span>
            </div>
          </div>
          <button style="border:none; background:none; font-size:20px; font-weight:800; color:var(--text-muted); cursor:pointer;" onclick="closeQueimaModal()">✕</button>
        </div>

        <div style="background:#fff1f2; border:1px solid #fecdd3; border-radius:12px; padding:12px; margin-bottom:12px; font-size:12px; line-height:1.6; color:#881337;">
          <div><strong>• Linha:</strong> 199 - Camela / Cabo (SJT)</div>
          <div><strong>• Coletivo:</strong> Veículo CTM 199-04 (Placa PE-4912)</div>
          <div><strong>• Local:</strong> Parada 030613 · Terminal de Camela</div>
          <div><strong>• Velocidade no Ponto:</strong> 44 km/h (Passou direto sem parar)</div>
          <div><strong>• Registro de Satélite:</strong> 10/11/2026 às 22h41m12s</div>
        </div>

        <p style="font-size:12px; color:#475569; line-height:1.4; margin-bottom:14px;">
          O motorista ignorou os passageiros no abrigo. O GrafoParada gerou a prova técnica completa para a Ouvidoria do CTM.
        </p>

        <button class="btn-primary" onclick="sendQueimaWhatsAppReport()" style="background:#e11d48; margin-bottom:8px;">
          📲 Denunciar no WhatsApp CTM (81 99488-3999)
        </button>
        <button class="btn-secondary" onclick="closeQueimaModal()">Fechar</button>
      </div>
    </div>

    <!-- 12. MODAL: DETALHES DA INTEGRAÇÃO TEMPORAL (VEM) -->
    <div id="modal-vem" class="modal-overlay">
      <div class="modal-card" style="border:2px solid #0284c7; max-width:400px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
          <div style="display:flex; align-items:center; gap:8px;">
            <span style="font-size:22px;">⏱️</span>
            <div>
              <h3 style="font-size:16px; font-weight:800; color:#0284c7; margin:0;">Integração Temporal VEM</h3>
              <span style="font-size:11px; color:var(--text-secondary);">Regulamento CTM · Janela de 120 Minutos</span>
            </div>
          </div>
          <button style="border:none; background:none; font-size:20px; font-weight:800; color:var(--text-muted); cursor:pointer;" onclick="closeVemModal()">✕</button>
        </div>

        <div style="background:#f0f9ff; border:1px solid #bae6fd; border-radius:12px; padding:12px; margin-bottom:12px; font-size:12px; line-height:1.5;">
          <div style="font-weight:800; color:#0369a1; margin-bottom:4px;">Como funciona a proteção:</div>
          <div>1. Seu cartão VEM foi debitado às <strong>21h35</strong> no primeiro embarque.</div>
          <div>2. A gratuidade de baldeação no TI Cabo é válida até às <strong>23h35</strong>.</div>
          <div>3. Previsão de chegada no TI Cabo pela STGCN: <strong>22h57</strong> (Folga de 38 minutos).</div>
        </div>

        <div style="background:#ecfdf5; border:1px solid #a7f3d0; border-radius:12px; padding:10px; margin-bottom:14px; font-size:11.5px; color:#065f46;">
          🛡️ <strong>Seguro Contra Dupla Cobrança:</strong> Se o ônibus atrasar por culpa da rodovia e a janela expirar, o GrafoParada emite automaticamente o <em>Atestado Digital de Atraso</em> para reembolso do débito de R$ 4,10 na Central do CTM.
        </div>

        <button class="btn-primary" onclick="closeVemModal()" style="background:#0284c7;">Entendido</button>
      </div>
    </div>


    <!-- 13. MODAL: DESEMBARQUE SEGURO NOTURNO (LEI ESTADUAL 15.878/2016) -->
    <div id="modal-safe-disembark" class="modal-overlay">
      <div class="modal-card" style="border:2px solid #9333ea; max-width:400px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
          <div style="display:flex; align-items:center; gap:8px;">
            <span style="font-size:24px;">🌙</span>
            <div>
              <h3 style="font-size:16px; font-weight:800; color:#9333ea; margin:0;">Parada Segura Noturna</h3>
              <span style="font-size:11px; color:var(--text-secondary);">Lei Estadual nº 15.878/2016 (PE)</span>
            </div>
          </div>
          <button style="border:none; background:none; font-size:20px; font-weight:800; color:var(--text-muted); cursor:pointer;" onclick="closeSafeDisembarkModal()">✕</button>
        </div>

        <div style="background:#fdf4ff; border:1px solid #f0abfc; border-radius:12px; padding:12px; margin-bottom:12px; font-size:12px; line-height:1.5; color:#581c87;">
          <strong>Seu Direito Legal:</strong> Entre <strong>22h e 05h</strong> (e em qualquer horário para PcD/idosos), você tem o direito garantido de desembarcar em qualquer local mais iluminado e seguro no itinerário do ônibus, mesmo fora do ponto oficial.
        </div>

        <!-- CARTÃO VISUAL PARA MOSTRAR AO MOTORISTA -->
        <div style="background:#000000; color:#facc15; border-radius:12px; padding:16px; text-align:center; margin-bottom:12px; border:2px solid #facc15;">
          <div style="font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:0.05em; color:#e2e8f0; margin-bottom:4px;">
            Mostre esta tela ao motorista / cobrador:
          </div>
          <div style="font-size:18px; font-weight:900; line-height:1.25;">
            "MOTORISTA, PEÇO DESEMBARQUE SEGURO NESTE PONTO ILUMINADO (LEI ESTADUAL Nº 15.878/2016). OBRIGADO!"
          </div>
        </div>

        <button class="btn-primary" onclick="speakDriverCourtesyAudio()" style="background:#9333ea; margin-bottom:8px;">
          🔊 Avisar Motorista com Áudio Cortês
        </button>
        <button class="btn-secondary" onclick="closeSafeDisembarkModal()">Fechar</button>
      </div>
    </div>

    <!-- 14. MODAL: RADAR DE ALAGAMENTO & SOCORRO DE TRANSBORDO -->
    <div id="modal-flood" class="modal-overlay">
      <div class="modal-card" style="border:2px solid #0891b2; max-width:400px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
          <div style="display:flex; align-items:center; gap:8px;">
            <span style="font-size:24px;">🌊</span>
            <div>
              <h3 style="font-size:16px; font-weight:800; color:#0891b2; margin:0;">Radar Alagamento & Pane</h3>
              <span style="font-size:11px; color:var(--text-secondary);">Monitoramento Crítico PE-60 / Cabo</span>
            </div>
          </div>
          <button style="border:none; background:none; font-size:20px; font-weight:800; color:var(--text-muted); cursor:pointer;" onclick="closeFloodModal()">✕</button>
        </div>

        <div style="background:#ecfeff; border:1px solid #a5f3fc; border-radius:12px; padding:12px; margin-bottom:12px; font-size:12px; line-height:1.5; color:#164e63;">
          <div><strong>• Trecho Crítico:</strong> PE-60 (km 14 · Próximo ao Trevo de Suape)</div>
          <div><strong>• Lâmina d'Água Detectada:</strong> 35 cm (Impassível para coletivos baixos)</div>
          <div><strong>• Desvio Automático:</strong> Linha 199 desviada 800m via via marginal asfaltada.</div>
          <div><strong>• Parada Provisória:</strong> Em frente à UPA de Ipojuca com iluminação.</div>
        </div>

        <!-- PROTOCOLO DE SOCORRO DE TRANSBORDO -->
        <div style="background:#fef2f2; border:1px solid #fecaca; border-radius:12px; padding:10px; margin-bottom:12px; font-size:11.5px; color:#991b1b; line-height:1.4;">
          <strong>🚨 Protocolo Anti-Abandono (Crise da Frota):</strong> Em caso de pane mecânica no meio da rodovia, o GrafoParada despacha automaticamente o veículo reserva do TI Cabo para resgate imediato dos passageiros.
        </div>

        <button class="btn-primary" onclick="simulateTransbordoRescue()" style="background:#0891b2; margin-bottom:8px;">
          🔧 Simular Pane & Resgate por Transbordo
        </button>
        <button class="btn-secondary" onclick="closeFloodModal()">Fechar</button>
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

        // CartoDB Voyager tiles: fast Cloudflare edge, high contrast road labels, clean transit styling
        const tileLayer = L.tileLayer("https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png", {
          subdomains: "abcd",
          maxZoom: 19
        });
        tileLayer.addTo(leafletMap);

        routePolylineLayer = L.layerGroup().addTo(leafletMap);
        stopsMarkersLayer = L.layerGroup().addTo(leafletMap);

        drawRoute(TELEMETRIA);
        selectStop(1, false);

        // Multiple invalidation passes to guarantee rendering on any screen/resize
        setTimeout(function() { if (leafletMap) leafletMap.invalidateSize(); }, 100);
        setTimeout(function() { if (leafletMap) leafletMap.invalidateSize(); }, 350);
        setTimeout(function() { if (leafletMap) leafletMap.invalidateSize(); }, 800);

        window.addEventListener("resize", function() {
          if (leafletMap) leafletMap.invalidateSize();
        });
      } catch (err) {
        console.error("Leaflet map init error:", err);
      }
    }

    function drawRoute(telemetria) {
      if (!leafletMap) return;
      if (routePolylineLayer) routePolylineLayer.clearLayers();
      if (stopsMarkersLayer) stopsMarkersLayer.clearLayers();

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
        const popupContent = '<div style="font-family:Plus Jakarta Sans,sans-serif; min-width:220px;">' +
          '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:3px;">' +
            '<span style="font-size:10px; font-weight:800; background:#f1f5f9; color:#475569; padding:1px 5px; border-radius:4px;">CÓD ' + (st.stop_id || '') + '</span>' +
            '<span style="font-size:10.5px; font-weight:700; color:#047857;">' + (st.municipio || 'Grande Recife') + '</span>' +
          '</div>' +
          '<div style="font-size:13px; font-weight:800; color:#0f172a; line-height:1.25; margin-bottom:3px;">' + st.name + '</div>' +
          (st.ref ? '<div style="font-size:11px; color:#64748b; line-height:1.3; margin-bottom:4px;">📍 ' + st.ref + '</div>' : '') +
          '<div style="display:flex; justify-content:space-between; align-items:center; border-top:1px solid #e2e8f0; padding-top:6px; margin-top:4px;">' +
            '<div>' +
              '<div style="font-size:10px; color:#64748b; font-weight:700;">PREVISÃO STGCN:</div>' +
              '<div style="font-size:16px; font-weight:800; color:#059669; font-family:JetBrains Mono,monospace;">' + (st.stgcn_horizon_min && st.stgcn_horizon_min[1] ? st.stgcn_horizon_min[1].toFixed(0) : '4') + ' min</div>' +
            '</div>' +
            '<button onclick="selectStop(' + st.seq + ', true); if(leafletMap) leafletMap.closePopup();" style="background:#059669; color:#fff; border:none; padding:5px 12px; border-radius:6px; font-size:11.5px; font-weight:800; cursor:pointer;">Selecionar ➔</button>' +
          '</div>' +
        '</div>';

        m.bindPopup(popupContent);
        m.on("click", function() { selectStop(st.seq, false); });
        stopsMarkersLayer.addLayer(m);
      });

      renderStopsAccordion(telemetria);
    }

    function selectStop(seq, pan) {
      activeStopSeq = seq;
      const st = TELEMETRIA.stops.find(function(s) { return s.seq === seq; }) || TELEMETRIA.stops[0];

      // Update current stop name with rich CTM details
      const nameEl = document.getElementById("current-stop-name");
      if (nameEl) {
        nameEl.innerHTML = '<div style="display:flex; flex-direction:column; gap:2px;">' +
          '<div style="display:flex; align-items:center; gap:6px;">' +
            '<span style="font-size:10.5px; font-weight:800; background:#f1f5f9; color:#475569; padding:2px 6px; border-radius:6px; border:1px solid #cbd5e1;">CÓD ' + (st.stop_id || '030613') + '</span>' +
            '<span style="font-size:11px; font-weight:800; color:#047857;">📍 ' + (st.municipio || 'Ipojuca') + '</span>' +
            (st.has_shelter ? '<span style="font-size:10px; background:#dcfce7; color:#15803d; padding:1px 5px; border-radius:4px; font-weight:700;">🏠 Abrigo Coberto</span>' : '<span style="font-size:10px; background:#fee2e2; color:#b91c1c; padding:1px 5px; border-radius:4px; font-weight:700;">☀️ Sem Abrigo</span>') +
          '</div>' +
          '<div style="font-size:14.5px; font-weight:800; color:var(--text-main); margin-top:2px;">' + st.name + '</div>' +
          (st.ref ? '<div style="font-size:11px; color:var(--text-secondary);">Ref: ' + st.ref + ' · Sentido TI Cabo</div>' : '') +
        '</div>';
      }

      // Update ETA
      const etaNum = document.getElementById("live-eta-num");
      const restingEta = document.getElementById("resting-eta-val");
      const etaVal = (st.stgcn_horizon_min && st.stgcn_horizon_min[1]) ? st.stgcn_horizon_min[1].toFixed(0) : "4";
      if (etaNum) etaNum.textContent = etaVal;
      if (restingEta) restingEta.textContent = etaVal;

      // Trigger Haptic and audio if <= 2 min
      if (parseInt(etaVal) <= 2) {
        triggerArrivalAlert();
      }

      if (pan && leafletMap) {
        leafletMap.panTo([st.lat, st.lon], { animate: true, duration: 0.4 });
      }
    }

    function speakCurrentArrival() {
      const st = (TELEMETRIA && TELEMETRIA.stops) ? (TELEMETRIA.stops.find(function(s) { return s.seq === activeStopSeq; }) || TELEMETRIA.stops[0]) : null;
      const stopName = st ? st.name : "Parada de Camela";
      const eta = (st && st.stgcn_horizon_min && st.stgcn_horizon_min[1]) ? st.stgcn_horizon_min[1].toFixed(0) : "4";
      playSimpleChime();
      playNaturalVoice("Próximo ônibus da Linha 199 chega em " + eta + " minutos na parada " + stopName + ". Destino Terminal Integrado do Cabo.");
    }

    function renderStopsAccordion(telemetria) {
      const container = document.getElementById("stops-container");
      const labelCount = document.getElementById("stops-count-label");
      if (labelCount) labelCount.textContent = telemetria.stops.length;
      if (!container) return;

      // Group stops by trecho
      const groups = {};
      telemetria.stops.forEach(function(st) {
        const tr = st.trecho || "Paradas da Rodovia";
        if (!groups[tr]) groups[tr] = [];
        groups[tr].push(st);
      });

      let html = "";
      Object.keys(groups).forEach(function(trechoName) {
        html += '<div style="font-size:11.5px; font-weight:800; color:var(--text-secondary); text-transform:uppercase; margin:10px 0 4px; padding-left:4px; letter-spacing:0.04em;">' +
          trechoName + ' (' + groups[trechoName].length + ' paradas)' +
        '</div>';

        groups[trechoName].forEach(function(st) {
          const isSel = st.seq === activeStopSeq;
          html += '<div style="background:' + (isSel ? '#ecfdf5; border:2px solid #059669;' : 'var(--bg-page); border:1px solid var(--border-color);') + ' border-radius:12px; padding:10px 12px; margin-bottom:6px; display:flex; justify-content:space-between; align-items:center; cursor:pointer; transition:all 0.15s ease;" onclick="selectStop(' + st.seq + ', true)">' +
            '<div style="max-width:78%;">' +
              '<div style="display:flex; align-items:center; gap:6px; margin-bottom:2px;">' +
                '<span style="font-size:10px; font-weight:800; background:#f1f5f9; color:#475569; padding:1px 5px; border-radius:4px;">#' + String(st.seq).padStart(2, '0') + '</span>' +
                '<span style="font-size:10px; font-weight:800; color:#0369a1;">CÓD ' + (st.stop_id || '') + '</span>' +
                (st.has_shelter ? '<span style="font-size:10px; color:#15803d;">🏠 Abrigo</span>' : '<span style="font-size:10px; color:#94a3b8;">☀️ Sem Abrigo</span>') +
              '</div>' +
              '<div style="font-size:13px; font-weight:800; color:#0f172a; line-height:1.25;">' + st.name + '</div>' +
              '<div style="font-size:11px; color:#64748b; margin-top:2px;">' + (st.ref || st.bairro || '') + '</div>' +
            '</div>' +
            '<div style="text-align:right;">' +
              '<div style="font-family:JetBrains Mono,monospace; font-size:16px; font-weight:800; color:' + (isSel ? '#059669' : 'var(--text-main)') + ';">' + (st.stgcn_horizon_min && st.stgcn_horizon_min[1] ? st.stgcn_horizon_min[1].toFixed(0) : '4') + ' <span style="font-size:11px;">min</span></div>' +
              '<div style="font-size:10px; font-weight:700; color:#15803d;">Sentado</div>' +
            '</div>' +
          '</div>';
        });
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

    // SEARCH AUTOCOMPLETE LOGIC (RODADA: NOMES DE PARADAS, LOCALIDADES E TERMINAIS SEI)
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

      // 1. Check terminals SEI (26 TIs)
      if (typeof SEI_TERMINALS !== "undefined" && SEI_TERMINALS) {
        SEI_TERMINALS.forEach(function(t) {
          const full = (t.ti_name + " " + t.municipio + " " + (t.bairro || "")).toLowerCase();
          if (full.includes(q) || ("ti " + full).includes(q)) {
            results.push({
              type: "terminal",
              title: t.ti_name,
              sub: t.municipio + " (" + (t.bairro || "SEI") + ") · Integração VEM R$ 4,10",
              lat: t.lat,
              lon: t.lon
            });
          }
        });
      }

      // 2. Check PE-60 Stops (43 Authentic Stops)
      if (typeof TELEMETRIA_199 !== "undefined" && TELEMETRIA_199.stops) {
        TELEMETRIA_199.stops.forEach(function(st) {
          const stopSearch = ((st.name || "") + " " + (st.ref || "") + " " + (st.bairro || "") + " " + (st.municipio || "") + " " + (st.stop_id || "")).toLowerCase();
          if (stopSearch.includes(q)) {
            results.push({
              type: "stop",
              title: st.name,
              sub: "Cód " + st.stop_id + " · " + (st.municipio || "PE-60") + " (" + (st.ref || "") + ")",
              seq: st.seq,
              lat: st.lat,
              lon: st.lon,
              eta: (st.stgcn_horizon_min && st.stgcn_horizon_min[1]) ? st.stgcn_horizon_min[1].toFixed(0) : "4"
            });
          }
        });
      }

      // 3. Check Priority Lines
      const priorityLines = [
        { code: "199", title: "Linha 199 - Camela / TI Cabo", sub: "Via PE-60 · São Judas Tadeu (SJT)", terms: ["199", "camela", "cabo", "sjt"] },
        { code: "178", title: "Linha 178 - Porto de Suape / TI Cabo", sub: "Via Refinaria & Estaleiro", terms: ["178", "suape", "porto"] },
        { code: "185", title: "Linha 185 - TI Cabo / Cais de Santa Rita", sub: "Expresso Centro do Recife", terms: ["185", "santa rita", "recife"] },
        { code: "191", title: "Linha 191 - Recife / Porto de Galinhas", sub: "Via Nossa Senhora do Ó & PE-60", terms: ["191", "porto de galinhas", "galinhas", "nossa senhora do o"] },
        { code: "196", title: "Linha 196 - TI Cabo / Porto de Galinhas", sub: "Via PE-60 & Ipojuca", terms: ["196", "porto", "ipojuca"] }
      ];

      priorityLines.forEach(function(l) {
        if (l.terms.some(function(term) { return q.includes(term) || term.includes(q); })) {
          results.push({ type: "route", title: l.title, sub: l.sub, code: l.code });
        }
      });

      if (results.length === 0) {
        drop.innerHTML = '<div style="padding:12px; font-size:12px; color:var(--text-muted); text-align:center;">Nenhum terminal, parada da PE-60 ou linha encontrado para "' + query + '".</div>';
        drop.style.display = "flex";
        return;
      }

      window.currentSearchResults = results.slice(0, 8);
      let html = "";
      window.currentSearchResults.forEach(function(r, idx) {
        if (r.type === "terminal") {
          html += '<div class="search-item" onclick="selectSearchedResult(' + idx + ')">' +
            '<div><strong style="color:var(--blue-accent);">🏛️ ' + r.title + '</strong><div style="font-size:11px; color:var(--text-secondary);">' + r.sub + '</div></div>' +
            '<span style="font-size:11.5px; font-weight:700; color:var(--blue-accent); background:#e0f2fe; padding:2px 8px; border-radius:6px;">T.I. SEI</span>' +
          '</div>';
        } else if (r.type === "stop") {
          html += '<div class="search-item" onclick="selectSearchedResult(' + idx + ')">' +
            '<div><strong style="color:var(--brand-green-dark);">🚏 ' + r.title + '</strong><div style="font-size:11px; color:var(--text-secondary);">' + r.sub + '</div></div>' +
            '<span style="font-size:11.5px; font-weight:800; color:var(--brand-green-dark); background:#dcfce7; padding:2px 8px; border-radius:6px;">' + r.eta + ' min</span>' +
          '</div>';
        } else {
          html += '<div class="search-item" onclick="selectSearchedResult(' + idx + ')">' +
            '<div><strong style="color:#0f172a;">🚌 ' + r.title + '</strong><div style="font-size:11px; color:var(--text-secondary);">' + r.sub + '</div></div>' +
            '<span style="font-size:11.5px; font-weight:700; color:#059669; background:#ecfdf5; padding:2px 8px; border-radius:6px;">Linha</span>' +
          '</div>';
        }
      });

      drop.innerHTML = html;
      drop.style.display = "flex";
    }

    function selectSearchedResult(idx) {
      if (!window.currentSearchResults || !window.currentSearchResults[idx]) return;
      const r = window.currentSearchResults[idx];
      if (r.type === "terminal") {
        selectSearchedTerminal(r.lat, r.lon, r.title);
      } else if (r.type === "stop") {
        selectSearchedStop(r.seq);
      } else if (r.type === "route") {
        selectSearchedRoute(r.code);
      }
    }

    function selectSearchedStop(seq) {
      clearQuickSearch();
      selectStop(seq, true);
      playSimpleChime();
      const st = TELEMETRIA.stops.find(function(s) { return s.seq === seq; });
      if (st) {
        playNaturalVoice("Parada selecionada: " + st.name + ". Primeiro ônibus chegando em " + ((st.stgcn_horizon_min && st.stgcn_horizon_min[1]) ? st.stgcn_horizon_min[1].toFixed(0) : "4") + " minutos.");
      }
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


    // ==========================================
    // GUIA DOS 26 TERMINAIS INTEGRADOS DO SEI
    // ==========================================
    function openSeiTerminalsModal() {
      document.getElementById("modal-sei-terminals").style.display = "flex";
      renderSeiTerminalsList("all");
      playNaturalVoice("Abrindo guia completo dos vinte e seis Terminais Integrados do Grande Recife. Escolha um terminal para ver no mapa ou traçar rota integrada.");
    }

    function closeSeiTerminalsModal() {
      document.getElementById("modal-sei-terminals").style.display = "none";
    }

    function filterTerminalsByRegion(region) {
      document.querySelectorAll(".ti-filter-btn").forEach(function(b) {
        b.style.background = "#f1f5f9";
        b.style.color = "#475569";
        b.style.border = "1px solid #cbd5e1";
      });
      const act = document.getElementById("btn-ti-filter-" + region);
      if (act) {
        act.style.background = "#0284c7";
        act.style.color = "#ffffff";
        act.style.border = "none";
      }
      renderSeiTerminalsList(region);
    }

    function renderSeiTerminalsList(region) {
      const box = document.getElementById("sei-terminals-list-box");
      if (!box || !SEI_TERMINALS) return;

      const filtered = SEI_TERMINALS.filter(function(t) {
        if (region === "all") return true;
        const mun = (t.municipio || "").toLowerCase();
        const nm = (t.ti_name || "").toLowerCase();
        if (region === "sul") return mun.includes("cabo") || mun.includes("jaboatão") || nm.includes("aeroporto") || nm.includes("prazeres") || nm.includes("cajueiro");
        if (region === "recife") return mun.includes("recife");
        if (region === "norte") return mun.includes("olinda") || mun.includes("paulista") || mun.includes("abreu") || mun.includes("igarassu");
        if (region === "oeste") return mun.includes("camaragibe") || mun.includes("jaboatão") || nm.includes("tip") || nm.includes("caxangá");
        return true;
      });

      window.currentFilteredTerminals = filtered;
      let html = "";
      filtered.forEach(function(t, idx) {
        const linesStr = (t.linhas_principais && t.linhas_principais.length) ? t.linhas_principais.join(", ") : "Linhas Alimentadoras";
        html += '<div style="background:var(--bg-page); border:1.5px solid var(--border-color); border-radius:12px; padding:10px 12px; display:flex; justify-content:space-between; align-items:center;">' +
          '<div>' +
            '<div style="font-size:13px; font-weight:800; color:#0f172a;">🏛️ ' + t.ti_name + '</div>' +
            '<div style="font-size:11px; color:#64748b; margin-top:2px;">📍 ' + t.municipio + ' (' + (t.bairro || '') + ')</div>' +
            '<div style="font-size:10.5px; color:#0284c7; font-weight:700; margin-top:3px;">🚌 Linhas: ' + linesStr + '</div>' +
          '</div>' +
          '<button onclick="flyToFilteredTerminal(' + idx + ')" style="background:#0284c7; color:#ffffff; border:none; border-radius:8px; padding:6px 12px; font-size:11.5px; font-weight:800; cursor:pointer; white-space:nowrap;">' +
            'Ver no Mapa ➔' +
          '</button>' +
        '</div>';
      });

      box.innerHTML = html;
    }

    function flyToFilteredTerminal(idx) {
      if (!window.currentFilteredTerminals || !window.currentFilteredTerminals[idx]) return;
      const t = window.currentFilteredTerminals[idx];
      flyToTerminal(t.lat, t.lon, t.ti_name, t.municipio);
    }

    function flyToTerminal(lat, lon, name, mun) {
      closeSeiTerminalsModal();
      if (leafletMap) {
        leafletMap.flyTo([lat, lon], 16, { animate: true, duration: 0.8 });
        const popup = '<div style="font-family:Plus Jakarta Sans,sans-serif; min-width:200px;">' +
          '<div style="font-size:10.5px; font-weight:800; color:#0284c7; text-transform:uppercase;">Terminal Integrado do SEI</div>' +
          '<div style="font-size:14px; font-weight:800; color:#0f172a; margin:3px 0;">🏛️ ' + name + '</div>' +
          '<div style="font-size:11px; color:#475569;">📍 ' + mun + ' · Integração Temporal VEM (R$ 4,10)</div>' +
          '<div style="font-size:11px; color:#059669; font-weight:700; margin-top:4px;">✅ Baldeação física e temporal garantida</div>' +
        '</div>';
        L.popup().setLatLng([lat, lon]).setContent(popup).openOn(leafletMap);
        playSimpleChime();
        playNaturalVoice("Exibindo no mapa o " + name + " em " + mun + ".");
      }
    }


        // NEURAL TTS

    // ==========================================
    // MODO FÁCIL / SÊNIOR (ACESSIBILIDADE UNIVERSAL)
    // ==========================================
    let isSeniorMode = false;
    function toggleSeniorMode() {
      isSeniorMode = !isSeniorMode;
      document.body.classList.toggle("mode-senior", isSeniorMode);
      const pillLabel = document.getElementById("label-senior-pill");
      const voiceBtn = document.getElementById("btn-senior-voice-action");
      if (isSeniorMode) {
        if (pillLabel) pillLabel.textContent = "Padrão";
        if (voiceBtn) voiceBtn.style.display = "flex";
        playNaturalVoice("Modo Fácil ativado. Letras grandes e som alto. Seu ônibus 199 chega em 4 minutos na Plataforma 4. Tem 14 bancos vazios pra sentar.");
      } else {
        if (pillLabel) pillLabel.textContent = "Aa Fácil";
        if (voiceBtn) voiceBtn.style.display = "none";
        playNaturalVoice("Modo padrão ativado.");
      }
    }

    function speakSeniorDirections() {
      playNaturalVoice("Dona Severina, o ônibus 199 de Camela para o Cabo chega em 4 minutos. Tem 14 bancos vazios pra sentar. Pode aguardar com tranquilidade na Plataforma 4.");
    }

    // ==========================================
    // CENTRAL CTM · REALOCAÇÃO DE FROTA NO VAZIO
    // ==========================================
    let isFleetReallocated = false;
    function openDispatchModal() {
      document.getElementById("modal-dispatch").style.display = "flex";
    }
    function closeDispatchModal() {
      document.getElementById("modal-dispatch").style.display = "none";
    }
    function executeFleetReallocation() {
      isFleetReallocated = true;
      closeDispatchModal();

      const bannerR = document.getElementById("resting-reallocation-banner");
      const bannerA = document.getElementById("active-reallocation-banner");
      const msg = "✨ <strong>FROTA REFORÇADA PELO CTM!</strong> 1 ônibus extra foi transferido da Linha 178 (vazia) para a Linha 199 com base na demanda da sua parada!";
      if (bannerR) { bannerR.innerHTML = msg; bannerR.style.display = "block"; }
      if (bannerA) { bannerA.innerHTML = msg; bannerA.style.display = "block"; }

      const etaNum = document.getElementById("live-eta-num");
      if (etaNum) etaNum.textContent = "4";

      if ("vibrate" in navigator) {
        navigator.vibrate([200, 100, 200, 100, 400]);
      }
      playSimpleChime();
      playNaturalVoice("Atenção! O Consórcio Grande Recife acabou de remanejar um ônibus extra da Linha 178 para atender a demanda de passageiros da sua parada. Ele chega em 4 minutos na Plataforma 4.");
    }

    // ==========================================
    // MODAL AUDITORIA DE USABILIDADE
    // ==========================================
    function openAuditModal() {
      document.getElementById("modal-audit").style.display = "flex";
    }
    function closeAuditModal() {
      document.getElementById("modal-audit").style.display = "none";
    }


    // ==========================================
    // FAROL NOTURNO DE EMBARQUE (ANTI-QUEIMA DE PARADA)
    // ==========================================
    function activateNightBeacon() {
      document.getElementById("night-beacon-screen").style.display = "flex";
      playNaturalVoice("Farol noturno ativado! Aponte a tela iluminada em direção à rodovia para sinalizar ao motorista da Linha 199 no escuro.");
      if ("vibrate" in navigator) {
        navigator.vibrate([100, 50, 100]);
      }
    }
    function deactivateNightBeacon() {
      document.getElementById("night-beacon-screen").style.display = "none";
    }

    // ==========================================
    // AUDITORIA FORENSE DE QUEIMA DE PARADA
    // ==========================================
    function simulateQueimaDeParada() {
      document.getElementById("modal-queima-parada").style.display = "flex";
      if ("vibrate" in navigator) {
        navigator.vibrate([400, 200, 400, 200, 800]);
      }
      playSimpleChime();
      playNaturalVoice("Alerta urgente: Queima de parada detectada pelo satélite! O veículo 199-04 cruzou a Parada 030613 a 44 km por hora sem parar. A prova técnica foi gerada para denúncia no WhatsApp do CTM.");
    }
    function closeQueimaModal() {
      document.getElementById("modal-queima-parada").style.display = "none";
    }
    function sendQueimaWhatsAppReport() {
      const lines = [
        "DENÚNCIA DE QUEIMA DE PARADA (CTM - Grande Recife)",
        "Linha: 199 - Camela/Cabo (SJT)",
        "Veículo: 199-04 (Placa PE-4912)",
        "Parada: 030613 - Terminal Camela",
        "Velocidade no ponto: 44 km/h (sem parada)",
        "Data/Hora: 10/11/2026 22:41:12",
        "Registrado via auditoria de satélite GrafoParada."
      ];
      const sep = String.fromCharCode(10);
      window.open("https://api.whatsapp.com/send?phone=5581994883999&text=" + encodeURIComponent(lines.join(sep)), "_blank");
    }

    // ==========================================
    // GUARDIÃO DA INTEGRAÇÃO TEMPORAL (VEM)
    // ==========================================
    function openVemModal() {
      document.getElementById("modal-vem").style.display = "flex";
    }
    function closeVemModal() {
      document.getElementById("modal-vem").style.display = "none";
    }


    // ==========================================
    // DESEMBARQUE SEGURO NOTURNO (LEI 15.878/2016)
    // ==========================================
    function openSafeDisembarkModal() {
      document.getElementById("modal-safe-disembark").style.display = "flex";
      playNaturalVoice("Modo Desembarque Seguro Noturno. Pela Lei Estadual 15.878, você tem direito de desembarcar em qualquer local mais iluminado após as 22 horas.");
    }
    function closeSafeDisembarkModal() {
      document.getElementById("modal-safe-disembark").style.display = "none";
    }
    function speakDriverCourtesyAudio() {
      playNaturalVoice("Motorista, boa noite! Por favor, gostaria de desembarcar aqui no ponto iluminado, conforme a Lei Estadual 15.878. Muito obrigado pela cortesia!");
    }

    // ==========================================
    // RADAR DE ALAGAMENTO & SOCORRO DE TRANSBORDO
    // ==========================================
    let isFloodActive = false;
    function openFloodModal() {
      document.getElementById("modal-flood").style.display = "flex";
    }
    function closeFloodModal() {
      document.getElementById("modal-flood").style.display = "none";
    }
    function toggleFloodAlertSimulation() {
      isFloodActive = !isFloodActive;
      const banner = document.getElementById("flood-alert-banner");
      if (isFloodActive) {
        if (banner) {
          banner.innerHTML = "🌊 <strong>ALAGAMENTO NA PE-60 (KM 14):</strong> Linha 199 desviada 800m pela marginal. Embarque temporário na UPA de Ipojuca.";
          banner.style.display = "block";
        }
        playSimpleChime();
        playNaturalVoice("Atenção: Alagamento detectado na Rodovia PE-60 no quilômetro 14. O ônibus da Linha 199 fez um desvio de 800 metros pela via marginal e atenderá temporariamente no ponto da UPA de Ipojuca.");
      } else {
        if (banner) banner.style.display = "none";
        playNaturalVoice("Alerta de alagamento encerrado. Rodovia PE-60 liberada no itinerário normal.");
      }
    }
    function simulateTransbordoRescue() {
      closeFloodModal();
      const banner = document.getElementById("flood-alert-banner");
      if (banner) {
        banner.innerHTML = "🔧 <strong>PANE NO VEÍCULO 199-04:</strong> Carro reserva do TI Cabo despachado para transbordo. Chegada estimada em 7 minutos.";
        banner.style.background = "#ea580c";
        banner.style.borderColor = "#fdba74";
        banner.style.display = "block";
      }
      if ("vibrate" in navigator) {
        navigator.vibrate([200, 100, 200, 100, 400]);
      }
      playSimpleChime();
      playNaturalVoice("Atenção: Pane mecânica registrada no coletivo. O socorro mecânico e o veículo reserva foram despachados pelo TI Cabo e chegam em 7 minutos para transbordo seguro.");
    }


    // ==========================================
    // MINHA ROTINA PENDULAR (MAPEADOR DE TURNO)
    // ==========================================
    let currentRoutineType = "suape";
    const routineData = {
      suape: {
        title: "Indústria Suape (Camela ➔ TI Cabo) · Entrada 07h00",
        pill: "Rotina: 05h45",
        tag: "Turno Ativo · 05h45",
        advice: "💡 <strong>Janela de Saída:</strong> Caminhada de 6 min. Saia de casa às <strong>06:08</strong> para pegar o 199 das 06:14 sem mofar no ponto.",
        demand: "48 trabalhadores",
        audio: "Rotina do turno de Suape selecionada. O ônibus 199 passa na sua parada às 06h14. Saia de casa às 06h08 para não ficar esperando na beira da pista."
      },
      comercio: {
        title: "Comércio / Centro Cabo · Entrada 08h30",
        pill: "Rotina: 07h30",
        tag: "Turno Ativo · 07h30",
        advice: "💡 <strong>Janela de Saída:</strong> Caminhada de 5 min. Saia de casa às <strong>07:42</strong> para pegar o 199 das 07:48 no ponto.",
        demand: "35 trabalhadores",
        audio: "Rotina do comércio selecionada. Saia de casa às 07h42 para embarcar com tranquilidade."
      },
      noturno: {
        title: "Universitário / Noite (Camela ➔ Fachuca / UFRPE)",
        pill: "Rotina: 17h40",
        tag: "Turno Ativo · 17h40",
        advice: "💡 <strong>Janela de Saída:</strong> Caminhada de 6 min. Saia de casa às <strong>17:50</strong>. Modo Bolso Seguro recomendado na volta.",
        demand: "29 estudantes",
        audio: "Rotina universitária selecionada. Na volta às 22 horas, lembre de ativar o Modo Bolso Seguro e a Parada Segura."
      },
      saude: {
        title: "Plantão Saúde 12x36 (Camela ➔ UPA Ipojuca)",
        pill: "Rotina: 06h30",
        tag: "Turno Ativo · 06h30",
        advice: "💡 <strong>Janela de Saída:</strong> Caminhada de 5 min. Saia às <strong>06h40</strong>. Previsão de chegada na UPA às 06h54.",
        demand: "22 profissionais",
        audio: "Rotina de plantão de saúde selecionada. Bom plantão!"
      }
    };

    function openRoutineModal() {
      document.getElementById("modal-routine").style.display = "flex";
    }
    function closeRoutineModal() {
      document.getElementById("modal-routine").style.display = "none";
    }
    function selectRoutinePreset(type) {
      currentRoutineType = type;
      ["suape", "comercio", "noturno", "saude"].forEach(function(key) {
        const btn = document.getElementById("btn-routine-" + key);
        if (btn) {
          if (key === type) {
            btn.style.background = "#ecfdf5";
            btn.style.borderColor = "#059669";
          } else {
            btn.style.background = "#f8fafc";
            btn.style.borderColor = "#e2e8f0";
          }
        }
      });
    }
    function confirmRoutineChoice() {
      const data = routineData[currentRoutineType];
      if (data) {
        const titleEl = document.getElementById("routine-title-desc");
        const adviceEl = document.getElementById("routine-advice-desc");
        const tagEl = document.getElementById("routine-tag-pill");
        const pillEl = document.getElementById("label-routine-pill");

        if (titleEl) titleEl.textContent = data.title;
        if (adviceEl) adviceEl.innerHTML = data.advice;
        if (tagEl) tagEl.textContent = data.tag;
        if (pillEl) pillEl.textContent = data.pill;

        playSimpleChime();
        playNaturalVoice(data.audio);
      }
      closeRoutineModal();
    }

    // ==========================================
    // MODO OFFLINE INERCIAL NA PE-60
    // ==========================================
    let isOfflineInertial = false;
    function toggleOfflineInertialSimulation() {
      isOfflineInertial = !isOfflineInertial;
      const banner = document.getElementById("offline-inertial-banner");
      if (isOfflineInertial) {
        if (banner) banner.style.display = "block";
        playSimpleChime();
        playNaturalVoice("Sinal 4G indisponível no quilômetro 12 da PE-60. Modo Offline Inercial ativado: a previsão do ônibus está sendo calculada pela memória local do grafo sem travar o aplicativo.");
      } else {
        if (banner) banner.style.display = "none";
        playNaturalVoice("Conexão 4G restabelecida. Telemetria em tempo real sincronizada.");
      }
    }

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
