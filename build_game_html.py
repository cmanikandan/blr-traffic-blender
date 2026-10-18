import base64
import glob
import gzip
import json
import os

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(WORKSPACE_DIR, "assets")

def build_embedded_glb_dict():
    embedded = {}
    for path in sorted(glob.glob(os.path.join(ASSETS_DIR, "*.glb"))):
        name = os.path.basename(path)
        with open(path, "rb") as f:
            raw = f.read()
        gz = gzip.compress(raw, compresslevel=9)
        embedded[name] = base64.b64encode(gz).decode("ascii")
    return embedded

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ಒಂದು ಸೆಕೆಂಡ್ | Ondu Second: Bangalore Gravity Glitch — Pro 3D WebGL Arcade</title>
  <style>
    :root {
      --in-oklab: ;
      --in-oklch: ;
      --auto-yellow: #ffd000;
      --auto-green: #009a44;
      --swiggy-orange: #fc8019;
      --zepto-green: #10f560;
      --blinkit-yellow: #ffe600;
      --nh-green: #006b38;
      --danger-red: #ff3b5c;
      --cop-blue: #2563eb;
      --grip-pct: 100%;
      --grip-hue: 145;
      --speed-pct: 50%;
    }

    @supports (background: linear-gradient(in oklab, white, black)) {
      :root {
        --in-oklab: in oklab;
        --in-oklch: in oklch;
      }
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      user-select: none;
    }

    html, body {
      width: 100%;
      height: 100%;
      overflow: hidden;
      background: #0f172a;
      color: #f8fafc;
      font-family: 'Inter', 'Noto Sans Kannada', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    #game-canvas {
      position: fixed;
      inset: 0;
      width: 100%;
      height: 100%;
      display: block;
      z-index: 1;
    }

    /* Cinematic Vignette & Optional Police Strobe Screen Edge */
    .vignette-overlay {
      position: fixed;
      inset: 0;
      pointer-events: none;
      z-index: 4;
      background: radial-gradient(circle at 50% 50%, transparent 62%, rgba(4, 8, 18, 0.55) 100%);
      transition: box-shadow 0.15s ease;
    }

    .vignette-overlay.cop-strobe {
      animation: police-screen-flash 0.36s infinite alternate;
    }

    @keyframes police-screen-flash {
      0% { box-shadow: inset 0 0 65px rgba(239, 68, 68, 0.55); }
      100% { box-shadow: inset 0 0 65px rgba(37, 99, 235, 0.55); }
    }

    /* =========================================================================
       PROFESSIONAL 4-CORNER ARCADE HUD (Responsive, Zero Overflow)
       ========================================================================= */
    .hud-layer {
      position: fixed;
      inset: 0;
      z-index: 10;
      pointer-events: none;
      padding: 14px 18px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }

    .hud-top-row,
    .hud-bottom-row {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 12px;
      width: 100%;
    }

    .hud-bottom-row {
      align-items: flex-end;
    }

    .interactive {
      pointer-events: auto;
    }

    /* Top-Left: Authentic Bengaluru Digital Auto Fare Meter */
    .auto-fare-unit {
      background: linear-gradient(165deg var(--in-oklab), rgba(20, 24, 33, 0.94), rgba(9, 12, 18, 0.96));
      border: 2px solid var(--auto-yellow);
      border-radius: 14px;
      padding: 10px 15px;
      min-width: 210px;
      box-shadow: 0 14px 32px rgba(0, 0, 0, 0.55), inset 0 1px 0 rgba(255, 255, 255, 0.14);
      position: relative;
      overflow: hidden;
      backdrop-filter: blur(12px);
    }

    .auto-fare-unit::before {
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 4px;
      --c1: #ffd000;
      --c2: #111318;
      background: repeating-linear-gradient(-45deg, var(--c1) 0 8px, var(--c2) 0 16px);
    }

    .meter-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 2px;
      margin-bottom: 4px;
      font-size: 0.64rem;
      font-weight: 800;
      letter-spacing: 0.08em;
      color: #94a3b8;
      text-transform: uppercase;
      gap: 8px;
    }

    .meter-status-dot {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      color: #4ade80;
      font-weight: 800;
    }

    .meter-status-dot::before {
      content: "";
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: #4ade80;
      box-shadow: 0 0 8px #4ade80;
    }

    .meter-screen {
      background: #05070b;
      border: 1px solid rgba(255, 208, 0, 0.25);
      border-radius: 8px;
      padding: 6px 10px;
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      gap: 12px;
    }

    .fare-digits {
      font-family: 'Courier New', ui-monospace, monospace;
      font-size: 1.5rem;
      font-weight: 900;
      color: #ff4757;
      text-shadow: 0 0 12px rgba(255, 71, 87, 0.55);
      letter-spacing: 0.03em;
    }

    .fare-sub {
      font-family: 'Courier New', ui-monospace, monospace;
      font-size: 0.75rem;
      font-weight: 800;
      color: var(--auto-yellow);
    }

    .dl-status-strip {
      margin-top: 5px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.63rem;
      font-weight: 800;
      color: #cbd5e1;
      letter-spacing: 0.04em;
    }

    .dl-badge {
      background: rgba(34, 197, 94, 0.18);
      border: 1px solid rgba(34, 197, 94, 0.45);
      color: #86efac;
      padding: 1px 6px;
      border-radius: 4px;
    }

    /* Top-Center: Authentic Bilingual (Kannada + English) Indian Highway Sign Banner */
    .highway-sign-cluster {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 7px;
      max-width: 500px;
    }

    .nh-sign-board {
      background: linear-gradient(180deg var(--in-oklab), #007a40, #004d27);
      border: 2.5px solid #ffffff;
      border-radius: 11px;
      padding: 6px 18px;
      box-shadow: 0 12px 28px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.25);
      display: flex;
      align-items: center;
      gap: 11px;
      color: #ffffff;
    }

    .nh-shield {
      background: var(--auto-yellow);
      color: #0b0e14;
      font-weight: 900;
      font-size: 0.68rem;
      padding: 3px 7px;
      border-radius: 4px;
      letter-spacing: 0.06em;
      border: 1px solid #0b0e14;
      white-space: nowrap;
    }

    .nh-text-stack {
      display: flex;
      flex-direction: column;
      line-height: 1.18;
    }

    .nh-kn {
      font-size: 0.86rem;
      font-weight: 900;
      color: #fde047;
      letter-spacing: 0.02em;
    }

    .nh-en {
      font-size: 0.70rem;
      font-weight: 800;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: #ffffff;
    }

    .rain-banner {
      background: linear-gradient(90deg var(--in-oklab), rgba(2, 132, 199, 0.94), rgba(79, 70, 229, 0.94));
      border: 1px solid #7dd3fc;
      color: #ffffff;
      padding: 5px 14px;
      border-radius: 999px;
      font-size: 0.70rem;
      font-weight: 800;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      display: none;
      box-shadow: 0 6px 20px rgba(2, 132, 199, 0.45);
    }

    .rain-banner.visible {
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }

    /* BTP Traffic Cop Sudden License Check Alert Banner */
    .cop-alert-banner {
      background: linear-gradient(95deg var(--in-oklab), rgba(15, 23, 42, 0.96), rgba(30, 41, 59, 0.96));
      border: 2px solid #ef4444;
      color: #ffffff;
      padding: 8px 16px;
      border-radius: 12px;
      display: none;
      align-items: center;
      gap: 12px;
      box-shadow: 0 12px 30px rgba(239, 68, 68, 0.45);
      animation: cop-border-pulse 0.4s infinite alternate;
    }

    .cop-alert-banner.visible {
      display: inline-flex;
    }

    @keyframes cop-border-pulse {
      from { border-color: #ef4444; box-shadow: 0 0 22px rgba(239, 68, 68, 0.55); }
      to { border-color: #3b82f6; box-shadow: 0 0 22px rgba(59, 130, 246, 0.55); }
    }

    .cop-alert-text {
      display: flex;
      flex-direction: column;
      gap: 2px;
    }

    .cop-alert-kn {
      font-size: 0.82rem;
      font-weight: 900;
      color: #fde047;
    }

    .cop-alert-en {
      font-size: 0.68rem;
      font-weight: 800;
      color: #f8fafc;
      letter-spacing: 0.04em;
    }

    .cop-dl-btn {
      appearance: none;
      background: #22c55e;
      color: #052e16;
      border: none;
      border-radius: 8px;
      padding: 6px 11px;
      font-size: 0.72rem;
      font-weight: 900;
      cursor: pointer;
      white-space: nowrap;
      box-shadow: 0 4px 12px rgba(34, 197, 94, 0.4);
    }

    .cop-dl-btn:hover {
      filter: brightness(1.1);
    }

    /* Top-Right: Compact Glass Pill Toolbar */
    .top-toolbar {
      display: flex;
      align-items: center;
      gap: 5px;
      background: rgba(15, 23, 42, 0.86);
      border: 1px solid rgba(255, 255, 255, 0.16);
      border-radius: 12px;
      padding: 5px;
      backdrop-filter: blur(12px);
      box-shadow: 0 10px 26px rgba(0, 0, 0, 0.4);
      flex-wrap: wrap;
      justify-content: flex-end;
    }

    .mode-segmented {
      display: flex;
      background: rgba(0, 0, 0, 0.38);
      border-radius: 8px;
      padding: 2px;
      gap: 2px;
    }

    .tool-btn {
      appearance: none;
      border: 1px solid transparent;
      background: transparent;
      color: #cbd5e1;
      font-size: 0.72rem;
      font-weight: 700;
      padding: 6px 9px;
      border-radius: 7px;
      cursor: pointer;
      transition: background-color 0.06s ease, color 0.06s ease;
      white-space: nowrap;
    }

    .tool-btn:hover {
      color: #ffffff;
      background: rgba(255, 255, 255, 0.09);
    }

    .tool-btn.active-mode {
      background: var(--auto-yellow);
      color: #0b0e14;
      font-weight: 900;
      box-shadow: 0 2px 10px rgba(255, 208, 0, 0.35);
    }

    .tool-btn.action-pill {
      background: rgba(255, 255, 255, 0.07);
      border-color: rgba(255, 255, 255, 0.14);
    }

    .tool-btn.action-pill:hover {
      border-color: var(--auto-yellow);
    }

    /* Bottom-Left: Minimalist Key Hints */
    .controls-card {
      background: rgba(15, 23, 42, 0.82);
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: 12px;
      padding: 10px 14px;
      backdrop-filter: blur(12px);
      display: flex;
      flex-wrap: wrap;
      gap: 8px 14px;
      font-size: 0.71rem;
      color: #e2e8f0;
      max-width: 520px;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
    }

    .key-item {
      display: inline-flex;
      align-items: center;
      gap: 5px;
    }

    kbd {
      background: rgba(255, 255, 255, 0.14);
      border: 1px solid rgba(255, 255, 255, 0.28);
      border-bottom-width: 2px;
      border-radius: 5px;
      padding: 1px 6px;
      font-family: ui-monospace, monospace;
      font-weight: 800;
      color: var(--auto-yellow);
      font-size: 0.67rem;
    }

    /* Bottom-Right: Sleek Speedometer & Auto Telemetry Cluster */
    .speed-cluster {
      background: rgba(15, 23, 42, 0.88);
      border: 1px solid rgba(255, 255, 255, 0.18);
      border-radius: 16px;
      padding: 12px 18px;
      backdrop-filter: blur(12px);
      min-width: 245px;
      box-shadow: 0 12px 30px rgba(0, 0, 0, 0.5);
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .speed-row {
      display: flex;
      justify-content: space-between;
      align-items: baseline;
    }

    .speed-num {
      font-size: 2.1rem;
      font-weight: 900;
      font-variant-numeric: tabular-nums;
      line-height: 1;
      color: #ffffff;
      letter-spacing: -0.02em;
    }

    .speed-unit {
      font-size: 0.72rem;
      font-weight: 800;
      color: var(--auto-yellow);
      margin-left: 4px;
    }

    .alt-badge {
      font-size: 0.7rem;
      font-weight: 800;
      color: #38bdf8;
      background: rgba(56, 189, 248, 0.14);
      border: 1px solid rgba(56, 189, 248, 0.35);
      padding: 2px 8px;
      border-radius: 99px;
    }

    .bar-group {
      display: flex;
      flex-direction: column;
      gap: 3px;
    }

    .bar-label {
      display: flex;
      justify-content: space-between;
      font-size: 0.64rem;
      font-weight: 800;
      letter-spacing: 0.06em;
      color: #94a3b8;
      text-transform: uppercase;
    }

    .bar-track {
      width: 100%;
      height: 6px;
      background: rgba(255, 255, 255, 0.12);
      border-radius: 99px;
      overflow: hidden;
    }

    .grip-fill {
      height: 100%;
      width: var(--grip-pct);
      background: hsl(var(--grip-hue) 90% 50%);
    }

    .wheel-status-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 4px;
      border-top: 1px solid rgba(255, 255, 255, 0.1);
    }

    .wheel-label {
      font-size: 0.64rem;
      font-weight: 800;
      color: #94a3b8;
      text-transform: uppercase;
    }

    .wheel-pills {
      display: flex;
      gap: 5px;
    }

    .wheel-pill {
      font-size: 0.62rem;
      font-weight: 800;
      padding: 2px 7px;
      border-radius: 5px;
      background: rgba(34, 197, 94, 0.18);
      border: 1px solid rgba(34, 197, 94, 0.55);
      color: #4ade80;
    }

    .wheel-pill.snapped {
      background: rgba(255, 59, 92, 0.28);
      border-color: var(--danger-red);
      color: #fda4af;
      animation: pulse-danger 0.5s infinite alternate;
    }

    @keyframes pulse-danger {
      from { transform: scale(1); }
      to { transform: scale(1.08); }
    }

    /* Comic Callout Popups */
    #callout-layer {
      position: fixed;
      inset: 0;
      pointer-events: none;
      z-index: 8;
      overflow: hidden;
    }

    .comic-pop {
      position: absolute;
      transform: translate(-50%, -50%);
      font-weight: 900;
      font-size: 0.90rem;
      letter-spacing: 0.02em;
      padding: 6px 13px;
      border-radius: 9px;
      background: var(--auto-yellow);
      color: #090d16;
      border: 2px solid #090d16;
      box-shadow: 0 8px 20px rgba(0, 0, 0, 0.45);
      white-space: nowrap;
      animation: float-up-fade 1.25s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    @keyframes float-up-fade {
      0% { opacity: 0; transform: translate(-50%, -20%) scale(0.7); }
      20% { opacity: 1; transform: translate(-50%, -65%) scale(1.04); }
      100% { opacity: 0; transform: translate(-50%, -145%) scale(0.95); }
    }

    /* =========================================================================
       NATIVE <dialog> DIFFICULTY & GRAVITY PROFILES OVERLAY
       ========================================================================= */
    dialog#gravity-modal {
      margin: auto;
      width: min(900px, 93vw);
      max-height: 91vh;
      overflow-y: auto;
      background: linear-gradient(160deg var(--in-oklab), rgba(15, 23, 42, 0.97), rgba(9, 13, 24, 0.99));
      color: #f8fafc;
      border: 2px solid rgba(255, 208, 0, 0.7);
      border-radius: 22px;
      padding: 0;
      box-shadow: 0 28px 70px rgba(0, 0, 0, 0.8);
    }

    dialog#gravity-modal::backdrop {
      background: rgba(6, 10, 20, 0.68);
      backdrop-filter: blur(8px);
    }

    .hazard-trim {
      height: 6px;
      width: 100%;
      --c1: #ffd000;
      --c2: #111318;
      background: repeating-linear-gradient(-45deg, var(--c1) 0 10px, var(--c2) 0 20px);
    }

    .modal-inner {
      padding: 22px 26px;
    }

    .modal-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      margin-bottom: 6px;
      flex-wrap: wrap;
    }

    .modal-badge {
      background: rgba(255, 208, 0, 0.16);
      border: 1px solid rgba(255, 208, 0, 0.45);
      color: var(--auto-yellow);
      font-size: 0.7rem;
      font-weight: 800;
      padding: 3px 10px;
      border-radius: 99px;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }

    .modal-inner h1 {
      font-size: 1.6rem;
      font-weight: 900;
      letter-spacing: -0.01em;
      color: #ffffff;
    }

    .modal-lead {
      color: #94a3b8;
      font-size: 0.86rem;
      line-height: 1.45;
      margin-top: 4px;
    }

    .mode-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 14px;
      margin: 16px 0;
    }

    .mode-card {
      background: rgba(30, 41, 59, 0.68);
      border: 1.5px solid rgba(255, 255, 255, 0.12);
      border-radius: 16px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 14px;
      cursor: pointer;
      transition: transform 0.16s ease, border-color 0.16s ease, background-color 0.16s ease;
    }

    .mode-card:hover,
    .mode-card.selected {
      transform: translateY(-3px);
      background: rgba(30, 41, 59, 0.94);
      border-color: var(--auto-yellow);
    }

    .mode-tag {
      display: inline-block;
      font-size: 0.66rem;
      font-weight: 800;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      padding: 3px 8px;
      border-radius: 6px;
      margin-bottom: 6px;
    }

    .tag-low { background: rgba(34, 197, 94, 0.18); color: #4ade80; }
    .tag-med { background: rgba(255, 208, 0, 0.18); color: #ffd000; }
    .tag-complex { background: rgba(255, 59, 92, 0.2); color: #fb7185; }

    .mode-card h2 {
      font-size: 1.1rem;
      font-weight: 800;
      color: #ffffff;
      margin-bottom: 4px;
    }

    .mode-desc {
      font-size: 0.78rem;
      color: #cbd5e1;
      line-height: 1.4;
      margin-bottom: 10px;
    }

    .mode-stats {
      list-style: none;
      font-size: 0.73rem;
      color: #94a3b8;
      display: flex;
      flex-direction: column;
      gap: 4px;
      border-top: 1px solid rgba(255, 255, 255, 0.08);
      padding-top: 8px;
    }

    .mode-stats li strong {
      color: #f1f5f9;
    }

    .launch-btn {
      width: 100%;
      padding: 10px 14px;
      border-radius: 10px;
      border: none;
      font-weight: 800;
      font-size: 0.8rem;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      cursor: pointer;
      background: var(--auto-yellow);
      color: #090d16;
      transition: filter 0.15s ease;
    }

    .launch-btn:hover {
      filter: brightness(1.08);
    }

    .asset-status-bar {
      padding: 10px 14px;
      border-radius: 12px;
      background: rgba(15, 23, 42, 0.78);
      border: 1px solid rgba(255, 255, 255, 0.08);
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 8px;
      font-size: 0.72rem;
      color: #94a3b8;
    }

    .asset-badges {
      display: flex;
      flex-wrap: wrap;
      gap: 5px;
    }

    .asset-chip {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 5px;
      padding: 2px 6px;
      font-family: ui-monospace, monospace;
      font-size: 0.63rem;
      color: #cbd5e1;
    }

    .asset-chip.loaded {
      border-color: rgba(34, 197, 94, 0.55);
      color: #86efac;
    }
  </style>

  <script type="importmap">
  {
    "imports": {
      "three": "https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js",
      "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.170.0/examples/jsm/"
    }
  }
  </script>
</head>
<body>
  <div class="vignette-overlay" id="vignette-fx"></div>

  <!-- 4-Corner Professional Arcade HUD -->
  <div class="hud-layer">
    <header class="hud-top-row">
      <!-- Top-Left: Authentic Bengaluru Auto Digital Fare Meter -->
      <div class="auto-fare-unit interactive">
        <div class="meter-header">
          <span>ನಮ್ಮ ಆಟೋ • KA-01 METER</span>
          <span class="meter-status-dot" id="surge-badge">1.0x HIRE</span>
        </div>
        <div class="meter-screen">
          <div class="fare-digits" id="hud-fare">₹30.00</div>
          <div class="fare-sub" id="hud-dist">0.0 KM</div>
        </div>
        <div class="dl-status-strip">
          <span>🪪 DIGILOCKER DL &amp; RC</span>
          <span class="dl-badge" id="hud-dl-status">VALID • PRESS [L]</span>
        </div>
      </div>

      <!-- Top-Center: Bilingual (Kannada + English) National Highway Sign & BTP Cop Alert -->
      <div class="highway-sign-cluster">
        <div class="nh-sign-board">
          <span class="nh-shield">NH 44</span>
          <div class="nh-text-stack">
            <span class="nh-kn" id="hud-landmark-kn">ಸಿಲ್ಕ್ ಬೋರ್ಡ್ ಮೇಲ್ಸೇತುವೆ • 45m</span>
            <span class="nh-en" id="hud-landmark">SILK BOARD FLYOVER GANTRY • 45m</span>
          </div>
        </div>
        <div class="cop-alert-banner interactive" id="hud-cop-alert">
          <div class="cop-alert-text">
            <span class="cop-alert-kn">👮‍♂️ ಬೆಂಗಳೂರು ಸಂಚಾರ ಪೊಲೀಸ್: "ಏಯ್ ಆಟೋ! ಸೈಡ್ ಹಾಕಿ! DL ತೋರಿಸಿ!"</span>
            <span class="cop-alert-en">BTP SUDDEN LICENSE CHECK AHEAD • SHOW DIGILOCKER DL OR SWERVE!</span>
          </div>
          <button type="button" class="cop-dl-btn" id="btn-show-dl">🪪 Show DL [L]</button>
        </div>
        <div class="rain-banner" id="hud-weather-alert">
          ⛈️ ಮುಂಗಾರು ಮಳೆ • MONSOON DOWNPOUR • TIRE FRICTION 0% (HYDROPLANING)
        </div>
      </div>

      <!-- Top-Right: Compact Glass Pill Toolbar -->
      <nav class="top-toolbar interactive" aria-label="Game Mode and Audio Controls">
        <div class="mode-segmented">
          <button type="button" class="tool-btn" data-quick-mode="low">Low</button>
          <button type="button" class="tool-btn active-mode" data-quick-mode="medium">Medium</button>
          <button type="button" class="tool-btn" data-quick-mode="complex">Peak Hour</button>
        </div>
        <button type="button" class="tool-btn action-pill" id="btn-horn-test">📯 Horn</button>
        <button type="button" class="tool-btn action-pill" id="btn-cop-test">👮 Cop Check</button>
        <button type="button" class="tool-btn action-pill" id="btn-rain-toggle">🌧️ Rain</button>
        <button type="button" class="tool-btn action-pill" id="btn-audio-toggle">🔊 Audio</button>
        <button type="button" class="tool-btn action-pill" id="btn-open-modal">⚙️ Menu</button>
      </nav>
    </header>

    <footer class="hud-bottom-row">
      <!-- Bottom-Left: Controls Guide -->
      <div class="controls-card interactive">
        <span class="key-item"><kbd>W</kbd><kbd>A</kbd><kbd>S</kbd><kbd>D</kbd> Steer &amp; Throttle</span>
        <span class="key-item"><kbd>SPACE</kbd> Gravity Glitch Hop</span>
        <span class="key-item"><kbd>H</kbd> Auto Horn ("Pa-Pa-Paarp!")</span>
        <span class="key-item"><kbd>L</kbd> Flash License to Cop</span>
        <span class="key-item"><kbd>R</kbd> Fix Wheel</span>
        <span class="key-item"><kbd>ESC</kbd> Menu</span>
      </div>

      <!-- Bottom-Right: Speedometer, Grip & 3-Wheel Status -->
      <div class="speed-cluster interactive">
        <div class="speed-row">
          <div>
            <span class="speed-num" id="hud-speed">65</span>
            <span class="speed-unit">KM/H</span>
          </div>
          <span class="alt-badge" id="hud-alt">ON ROAD</span>
        </div>

        <div class="bar-group">
          <div class="bar-label">
            <span>TIRE GRIP</span>
            <span id="hud-grip-text">100% DRY ASPHALT</span>
          </div>
          <div class="bar-track">
            <div class="grip-fill"></div>
          </div>
        </div>

        <div class="wheel-status-row">
          <span class="wheel-label">WHEELS</span>
          <div class="wheel-pills">
            <span class="wheel-pill" id="w-pill-0">FRONT</span>
            <span class="wheel-pill" id="w-pill-1">REAR-L</span>
            <span class="wheel-pill" id="w-pill-2">REAR-R</span>
          </div>
        </div>
      </div>
    </footer>
  </div>

  <!-- 3D Viewport -->
  <main>
    <canvas id="game-canvas" aria-label="Ondu Second 3D Bangalore Traffic Viewport"></canvas>
    <div id="callout-layer" aria-hidden="true"></div>
  </main>

  <!-- Native Modal Dialog: Difficulty & Gravity Profiles Menu -->
  <dialog id="gravity-modal" aria-labelledby="modal-title">
    <div class="hazard-trim"></div>
    <div class="modal-inner">
      <div class="modal-top">
        <span class="modal-badge">ನಮ್ಮ ಬೆಂಗಳೂರು • KA-01 BENGALURU TRAFFIC PRO EDITION</span>
      </div>
      <h1 id="modal-title">ಒಂದು ಸೆಕೆಂಡ್ | ONDU SECOND: BANGALORE GRAVITY GLITCH</h1>
      <p class="modal-lead">
        Drive the iconic emerald-and-canary Bengaluru Auto-Rickshaw down a realistic PBR highway lined with bilingual <strong>Kannada + English hoardings</strong>, sudden <strong>Bengaluru Traffic Police (BTP) license checks</strong>, darting <strong>Indie stray dogs</strong>, "Ondu Second!" jaywalkers, hyper-speed Zepto/Blinkit riders, and magnetic BBMP potholes!
      </p>

      <div class="mode-grid">
        <article class="mode-card" data-mode="low">
          <div>
            <span class="mode-tag tag-low">Low • Easy Mode</span>
            <h2>ಕಬ್ಬನ್ ಪಾರ್ಕ್ ಬೆಳಿಗ್ಗೆ | Cubbon Park Morning</h2>
            <p class="mode-desc">
              Cruising morning traffic with bilingual Kannada hoardings, occasional stray dogs &amp; jaywalkers, and friendly BTP patrol checkposts.
            </p>
            <ul class="mode-stats">
              <li><strong>Traffic:</strong> 12 Two-Way Vehicles</li>
              <li><strong>Hazards:</strong> 5 Jaywalkers • 3 Stray Dogs • 1 BTP Cop</li>
              <li><strong>Pothole Pull:</strong> Mild Magnetic Pull</li>
            </ul>
          </div>
          <button type="button" class="launch-btn" data-select-mode="low">Play Low Mode</button>
        </article>

        <article class="mode-card selected" data-mode="medium">
          <div>
            <span class="mode-tag tag-med">Medium • Normal Mode</span>
            <h2>ಇಂದಿರಾನಗರ ಸಂಜೆ ರಶ್ | Indiranagar 6 PM Rush</h2>
            <p class="mode-desc">
              Bustling evening rush with oncoming BMTC 500D buses, sudden BTP Traffic Cop license stops, darting Indie stray dogs, and Zepto/Blinkit cut-offs.
            </p>
            <ul class="mode-stats">
              <li><strong>Traffic:</strong> 20 Two-Way Vehicles</li>
              <li><strong>Hazards:</strong> 8 Jaywalkers • 5 Stray Dogs • 2 BTP Cops</li>
              <li><strong>Pothole Pull:</strong> Strong Sinkhole Pull</li>
            </ul>
          </div>
          <button type="button" class="launch-btn" data-select-mode="medium">Play Normal Mode</button>
        </article>

        <article class="mode-card" data-mode="complex">
          <div>
            <span class="mode-tag tag-complex">Complex • Peak Hour</span>
            <h2>ಸಿಲ್ಕ್ ಬೋರ್ಡ್ ಟ್ರಾಫಿಕ್ | Silk Board 8 PM Gridlock</h2>
            <p class="mode-desc">
              Full Silk Board peak-hour madness! Non-stop BMTC convoys, aggressive BTP e-Challan nakabandis, pack of darting stray dogs, and monsoon hydroplaning.
            </p>
            <ul class="mode-stats">
              <li><strong>Traffic:</strong> 30 Dense Two-Way Vehicles</li>
              <li><strong>Hazards:</strong> 12 Jaywalkers • 7 Stray Dogs • 3 BTP Cops</li>
              <li><strong>Pothole Pull:</strong> Maximum Gravity Glitch</li>
            </ul>
          </div>
          <button type="button" class="launch-btn" data-select-mode="complex">Play Peak Hour</button>
        </article>
      </div>

      <div class="asset-status-bar">
        <div><strong>Blender 3D PBR Assets:</strong> <span id="asset-load-summary">Loading 12/12 .glb models...</span></div>
        <div class="asset-badges">
          <span class="asset-chip" data-asset="auto_rickshaw.glb">auto_rickshaw.glb</span>
          <span class="asset-chip" data-asset="traffic_police.glb">traffic_police.glb</span>
          <span class="asset-chip" data-asset="stray_dog.glb">stray_dog.glb</span>
          <span class="asset-chip" data-asset="delivery_swiggy.glb">delivery_swiggy.glb</span>
          <span class="asset-chip" data-asset="delivery_zepto.glb">delivery_zepto.glb</span>
          <span class="asset-chip" data-asset="delivery_blinkit.glb">delivery_blinkit.glb</span>
          <span class="asset-chip" data-asset="commuter_techie.glb">commuter_techie.glb</span>
          <span class="asset-chip" data-asset="bmtc_bus.glb">bmtc_bus.glb</span>
          <span class="asset-chip" data-asset="pedestrian_jaywalker.glb">pedestrian_jaywalker.glb</span>
          <span class="asset-chip" data-asset="vidhana_soudha.glb">vidhana_soudha.glb</span>
          <span class="asset-chip" data-asset="metro_station.glb">metro_station.glb</span>
          <span class="asset-chip" data-asset="silk_board_sign.glb">silk_board_sign.glb</span>
        </div>
      </div>
    </div>
    <div class="hazard-trim"></div>
  </dialog>

  <script type="module">
    import * as THREE from 'three';
    import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
    import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
    import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
    import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
    import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
    import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';

    // =========================================================================
    // 1. BLENDER GLB ASSET LOADER (HTTP + Embedded Gzip Binary Fallback)
    // =========================================================================
    const EMBEDDED_GLB_GZ = __EMBEDDED_GLB_JSON__;

    async function decodeGzipBase64(b64) {
      const binStr = atob(b64);
      const bytes = new Uint8Array(binStr.length);
      for (let i = 0; i < binStr.length; i++) bytes[i] = binStr.charCodeAt(i);
      const ds = new DecompressionStream('gzip');
      const writer = ds.writable.getWriter();
      writer.write(bytes);
      writer.close();
      return await new Response(ds.readable).arrayBuffer();
    }

    const gltfLoader = new GLTFLoader();
    const loadedTemplates = {};

    async function loadBlenderAsset(filename) {
      for (const url of [`./assets/${filename}`, `./${filename}`]) {
        try {
          const res = await fetch(url);
          if (res.ok) {
            const buf = await res.arrayBuffer();
            const gltf = await gltfLoader.parseAsync(buf, '');
            return gltf.scene;
          }
        } catch (_) {}
      }
      if (EMBEDDED_GLB_GZ[filename]) {
        const buf = await decodeGzipBase64(EMBEDDED_GLB_GZ[filename]);
        const gltf = await gltfLoader.parseAsync(buf, '');
        return gltf.scene;
      }
      throw new Error(`Asset ${filename} not found`);
    }

    // =========================================================================
    // 2. WEB AUDIO API SYNTHESIZER (Tuk-Tuk, Horn, BTP Whistle, Stray Dog Bark)
    // =========================================================================
    class BangaloreAudioEngine {
      constructor() {
        this.ctx = null;
        this.enabled = true;
        this.initialized = false;
      }

      init() {
        if (this.initialized) {
          if (this.ctx && this.ctx.state === 'suspended' && this.enabled) this.ctx.resume();
          return;
        }
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        if (!AudioCtx) return;
        this.ctx = new AudioCtx();
        this.initialized = true;

        this.master = this.ctx.createDynamicsCompressor();
        this.master.threshold.value = -16;
        this.master.ratio.value = 6;
        this.master.connect(this.ctx.destination);

        this._setupCityDrone();
        this._setupAutoTukTukEngine();
        this._setupRainWhiteNoiseLayer();
        this._setupHornEchoChain();
      }

      _setupHornEchoChain() {
        const samples = 1024;
        const curve = new Float32Array(samples);
        for (let i = 0; i < samples; i++) {
          const x = (i * 2) / samples - 1;
          curve[i] = Math.tanh(x * 3.4) + 0.12 * Math.sin(x * Math.PI * 3);
        }
        this.hornShaper = this.ctx.createWaveShaper();
        this.hornShaper.curve = curve;
        this.hornShaper.oversample = '2x';

        this.hornBellFilter = this.ctx.createBiquadFilter();
        this.hornBellFilter.type = 'peaking';
        this.hornBellFilter.frequency.value = 1140;
        this.hornBellFilter.Q.value = 3.2;
        this.hornBellFilter.gain.value = 9.5;

        const delay = this.ctx.createDelay(0.5);
        delay.delayTime.value = 0.088;
        const fb = this.ctx.createGain();
        fb.gain.value = 0.22;
        const echoWet = this.ctx.createGain();
        echoWet.gain.value = 0.24;

        this.hornShaper.connect(this.hornBellFilter);
        this.hornBellFilter.connect(this.master);
        this.hornBellFilter.connect(delay);
        delay.connect(fb);
        fb.connect(delay);
        delay.connect(echoWet);
        echoWet.connect(this.master);
      }

      _setupCityDrone() {
        this.droneGain = this.ctx.createGain();
        this.droneGain.gain.value = 0.05;
        const filter = this.ctx.createBiquadFilter();
        filter.type = 'lowpass';
        filter.frequency.value = 240;

        [55.0, 82.41, 110.0, 164.81].forEach((f, idx) => {
          const osc = this.ctx.createOscillator();
          osc.type = idx % 2 === 0 ? 'triangle' : 'sine';
          osc.frequency.value = f;
          const g = this.ctx.createGain();
          g.gain.value = 0.2;
          osc.connect(g);
          g.connect(filter);
          osc.start();
        });
        filter.connect(this.droneGain);
        this.droneGain.connect(this.master);
      }

      _setupAutoTukTukEngine() {
        this.tukGain = this.ctx.createGain();
        this.tukGain.gain.value = 0.11;

        this.tukOsc = this.ctx.createOscillator();
        this.tukOsc.type = 'sawtooth';
        this.tukOsc.frequency.value = 58;

        this.tukFilter = this.ctx.createBiquadFilter();
        this.tukFilter.type = 'bandpass';
        this.tukFilter.frequency.value = 195;
        this.tukFilter.Q.value = 2.5;

        const pulseVca = this.ctx.createGain();
        pulseVca.gain.value = 0.5;
        this.tukLfo = this.ctx.createOscillator();
        this.tukLfo.type = 'square';
        this.tukLfo.frequency.value = 14;
        const lfoDepth = this.ctx.createGain();
        lfoDepth.gain.value = 0.42;
        this.tukLfo.connect(lfoDepth);
        lfoDepth.connect(pulseVca.gain);

        this.tukOsc.connect(this.tukFilter);
        this.tukFilter.connect(pulseVca);
        pulseVca.connect(this.tukGain);
        this.tukGain.connect(this.master);

        this.tukOsc.start();
        this.tukLfo.start();
      }

      _setupRainWhiteNoiseLayer() {
        const sr = this.ctx.sampleRate;
        const len = sr * 3;
        const buffer = this.ctx.createBuffer(1, len, sr);
        const data = buffer.getChannelData(0);
        let b0 = 0, b1 = 0, b2 = 0;
        for (let i = 0; i < len; i++) {
          const white = Math.random() * 2 - 1;
          b0 = 0.997 * b0 + white * 0.029;
          b1 = 0.985 * b1 + white * 0.032;
          b2 = 0.950 * b2 + white * 0.048;
          data[i] = (b0 + b1 + b2 + white * 0.18) * 0.5;
        }
        const noise = this.ctx.createBufferSource();
        noise.buffer = buffer;
        noise.loop = true;

        this.rainFilter = this.ctx.createBiquadFilter();
        this.rainFilter.type = 'bandpass';
        this.rainFilter.frequency.value = 900;
        this.rainFilter.Q.value = 0.7;

        this.rainGain = this.ctx.createGain();
        this.rainGain.gain.value = 0.0001;

        noise.connect(this.rainFilter);
        this.rainFilter.connect(this.rainGain);
        this.rainGain.connect(this.master);
        noise.start();
      }

      updateContinuous(speedKmh, rainIntensity, altitude) {
        if (!this.initialized || !this.enabled) return;
        const now = this.ctx.currentTime;
        const normSpeed = Math.min(1.4, Math.max(0, speedKmh / 85));
        const baseFreq = 52 + normSpeed * 58 + Math.min(20, altitude * 3);
        this.tukOsc.frequency.setTargetAtTime(baseFreq, now, 0.06);
        this.tukLfo.frequency.setTargetAtTime(12 + normSpeed * 26, now, 0.06);
        this.tukFilter.frequency.setTargetAtTime(175 + normSpeed * 280, now, 0.08);
        this.rainGain.gain.setTargetAtTime(Math.max(0.0001, rainIntensity * 0.24), now, 0.15);
      }

      playBeepBeepHorn(variant = 'auto') {
        if (!this.initialized || !this.enabled) return;
        const now = this.ctx.currentTime;

        if (variant === 'auto') {
          const bursts = [
            { offset: 0.00, dur: 0.095, pitchMult: 1.00, peakGain: 0.28 },
            { offset: 0.115, dur: 0.095, pitchMult: 1.03, peakGain: 0.30 },
            { offset: 0.230, dur: 0.230, pitchMult: 0.99, peakGain: 0.34 }
          ];
          const baseF1 = 442 + (Math.random() - 0.5) * 14;
          const baseF2 = baseF1 * 1.254;
          const baseF3 = baseF1 * 2.0;
          const subBulb = baseF1 * 0.5;

          bursts.forEach((b) => {
            const start = now + b.offset;
            const end = start + b.dur;

            const o1 = this.ctx.createOscillator();
            const o2 = this.ctx.createOscillator();
            const o3 = this.ctx.createOscillator();
            const oSub = this.ctx.createOscillator();
            o1.type = 'sawtooth';
            o2.type = 'sawtooth';
            o3.type = 'square';
            oSub.type = 'triangle';

            const f1 = baseF1 * b.pitchMult;
            const f2 = baseF2 * b.pitchMult;
            const f3 = baseF3 * b.pitchMult;

            o1.frequency.setValueAtTime(f1 * 0.94, start);
            o1.frequency.linearRampToValueAtTime(f1 * 1.06, start + 0.022);
            o1.frequency.exponentialRampToValueAtTime(f1 * 0.97, end);

            o2.frequency.setValueAtTime(f2 * 0.94, start);
            o2.frequency.linearRampToValueAtTime(f2 * 1.065, start + 0.022);
            o2.frequency.exponentialRampToValueAtTime(f2 * 0.97, end);

            o3.frequency.setValueAtTime(f3, start);
            oSub.frequency.setValueAtTime(subBulb, start);

            const rattleLfo = this.ctx.createOscillator();
            rattleLfo.type = 'sine';
            rattleLfo.frequency.value = 52;
            const rattleDepth = this.ctx.createGain();
            rattleDepth.gain.value = 11.0;
            rattleLfo.connect(rattleDepth);
            rattleDepth.connect(o1.frequency);
            rattleDepth.connect(o2.frequency);

            const mix = this.ctx.createGain();
            const g1 = this.ctx.createGain(); g1.gain.value = 0.45;
            const g2 = this.ctx.createGain(); g2.gain.value = 0.45;
            const g3 = this.ctx.createGain(); g3.gain.value = 0.22;
            const gSub = this.ctx.createGain(); gSub.gain.value = 0.35;

            o1.connect(g1); g1.connect(mix);
            o2.connect(g2); g2.connect(mix);
            o3.connect(g3); g3.connect(mix);
            oSub.connect(gSub); gSub.connect(mix);

            const bp = this.ctx.createBiquadFilter();
            bp.type = 'bandpass';
            bp.frequency.value = 820;
            bp.Q.value = 1.25;

            const env = this.ctx.createGain();
            env.gain.setValueAtTime(0.001, start);
            env.gain.linearRampToValueAtTime(b.peakGain, start + 0.012);
            env.gain.setValueAtTime(b.peakGain * 0.92, Math.max(start + 0.015, end - 0.035));
            env.gain.exponentialRampToValueAtTime(0.001, end);

            mix.connect(bp);
            bp.connect(env);
            env.connect(this.hornShaper || this.master);

            o1.start(start); o2.start(start); o3.start(start); oSub.start(start); rattleLfo.start(start);
            o1.stop(end + 0.01); o2.stop(end + 0.01); o3.stop(end + 0.01); oSub.stop(end + 0.01); rattleLfo.stop(end + 0.01);
          });
          return;
        }

        const isBus = variant === 'bus';
        const f1 = isBus ? 185 : 1120 + (Math.random() - 0.5) * 60;
        const f2 = isBus ? 233 : f1 * 1.25;

        [0, isBus ? 0.18 : 0.11].forEach((offset) => {
          const start = now + offset;
          const dur = isBus ? 0.18 : 0.08;
          const o1 = this.ctx.createOscillator();
          const o2 = this.ctx.createOscillator();
          o1.type = 'sawtooth';
          o2.type = isBus ? 'sawtooth' : 'square';
          o1.frequency.setValueAtTime(f1, start);
          o2.frequency.setValueAtTime(f2, start);

          const bp = this.ctx.createBiquadFilter();
          bp.type = 'bandpass';
          bp.frequency.value = isBus ? 360 : 1450;
          bp.Q.value = 2.2;

          const g = this.ctx.createGain();
          g.gain.setValueAtTime(0.001, start);
          g.gain.exponentialRampToValueAtTime(isBus ? 0.22 : 0.14, start + 0.012);
          g.gain.exponentialRampToValueAtTime(0.001, start + dur);

          o1.connect(bp);
          o2.connect(bp);
          bp.connect(g);
          g.connect(this.hornShaper || this.master);
          o1.start(start);
          o2.start(start);
          o1.stop(start + dur + 0.01);
          o2.stop(start + dur + 0.01);
        });
      }

      // Authentic Shrill Bengaluru Traffic Police Pea-Whistle ("PRRREEEET!")
      playPoliceWhistle(withSiren = false) {
        if (!this.initialized || !this.enabled) return;
        const now = this.ctx.currentTime;
        const dur = 0.42;
        const o1 = this.ctx.createOscillator();
        const o2 = this.ctx.createOscillator();
        const peaLfo = this.ctx.createOscillator();
        o1.type = 'sine';
        o2.type = 'triangle';
        peaLfo.type = 'sine';

        o1.frequency.setValueAtTime(2780, now);
        o1.frequency.linearRampToValueAtTime(2960, now + 0.08);
        o1.frequency.setValueAtTime(2920, now + dur);

        o2.frequency.setValueAtTime(2835, now);
        peaLfo.frequency.value = 48; // Pea trill inside whistle chamber
        const lfoGain = this.ctx.createGain();
        lfoGain.gain.value = 115;
        peaLfo.connect(lfoGain);
        lfoGain.connect(o1.frequency);
        lfoGain.connect(o2.frequency);

        const g = this.ctx.createGain();
        g.gain.setValueAtTime(0.001, now);
        g.gain.linearRampToValueAtTime(0.22, now + 0.02);
        g.gain.setValueAtTime(0.20, now + dur - 0.05);
        g.gain.exponentialRampToValueAtTime(0.001, now + dur);

        o1.connect(g);
        o2.connect(g);
        g.connect(this.master);
        o1.start(now); o2.start(now); peaLfo.start(now);
        o1.stop(now + dur + 0.02); o2.stop(now + dur + 0.02); peaLfo.stop(now + dur + 0.02);

        if (withSiren) {
          const sOsc = this.ctx.createOscillator();
          sOsc.type = 'sawtooth';
          sOsc.frequency.setValueAtTime(650, now + 0.12);
          sOsc.frequency.linearRampToValueAtTime(1180, now + 0.32);
          sOsc.frequency.linearRampToValueAtTime(620, now + 0.54);
          const sg = this.ctx.createGain();
          sg.gain.setValueAtTime(0.15, now + 0.12);
          sg.gain.exponentialRampToValueAtTime(0.001, now + 0.56);
          sOsc.connect(sg);
          sg.connect(this.master);
          sOsc.start(now + 0.12);
          sOsc.stop(now + 0.58);
        }
      }

      // DigiLocker License Verified Chime
      playLicenseVerified() {
        if (!this.initialized || !this.enabled) return;
        const now = this.ctx.currentTime;
        [587.33, 880.0, 1174.66].forEach((freq, idx) => {
          const o = this.ctx.createOscillator();
          o.type = 'triangle';
          o.frequency.setValueAtTime(freq, now + idx * 0.07);
          const g = this.ctx.createGain();
          g.gain.setValueAtTime(0.18, now + idx * 0.07);
          g.gain.exponentialRampToValueAtTime(0.001, now + idx * 0.07 + 0.22);
          o.connect(g);
          g.connect(this.master);
          o.start(now + idx * 0.07);
          o.stop(now + idx * 0.07 + 0.24);
        });
      }

      // Authentic Indie Street Dog Double Bark ("BOW-WOW!")
      playDogBark() {
        if (!this.initialized || !this.enabled) return;
        const now = this.ctx.currentTime;
        [0.0, 0.16].forEach((offset, idx) => {
          const start = now + offset;
          const dur = 0.12;
          const osc = this.ctx.createOscillator();
          osc.type = 'sawtooth';
          const fPeak = idx === 0 ? 490 : 540;
          osc.frequency.setValueAtTime(310, start);
          osc.frequency.linearRampToValueAtTime(fPeak, start + 0.035);
          osc.frequency.exponentialRampToValueAtTime(220, start + dur);

          const bp = this.ctx.createBiquadFilter();
          bp.type = 'bandpass';
          bp.frequency.setValueAtTime(750, start);
          bp.frequency.linearRampToValueAtTime(1150, start + 0.04);
          bp.frequency.exponentialRampToValueAtTime(520, start + dur);
          bp.Q.value = 2.4;

          const g = this.ctx.createGain();
          g.gain.setValueAtTime(0.001, start);
          g.gain.linearRampToValueAtTime(0.24, start + 0.015);
          g.gain.exponentialRampToValueAtTime(0.001, start + dur);

          osc.connect(bp);
          bp.connect(g);
          g.connect(this.master);
          osc.start(start);
          osc.stop(start + dur + 0.01);
        });
      }

      playBounceImpact(isHyperDelivery = false) {
        if (!this.initialized || !this.enabled) return;
        const now = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        osc.type = isHyperDelivery ? 'sawtooth' : 'triangle';
        osc.frequency.setValueAtTime(isHyperDelivery ? 280 : 150, now);
        osc.frequency.exponentialRampToValueAtTime(isHyperDelivery ? 660 : 52, now + 0.22);
        const g = this.ctx.createGain();
        g.gain.setValueAtTime(0.22, now);
        g.gain.exponentialRampToValueAtTime(0.001, now + 0.24);
        osc.connect(g);
        g.connect(this.master);
        osc.start(now);
        osc.stop(now + 0.25);
      }

      playWheelSnap() {
        if (!this.initialized || !this.enabled) return;
        const now = this.ctx.currentTime;
        [620, 940].forEach((freq, i) => {
          const o = this.ctx.createOscillator();
          o.type = 'square';
          o.frequency.setValueAtTime(freq, now + i * 0.02);
          o.frequency.exponentialRampToValueAtTime(freq * 0.45, now + 0.2);
          const g = this.ctx.createGain();
          g.gain.setValueAtTime(0.12, now + i * 0.02);
          g.gain.exponentialRampToValueAtTime(0.001, now + 0.22);
          o.connect(g);
          g.connect(this.master);
          o.start(now + i * 0.02);
          o.stop(now + 0.23);
        });
      }

      toggleMute() {
        this.init();
        this.enabled = !this.enabled;
        if (this.ctx) {
          this.enabled ? this.ctx.resume() : this.ctx.suspend();
        }
        return this.enabled;
      }
    }

    const audio = new BangaloreAudioEngine();

    // =========================================================================
    // 3. DIFFICULTY PROFILES (Two-Way Traffic + Jaywalkers + BTP Cops + Stray Dogs)
    // =========================================================================
    const GRAVITY_PROFILES = {
      low: {
        id: 'low',
        trafficCount: 12,
        jaywalkerCount: 5,
        dogCount: 3,
        copCount: 1,
        busRatio: 0.14,
        deliveryRatio: 0.35,
        deliverySpeedMult: 1.15,
        cutOffAggression: 0.20,
        potholeCount: 4,
        potholePullStrength: 10.0,
        potholeRadius: 4.5,
        rainCycleDuration: 30,
        rainStormDuration: 7,
        gravityReturn: 24.0,
        glitchBounceVy: 5.2,
        fareRateMult: 1.0
      },
      medium: {
        id: 'medium',
        trafficCount: 20,
        jaywalkerCount: 8,
        dogCount: 5,
        copCount: 2,
        busRatio: 0.22,
        deliveryRatio: 0.48,
        deliverySpeedMult: 1.45,
        cutOffAggression: 0.55,
        potholeCount: 6,
        potholePullStrength: 18.0,
        potholeRadius: 5.5,
        rainCycleDuration: 22,
        rainStormDuration: 9,
        gravityReturn: 19.0,
        glitchBounceVy: 6.8,
        fareRateMult: 1.5
      },
      complex: {
        id: 'complex',
        trafficCount: 30,
        jaywalkerCount: 12,
        dogCount: 7,
        copCount: 3,
        busRatio: 0.32,
        deliveryRatio: 0.48,
        deliverySpeedMult: 1.75,
        cutOffAggression: 0.82,
        potholeCount: 9,
        potholePullStrength: 26.0,
        potholeRadius: 6.4,
        rainCycleDuration: 15,
        rainStormDuration: 11,
        gravityReturn: 14.5,
        glitchBounceVy: 8.5,
        fareRateMult: 2.5
      }
    };

    let currentProfile = GRAVITY_PROFILES.medium;

    // =========================================================================
    // 4. PRO THREE.JS SCENE, PMREM ENVIRONMENT, UNREAL BLOOM & SKY DOME
    // =========================================================================
    const canvas = document.getElementById('game-canvas');
    const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, powerPreference: 'high-performance' });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 0.95;

    const scene = new THREE.Scene();
    const drySkyColor = new THREE.Color(0x1b2b48);
    const rainSkyColor = new THREE.Color(0x0d1524);
    scene.background = drySkyColor.clone();
    scene.fog = new THREE.FogExp2(0x1b2b48, 0.0038);

    // PMREM Metallic & Glass Reflections (Pro-Game PBR Lighting)
    const pmremGenerator = new THREE.PMREMGenerator(renderer);
    scene.environment = pmremGenerator.fromScene(new RoomEnvironment(), 0.04).texture;
    scene.environmentIntensity = 0.28;

    const camera = new THREE.PerspectiveCamera(58, window.innerWidth / window.innerHeight, 0.1, 440);
    camera.position.set(0, 4.2, 7.8);

    // Post-Processing Composer with Subtle UnrealBloomPass
    const composer = new EffectComposer(renderer);
    composer.addPass(new RenderPass(scene, camera));
    const bloomPass = new UnrealBloomPass(
      new THREE.Vector2(window.innerWidth, window.innerHeight),
      0.16, // strength
      0.32, // radius
      0.94  // threshold (only bright lights/neon/LEDs bloom!)
    );
    composer.addPass(bloomPass);
    composer.addPass(new OutputPass());

    const hemiLight = new THREE.HemisphereLight(0x9ec5ff, 0x362c24, 0.95);
    scene.add(hemiLight);

    const sunLight = new THREE.DirectionalLight(0xffe6bd, 1.85);
    sunLight.position.set(36, 58, 28);
    sunLight.castShadow = true;
    sunLight.shadow.mapSize.set(2048, 2048);
    sunLight.shadow.camera.near = 1;
    sunLight.shadow.camera.far = 190;
    const d = 48;
    sunLight.shadow.camera.left = -d;
    sunLight.shadow.camera.right = d;
    sunLight.shadow.camera.top = d;
    sunLight.shadow.camera.bottom = -d;
    sunLight.shadow.bias = -0.0005;
    scene.add(sunLight);

    // Procedural Bengaluru Golden-Hour / Dusk Horizon Sky Dome
    function createSkyDomeTexture() {
      const c = document.createElement('canvas');
      c.width = 1024;
      c.height = 512;
      const ctx = c.getContext('2d');
      const grad = ctx.createLinearGradient(0, 0, 0, 512);
      grad.addColorStop(0.0, '#0b1329');
      grad.addColorStop(0.35, '#192b52');
      grad.addColorStop(0.47, '#3b4d7a');
      grad.addColorStop(0.53, '#d97745');
      grad.addColorStop(0.58, '#2b354f');
      grad.addColorStop(1.0, '#111827');
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, 1024, 512);

      // Soft dusk clouds near horizon
      for (let i = 0; i < 40; i++) {
        const cx = Math.random() * 1024;
        const cy = 150 + Math.random() * 110;
        const rw = 60 + Math.random() * 140;
        const rh = 8 + Math.random() * 20;
        const cg = ctx.createRadialGradient(cx, cy, 2, cx, cy, rw);
        cg.addColorStop(0, 'rgba(255, 196, 138, 0.16)');
        cg.addColorStop(1, 'rgba(255, 196, 138, 0.0)');
        ctx.fillStyle = cg;
        ctx.beginPath();
        ctx.ellipse(cx, cy, rw, rh, 0, 0, Math.PI * 2);
        ctx.fill();
      }
      const tex = new THREE.CanvasTexture(c);
      tex.colorSpace = THREE.SRGBColorSpace;
      return tex;
    }

    const skyDome = new THREE.Mesh(
      new THREE.SphereGeometry(380, 32, 20),
      new THREE.MeshBasicMaterial({ map: createSkyDomeTexture(), side: THREE.BackSide, fog: false })
    );
    scene.add(skyDome);

    // =========================================================================
    // 5. PROCEDURAL PBR ASPHALT HIGHWAY, SKYLINE, & BILINGUAL KANNADA HOARDINGS
    // =========================================================================
    const ROAD_WIDTH = 22.8; // 6 lanes * 3.8m
    const LANES = [-9.5, -5.7, -1.9, 1.9, 5.7, 9.5];
    const CORRIDOR_LENGTH = 360;

    function createAsphaltTextures() {
      const c = document.createElement('canvas');
      c.width = 1024;
      c.height = 1024;
      const ctx = c.getContext('2d');
      ctx.fillStyle = '#242935';
      ctx.fillRect(0, 0, 1024, 1024);

      // Micro-aggregate asphalt grain & tar patches
      for (let i = 0; i < 28000; i++) {
        const x = Math.random() * 1024;
        const y = Math.random() * 1024;
        const v = 28 + Math.floor(Math.random() * 30);
        ctx.fillStyle = `rgb(${v}, ${v + 3}, ${v + 9})`;
        ctx.fillRect(x, y, 2, 2);
      }

      // Subtle glossy tire wear tracks down each of the 6 lanes
      for (let lane = 0; lane < 6; lane++) {
        const lx = ((lane + 0.5) / 6) * 1024;
        for (const wheelOffset of [-32, 32]) {
          const tg = ctx.createLinearGradient(lx + wheelOffset - 22, 0, lx + wheelOffset + 22, 0);
          tg.addColorStop(0, 'rgba(15, 18, 25, 0)');
          tg.addColorStop(0.5, 'rgba(14, 17, 24, 0.42)');
          tg.addColorStop(1, 'rgba(15, 18, 25, 0)');
          ctx.fillStyle = tg;
          ctx.fillRect(lx + wheelOffset - 22, 0, 44, 1024);
        }
      }

      const tex = new THREE.CanvasTexture(c);
      tex.wrapS = THREE.RepeatWrapping;
      tex.wrapT = THREE.RepeatWrapping;
      tex.repeat.set(1, 28);
      tex.anisotropy = renderer.capabilities.getMaxAnisotropy();
      tex.colorSpace = THREE.SRGBColorSpace;
      return tex;
    }

    const roadMat = new THREE.MeshStandardMaterial({
      map: createAsphaltTextures(),
      color: 0xd8dee9,
      roughness: 0.68,
      metalness: 0.14
    });
    const roadMesh = new THREE.Mesh(new THREE.PlaneGeometry(ROAD_WIDTH, CORRIDOR_LENGTH * 1.6), roadMat);
    roadMesh.rotation.x = -Math.PI / 2;
    roadMesh.position.set(0, 0, -CORRIDOR_LENGTH * 0.35);
    roadMesh.receiveShadow = true;
    scene.add(roadMesh);

    const groundMat = new THREE.MeshStandardMaterial({ color: 0x2c3444, roughness: 0.86 });
    const groundMesh = new THREE.Mesh(new THREE.PlaneGeometry(260, CORRIDOR_LENGTH * 1.6), groundMat);
    groundMesh.rotation.x = -Math.PI / 2;
    groundMesh.position.set(0, -0.04, -CORRIDOR_LENGTH * 0.35);
    groundMesh.receiveShadow = true;
    scene.add(groundMesh);

    // =========================================================================
    // 5B. BILINGUAL KANNADA + ENGLISH (60:40 RULE) HOARDINGS & HIGHWAY GANTRIES
    // =========================================================================
    const BILINGUAL_HOARDING_ADS = [
      {
        bgTop: '#7c1d1d',
        bgBot: '#3b0a0a',
        border: '#fbbf24',
        badge: 'ಇಂದಿರಾನಗರ • INDIRANAGAR',
        knTitle: 'ದಿ ರಾಮೇಶ್ವರಂ ಕೆಫೆ',
        enTitle: 'THE RAMESHWARAM CAFE',
        knSub: 'ಶುದ್ಧ ತುಪ್ಪದ ಪುದಿ ಮಸಾಲೆ ದೋಸೆ ಮತ್ತು ಫಿಲ್ಟರ್ ಕಾಫಿ',
        enSub: 'PURE GHEE PUDI MASALA DOSA & DEGREE FILTER COFFEE',
        accent: '#fde047'
      },
      {
        bgTop: '#064e3b',
        bgBot: '#022c22',
        border: '#ffd000',
        badge: 'ನಮ್ಮ ಬೆಂಗಳೂರು • ZERO COMMISSION',
        knTitle: 'ನಮ್ಮ ಯಾತ್ರಿ ಆಟೋ ಆಪ್',
        enTitle: 'NAMMA YATRI • AUTO APP',
        knSub: 'ಆಟೋ ಚಾಲಕರ ಸ್ವಂತ ಆಪ್ • ಮೀಟರ್ ಮೇಲೆ ₹೨೦ ಬೇಡ!',
        enSub: '100% DIRECT TO DRIVER • ONE CLICK INSTANT PICKUP',
        accent: '#ffd000'
      },
      {
        bgTop: '#1e3a8a',
        bgBot: '#0f172a',
        border: '#38bdf8',
        badge: 'ಕರ್ನಾಟಕ ಹಾಲು ಮಹಾಮಂಡಳಿ • KMF',
        knTitle: 'ನಂದಿನಿ ತಾಜಾ ಹಾಲು ಮತ್ತು ಸಿಹಿ',
        enTitle: 'KMF NANDINI MILK & MYSORE PAK',
        knSub: 'ಪ್ರತಿ ದಿನ ಬೆಳಿಗ್ಗೆ ಪರಿಶುದ್ಧ ಹಾಲು, ಮೊಸರು ಮತ್ತು ತುಪ್ಪ',
        enSub: 'GOOD LIFE PURE MILK, CURD & GHEE SWEETS',
        accent: '#7dd3fc'
      },
      {
        bgTop: '#4c1d95',
        bgBot: '#1e1b4b',
        border: '#c084fc',
        badge: 'BMRCL • ನಮ್ಮ ಮೆಟ್ರೋ',
        knTitle: 'ನಮ್ಮ ಮೆಟ್ರೋ - ನೇರಳೆ ಮಾರ್ಗ',
        enTitle: 'NAMMA METRO PURPLE LINE',
        knSub: 'ವೈಟ್‌ಫೀಲ್ಡ್ ನಿಂದ ಚಲ್ಲಘಟ್ಟ ವರೆಗೆ ಟ್ರಾಫಿಕ್ ಇಲ್ಲದ ಪ್ರಯಾಣ!',
        enSub: 'WHITEFIELD TO CHALLAGHATTA • BEAT SILK BOARD RUSH',
        accent: '#e9d5ff'
      },
      {
        bgTop: '#78350f',
        bgBot: '#451a03',
        border: '#f59e0b',
        badge: 'ಕರ್ನಾಟಕದ ಹೆಮ್ಮೆ • SINCE 1916',
        knTitle: 'ಮೈಸೂರು ಸ್ಯಾಂಡಲ್ ಸೋಪ್',
        enTitle: 'MYSORE SANDAL SOAP',
        knSub: 'ಶೇಕಡಾ ೧೦೦ ಪರಿಶುದ್ಧ ಶ್ರೀಗಂಧದ ಎಣ್ಣೆಯ ಸೋಪು',
        enSub: '100% PURE NATURAL SANDALWOOD OIL • HERITAGE',
        accent: '#fde68a'
      },
      {
        bgTop: '#0f172a',
        bgBot: '#1e293b',
        border: '#ef4444',
        badge: 'BTP • ಬೆಂಗಳೂರು ಸಂಚಾರ ಪೊಲೀಸ್',
        knTitle: 'ಸಂಚಾರ ನಿಯಮ ಪಾಲಿಸಿ • ಸುರಕ್ಷಿತವಾಗಿರಿ',
        enTitle: 'BENGALURU TRAFFIC POLICE ALERT',
        knSub: 'ಮುಂದೆ ತಪಾಸಣೆ ಇದೆ • DL, RC ಮತ್ತು ಇನ್ಶೂರೆನ್ಸ್ ತೋರಿಸಿ!',
        enSub: 'SUDDEN LICENSE & E-CHALLAN CHECK AHEAD • PRESS [L]',
        accent: '#bef264'
      },
      {
        bgTop: '#581c87',
        bgBot: '#2e1065',
        border: '#10f560',
        badge: '೧೦ ನಿಮಿಷದಲ್ಲಿ • 10-MIN DELIVERY',
        knTitle: 'ಜೆಪ್ಟೊ ಮತ್ತು ಬ್ಲಿಂಕಿಟ್ ಸೂಪರ್ ಸ್ಟೋರ್',
        enTitle: 'ZEPTO & BLINKIT DARK STORE',
        knSub: 'ಕೊತ್ತಂಬರಿ ಸೊಪ್ಪು, ಹಾಲು ಮತ್ತು ತಿಂಡಿ ೧೦ ನಿಮಿಷದಲ್ಲಿ!',
        enSub: 'FRESH CORIANDER, MILK & SNACKS IN 10 MINUTES',
        accent: '#10f560'
      },
      {
        bgTop: '#431407',
        bgBot: '#1c0a00',
        border: '#fb923c',
        badge: 'ಗಾಂಧಿ ಬಜಾರ್ • SINCE 1943',
        knTitle: 'ವಿದ್ಯಾರ್ಥಿ ಭವನ ಮಸಾಲೆ ದೋಸೆ',
        enTitle: 'VIDYARTHI BHAVAN HERITAGE',
        knSub: 'ಬೆಂಗಳೂರಿನ ಇತಿಹಾಸ ಪ್ರಸಿದ್ಧ ಗರಿಗರಿ ಬೆಣ್ಣೆ ಮಸಾಲೆ ದೋಸೆ',
        enSub: 'LEGENDARY CRISPY BUTTER MASALA DOSA & COFFEE',
        accent: '#fed7aa'
      }
    ];

    function createBilingualHoardingTexture(ad) {
      const c = document.createElement('canvas');
      c.width = 1024;
      c.height = 512;
      const ctx = c.getContext('2d');

      const grad = ctx.createLinearGradient(0, 0, 1024, 512);
      grad.addColorStop(0, ad.bgTop);
      grad.addColorStop(1, ad.bgBot);
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, 1024, 512);

      // Outer & inner neon border
      ctx.strokeStyle = ad.border;
      ctx.lineWidth = 14;
      ctx.strokeRect(14, 14, 996, 484);
      ctx.strokeStyle = 'rgba(255,255,255,0.28)';
      ctx.lineWidth = 4;
      ctx.strokeRect(30, 30, 964, 452);

      // Top 60% Kannada Header Pill
      ctx.fillStyle = ad.border;
      ctx.beginPath();
      ctx.roundRect(52, 46, 460, 48, 10);
      ctx.fill();
      ctx.fillStyle = '#090d16';
      ctx.font = '900 24px "Noto Sans Kannada", "Inter", sans-serif';
      ctx.fillText(ad.badge, 70, 79);

      // 60:40 Rule Tag on top-right
      ctx.fillStyle = 'rgba(255,255,255,0.14)';
      ctx.beginPath();
      ctx.roundRect(750, 46, 220, 46, 8);
      ctx.fill();
      ctx.fillStyle = '#ffffff';
      ctx.font = '800 20px "Inter", sans-serif';
      ctx.fillText('ಕನ್ನಡ 60% • BBMP', 772, 76);

      // Prominent Kannada Headline (60% Primary Display)
      ctx.fillStyle = ad.accent;
      ctx.shadowColor = 'rgba(0,0,0,0.65)';
      ctx.shadowBlur = 10;
      ctx.font = '900 66px "Noto Sans Kannada", "Arial Unicode MS", sans-serif';
      ctx.fillText(ad.knTitle, 54, 185);

      // Kannada Sub-headline
      ctx.fillStyle = '#ffffff';
      ctx.font = '700 34px "Noto Sans Kannada", "Arial Unicode MS", sans-serif';
      ctx.fillText(ad.knSub, 54, 248);

      // Divider rule
      ctx.strokeStyle = ad.border;
      ctx.lineWidth = 4;
      ctx.beginPath();
      ctx.moveTo(54, 285);
      ctx.lineTo(968, 285);
      ctx.stroke();

      // English Headline (40% Secondary Display)
      ctx.fillStyle = '#ffffff';
      ctx.font = '900 48px "Inter", -apple-system, sans-serif';
      ctx.fillText(ad.enTitle, 54, 360);

      // English Sub-headline
      ctx.fillStyle = '#cbd5e1';
      ctx.font = '800 27px "Inter", -apple-system, sans-serif';
      ctx.fillText(ad.enSub, 54, 422);

      const tex = new THREE.CanvasTexture(c);
      tex.anisotropy = renderer.capabilities.getMaxAnisotropy();
      tex.colorSpace = THREE.SRGBColorSpace;
      return tex;
    }

    function createBilingualGantrySignTexture(isHebbal = false) {
      const c = document.createElement('canvas');
      c.width = 2048;
      c.height = 512;
      const ctx = c.getContext('2d');

      const g = ctx.createLinearGradient(0, 0, 0, 512);
      g.addColorStop(0, '#006b38');
      g.addColorStop(1, '#004725');
      ctx.fillStyle = g;
      ctx.fillRect(0, 0, 2048, 512);

      // White reflective highway border
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 16;
      ctx.strokeRect(18, 18, 2012, 476);

      // NH 44 Yellow Shield
      ctx.fillStyle = '#ffd000';
      ctx.beginPath();
      ctx.roundRect(56, 52, 180, 96, 14);
      ctx.fill();
      ctx.fillStyle = '#090d16';
      ctx.font = '900 44px "Inter", sans-serif';
      ctx.fillText('NH 44', 78, 116);

      // Top Bold Kannada Highway Destination
      ctx.fillStyle = '#fde047';
      ctx.font = '900 78px "Noto Sans Kannada", "Inter", sans-serif';
      ctx.fillText(
        isHebbal
          ? 'ಹೆಬ್ಬಾಳ ಮೇಲ್ಸೇತುವೆ • ಹೊರ ವರ್ತುಲ ರಸ್ತೆ (ORR)'
          : 'ಸಿಲ್ಕ್ ಬೋರ್ಡ್ ಜಂಕ್ಷನ್ • ಹೊಸೂರು ರಸ್ತೆ',
        270,
        125
      );

      // Middle Bold English Highway Destination
      ctx.fillStyle = '#ffffff';
      ctx.font = '900 58px "Inter", sans-serif';
      ctx.fillText(
        isHebbal
          ? 'HEBBAL FLYOVER • OUTER RING ROAD (KIAL AIRPORT)'
          : 'SILK BOARD JUNCTION • HOSUR ROAD (ELECTRONIC CITY)',
        270,
        215
      );

      // Horizontal Divider
      ctx.strokeStyle = 'rgba(255,255,255,0.75)';
      ctx.lineWidth = 6;
      ctx.beginPath();
      ctx.moveTo(40, 260);
      ctx.lineTo(2008, 260);
      ctx.stroke();

      // 3 Bilingual Lane Guidance Columns
      const cols = isHebbal
        ? [
            { x: 110, kn: '← ಯಶವಂತಪುರ', en: 'YESHWANTHPUR' },
            { x: 760, kn: '↑ ಕೆಂಪೇಗೌಡ ಏರ್‌ಪೋರ್ಟ್', en: 'BENGALURU AIRPORT' },
            { x: 1470, kn: '→ ಮಾರತ್ತಹಳ್ಳಿ', en: 'MARATHAHALLI' }
          ]
        : [
            { x: 110, kn: '← ಬಿಟಿಎಂ ಲೇಔಟ್', en: 'BTM LAYOUT' },
            { x: 760, kn: '↑ ಎಲೆಕ್ಟ್ರಾನಿಕ್ ಸಿಟಿ', en: 'ELECTRONIC CITY' },
            { x: 1470, kn: '→ ಎಚ್‌ಎಸ್‌ಆರ್ ಲೇಔಟ್', en: 'HSR LAYOUT' }
          ];

      cols.forEach((col) => {
        ctx.fillStyle = '#fde047';
        ctx.font = '900 44px "Noto Sans Kannada", "Inter", sans-serif';
        ctx.fillText(col.kn, col.x, 355);
        ctx.fillStyle = '#ffffff';
        ctx.font = '800 34px "Inter", sans-serif';
        ctx.fillText(col.en, col.x, 425);
      });

      const tex = new THREE.CanvasTexture(c);
      tex.anisotropy = renderer.capabilities.getMaxAnisotropy();
      tex.colorSpace = THREE.SRGBColorSpace;
      return tex;
    }

    // Build Scrolling Corridor Segments (6m each) — Includes Viaduct, Streetlamps & Skyline
    const scrollingStrips = [];
    const whiteDashMat = new THREE.MeshBasicMaterial({ color: 0xf1f5f9 });
    const yellowLineMat = new THREE.MeshBasicMaterial({ color: 0xffd000 });
    const kerbYellowMat = new THREE.MeshStandardMaterial({ color: 0xffd000, roughness: 0.42 });
    const kerbBlackMat = new THREE.MeshStandardMaterial({ color: 0x1e2430, roughness: 0.65 });
    const concreteMat = new THREE.MeshStandardMaterial({ color: 0x94a3b8, roughness: 0.72 });
    const metroPurpleMat = new THREE.MeshStandardMaterial({
      color: 0x7c3aed,
      roughness: 0.32,
      emissive: 0x5b21b6,
      emissiveIntensity: 0.45
    });
    const poleMetalMat = new THREE.MeshStandardMaterial({ color: 0x475569, metalness: 0.85, roughness: 0.25 });
    const lampBulbMat = new THREE.MeshBasicMaterial({ color: 0xfff3c4 });
    const treeTrunkMat = new THREE.MeshStandardMaterial({ color: 0x5c4033, roughness: 0.9 });
    const treeLeafMat = new THREE.MeshStandardMaterial({ color: 0x2d6a4f, roughness: 0.75 });
    const gulmoharLeafMat = new THREE.MeshStandardMaterial({ color: 0x40916c, roughness: 0.7 });

    const dashGeo = new THREE.BoxGeometry(0.16, 0.02, 2.8);
    const kerbGeo = new THREE.BoxGeometry(0.55, 0.26, 6.02);
    const viaductDeckGeo = new THREE.BoxGeometry(6.8, 1.1, 6.06);
    const viaductWallGeo = new THREE.BoxGeometry(0.26, 1.15, 6.06);
    const viaductPierGeo = new THREE.CylinderGeometry(0.95, 1.05, 7.6, 14);
    const viaductCapGeo = new THREE.BoxGeometry(5.8, 1.1, 2.0);

    const METRO_X = 18.5;

    for (let z = 36; z > -CORRIDOR_LENGTH + 36; z -= 6) {
      const segIdx = Math.round(Math.abs(z) / 6);
      const row = new THREE.Group();
      row.position.z = z;

      // Lane Divider Dashes between the 6 lanes
      for (const lx of [-7.6, -3.8, 0.0, 3.8, 7.6]) {
        if (lx === 0.0) {
          const cl = new THREE.Mesh(new THREE.BoxGeometry(0.24, 0.022, 6.02), yellowLineMat);
          cl.position.set(0, 0.012, 0);
          row.add(cl);
        } else if (segIdx % 2 === 0) {
          const dash = new THREE.Mesh(dashGeo, whiteDashMat);
          dash.position.set(lx, 0.012, 0);
          row.add(dash);
        }
      }

      // Yellow-and-Black Bengaluru Roadside Kerbs
      const kMat = segIdx % 2 === 0 ? kerbYellowMat : kerbBlackMat;
      const kerbL = new THREE.Mesh(kerbGeo, kMat);
      kerbL.position.set(-ROAD_WIDTH / 2 - 0.28, 0.13, 0);
      const kerbR = new THREE.Mesh(kerbGeo, kMat);
      kerbR.position.set(ROAD_WIDTH / 2 + 0.28, 0.13, 0);
      row.add(kerbL, kerbR);

      // Painted White Zebra Crossings at key pedestrian crossing intervals
      if (segIdx % 14 === 3) {
        const zebraGeo = new THREE.BoxGeometry(0.95, 0.024, 3.8);
        for (let zx = -9.6; zx <= 9.6; zx += 1.6) {
          if (Math.abs(zx) < 0.5) continue;
          const stripe = new THREE.Mesh(zebraGeo, whiteDashMat);
          stripe.position.set(zx, 0.014, 0);
          row.add(stripe);
        }
      }

      // Continuous Unbroken Namma Metro Elevated Viaduct along X = +18.5
      const vDeck = new THREE.Mesh(viaductDeckGeo, concreteMat);
      vDeck.position.set(METRO_X, 8.2, 0);
      vDeck.receiveShadow = true;
      const vWallL = new THREE.Mesh(viaductWallGeo, metroPurpleMat);
      vWallL.position.set(METRO_X - 3.3, 9.1, 0);
      const vWallR = new THREE.Mesh(viaductWallGeo, metroPurpleMat);
      vWallR.position.set(METRO_X + 3.3, 9.1, 0);
      row.add(vDeck, vWallL, vWallR);

      if (segIdx % 3 === 0) {
        const pier = new THREE.Mesh(viaductPierGeo, concreteMat);
        pier.position.set(METRO_X, 3.8, 0);
        const cap = new THREE.Mesh(viaductCapGeo, concreteMat);
        cap.position.set(METRO_X, 7.3, 0);
        row.add(pier, cap);
      }

      // Lush Bengaluru Rain Trees (set behind hoardings) & Warm LED Highway Streetlamps
      if (segIdx % 5 === 0) {
        const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.28, 0.38, 3.6, 8), treeTrunkMat);
        trunk.position.set(-ROAD_WIDTH / 2 - 11.2, 1.8, 0);
        const crown1 = new THREE.Mesh(new THREE.SphereGeometry(2.6, 12, 10), segIdx % 10 === 0 ? treeLeafMat : gulmoharLeafMat);
        crown1.scale.set(1.25, 0.68, 1.25);
        crown1.position.set(-ROAD_WIDTH / 2 - 11.2, 4.6, 0);
        row.add(trunk, crown1);

        // Dual Boulevard Streetlamp
        const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.13, 7.5, 8), poleMetalMat);
        pole.position.set(-ROAD_WIDTH / 2 - 1.2, 3.75, 2.2);
        const arm = new THREE.Mesh(new THREE.BoxGeometry(1.8, 0.10, 0.10), poleMetalMat);
        arm.position.set(-ROAD_WIDTH / 2 - 0.4, 7.4, 2.2);
        const bulb = new THREE.Mesh(new THREE.BoxGeometry(0.55, 0.08, 0.24), lampBulbMat);
        bulb.position.set(-ROAD_WIDTH / 2 + 0.2, 7.34, 2.2);
        row.add(pole, arm, bulb);
      }

      scene.add(row);
      scrollingStrips.push(row);
    }

    // Build Illuminated Bilingual (Kannada + English) Roadside Hoardings & Tech Park Skyline
    const hoardingGroup = new THREE.Group();
    scene.add(hoardingGroup);
    const hoardingInstances = [];

    function buildBilingualHoardings() {
      const frameMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, metalness: 0.75, roughness: 0.3 });
      const glowBarMat = new THREE.MeshBasicMaterial({ color: 0xfffbeb });

      for (let i = 0; i < BILINGUAL_HOARDING_ADS.length; i++) {
        const ad = BILINGUAL_HOARDING_ADS[i];
        const tex = createBilingualHoardingTexture(ad);
        const g = new THREE.Group();

        const isLeft = i % 2 === 0;
        const w = 9.0;
        const h = 4.5;

        // Steel support pillars
        for (const px of [-w * 0.36, w * 0.36]) {
          const post = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.22, 4.6, 10), poleMetalMat);
          post.position.set(px, 2.3, 0);
          g.add(post);
        }

        // Backing cabinet
        const cabinet = new THREE.Mesh(new THREE.BoxGeometry(w + 0.35, h + 0.35, 0.28), frameMat);
        cabinet.position.set(0, 5.8, 0);
        g.add(cabinet);

        // Illuminated Bilingual Ad Face (Self-lit so Kannada & English text is super crisp day or rain!)
        const faceMat = new THREE.MeshBasicMaterial({ map: tex });
        const faceFront = new THREE.Mesh(new THREE.PlaneGeometry(w, h), faceMat);
        faceFront.position.set(0, 5.8, 0.16);
        g.add(faceFront);

        // Top LED floodlight bar
        const floodBar = new THREE.Mesh(new THREE.BoxGeometry(w * 0.92, 0.14, 0.35), glowBarMat);
        floodBar.position.set(0, 5.8 + h * 0.5 + 0.18, 0.22);
        g.add(floodBar);

        const xPos = isLeft ? (-ROAD_WIDTH / 2 - 5.2) : (ROAD_WIDTH / 2 + 4.4);
        const zPos = -18 - i * (CORRIDOR_LENGTH / BILINGUAL_HOARDING_ADS.length);
        g.position.set(xPos, 0, zPos);
        // Angle slightly toward the road so driver reads Kannada + English effortlessly
        g.rotation.y = isLeft ? 0.34 : -0.34;

        hoardingGroup.add(g);
        hoardingInstances.push(g);
      }
    }
    buildBilingualHoardings();

    // Dynamic Scrolling Bangalore Landmarks (Silk Board Gantry with Kannada+English, Vidhana Soudha, Metro)
    const landmarkInstances = [];
    let continuousMetroTrain = null;

    function spawnLandmarksFromGLB() {
      // 1. Massive "Silk Board" & "Hebbal" Bilingual Highway Green Sign Gantries
      const gantryConfigs = [
        {
          zPos: -42,
          isHebbal: false,
          kn: 'ಸಿಲ್ಕ್ ಬೋರ್ಡ್ ಮೇಲ್ಸೇತುವೆ',
          en: 'SILK BOARD FLYOVER GANTRY'
        },
        {
          zPos: -222,
          isHebbal: true,
          kn: 'ಹೆಬ್ಬಾಳ ಮೇಲ್ಸೇತುವೆ (ORR)',
          en: 'HEBBAL FLYOVER GANTRY'
        }
      ];

      gantryConfigs.forEach((cfg) => {
        const silk = loadedTemplates['silk_board_sign.glb'].clone(true);
        const signTex = createBilingualGantrySignTexture(cfg.isHebbal);
        const signMat = new THREE.MeshBasicMaterial({ map: signTex });

        // Attach ultra-crisp Bilingual Kannada+English highway signboard over the 3D gantry frame
        const frontBoard = new THREE.Mesh(new THREE.PlaneGeometry(19.4, 3.75), signMat);
        frontBoard.position.set(0, 8.85, 0.72);
        silk.add(frontBoard);

        const backBoard = new THREE.Mesh(new THREE.PlaneGeometry(19.4, 3.75), signMat);
        backBoard.position.set(0, 8.85, -0.72);
        backBoard.rotation.y = Math.PI;
        silk.add(backBoard);

        silk.position.set(0, 0, cfg.zPos);
        scene.add(silk);
        landmarkInstances.push({
          mesh: silk,
          kn: cfg.kn,
          type: cfg.en
        });
      });

      // 2. Vidhana Soudha Grand Facade along the Left Boulevard Vista
      for (const zPos of [-135, -315]) {
        const vidhana = loadedTemplates['vidhana_soudha.glb'].clone(true);
        vidhana.position.set(-32, 0, zPos);
        vidhana.rotation.y = Math.PI * 0.42;
        scene.add(vidhana);
        landmarkInstances.push({
          mesh: vidhana,
          kn: 'ವಿಧಾನ ಸೌಧ • ಬೆಂಗಳೂರು',
          type: 'VIDHANA SOUDHA GRAND FACADE'
        });
      }

      // 3. Namma Metro Station seamlessly aligned onto the continuous viaduct at X = METRO_X
      const metro = loadedTemplates['metro_station.glb'].clone(true);
      metro.position.set(METRO_X, 0, -185);
      metro.traverse((child) => {
        if (child.name && child.name.startsWith('Metro_Train')) {
          continuousMetroTrain = child;
        }
      });
      if (continuousMetroTrain) {
        scene.attach(continuousMetroTrain);
        continuousMetroTrain.position.set(METRO_X - 1.2, 0, -90);
      }
      scene.add(metro);
      landmarkInstances.push({
        mesh: metro,
        kn: 'ನಮ್ಮ ಮೆಟ್ರೋ ನೇರಳೆ ಮಾರ್ಗ ನಿಲ್ದಾಣ',
        type: 'NAMMA METRO PURPLE LINE STATION'
      });
    }

    // =========================================================================
    // 6. REALISTIC ASPHALT POTHOLES (Broken Crater + Puddle + Traffic Cone)
    // =========================================================================
    const potholes = [];
    const potholeGroup = new THREE.Group();
    scene.add(potholeGroup);

    const potholeRimMat = new THREE.MeshStandardMaterial({ color: 0x161922, roughness: 0.92 });
    const potholeWaterMat = new THREE.MeshStandardMaterial({
      color: 0x1e293b,
      roughness: 0.05,
      metalness: 0.85
    });
    const potholeGlowMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.55 });
    const coneOrangeMat = new THREE.MeshStandardMaterial({ color: 0xf97316, roughness: 0.35 });
    const coneWhiteMat = new THREE.MeshStandardMaterial({ color: 0xf8fafc, roughness: 0.25 });

    function rebuildPotholes(count) {
      while (potholeGroup.children.length > 0) {
        potholeGroup.remove(potholeGroup.children[0]);
      }
      potholes.length = 0;

      for (let i = 0; i < count; i++) {
        const g = new THREE.Group();
        const rim = new THREE.Mesh(new THREE.CylinderGeometry(1.55, 1.75, 0.06, 7), potholeRimMat);
        rim.position.y = 0.02;
        const puddle = new THREE.Mesh(new THREE.CylinderGeometry(1.25, 1.25, 0.07, 12), potholeWaterMat);
        puddle.position.y = 0.025;
        const anomalyRing = new THREE.Mesh(new THREE.RingGeometry(0.95, 1.12, 20), potholeGlowMat);
        anomalyRing.rotation.x = -Math.PI / 2;
        anomalyRing.position.y = 0.065;

        const cone = new THREE.Mesh(new THREE.ConeGeometry(0.22, 0.65, 12), coneOrangeMat);
        cone.position.set(1.45, 0.32, 0.4);
        const coneBand = new THREE.Mesh(new THREE.CylinderGeometry(0.11, 0.16, 0.18, 12), coneWhiteMat);
        coneBand.position.set(1.45, 0.36, 0.4);

        g.add(rim, puddle, anomalyRing, cone, coneBand);

        const laneX = LANES[Math.floor(Math.random() * LANES.length)] + (Math.random() - 0.5) * 0.8;
        g.position.set(laneX, 0, -35 - i * (CORRIDOR_LENGTH / count));
        potholeGroup.add(g);
        potholes.push({
          group: g,
          anomalyRing,
          phase: Math.random() * Math.PI * 2
        });
      }
    }

    // Tropical Rain Particle System (1600 Slanted Rain Streaks)
    const RAIN_COUNT = 1600;
    const rainGeo = new THREE.BufferGeometry();
    const rainPositions = new Float32Array(RAIN_COUNT * 6);
    for (let i = 0; i < RAIN_COUNT; i++) {
      const rx = (Math.random() - 0.5) * 50;
      const ry = Math.random() * 26;
      const rz = 10 - Math.random() * 90;
      const idx = i * 6;
      rainPositions[idx] = rx;
      rainPositions[idx + 1] = ry;
      rainPositions[idx + 2] = rz;
      rainPositions[idx + 3] = rx - 0.2;
      rainPositions[idx + 4] = ry - 1.25;
      rainPositions[idx + 5] = rz + 0.4;
    }
    rainGeo.setAttribute('position', new THREE.BufferAttribute(rainPositions, 3));
    const rainMat = new THREE.LineBasicMaterial({ color: 0xbae6fd, transparent: true, opacity: 0.0 });
    const rainLines = new THREE.LineSegments(rainGeo, rainMat);
    scene.add(rainLines);

    // Collision Sparks & Detached Flying Wheels Pool
    const detachedWheels = [];
    const sparkParticles = [];
    const sparkGeo = new THREE.BoxGeometry(0.10, 0.10, 0.10);
    const sparkMat = new THREE.MeshBasicMaterial({ color: 0xffaa00 });

    function spawnCollisionSparks(worldPos, count = 12, colorHex = 0xffaa00) {
      const mat = colorHex === 0xffaa00 ? sparkMat : new THREE.MeshBasicMaterial({ color: colorHex });
      for (let i = 0; i < count; i++) {
        const m = new THREE.Mesh(sparkGeo, mat);
        m.position.copy(worldPos);
        scene.add(m);
        sparkParticles.push({
          mesh: m,
          vx: (Math.random() - 0.5) * 12,
          vy: 2 + Math.random() * 8,
          vz: (Math.random() - 0.5) * 12,
          life: 0.45 + Math.random() * 0.3
        });
      }
    }

    // =========================================================================
    // 7. PLAYER AUTO-RICKSHAW (With Bilingual Rear Hood Decal & Headlight Beam)
    // =========================================================================
    function extractWheelNodes(rootMesh) {
      const wheels = [];
      rootMesh.traverse((node) => {
        if (node.name && node.name.startsWith('Wheel_')) {
          wheels.push({
            node,
            origLocalPos: node.position.clone(),
            origLocalQuat: node.quaternion.clone(),
            attached: true
          });
        }
      });
      return wheels;
    }

    function createAutoBackDecalTexture() {
      const c = document.createElement('canvas');
      c.width = 512;
      c.height = 160;
      const ctx = c.getContext('2d');
      ctx.fillStyle = '#111827';
      ctx.fillRect(0, 0, 512, 160);
      ctx.strokeStyle = '#ffd000';
      ctx.lineWidth = 8;
      ctx.strokeRect(6, 6, 500, 148);
      ctx.fillStyle = '#fde047';
      ctx.font = '900 42px "Noto Sans Kannada", "Inter", sans-serif';
      ctx.fillText('ನಮ್ಮ ಬೆಂಗಳೂರು • ಒಂದು ಸೆಕೆಂಡ್', 28, 68);
      ctx.fillStyle = '#4ade80';
      ctx.font = '900 30px "Inter", sans-serif';
      ctx.fillText('NAMMA BENGALURU • KA-01-AG-9999', 28, 124);
      const tex = new THREE.CanvasTexture(c);
      tex.colorSpace = THREE.SRGBColorSpace;
      return tex;
    }

    const player = {
      mesh: null,
      wheels: [],
      pos: new THREE.Vector3(-1.9, 0, 0),
      vel: new THREE.Vector3(0, 0, 0),
      rot: new THREE.Euler(0, 0, 0, 'YXZ'),
      forwardSpeed: 32,
      distanceKm: 0,
      radius: 1.0,
      mass: 1.4,
      fareRupees: 30.0,
      wheelRepairTimer: 0,
      hornCooldown: 0,
      dlVerifiedTimer: 0
    };

    function createPlayerAuto() {
      if (player.mesh) scene.remove(player.mesh);
      player.mesh = loadedTemplates['auto_rickshaw.glb'].clone(true);
      player.mesh.traverse((c) => {
        if (c.isMesh) {
          c.castShadow = true;
          c.receiveShadow = true;
        }
      });

      // Add Bilingual Kannada+English Stencil Plate on Rear Canopy Hood
      const decalMesh = new THREE.Mesh(
        new THREE.PlaneGeometry(0.92, 0.26),
        new THREE.MeshBasicMaterial({ map: createAutoBackDecalTexture() })
      );
      decalMesh.position.set(0, 1.16, 1.06);
      decalMesh.rotation.x = -0.08;
      player.mesh.add(decalMesh);

      player.wheels = extractWheelNodes(player.mesh);
      scene.add(player.mesh);
      updateWheelHUD();
    }

    function snapOffVehicleWheel(entity, isPlayer = false) {
      const attachedList = entity.wheels.filter((w) => w.attached);
      if (attachedList.length === 0) return false;
      const chosen = attachedList[Math.floor(Math.random() * attachedList.length)];
      chosen.attached = false;

      const worldPos = new THREE.Vector3();
      const worldQuat = new THREE.Quaternion();
      chosen.node.getWorldPosition(worldPos);
      chosen.node.getWorldQuaternion(worldQuat);
      chosen.node.visible = false;

      const flyingWheel = chosen.node.clone(true);
      flyingWheel.visible = true;
      flyingWheel.position.copy(worldPos);
      flyingWheel.quaternion.copy(worldQuat);
      scene.add(flyingWheel);

      detachedWheels.push({
        mesh: flyingWheel,
        vx: (Math.random() - 0.5) * 14,
        vy: 5 + Math.random() * 8,
        vz: -player.forwardSpeed * 0.35 + (Math.random() - 0.5) * 10,
        avx: (Math.random() - 0.5) * 14,
        avy: (Math.random() - 0.5) * 14,
        avz: (Math.random() - 0.5) * 14,
        life: 4.0
      });

      audio.playWheelSnap();
      spawnCollisionSparks(worldPos, 14, 0xff5500);

      if (isPlayer) {
        player.wheelRepairTimer = 6.0;
        updateWheelHUD();
        spawnComicCallout(worldPos, '🔧 WHEEL SNAPPED! PRESS [R] TO FIX', '#ff3b5c');
      }
      return true;
    }

    function reattachAllPlayerWheels() {
      let fixed = false;
      player.wheels.forEach((w) => {
        if (!w.attached) {
          w.attached = true;
          w.node.visible = true;
          w.node.position.copy(w.origLocalPos);
          w.node.quaternion.copy(w.origLocalQuat);
          fixed = true;
        }
      });
      player.wheelRepairTimer = 0;
      updateWheelHUD();
      if (fixed) {
        spawnComicCallout(player.pos, '🔧 ALL 3 AUTO WHEELS RESTORED!', '#4ade80');
      }
    }

    function updateWheelHUD() {
      for (let i = 0; i < 3; i++) {
        const pill = document.getElementById(`w-pill-${i}`);
        if (!pill) continue;
        const w = player.wheels[i];
        pill.classList.toggle('snapped', Boolean(w && !w.attached));
      }
    }

    // =========================================================================
    // 7B. TWO-WAY GROUNDED LANE TRAFFIC POOL
    // =========================================================================
    const trafficPool = [];

    const VEHICLE_SPECS = {
      zepto: {
        asset: 'delivery_zepto.glb',
        color: '#10f560',
        colorHex: 0x10f560,
        isHyperDelivery: true,
        radius: 0.75,
        lengthZ: 2.2,
        mass: 0.85,
        hornType: 'scooter',
        callouts: ['⚡ ZEPTO 10-MIN CUT-OFF!', '🟢 ZERO-G GROCERY BOUNCE!', '💨 MOVE ANNA!']
      },
      blinkit: {
        asset: 'delivery_blinkit.glb',
        color: '#ffe600',
        colorHex: 0xffe600,
        isHyperDelivery: true,
        radius: 0.75,
        lengthZ: 2.2,
        mass: 0.85,
        hornType: 'scooter',
        callouts: ['⚡ BLINKIT INSTANT CUT!', '🟡 EXPRESS DELIVERY BOUNCE!']
      },
      swiggy: {
        asset: 'delivery_swiggy.glb',
        color: '#fc8019',
        colorHex: 0xfc8019,
        isHyperDelivery: false,
        radius: 0.75,
        lengthZ: 2.2,
        mass: 0.9,
        hornType: 'scooter',
        callouts: ['🧡 SWIGGY HOT BIRYANI!', '🍛 EXPRESS ORDER ANNA!']
      },
      techie: {
        asset: 'commuter_techie.glb',
        color: '#38bdf8',
        colorHex: 0x38bdf8,
        isHyperDelivery: false,
        radius: 0.75,
        lengthZ: 2.2,
        mass: 0.95,
        hornType: 'scooter',
        callouts: ['💻 LATE FOR STANDUP!', '🪪 DEPLOYING ON PROD!']
      },
      bmtc: {
        asset: 'bmtc_bus.glb',
        color: '#3b82f6',
        colorHex: 0x3b82f6,
        isHyperDelivery: false,
        radius: 1.65,
        lengthZ: 8.5,
        mass: 5.5,
        hornType: 'bus',
        callouts: ['🚌 BMTC 500D ಸಿಲ್ಕ್ ಬೋರ್ಡ್!', '📢 SIDE KODI! HEAVY BUS!']
      },
      npc_auto: {
        asset: 'auto_rickshaw.glb',
        color: '#ffd000',
        colorHex: 0xffd000,
        isHyperDelivery: false,
        radius: 0.98,
        lengthZ: 2.8,
        mass: 1.35,
        hornType: 'auto',
        callouts: ['🛺 ಒಂದು ಸೆಕೆಂಡ್ ಅಣ್ಣ! ONDU SECOND!', '💸 METER ONE-AND-HALF!']
      }
    };

    function pickVehicleType(profile) {
      const r = Math.random();
      if (r < profile.busRatio) return 'bmtc';
      if (r < profile.busRatio + profile.deliveryRatio) {
        const dr = Math.random();
        if (dr < 0.4) return 'zepto';
        if (dr < 0.8) return 'blinkit';
        return 'swiggy';
      }
      return Math.random() < 0.6 ? 'techie' : 'npc_auto';
    }

    function findFreeLaneAndZ(preferBehind = false, forceOncoming = null) {
      for (let attempt = 0; attempt < 24; attempt++) {
        let laneIdx;
        if (forceOncoming === true) {
          laneIdx = 3 + Math.floor(Math.random() * 3);
        } else if (forceOncoming === false) {
          laneIdx = Math.floor(Math.random() * 3);
        } else {
          laneIdx = Math.floor(Math.random() * LANES.length);
        }
        const isOncoming = laneIdx >= 3;
        const laneX = LANES[laneIdx];
        const z = (!isOncoming && preferBehind)
          ? 16 + Math.random() * 18
          : -32 - Math.random() * (CORRIDOR_LENGTH - 65);

        let clear = true;
        for (const other of trafficPool) {
          if (Math.abs(other.pos.x - laneX) < 2.2 && Math.abs(other.pos.z - z) < 16.0) {
            clear = false;
            break;
          }
        }
        if (clear) return { laneIdx, laneX, z, isOncoming };
      }
      const fallbackLane = forceOncoming === true ? 4 : forceOncoming === false ? 1 : Math.floor(Math.random() * LANES.length);
      return {
        laneIdx: fallbackLane,
        laneX: LANES[fallbackLane],
        z: -45 - Math.random() * (CORRIDOR_LENGTH - 75),
        isOncoming: fallbackLane >= 3
      };
    }

    const HERO_SLOTS = [
      { type: 'techie', laneIdx: 2, z: -13.5 },
      { type: 'bmtc', laneIdx: 0, z: -27.0 },
      { type: 'swiggy', laneIdx: 1, z: -22.5 },
      { type: 'npc_auto', laneIdx: 3, z: -15.0 },
      { type: 'bmtc', laneIdx: 4, z: -23.0 },
      { type: 'zepto', laneIdx: 5, z: -11.5 },
      { type: 'blinkit', laneIdx: 3, z: -29.0 }
    ];

    function spawnTrafficVehicle(slotIndex, totalSlots) {
      const hero = slotIndex < HERO_SLOTS.length ? HERO_SLOTS[slotIndex] : null;
      const vKey = hero ? hero.type : pickVehicleType(currentProfile);
      const spec = VEHICLE_SPECS[vKey];
      const mesh = loadedTemplates[spec.asset].clone(true);
      mesh.traverse((c) => {
        if (c.isMesh) {
          c.castShadow = true;
          c.receiveShadow = true;
        }
      });

      const wheels = extractWheelNodes(mesh);
      const laneIdx = hero ? hero.laneIdx : slotIndex % LANES.length;
      const isOncoming = laneIdx >= 3;
      const laneX = LANES[laneIdx];
      const rowIdx = Math.floor(slotIndex / LANES.length);
      const zOffset = hero ? hero.z : -30 - rowIdx * 22 - (slotIndex % 3) * 6;

      const baseSpeed = spec.isHyperDelivery
        ? (28 + Math.random() * 10) * currentProfile.deliverySpeedMult
        : vKey === 'bmtc'
          ? 18 + Math.random() * 4
          : 22 + Math.random() * 6;

      const baseYaw = isOncoming ? Math.PI : 0;
      const targetVelZ = isOncoming ? baseSpeed * 0.42 : -baseSpeed;

      mesh.position.set(laneX, 0, zOffset);
      mesh.rotation.set(0, baseYaw, 0);
      scene.add(mesh);

      return {
        type: vKey,
        spec,
        mesh,
        wheels,
        pos: mesh.position,
        vel: new THREE.Vector3(0, 0, targetVelZ),
        rot: new THREE.Euler(0, baseYaw, 0, 'YXZ'),
        baseSpeed,
        isOncoming,
        baseYaw,
        laneIdx,
        targetLaneX: laneX,
        weaveTimer: 1.0 + Math.random() * 2.5,
        hitCooldown: 0
      };
    }

    function rebuildTrafficForProfile(profile) {
      trafficPool.forEach((v) => scene.remove(v.mesh));
      trafficPool.length = 0;

      for (let i = 0; i < profile.trafficCount; i++) {
        trafficPool.push(spawnTrafficVehicle(i, profile.trafficCount));
      }
    }

    function recycleTrafficVehicle(v) {
      v.wheels.forEach((w) => {
        w.attached = true;
        w.node.visible = true;
        w.node.position.copy(w.origLocalPos);
        w.node.quaternion.copy(w.origLocalQuat);
      });

      const spawnBehind = !v.isOncoming && v.spec.isHyperDelivery && Math.random() < 0.35;
      const spot = findFreeLaneAndZ(spawnBehind, v.isOncoming);
      v.laneIdx = spot.laneIdx;
      v.isOncoming = spot.isOncoming;
      v.baseYaw = v.isOncoming ? Math.PI : 0;
      v.targetLaneX = spot.laneX;
      v.pos.set(spot.laneX, 0, spot.z);
      v.baseSpeed = v.spec.isHyperDelivery
        ? (28 + Math.random() * 10) * currentProfile.deliverySpeedMult
        : v.type === 'bmtc'
          ? 18 + Math.random() * 4
          : 22 + Math.random() * 6;
      const targetVelZ = v.isOncoming ? v.baseSpeed * 0.42 : -v.baseSpeed;
      v.vel.set(0, 0, targetVelZ);
      v.rot.set(0, v.baseYaw, 0);
    }

    // =========================================================================
    // 7C. SUDDEN BENGALURU JAYWALKER PEDESTRIANS (Crossing Road + Stop Hand!)
    // =========================================================================
    const jaywalkers = [];
    const JAYWALKER_SHIRT_COLORS = [0xf97316, 0x06b6d4, 0xec4899, 0xeab308, 0x22c55e, 0xa855f7];
    const JAYWALKER_CALLOUTS = [
      '✋ "ಒಂದು ಸೆಕೆಂಡ್ ಅಣ್ಣ! ONDU SECOND!"',
      '🚶‍♂️ SUDDEN JAYWALKER ON ROAD!',
      '✋ "ಸ್ವಲ್ಪ ತಡೀರಿ! WAIT MAADI!"',
      '🛍️ UNCLE CROSSING SILK BOARD!'
    ];

    function spawnJaywalker(index, total) {
      const mesh = loadedTemplates['pedestrian_jaywalker.glb'].clone(true);
      let legL = null, legR = null, armL = null, armR = null;
      const shirtHex = JAYWALKER_SHIRT_COLORS[index % JAYWALKER_SHIRT_COLORS.length];

      mesh.traverse((c) => {
        if (c.isMesh) {
          c.castShadow = true;
          c.receiveShadow = true;
          if (c.name === 'Ped_Torso' && c.material) {
            c.material = c.material.clone();
            c.material.color.setHex(shirtHex);
          }
        }
        if (c.name === 'Leg_L') legL = c;
        if (c.name === 'Leg_R') legR = c;
        if (c.name === 'Arm_L') armL = c;
        if (c.name === 'Arm_R') armR = c;
      });

      let startX, startZ, dirX, state;
      if (index === 0) {
        startX = 0.6;
        startZ = -19.5;
        dirX = 1;
        state = 'crossing';
      } else if (index === 1) {
        startX = 3.6;
        startZ = -34.0;
        dirX = -1;
        state = 'crossing';
      } else {
        dirX = index % 2 === 0 ? 1 : -1;
        startX = dirX > 0 ? -ROAD_WIDTH / 2 - 0.8 : ROAD_WIDTH / 2 + 0.8;
        startZ = -48 - (index - 1) * (CORRIDOR_LENGTH / Math.max(4, total));
        state = 'waiting';
      }

      const yaw = dirX > 0 ? Math.PI * 0.42 : -Math.PI * 0.42;
      mesh.position.set(startX, 0, startZ);
      mesh.rotation.set(0, yaw, 0);
      scene.add(mesh);

      return {
        mesh,
        pos: mesh.position,
        legL,
        legR,
        armL,
        armR,
        dirX,
        state,
        crossSpeed: 3.6 + (index % 3) * 0.65,
        speedBoost: 1.0,
        triggerDist: 46 + (index % 4) * 7,
        walkPhase: index * 1.3,
        vy: 0,
        warned: index < 2,
        hitCooldown: 0
      };
    }

    function rebuildJaywalkers(count) {
      jaywalkers.forEach((p) => scene.remove(p.mesh));
      jaywalkers.length = 0;
      if (!loadedTemplates['pedestrian_jaywalker.glb']) return;
      for (let i = 0; i < count; i++) {
        jaywalkers.push(spawnJaywalker(i, count));
      }
    }

    function resetJaywalkerToKerb(p) {
      p.dirX = Math.random() < 0.5 ? 1 : -1;
      p.pos.x = p.dirX > 0 ? -ROAD_WIDTH / 2 - 0.9 : ROAD_WIDTH / 2 + 0.9;
      p.pos.y = 0;
      p.pos.z -= CORRIDOR_LENGTH + Math.random() * 25;
      p.state = 'waiting';
      p.speedBoost = 1.0;
      p.vy = 0;
      p.warned = false;
      p.triggerDist = 44 + Math.random() * 24;
      p.mesh.rotation.set(0, p.dirX > 0 ? Math.PI * 0.42 : -Math.PI * 0.42, 0);
    }

    // =========================================================================
    // 7D. NEW! BENGALURU TRAFFIC POLICE (BTP) SUDDEN LICENSE CHECK ("DL TORSI!")
    // =========================================================================
    const trafficCops = [];

    function createBtpBarricadeTexture() {
      const c = document.createElement('canvas');
      c.width = 512;
      c.height = 256;
      const ctx = c.getContext('2d');
      ctx.fillStyle = '#1e3a8a';
      ctx.fillRect(0, 0, 512, 256);
      ctx.strokeStyle = '#ffd000';
      ctx.lineWidth = 12;
      ctx.strokeRect(8, 8, 496, 240);
      ctx.fillStyle = '#fde047';
      ctx.font = '900 36px "Noto Sans Kannada", "Inter", sans-serif';
      ctx.fillText('ಬೆಂಗಳೂರು ಸಂಚಾರ ಪೊಲೀಸ್', 30, 82);
      ctx.fillStyle = '#ffffff';
      ctx.font = '900 30px "Inter", sans-serif';
      ctx.fillText('BENGALURU TRAFFIC POLICE', 28, 140);
      ctx.fillStyle = '#ef4444';
      ctx.fillRect(28, 165, 456, 62);
      ctx.fillStyle = '#ffffff';
      ctx.font = '900 30px "Inter", sans-serif';
      ctx.fillText('STOP • ನಿಲ್ಲಿಸಿ • DL & RC CHECK', 48, 207);
      const tex = new THREE.CanvasTexture(c);
      tex.colorSpace = THREE.SRGBColorSpace;
      return tex;
    }

    const btpBarricadeTex = createBtpBarricadeTexture();
    const strobeRedMat = new THREE.MeshBasicMaterial({ color: 0xff1e42 });
    const strobeBlueMat = new THREE.MeshBasicMaterial({ color: 0x2563eb });

    function spawnTrafficCopCheckpost(index, total) {
      const group = new THREE.Group();

      // 1. BTP Officer Mesh (`traffic_police.glb`)
      const copMesh = loadedTemplates['traffic_police.glb'].clone(true);
      let legL = null, legR = null, armL = null, armR = null;
      copMesh.traverse((c) => {
        if (c.isMesh) {
          c.castShadow = true;
          c.receiveShadow = true;
        }
        if (c.name === 'Cop_Leg_L') legL = c;
        if (c.name === 'Cop_Leg_R') legR = c;
        if (c.name === 'Cop_Arm_L') armL = c;
        if (c.name === 'Cop_Arm_R') armR = c;
      });
      // Rotate cop to face oncoming player auto (+Z) and scale slightly for arcade hero visibility
      copMesh.rotation.y = Math.PI;
      copMesh.scale.setScalar(1.18);
      group.add(copMesh);

      // 2. BTP Steel Checkpost Barricade with Flashing Red/Blue Police Strobe Lights
      const barricade = new THREE.Group();
      const board = new THREE.Mesh(
        new THREE.BoxGeometry(2.5, 1.25, 0.14),
        new THREE.MeshBasicMaterial({ map: btpBarricadeTex })
      );
      board.position.set(0, 1.0, 0);
      const leg1 = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 1.5, 8), poleMetalMat);
      leg1.position.set(-1.05, 0.75, 0);
      const leg2 = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 1.5, 8), poleMetalMat);
      leg2.position.set(1.05, 0.75, 0);
      const beaconR = new THREE.Mesh(new THREE.SphereGeometry(0.15, 10, 8), strobeRedMat);
      beaconR.position.set(-0.85, 1.75, 0);
      const beaconB = new THREE.Mesh(new THREE.SphereGeometry(0.15, 10, 8), strobeBlueMat);
      beaconB.position.set(0.85, 1.75, 0);
      barricade.add(board, leg1, leg2, beaconR, beaconB);
      barricade.position.set(-1.75, 0, 0.5);
      group.add(barricade);

      // Place first cop at z = -14.5m in Lane 1 so player sees & experiences the BTP checkpost right away!
      const startZ = index === 0 ? -14.5 : -48 - index * (CORRIDOR_LENGTH / Math.max(2, total));
      const kerbX = -ROAD_WIDTH / 2 + 1.15;
      const targetLaneIdx = index === 0 ? 1 : (index % 2 === 0 ? 0 : 1);
      group.position.set(index === 0 ? LANES[1] : kerbX, 0, startZ);
      scene.add(group);

      return {
        group,
        copMesh,
        barricade,
        beaconR,
        beaconB,
        legL,
        legR,
        armL,
        armR,
        pos: group.position,
        state: index === 0 ? 'stepping_out' : 'waiting', // waiting -> stepping_out -> cleared / fined
        targetX: LANES[targetLaneIdx],
        kerbX,
        triggerDist: 58,
        walkPhase: index * 1.7,
        whistleBlown: false,
        resolved: false
      };
    }

    function rebuildTrafficCops(count) {
      trafficCops.forEach((c) => scene.remove(c.group));
      trafficCops.length = 0;
      if (!loadedTemplates['traffic_police.glb']) return;
      for (let i = 0; i < count; i++) {
        trafficCops.push(spawnTrafficCopCheckpost(i, count));
      }
    }

    function resetCopCheckpost(cop) {
      cop.pos.z -= CORRIDOR_LENGTH + Math.random() * 30;
      cop.pos.x = cop.kerbX;
      cop.targetX = LANES[Math.floor(Math.random() * 2)]; // Left lanes 0 or 1
      cop.state = 'waiting';
      cop.whistleBlown = false;
      cop.resolved = false;
      if (cop.legL) cop.legL.rotation.x = 0;
      if (cop.legR) cop.legR.rotation.x = 0;
    }

    // =========================================================================
    // 7E. NEW! SUDDEN DARTING BENGALURU STRAY DOGS (`stray_dog.glb`)
    // =========================================================================
    const strayDogs = [];
    const DOG_COAT_COLORS = [0xb86b35, 0xd99b66, 0x4a3525, 0xe2e8f0];
    const DOG_CALLOUTS = [
      '🐕 "ಬೌ-ಬೌ! BOW-WOW!" STRAY DOG DARTING!',
      '🐕 SUDDEN INDIE DOGGO ON ROAD! WATCH OUT!',
      '🐾 STREET DOG CHASING SCOOTER!'
    ];

    function spawnStrayDog(index, total) {
      const mesh = loadedTemplates['stray_dog.glb'].clone(true);
      let legFL = null, legFR = null, legRL = null, legRR = null;
      const coatHex = DOG_COAT_COLORS[index % DOG_COAT_COLORS.length];

      mesh.traverse((c) => {
        if (c.isMesh) {
          c.castShadow = true;
          c.receiveShadow = true;
          if (c.name === 'Dog_Body' && c.material && index > 0) {
            c.material = c.material.clone();
            c.material.color.setHex(coatHex);
          }
        }
        if (c.name === 'Dog_Leg_FL') legFL = c;
        if (c.name === 'Dog_Leg_FR') legFR = c;
        if (c.name === 'Dog_Leg_RL') legRL = c;
        if (c.name === 'Dog_Leg_RR') legRR = c;
      });

      // Scale slightly so the Indie dog is clearly visible in arcade camera
      mesh.scale.setScalar(1.38);

      let dirX, startX, startZ, state;
      if (index === 0) {
        dirX = 1;
        startX = -0.3;
        startZ = -9.8;
        state = 'darting';
      } else {
        dirX = index % 2 === 0 ? 1 : -1;
        startX = dirX > 0 ? -ROAD_WIDTH / 2 - 1.2 : ROAD_WIDTH / 2 + 1.2;
        startZ = -36 - index * (CORRIDOR_LENGTH / Math.max(3, total));
        state = 'waiting';
      }

      // In Three.js after export_yup: +Y in Blender -> -Z in Three.js.
      // So rotation.y = -Math.PI/2 faces +X (right), and +Math.PI/2 faces -X (left).
      const yaw = dirX > 0 ? -Math.PI * 0.48 : Math.PI * 0.48;
      mesh.position.set(startX, 0, startZ);
      mesh.rotation.set(0, yaw, 0);
      scene.add(mesh);

      return {
        mesh,
        pos: mesh.position,
        legFL,
        legFR,
        legRL,
        legRR,
        dirX,
        state,
        runSpeed: 6.4 + (index % 3) * 1.1,
        speedBoost: 1.0,
        triggerDist: 42 + (index % 3) * 9,
        gallopPhase: index * 1.9,
        vy: 0,
        barked: index === 0,
        hopBonusAwarded: false,
        hitCooldown: 0
      };
    }

    function rebuildStrayDogs(count) {
      strayDogs.forEach((d) => scene.remove(d.mesh));
      strayDogs.length = 0;
      if (!loadedTemplates['stray_dog.glb']) return;
      for (let i = 0; i < count; i++) {
        strayDogs.push(spawnStrayDog(i, count));
      }
    }

    function resetStrayDogToKerb(d) {
      d.dirX = Math.random() < 0.5 ? 1 : -1;
      d.pos.x = d.dirX > 0 ? -ROAD_WIDTH / 2 - 1.2 : ROAD_WIDTH / 2 + 1.2;
      d.pos.y = 0;
      d.pos.z -= CORRIDOR_LENGTH + Math.random() * 25;
      d.state = 'waiting';
      d.speedBoost = 1.0;
      d.vy = 0;
      d.barked = false;
      d.hopBonusAwarded = false;
      d.triggerDist = 38 + Math.random() * 24;
      d.mesh.rotation.set(0, d.dirX > 0 ? -Math.PI * 0.48 : Math.PI * 0.48, 0);
    }

    // =========================================================================
    // 8. COMIC CALLOUTS, LICENSE CHECK ACTION & INPUT CONTROLS
    // =========================================================================
    const calloutLayer = document.getElementById('callout-layer');
    let lastCalloutTime = 0;

    function spawnComicCallout(worldPos, text, bgColor = '#ffd000') {
      const now = performance.now();
      if (now - lastCalloutTime < 190) return;
      lastCalloutTime = now;

      const proj = worldPos.clone().add(new THREE.Vector3(0, 2.0, 0)).project(camera);
      if (proj.z > 1) return;
      const x = (proj.x * 0.5 + 0.5) * window.innerWidth;
      const y = (-proj.y * 0.5 + 0.5) * window.innerHeight;

      const el = document.createElement('div');
      el.className = 'comic-pop';
      el.textContent = text;
      el.style.left = `${Math.min(window.innerWidth - 150, Math.max(150, x))}px`;
      el.style.top = `${Math.min(window.innerHeight - 95, Math.max(95, y))}px`;
      el.style.backgroundColor = bgColor;
      calloutLayer.appendChild(el);
      setTimeout(() => el.remove(), 1250);
    }

    function flashDigiLockerLicenseToCop() {
      audio.init();
      player.dlVerifiedTimer = 6.0;
      const dlBadge = document.getElementById('hud-dl-status');
      dlBadge.textContent = 'VERIFIED ✓ (+₹100)';

      let clearedAnyCop = false;
      trafficCops.forEach((cop) => {
        const distAhead = -cop.pos.z;
        if (distAhead > -8 && distAhead < 85 && !cop.resolved) {
          cop.resolved = true;
          cop.state = 'cleared';
          clearedAnyCop = true;
          player.fareRupees += 100;
          audio.playLicenseVerified();
          spawnComicCallout(
            cop.pos,
            '🪪 "ಸರಿ ಬಿಡಿ! ಮುಂದೆ ಹೋಗಿ!" (DL VERIFIED! +₹100)',
            '#4ade80'
          );
        }
      });

      if (!clearedAnyCop) {
        audio.playLicenseVerified();
        spawnComicCallout(player.pos, '🪪 DIGILOCKER DL & GREEN EMISSION READY!', '#4ade80');
      }
      document.getElementById('hud-cop-alert').classList.remove('visible');
      document.getElementById('vignette-fx').classList.remove('cop-strobe');
    }

    function triggerSuddenCopEncounterNow() {
      audio.init();
      if (trafficCops.length === 0) return;
      const cop = trafficCops[0];
      cop.pos.z = -12.5;
      cop.pos.x = -3.8;
      cop.targetX = -3.8;
      cop.state = 'stepping_out';
      cop.whistleBlown = true;
      cop.resolved = false;
      audio.playPoliceWhistle(false);
      document.getElementById('hud-cop-alert').classList.add('visible');
      document.getElementById('vignette-fx').classList.add('cop-strobe');
      spawnComicCallout(cop.pos, '👮‍♂️ "ಏಯ್ ಆಟೋ! ಸೈಡ್ ಹಾಕಿ! DL ತೋರಿಸಿ!" [PRESS L]', '#ef4444');
    }

    const keys = { up: false, down: false, left: false, right: false, space: false };

    window.addEventListener('keydown', (e) => {
      if (e.code === 'Escape') {
        e.preventDefault();
        toggleGravityModal();
        return;
      }
      audio.init();
      switch (e.code) {
        case 'KeyW':
        case 'ArrowUp':
          keys.up = true;
          break;
        case 'KeyS':
        case 'ArrowDown':
          keys.down = true;
          break;
        case 'KeyA':
        case 'ArrowLeft':
          keys.left = true;
          break;
        case 'KeyD':
        case 'ArrowRight':
          keys.right = true;
          break;
        case 'Space':
          e.preventDefault();
          if (!keys.space && player.pos.y < 0.5) {
            player.vel.y = currentProfile.glitchBounceVy;
            audio.playBounceImpact(false);
            spawnComicCallout(player.pos, '⚡ ZERO-G GLITCH HOP!', '#38bdf8');
          }
          keys.space = true;
          break;
        case 'KeyH':
          triggerPlayerHorn();
          break;
        case 'KeyL':
          flashDigiLockerLicenseToCop();
          break;
        case 'KeyC':
          triggerSuddenCopEncounterNow();
          break;
        case 'KeyR':
          reattachAllPlayerWheels();
          break;
        case 'KeyT':
          toggleManualRainStorm();
          break;
      }
    });

    window.addEventListener('keyup', (e) => {
      switch (e.code) {
        case 'KeyW':
        case 'ArrowUp':
          keys.up = false;
          break;
        case 'KeyS':
        case 'ArrowDown':
          keys.down = false;
          break;
        case 'KeyA':
        case 'ArrowLeft':
          keys.left = false;
          break;
        case 'KeyD':
        case 'ArrowRight':
          keys.right = false;
          break;
        case 'Space':
          keys.space = false;
          break;
      }
    });

    function triggerPlayerHorn() {
      if (player.hornCooldown > 0) return;
      player.hornCooldown = 0.28;
      audio.init();
      audio.playBeepBeepHorn('auto');
      spawnComicCallout(player.pos, '📯 ಪಾ-ಪಾ-ಪಾರ್ಪ್! ಸೈಡ್ ಕೊಡಿ! (SIDE KODI!)', '#ffd000');

      // Same-direction vehicles ahead yield slightly when honked at
      trafficPool.forEach((v) => {
        const dz = Math.abs(v.pos.z - player.pos.z);
        const dx = v.pos.x - player.pos.x;
        if (!v.isOncoming && dz < 16 && Math.abs(dx) < 4.5 && v.type !== 'bmtc') {
          const shiftDir = dx >= 0 ? 1 : -1;
          v.targetLaneX = THREE.MathUtils.clamp(v.targetLaneX + shiftDir * 3.8, LANES[0], LANES[2]);
        }
      });

      // Jaywalkers scurry faster across the road when honked at
      jaywalkers.forEach((p) => {
        const dz = p.pos.z - player.pos.z;
        if (dz < 2 && dz > -34 && p.state === 'crossing') {
          p.speedBoost = 1.85;
          spawnComicCallout(p.pos, '🏃‍♂️ "ಅಯ್ಯೋ! ತಡೀರಿ ಅಣ್ಣ! WAIT MAADI!"', '#fb923c');
        }
      });

      // Stray dogs bark back and bolt 2x faster when honked at!
      strayDogs.forEach((d) => {
        const dz = d.pos.z - player.pos.z;
        if (dz < 2 && dz > -38 && d.state === 'darting') {
          d.speedBoost = 2.0;
          audio.playDogBark();
          spawnComicCallout(d.pos, '🐕 "ಬೌ-ಬೌ! BOW-WOW!" BOLTING!', '#fde047');
        }
      });
    }

    // Weather & Modal Controls
    let rainActive = false;
    let rainIntensity = 0.0;
    let weatherTimer = 14.0;

    function toggleManualRainStorm() {
      rainActive = !rainActive;
      weatherTimer = rainActive ? currentProfile.rainStormDuration : currentProfile.rainCycleDuration;
      updateWeatherBanner();
    }

    function updateWeatherBanner() {
      document.getElementById('hud-weather-alert').classList.toggle('visible', rainActive);
    }

    const modal = document.getElementById('gravity-modal');
    let gamePaused = true;

    function applyGravityProfile(modeKey, closeDialog = true) {
      currentProfile = GRAVITY_PROFILES[modeKey] || GRAVITY_PROFILES.medium;

      document.querySelectorAll('[data-quick-mode]').forEach((btn) => {
        btn.classList.toggle('active-mode', btn.dataset.quickMode === modeKey);
      });
      document.querySelectorAll('.mode-card').forEach((card) => {
        card.classList.toggle('selected', card.dataset.mode === modeKey);
      });

      rebuildPotholes(currentProfile.potholeCount);
      rebuildTrafficForProfile(currentProfile);
      rebuildJaywalkers(currentProfile.jaywalkerCount);
      rebuildTrafficCops(currentProfile.copCount);
      rebuildStrayDogs(currentProfile.dogCount);
      reattachAllPlayerWheels();

      rainActive = false;
      rainIntensity = 0.0;
      weatherTimer = currentProfile.rainCycleDuration;
      updateWeatherBanner();
      document.getElementById('hud-cop-alert').classList.remove('visible');
      document.getElementById('vignette-fx').classList.remove('cop-strobe');

      if (closeDialog && modal.open) {
        modal.close();
      }
      gamePaused = false;
      audio.init();
    }

    function toggleGravityModal() {
      if (modal.open) {
        modal.close();
        gamePaused = false;
      } else {
        modal.showModal();
        gamePaused = true;
      }
    }

    modal.addEventListener('close', () => {
      gamePaused = false;
    });

    document.querySelectorAll('[data-select-mode]').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        applyGravityProfile(btn.dataset.selectMode, true);
      });
    });

    document.querySelectorAll('.mode-card').forEach((card) => {
      card.addEventListener('click', () => {
        applyGravityProfile(card.dataset.mode, true);
      });
    });

    document.querySelectorAll('[data-quick-mode]').forEach((btn) => {
      btn.addEventListener('click', () => {
        applyGravityProfile(btn.dataset.quickMode, false);
      });
    });

    document.getElementById('btn-horn-test').addEventListener('click', () => triggerPlayerHorn());
    document.getElementById('btn-cop-test').addEventListener('click', () => triggerSuddenCopEncounterNow());
    document.getElementById('btn-show-dl').addEventListener('click', () => flashDigiLockerLicenseToCop());
    document.getElementById('btn-open-modal').addEventListener('click', () => toggleGravityModal());
    document.getElementById('btn-rain-toggle').addEventListener('click', () => {
      audio.init();
      toggleManualRainStorm();
    });
    document.getElementById('btn-audio-toggle').addEventListener('click', (e) => {
      const on = audio.toggleMute();
      e.currentTarget.textContent = on ? '🔊 Audio' : '🔇 Muted';
    });

    // =========================================================================
    // 9. SIMULATION, TWO-WAY TRAFFIC, BTP COPS & STRAY DOGS PHYSICS LOOP
    // =========================================================================
    let cameraShake = 0;
    const clock = new THREE.Clock();

    function updateSimulation(dt, elapsed) {
      if (player.hornCooldown > 0) player.hornCooldown -= dt;
      if (player.dlVerifiedTimer > 0) {
        player.dlVerifiedTimer -= dt;
        if (player.dlVerifiedTimer <= 0) {
          document.getElementById('hud-dl-status').textContent = 'VALID • PRESS [L]';
        }
      }

      // 1. Weather State Machine & Hydroplaning
      weatherTimer -= dt;
      if (weatherTimer <= 0) {
        rainActive = !rainActive;
        weatherTimer = rainActive ? currentProfile.rainStormDuration : currentProfile.rainCycleDuration;
        updateWeatherBanner();
      }

      const targetRain = rainActive ? 1.0 : 0.0;
      rainIntensity += (targetRain - rainIntensity) * Math.min(1, dt * 2.5);
      rainMat.opacity = rainIntensity * 0.68;
      roadMat.roughness = 0.68 - rainIntensity * 0.54;
      roadMat.metalness = 0.14 + rainIntensity * 0.45;
      scene.background.lerpColors(drySkyColor, rainSkyColor, rainIntensity);
      scene.fog.color.copy(scene.background);

      if (rainIntensity > 0.02) {
        const posArr = rainGeo.attributes.position.array;
        for (let i = 0; i < RAIN_COUNT; i++) {
          const idx = i * 6;
          posArr[idx + 1] -= 36 * dt;
          posArr[idx + 4] -= 36 * dt;
          posArr[idx + 2] += player.forwardSpeed * 0.6 * dt;
          posArr[idx + 5] += player.forwardSpeed * 0.6 * dt;
          if (posArr[idx + 1] < 0) {
            const rx = player.pos.x + (Math.random() - 0.5) * 50;
            const ry = 22 + Math.random() * 5;
            const rz = player.pos.z + 10 - Math.random() * 90;
            posArr[idx] = rx;
            posArr[idx + 1] = ry;
            posArr[idx + 2] = rz;
            posArr[idx + 3] = rx - 0.2;
            posArr[idx + 4] = ry - 1.25;
            posArr[idx + 5] = rz + 0.4;
          }
        }
        rainGeo.attributes.position.needsUpdate = true;
      }

      const tireGrip = Math.max(0, 1.0 - rainIntensity);
      const gripPct = Math.round(tireGrip * 100);
      document.documentElement.style.setProperty('--grip-pct', `${Math.max(5, gripPct)}%`);
      document.documentElement.style.setProperty('--grip-hue', String(Math.round(tireGrip * 145)));
      document.getElementById('hud-grip-text').textContent =
        gripPct < 15 ? '0% HYDROPLANING!' : `${gripPct}% DRY ASPHALT`;

      // 2. Player Auto-Rickshaw Grounded Physics + Controlled Low-G Bounce
      const targetSpeed = keys.up ? 48 : keys.down ? 16 : 32;
      player.forwardSpeed += (targetSpeed - player.forwardSpeed) * dt * 3.5;
      player.distanceKm += (player.forwardSpeed * dt) / 1000;

      const steerInput = (keys.right ? 1 : 0) - (keys.left ? 1 : 0);
      const attachedWheelCount = player.wheels.filter((w) => w.attached).length;
      const wheelStability = 0.45 + 0.55 * (attachedWheelCount / 3);

      const steerAccel = (24 + (1 - tireGrip) * 8) * wheelStability;
      player.vel.x += steerInput * steerAccel * dt;

      if (attachedWheelCount < 3) {
        player.wheelRepairTimer -= dt;
        if (player.wheelRepairTimer <= 0) reattachAllPlayerWheels();
      }

      const lateralFrictionDamping = 0.65 + tireGrip * 5.5;
      player.vel.x *= Math.exp(-lateralFrictionDamping * dt);

      player.vel.y -= currentProfile.gravityReturn * dt;
      player.pos.x += player.vel.x * dt;
      player.pos.y += player.vel.y * dt;

      if (player.pos.y <= 0) {
        player.pos.y = 0;
        if (player.vel.y < -4.0) {
          player.vel.y = -player.vel.y * 0.30;
        } else {
          player.vel.y = 0;
        }
      }

      const maxRoadX = ROAD_WIDTH / 2 - 1.1;
      if (Math.abs(player.pos.x) > maxRoadX) {
        player.pos.x = Math.sign(player.pos.x) * maxRoadX;
        player.vel.x = -player.vel.x * 0.6;
      }

      const missingWheelTilt = (3 - attachedWheelCount) * 0.10;
      const targetPitch = THREE.MathUtils.clamp(-player.vel.y * 0.03 + (keys.up ? -0.03 : 0), -0.28, 0.28);
      const targetYaw = THREE.MathUtils.clamp(-steerInput * 0.10 - player.vel.x * 0.012, -0.32, 0.32);
      const targetRoll = THREE.MathUtils.clamp(-steerInput * 0.11 + missingWheelTilt, -0.28, 0.28);

      player.rot.x += (targetPitch - player.rot.x) * dt * 8.0;
      player.rot.y += (targetYaw - player.rot.y) * dt * 8.0;
      player.rot.z += (targetRoll - player.rot.z) * dt * 8.0;

      if (player.mesh) {
        player.mesh.position.copy(player.pos);
        player.mesh.rotation.copy(player.rot);
        player.wheels.forEach((w) => {
          if (w.attached) w.node.rotation.x -= (player.forwardSpeed * dt) / 0.28;
        });
      }

      // 3. Seamless Scrolling Corridor, Bilingual Hoardings, Viaduct & Metro Train
      const scrollStep = player.forwardSpeed * dt;
      scrollingStrips.forEach((row) => {
        row.position.z += scrollStep;
        if (row.position.z > 36) {
          row.position.z -= CORRIDOR_LENGTH;
        }
      });

      hoardingInstances.forEach((h) => {
        h.position.z += scrollStep;
        if (h.position.z > 36) {
          h.position.z -= CORRIDOR_LENGTH;
        }
      });

      if (continuousMetroTrain) {
        continuousMetroTrain.position.z += (player.forwardSpeed - 24) * dt;
        if (continuousMetroTrain.position.z > 65) {
          continuousMetroTrain.position.z = -CORRIDOR_LENGTH + 65;
        }
      }

      let nearestDist = Infinity;
      let nearestName = 'SILK BOARD JUNCTION';
      let nearestKn = 'ಸಿಲ್ಕ್ ಬೋರ್ಡ್ ಜಂಕ್ಷನ್';
      landmarkInstances.forEach((lm) => {
        lm.mesh.position.z += scrollStep;
        if (lm.mesh.position.z > 60) {
          lm.mesh.position.z -= CORRIDOR_LENGTH;
        }
        const distAhead = -lm.mesh.position.z;
        if (distAhead > -10 && distAhead < nearestDist) {
          nearestDist = distAhead;
          nearestName = lm.type;
          nearestKn = lm.kn;
        }
      });
      const distMeters = Math.max(0, Math.round(nearestDist));
      document.getElementById('hud-landmark').textContent = `${nearestName} • ${distMeters}m`;
      document.getElementById('hud-landmark-kn').textContent = `${nearestKn} • ${distMeters}m`;

      // 4. Realistic Potholes with Magnetic Pull & Gravity Glitch Hop
      potholes.forEach((p) => {
        p.group.position.z += scrollStep;
        p.anomalyRing.rotation.z += dt * 2.5;
        if (p.group.position.z > 20) {
          p.group.position.z -= CORRIDOR_LENGTH;
          p.group.position.x = LANES[Math.floor(Math.random() * LANES.length)];
        }

        if (player.pos.y < 1.2) {
          const dx = p.group.position.x - player.pos.x;
          const dz = p.group.position.z - player.pos.z;
          const distSq = dx * dx + dz * dz;
          const pullR = currentProfile.potholeRadius;
          if (distSq < pullR * pullR) {
            const dist = Math.max(0.5, Math.sqrt(distSq));
            const falloff = 1 - dist / pullR;
            player.vel.x += (dx / dist) * currentProfile.potholePullStrength * falloff * dt;

            if (dist < 1.35 && player.pos.y < 0.35) {
              player.vel.y = currentProfile.glitchBounceVy * 0.85;
              cameraShake = 0.3;
              audio.playBounceImpact(false);
              spawnComicCallout(player.pos, '🕳️ BBMP POTHOLE GRAVITY GLITCH!', '#38bdf8');
            }
          }
        }
      });

      // 5. Sudden Road-Crossing Bengaluru Jaywalkers
      for (let i = 0; i < jaywalkers.length; i++) {
        const p = jaywalkers[i];
        if (p.hitCooldown > 0) p.hitCooldown -= dt;
        p.pos.z += scrollStep;

        const distAhead = -p.pos.z;
        if (p.state === 'waiting' && distAhead < p.triggerDist && distAhead > 8) {
          p.state = 'crossing';
          if (!p.warned && distAhead < 48) {
            p.warned = true;
            const call = JAYWALKER_CALLOUTS[i % JAYWALKER_CALLOUTS.length];
            spawnComicCallout(p.pos, call, '#fb923c');
          }
        }

        if (p.state === 'crossing') {
          p.pos.x += p.dirX * p.crossSpeed * p.speedBoost * dt;
          p.walkPhase += dt * 11.5 * p.speedBoost;

          const swing = Math.sin(p.walkPhase) * 0.62;
          if (p.legL) p.legL.rotation.x = swing;
          if (p.legR) p.legR.rotation.x = -swing;
          if (p.armL) p.armL.rotation.x = -swing * 0.7;
          if (p.armR) p.armR.rotation.z = Math.sin(p.walkPhase * 1.4) * 0.22;

          if ((p.dirX > 0 && p.pos.x > ROAD_WIDTH / 2 + 1.0) || (p.dirX < 0 && p.pos.x < -ROAD_WIDTH / 2 - 1.0)) {
            p.state = 'crossed';
            if (p.legL) p.legL.rotation.x = 0;
            if (p.legR) p.legR.rotation.x = 0;
          }
        }

        if (p.pos.y > 0 || p.vy !== 0) {
          p.vy -= currentProfile.gravityReturn * dt;
          p.pos.y += p.vy * dt;
          if (p.pos.y <= 0) {
            p.pos.y = 0;
            p.vy = 0;
          }
        }

        const pdx = player.pos.x - p.pos.x;
        const pdz = player.pos.z - p.pos.z;
        if (Math.abs(pdx) < 1.1 && Math.abs(pdz) < 1.15 && player.pos.y < 1.6 && p.hitCooldown <= 0) {
          p.hitCooldown = 0.8;
          const push = pdx >= 0 ? 1 : -1;
          player.vel.x = push * 10.5;
          player.vel.y = currentProfile.glitchBounceVy * 0.9;
          p.vy = currentProfile.glitchBounceVy * 1.1;
          p.speedBoost = 1.9;
          cameraShake = 0.35;
          audio.playBeepBeepHorn('auto');
          audio.playBounceImpact(false);
          spawnCollisionSparks(p.pos, 10, 0xfb923c);
          spawnComicCallout(p.pos, '🤸 "ಅಯ್ಯೋ! ನೋಡ್ಕೊಂಡು ಹೋಗಿ ಅಣ್ಣ!"', '#ff3b5c');
        }

        if (p.pos.z > 20) {
          resetJaywalkerToKerb(p);
        }
      }

      // 5B. NEW! Sudden Bengaluru Traffic Police (BTP) License Check Encounter
      let anyCopAlertActive = false;
      for (let i = 0; i < trafficCops.length; i++) {
        const cop = trafficCops[i];
        cop.pos.z += scrollStep;
        cop.walkPhase += dt * 9.0;

        // Flash Red & Blue Police Barricade Strobe Beacons
        const strobeToggle = Math.floor(elapsed * 10) % 2 === 0;
        cop.beaconR.scale.setScalar(strobeToggle ? 1.35 : 0.85);
        cop.beaconB.scale.setScalar(strobeToggle ? 0.85 : 1.35);

        const distAhead = -cop.pos.z;

        // Cop suddenly blows whistle & steps out into the lane to check license!
        if (cop.state === 'waiting' && distAhead < cop.triggerDist && distAhead > 10) {
          cop.state = 'stepping_out';
          if (!cop.whistleBlown) {
            cop.whistleBlown = true;
            audio.playPoliceWhistle(false);
            spawnComicCallout(
              cop.pos,
              '👮‍♂️ "ಏಯ್ ಆಟೋ! ಸೈಡ್ ಹಾಕಿ! DL & RC ತೋರಿಸಿ!" [PRESS L]',
              '#ef4444'
            );
          }
        }

        if (cop.state === 'stepping_out' && !cop.resolved) {
          if (distAhead > -2 && distAhead < 56) {
            anyCopAlertActive = true;
          }
          // Step into target lane & wave Red LED Baton
          const stepErr = cop.targetX - cop.pos.x;
          cop.pos.x += Math.sign(stepErr) * Math.min(Math.abs(stepErr), 4.2 * dt);
          if (Math.abs(stepErr) > 0.1) {
            const swing = Math.sin(cop.walkPhase) * 0.55;
            if (cop.legL) cop.legL.rotation.x = swing;
            if (cop.legR) cop.legR.rotation.x = -swing;
          } else {
            if (cop.legL) cop.legL.rotation.x = 0;
            if (cop.legR) cop.legR.rotation.x = 0;
          }
          if (cop.armR) {
            cop.armR.rotation.z = Math.sin(elapsed * 8.5) * 0.35;
          }

          // If Player Auto has verified DL active, auto-clear when approaching!
          if (player.dlVerifiedTimer > 0 && distAhead < 22 && distAhead > 0) {
            cop.resolved = true;
            cop.state = 'cleared';
            player.fareRupees += 100;
            audio.playLicenseVerified();
            spawnComicCallout(cop.pos, '🪪 "ಸರಿ ಬಿಡಿ! ಮುಂದೆ ಹೋಗಿ!" (DL VERIFIED! +₹100)', '#4ade80');
          }

          // Check if Cop intercepts Player Auto without showing License!
          const cdx = player.pos.x - cop.pos.x;
          const cdz = player.pos.z - cop.pos.z;
          if (!cop.resolved && Math.abs(cdx) < 2.25 && Math.abs(cdz) < 2.0 && player.pos.y < 1.8) {
            cop.resolved = true;
            cop.state = 'fined';
            // Sudden BTP Traffic Stop! Brakes auto & issues e-Challan fine
            player.forwardSpeed = 11.0;
            player.vel.x = (cdx >= 0 ? 1 : -1) * 8.5;
            player.fareRupees = Math.max(30, player.fareRupees - 100);
            cameraShake = 0.42;
            audio.playPoliceWhistle(true);
            spawnCollisionSparks(cop.pos, 14, 0x3b82f6);
            document.getElementById('hud-dl-status').textContent = 'e-CHALLAN -₹100!';
            player.dlVerifiedTimer = 4.0;
            spawnComicCallout(
              cop.pos,
              '🚔 "DL ಎಲ್ಲಿದೆ ಸಾರ್?! ₹100 e-CHALLAN FINE!" (-₹100)',
              '#ef4444'
            );
          }

          // If player swerved cleanly past the checkpost without getting caught
          if (!cop.resolved && cop.pos.z > 4.5) {
            cop.resolved = true;
            cop.state = 'evaded';
            player.fareRupees += 60;
            audio.playPoliceWhistle(false);
            spawnComicCallout(
              cop.pos,
              '💨 DODGED BTP CHECKPOST! "ನಿಲ್ಲಿಸಿ! ಕ್ಯಾಮೆರಾ ಚಲನ್!" (+₹60)',
              '#38bdf8'
            );
          }
        } else if (cop.state === 'cleared') {
          // Cop steps politely back toward the kerb
          const backErr = cop.kerbX - cop.pos.x;
          cop.pos.x += Math.sign(backErr) * Math.min(Math.abs(backErr), 5.0 * dt);
        }

        if (cop.pos.z > 22) {
          resetCopCheckpost(cop);
        }
      }

      document.getElementById('hud-cop-alert').classList.toggle('visible', anyCopAlertActive);
      document.getElementById('vignette-fx').classList.toggle('cop-strobe', anyCopAlertActive);

      // 5C. NEW! Sudden Darting Bengaluru Indie Stray Dogs
      for (let i = 0; i < strayDogs.length; i++) {
        const d = strayDogs[i];
        if (d.hitCooldown > 0) d.hitCooldown -= dt;
        d.pos.z += scrollStep;

        const distAhead = -d.pos.z;
        if (d.state === 'waiting' && distAhead < d.triggerDist && distAhead > 6) {
          d.state = 'darting';
          if (!d.barked && distAhead < 45) {
            d.barked = true;
            audio.playDogBark();
            const msg = DOG_CALLOUTS[i % DOG_CALLOUTS.length];
            spawnComicCallout(d.pos, msg, '#fde047');
          }
        }

        if (d.state === 'darting') {
          d.pos.x += d.dirX * d.runSpeed * d.speedBoost * dt;
          d.gallopPhase += dt * 18.0 * d.speedBoost;

          // 4-leg bounding gallop cycle + subtle body hop
          const bound = Math.sin(d.gallopPhase) * 0.78;
          if (d.legFL) d.legFL.rotation.x = bound;
          if (d.legFR) d.legFR.rotation.x = Math.sin(d.gallopPhase + 0.6) * 0.78;
          if (d.legRL) d.legRL.rotation.x = -bound;
          if (d.legRR) d.legRR.rotation.x = -Math.sin(d.gallopPhase + 0.6) * 0.78;
          if (d.vy === 0) {
            d.pos.y = Math.abs(Math.sin(d.gallopPhase)) * 0.14;
          }

          if ((d.dirX > 0 && d.pos.x > ROAD_WIDTH / 2 + 1.5) || (d.dirX < 0 && d.pos.x < -ROAD_WIDTH / 2 - 1.5)) {
            d.state = 'crossed';
            d.pos.y = 0;
          }
        }

        if (d.vy !== 0) {
          d.vy -= currentProfile.gravityReturn * dt;
          d.pos.y += d.vy * dt;
          if (d.pos.y <= 0) {
            d.pos.y = 0;
            d.vy = 0;
          }
        }

        // Check interaction between Player Auto and Stray Dog
        const ddx = player.pos.x - d.pos.x;
        const ddz = player.pos.z - d.pos.z;
        if (Math.abs(ddx) < 1.15 && Math.abs(ddz) < 1.2) {
          if (player.pos.y >= 0.85 && !d.hopBonusAwarded) {
            // Player hopped cleanly over the stray dog with SPACE!
            d.hopBonusAwarded = true;
            player.fareRupees += 75;
            audio.playDogBark();
            spawnComicCallout(d.pos, '🐕 GRAVITY HOP OVER DOGGO! +₹75 GOOD BOY BONUS!', '#4ade80');
          } else if (player.pos.y < 0.85 && d.hitCooldown <= 0) {
            d.hitCooldown = 0.85;
            const push = ddx >= 0 ? 1 : -1;
            player.vel.x = push * 9.0;
            player.vel.y = currentProfile.glitchBounceVy * 0.75;
            d.vy = currentProfile.glitchBounceVy * 1.05;
            d.speedBoost = 2.2;
            cameraShake = 0.28;
            audio.playDogBark();
            audio.playBounceImpact(false);
            spawnCollisionSparks(d.pos, 8, 0xfde047);
            spawnComicCallout(d.pos, '🐕 "ಬೌ-ಬೌ! BOW-WOW! WATCH IT ANNA!"', '#fb923c');
          }
        }

        if (d.pos.z > 20) {
          resetStrayDogToKerb(d);
        }
      }

      // 6. Two-Way Grounded Lane Traffic AI (Left Side Forward -Z, Right Side Oncoming +Z)
      for (let i = 0; i < trafficPool.length; i++) {
        const v = trafficPool[i];
        if (v.hitCooldown > 0) v.hitCooldown -= dt;

        const minLane = v.isOncoming ? 3 : 0;
        const maxLane = v.isOncoming ? 5 : 2;

        for (let j = 0; j < trafficPool.length; j++) {
          if (i === j) continue;
          const other = trafficPool[j];
          if (other.isOncoming !== v.isOncoming) continue;
          const dz = v.isOncoming ? (other.pos.z - v.pos.z) : (v.pos.z - other.pos.z);
          if (dz > 0 && dz < 14 && Math.abs(v.pos.x - other.pos.x) < 2.2) {
            if (v.baseSpeed > other.baseSpeed) {
              const nextLane = minLane + ((v.laneIdx - minLane + 1) % 3);
              v.laneIdx = nextLane;
              v.targetLaneX = LANES[nextLane];
            }
          }
        }

        v.weaveTimer -= dt;
        if (v.spec.isHyperDelivery && v.weaveTimer <= 0) {
          v.weaveTimer = 1.2 + Math.random() * 1.4;
          if (Math.abs(v.pos.z - player.pos.z) < 38 && Math.random() < currentProfile.cutOffAggression) {
            const shift = Math.random() < 0.5 ? -1 : 1;
            v.laneIdx = THREE.MathUtils.clamp(v.laneIdx + shift, minLane, maxLane);
            v.targetLaneX = LANES[v.laneIdx];
          }
        }

        const relZSpeed = player.forwardSpeed + v.vel.z;
        v.pos.z += relZSpeed * dt;
        v.pos.x += v.vel.x * dt;
        v.pos.y += v.vel.y * dt;

        const laneErr = v.targetLaneX - v.pos.x;
        v.vel.x += laneErr * 7.5 * dt;
        v.vel.x *= Math.exp(-4.2 * dt);

        v.vel.y -= currentProfile.gravityReturn * dt;
        if (v.pos.y <= 0) {
          v.pos.y = 0;
          v.vel.y = 0;
        }

        const targetVelZ = v.isOncoming ? v.baseSpeed * 0.42 : -v.baseSpeed;
        v.vel.z += (targetVelZ - v.vel.z) * dt * 2.5;

        const dirSign = v.isOncoming ? -1 : 1;
        const npcPitch = THREE.MathUtils.clamp(-v.vel.y * 0.025 * dirSign, -0.22, 0.22);
        const npcYaw = v.baseYaw + THREE.MathUtils.clamp(-v.vel.x * 0.025 * dirSign, -0.25, 0.25);
        const npcRoll = THREE.MathUtils.clamp(-v.vel.x * 0.03 * dirSign, -0.22, 0.22);
        v.rot.set(npcPitch, npcYaw, npcRoll);

        v.mesh.position.copy(v.pos);
        v.mesh.rotation.copy(v.rot);

        v.wheels.forEach((w) => {
          if (w.attached) w.node.rotation.x -= (v.baseSpeed * dt) / 0.26;
        });

        // Player <-> NPC Collision Check
        const hitX = (player.radius + v.spec.radius) * 0.88;
        const hitZ = (1.2 + v.spec.lengthZ * 0.45);
        const dx = player.pos.x - v.pos.x;
        const dy = Math.abs(player.pos.y - v.pos.y);
        const dz = player.pos.z - v.pos.z;

        if (Math.abs(dx) < hitX && Math.abs(dz) < hitZ && dy < 2.0 && v.hitCooldown <= 0) {
          v.hitCooldown = 0.45;
          const isHyper = v.spec.isHyperDelivery;

          const pushDir = dx >= 0 ? 1 : -1;
          player.vel.x = pushDir * (isHyper ? 13.5 : 9.5);
          v.vel.x = -pushDir * (v.type === 'bmtc' ? 3.0 : 11.0);

          player.vel.y = isHyper ? currentProfile.glitchBounceVy * 1.15 : currentProfile.glitchBounceVy * 0.80;
          if (v.type !== 'bmtc') {
            v.vel.y = currentProfile.glitchBounceVy * 0.95;
          }

          audio.playBeepBeepHorn(v.spec.hornType);
          audio.playBounceImpact(isHyper);
          spawnCollisionSparks(v.pos, isHyper ? 18 : 10, v.spec.colorHex);
          cameraShake = isHyper ? 0.45 : 0.28;

          const bonus = isHyper ? 150 : 50;
          player.fareRupees += bonus;
          const msg = v.isOncoming
            ? `🚨 ರಾಂಗ್ ಸೈಡ್! WRONG-SIDE! ${v.spec.callouts[0]}`
            : `${v.spec.callouts[Math.floor(Math.random() * v.spec.callouts.length)]} +₹${bonus}`;
          spawnComicCallout(v.pos, msg, v.spec.color);

          if (Math.random() < 0.35 && v.type !== 'bmtc') {
            snapOffVehicleWheel(v, false);
          }
          if (Math.random() < (v.type === 'bmtc' ? 0.35 : 0.16)) {
            snapOffVehicleWheel(player, true);
          }
        }

        if (v.pos.z > 26 || v.pos.z < -CORRIDOR_LENGTH + 15) {
          recycleTrafficVehicle(v);
        }
      }

      // 7. Update Detached Flying Wheels & Sparks
      for (let i = detachedWheels.length - 1; i >= 0; i--) {
        const dw = detachedWheels[i];
        dw.life -= dt;
        dw.vy -= 18 * dt;
        dw.mesh.position.x += dw.vx * dt;
        dw.mesh.position.y += dw.vy * dt;
        dw.mesh.position.z += (player.forwardSpeed + dw.vz) * dt;
        dw.mesh.rotation.x += dw.avx * dt;
        dw.mesh.rotation.y += dw.avy * dt;
        if (dw.mesh.position.y < 0.26) {
          dw.mesh.position.y = 0.26;
          dw.vy = Math.abs(dw.vy) * 0.65;
        }
        if (dw.life <= 0) {
          scene.remove(dw.mesh);
          detachedWheels.splice(i, 1);
        }
      }

      for (let i = sparkParticles.length - 1; i >= 0; i--) {
        const sp = sparkParticles[i];
        sp.life -= dt;
        sp.vy -= 18 * dt;
        sp.mesh.position.x += sp.vx * dt;
        sp.mesh.position.y += sp.vy * dt;
        sp.mesh.position.z += (player.forwardSpeed + sp.vz) * dt;
        sp.mesh.scale.setScalar(Math.max(0.01, sp.life * 1.4));
        if (sp.life <= 0) {
          scene.remove(sp.mesh);
          sparkParticles.splice(i, 1);
        }
      }

      // 8. Smooth Chase Camera, Sky Dome Lock & HUD Updates
      if (cameraShake > 0) cameraShake = Math.max(0, cameraShake - dt * 1.8);
      const shakeX = (Math.random() - 0.5) * cameraShake;
      const shakeY = (Math.random() - 0.5) * cameraShake;

      camera.position.x += (player.pos.x * 0.58 - camera.position.x) * dt * 7.5 + shakeX;
      camera.position.y += (3.85 + player.pos.y * 0.45 - camera.position.y) * dt * 6.5 + shakeY;
      camera.position.z = 7.2;
      camera.lookAt(player.pos.x * 0.75, 1.25 + player.pos.y * 0.3, -14);

      skyDome.position.x = camera.position.x;

      const surgeMult = (rainActive ? 1.5 : 1.0) * currentProfile.fareRateMult;
      player.fareRupees += (player.forwardSpeed * 0.14 * surgeMult) * dt;
      const speedKmh = Math.round(player.forwardSpeed * 2.1);

      document.getElementById('hud-fare').textContent = `₹${player.fareRupees.toFixed(2)}`;
      document.getElementById('hud-dist').textContent = `${player.distanceKm.toFixed(1)} KM`;
      document.getElementById('surge-badge').textContent =
        rainActive ? `${surgeMult.toFixed(1)}x SURGE` : `${surgeMult.toFixed(1)}x HIRE`;
      document.getElementById('hud-speed').textContent = String(speedKmh);
      document.getElementById('hud-alt').textContent =
        player.pos.y > 0.15 ? `AIR +${player.pos.y.toFixed(1)}m` : 'ON ROAD';

      audio.updateContinuous(speedKmh, rainIntensity, player.pos.y);
    }

    function animate() {
      requestAnimationFrame(animate);
      const dt = Math.min(0.05, clock.getDelta());
      const elapsed = clock.getElapsedTime();

      if (!gamePaused && player.mesh) {
        updateSimulation(dt, elapsed);
      }

      composer.render();
    }

    window.addEventListener('resize', () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
      composer.setSize(window.innerWidth, window.innerHeight);
    });

    // =========================================================================
    // 10. BOOTSTRAP
    // =========================================================================
    async function bootGame() {
      const params = new URLSearchParams(window.location.search);
      const autoMode = params.get('autostart');
      if (autoMode && GRAVITY_PROFILES[autoMode]) {
        document.querySelectorAll('[data-quick-mode]').forEach((btn) => {
          btn.classList.toggle('active-mode', btn.dataset.quickMode === autoMode);
        });
      } else {
        modal.showModal();
        gamePaused = true;
      }

      const assetFiles = [
        'auto_rickshaw.glb',
        'traffic_police.glb',
        'stray_dog.glb',
        'delivery_swiggy.glb',
        'delivery_zepto.glb',
        'delivery_blinkit.glb',
        'commuter_techie.glb',
        'bmtc_bus.glb',
        'pedestrian_jaywalker.glb',
        'vidhana_soudha.glb',
        'metro_station.glb',
        'silk_board_sign.glb'
      ];

      let loadedCount = 0;
      await Promise.all(
        assetFiles.map(async (file) => {
          loadedTemplates[file] = await loadBlenderAsset(file);
          loadedCount++;
          const chip = document.querySelector(`.asset-chip[data-asset="${file}"]`);
          if (chip) chip.classList.add('loaded');
          document.getElementById('asset-load-summary').textContent =
            `Loaded ${loadedCount}/${assetFiles.length} Blender .glb assets ✓`;
        })
      );

      createPlayerAuto();
      spawnLandmarksFromGLB();

      if (autoMode && GRAVITY_PROFILES[autoMode]) {
        applyGravityProfile(autoMode, true);
        if (params.get('rain') === '1') {
          rainActive = true;
          rainIntensity = 1.0;
          updateWeatherBanner();
        }
        if (params.get('snapwheel') === '1') {
          snapOffVehicleWheel(player, true);
        }
        if (params.get('copcheck') === '1') {
          triggerSuddenCopEncounterNow();
        }
        if (params.get('hop') === '1') {
          player.pos.y = 1.15;
          player.vel.y = 2.5;
          player.rot.z = -0.12;
          setTimeout(() => {
            lastCalloutTime = 0;
            if (trafficCops[0]) {
              spawnComicCallout(trafficCops[0].pos, '👮‍♂️ "ಏಯ್ ಆಟೋ! ಸೈಡ್ ಹಾಕಿ! DL ತೋರಿಸಿ!" [PRESS L]', '#ef4444');
            }
            setTimeout(() => {
              lastCalloutTime = 0;
              if (strayDogs[0]) {
                spawnComicCallout(strayDogs[0].pos, '🐕 "ಬೌ-ಬೌ! BOW-WOW!" +₹75 HOP BONUS!', '#4ade80');
              }
            }, 220);
          }, 2300);
        }
        updateSimulation(0.05, 0.2);
        gamePaused = false;
      } else {
        applyGravityProfile('medium', false);
        updateSimulation(0.05, 0.2);
        if (!modal.open) modal.showModal();
        gamePaused = true;
      }
      composer.render();
      animate();
    }

    bootGame();
  </script>
</body>
</html>
"""

def main():
    embedded = build_embedded_glb_dict()
    html_out = HTML_TEMPLATE.replace("__EMBEDDED_GLB_JSON__", json.dumps(embedded))
    out_file = os.path.join(WORKSPACE_DIR, "index.html")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html_out)
    print(f"Wrote {out_file} ({os.path.getsize(out_file)} bytes) with {len(embedded)} embedded GLB models")

if __name__ == "__main__":
    main()
