import base64
import glob
import gzip
import json
import os

WORKSPACE_DIR = "/Users/mani/Documents/Mani/games/blr-traffic-blender"
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
  <title>Ondu Second: Bangalore Gravity Glitch | 3D WebGL Arcade</title>
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
      background: #1a2436;
      color: #f8fafc;
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    #game-canvas {
      position: fixed;
      inset: 0;
      width: 100%;
      height: 100%;
      display: block;
      z-index: 1;
    }

    /* =========================================================================
       PROFESSIONAL 4-CORNER ARCADE HUD (Responsive, Zero Overflow)
       ========================================================================= */
    .hud-layer {
      position: fixed;
      inset: 0;
      z-index: 10;
      pointer-events: none;
      padding: 16px 20px;
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
      background: linear-gradient(165deg var(--in-oklab), #141821, #090c12);
      border: 2px solid var(--auto-yellow);
      border-radius: 14px;
      padding: 10px 16px;
      min-width: 195px;
      box-shadow: 0 12px 28px rgba(0, 0, 0, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.12);
      position: relative;
      overflow: hidden;
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
      font-size: 0.65rem;
      font-weight: 800;
      letter-spacing: 0.1em;
      color: #94a3b8;
      text-transform: uppercase;
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
      border: 1px solid rgba(255, 208, 0, 0.22);
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

    /* Top-Center: Authentic Indian Highway Sign Banner */
    .highway-sign-cluster {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 8px;
    }

    .nh-sign-board {
      background: linear-gradient(180deg var(--in-oklab), #007a40, #00542b);
      border: 2.5px solid #ffffff;
      border-radius: 10px;
      padding: 6px 18px;
      box-shadow: 0 10px 24px rgba(0, 0, 0, 0.4);
      display: flex;
      align-items: center;
      gap: 10px;
      color: #ffffff;
    }

    .nh-shield {
      background: var(--auto-yellow);
      color: #0b0e14;
      font-weight: 900;
      font-size: 0.66rem;
      padding: 2px 6px;
      border-radius: 4px;
      letter-spacing: 0.06em;
    }

    .nh-text {
      font-size: 0.8rem;
      font-weight: 800;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }

    .rain-banner {
      background: linear-gradient(90deg var(--in-oklab), rgba(2, 132, 199, 0.92), rgba(79, 70, 229, 0.92));
      border: 1px solid #7dd3fc;
      color: #ffffff;
      padding: 5px 14px;
      border-radius: 999px;
      font-size: 0.72rem;
      font-weight: 800;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      display: none;
      box-shadow: 0 6px 20px rgba(2, 132, 199, 0.45);
    }

    .rain-banner.visible {
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }

    /* Top-Right: Compact Glass Pill Toolbar */
    .top-toolbar {
      display: flex;
      align-items: center;
      gap: 6px;
      background: rgba(15, 23, 42, 0.82);
      border: 1px solid rgba(255, 255, 255, 0.16);
      border-radius: 12px;
      padding: 5px;
      backdrop-filter: blur(12px);
      box-shadow: 0 10px 26px rgba(0, 0, 0, 0.35);
      flex-wrap: wrap;
      justify-content: flex-end;
    }

    .mode-segmented {
      display: flex;
      background: rgba(0, 0, 0, 0.35);
      border-radius: 8px;
      padding: 2px;
      gap: 2px;
    }

    .pill-btn {
      appearance: none;
    }

    .tool-btn {
      appearance: none;
      border: 1px solid transparent;
      background: transparent;
      color: #cbd5e1;
      font-size: 0.74rem;
      font-weight: 700;
      padding: 6px 10px;
      border-radius: 7px;
      cursor: pointer;
      transition: background-color 0.04s ease, color 0.04s ease;
      white-space: nowrap;
    }

    .tool-btn:hover {
      color: #ffffff;
      background: rgba(255, 255, 255, 0.08);
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
      background: rgba(15, 23, 42, 0.78);
      border: 1px solid rgba(255, 255, 255, 0.14);
      border-radius: 12px;
      padding: 10px 14px;
      backdrop-filter: blur(10px);
      display: flex;
      flex-wrap: wrap;
      gap: 10px 16px;
      font-size: 0.72rem;
      color: #e2e8f0;
      max-width: 460px;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
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
      font-size: 0.68rem;
    }

    /* Bottom-Right: Sleek Speedometer & Auto Telemetry Cluster */
    .speed-cluster {
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid rgba(255, 255, 255, 0.18);
      border-radius: 16px;
      padding: 12px 18px;
      backdrop-filter: blur(12px);
      min-width: 240px;
      box-shadow: 0 12px 30px rgba(0, 0, 0, 0.45);
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
      font-size: 0.92rem;
      letter-spacing: 0.03em;
      padding: 5px 12px;
      border-radius: 8px;
      background: var(--auto-yellow);
      color: #090d16;
      border: 2px solid #090d16;
      box-shadow: 0 6px 16px rgba(0, 0, 0, 0.35);
      white-space: nowrap;
      animation: float-up-fade 1.15s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    @keyframes float-up-fade {
      0% { opacity: 0; transform: translate(-50%, -20%) scale(0.7); }
      20% { opacity: 1; transform: translate(-50%, -65%) scale(1.04); }
      100% { opacity: 0; transform: translate(-50%, -140%) scale(0.95); }
    }

    /* =========================================================================
       NATIVE <dialog> DIFFICULTY & GRAVITY PROFILES OVERLAY
       ========================================================================= */
    dialog#gravity-modal {
      margin: auto;
      width: min(880px, 92vw);
      max-height: 90vh;
      overflow-y: auto;
      background: linear-gradient(160deg var(--in-oklab), rgba(15, 23, 42, 0.96), rgba(9, 13, 24, 0.98));
      color: #f8fafc;
      border: 2px solid rgba(255, 208, 0, 0.65);
      border-radius: 22px;
      padding: 0;
      box-shadow: 0 28px 70px rgba(0, 0, 0, 0.75);
    }

    dialog#gravity-modal::backdrop {
      background: rgba(6, 10, 20, 0.65);
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
      padding: 24px 28px;
    }

    .modal-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      margin-bottom: 6px;
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
      font-size: 1.65rem;
      font-weight: 900;
      letter-spacing: -0.01em;
      color: #ffffff;
    }

    .modal-lead {
      color: #94a3b8;
      font-size: 0.88rem;
      line-height: 1.45;
      margin-top: 4px;
    }

    .mode-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(235px, 1fr));
      gap: 14px;
      margin: 18px 0;
    }

    .mode-card {
      background: rgba(30, 41, 59, 0.65);
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
      background: rgba(30, 41, 59, 0.92);
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
      font-size: 1.12rem;
      font-weight: 800;
      color: #ffffff;
      margin-bottom: 4px;
    }

    .mode-desc {
      font-size: 0.8rem;
      color: #cbd5e1;
      line-height: 1.4;
      margin-bottom: 10px;
    }

    .mode-stats {
      list-style: none;
      font-size: 0.74rem;
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
      background: rgba(15, 23, 42, 0.75);
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
      font-size: 0.65rem;
      color: #cbd5e1;
    }

    .asset-chip.loaded {
      border-color: rgba(34, 197, 94, 0.5);
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
  <!-- 4-Corner Professional Arcade HUD -->
  <div class="hud-layer">
    <header class="hud-top-row">
      <!-- Top-Left: Authentic Bengaluru Auto Digital Fare Meter -->
      <div class="auto-fare-unit interactive">
        <div class="meter-header">
          <span>KA-01 BAJAJ RE METER</span>
          <span class="meter-status-dot" id="surge-badge">1.0x HIRE</span>
        </div>
        <div class="meter-screen">
          <div class="fare-digits" id="hud-fare">₹30.00</div>
          <div class="fare-sub" id="hud-dist">0.0 KM</div>
        </div>
      </div>

      <!-- Top-Center: National Highway Landmark Distance Sign -->
      <div class="highway-sign-cluster">
        <div class="nh-sign-board">
          <span class="nh-shield">NH 44</span>
          <span class="nh-text" id="hud-landmark">SILK BOARD JUNCTION • 45m</span>
        </div>
        <div class="rain-banner" id="hud-weather-alert">
          ⛈️ MONSOON DOWNPOUR • TIRE FRICTION 0% (HYDROPLANING)
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
          <span class="alt-badge" id="hud-alt">ROAD 0.0m</span>
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
        <span class="modal-badge">KA-01 BENGALURU TRAFFIC ARCADE</span>
      </div>
      <h1 id="modal-title">ONDU SECOND: BANGALORE GRAVITY GLITCH</h1>
      <p class="modal-lead">
        Drive the iconic green-and-yellow Bengaluru Auto-Rickshaw on the left-hand lanes while dodging oncoming right-side traffic, sudden road-crossing jaywalkers raising the classic "Ondu Second!" stop hand, hyper-speed Zepto/Blinkit riders, and magnetic BBMP potholes!
      </p>

      <div class="mode-grid">
        <article class="mode-card" data-mode="low">
          <div>
            <span class="mode-tag tag-low">Low • Easy Mode</span>
            <h2>Cubbon Park Morning</h2>
            <p class="mode-desc">
              Light two-way morning traffic, occasional pedestrians crossing, gentle pothole gravity pull, and clear dry roads.
            </p>
            <ul class="mode-stats">
              <li><strong>Traffic:</strong> 12 Two-Way Vehicles</li>
              <li><strong>Jaywalkers:</strong> 5 Pedestrians</li>
              <li><strong>Pothole Pull:</strong> Mild Magnetic Pull</li>
            </ul>
          </div>
          <button type="button" class="launch-btn" data-select-mode="low">Play Low Mode</button>
        </article>

        <article class="mode-card selected" data-mode="medium">
          <div>
            <span class="mode-tag tag-med">Medium • Normal Mode</span>
            <h2>Indiranagar 6 PM Rush</h2>
            <p class="mode-desc">
              Bustling two-way Bengaluru rush with oncoming BMTC buses, sudden jaywalkers darting across lanes, and Zepto/Blinkit cut-offs.
            </p>
            <ul class="mode-stats">
              <li><strong>Traffic:</strong> 20 Two-Way Vehicles</li>
              <li><strong>Jaywalkers:</strong> 8 Sudden Crossers</li>
              <li><strong>Pothole Pull:</strong> Strong Sinkhole Pull</li>
            </ul>
          </div>
          <button type="button" class="launch-btn" data-select-mode="medium">Play Normal Mode</button>
        </article>

        <article class="mode-card" data-mode="complex">
          <div>
            <span class="mode-tag tag-complex">Complex • Peak Hour</span>
            <h2>Silk Board 8 PM Gridlock</h2>
            <p class="mode-desc">
              Complete Silk Board peak-hour chaos! Convoys of oncoming BMTC 500D buses, non-stop jaywalkers, monsoon downpours, and low-G glitch bounces.
            </p>
            <ul class="mode-stats">
              <li><strong>Traffic:</strong> 30 Dense Two-Way Vehicles</li>
              <li><strong>Jaywalkers:</strong> 12 Non-Stop Crossers</li>
              <li><strong>Pothole Pull:</strong> Maximum Gravity Glitch</li>
            </ul>
          </div>
          <button type="button" class="launch-btn" data-select-mode="complex">Play Peak Hour</button>
        </article>
      </div>

      <div class="asset-status-bar">
        <div><strong>Blender MCP 3D Assets:</strong> <span id="asset-load-summary">Loading 10/10 .glb models...</span></div>
        <div class="asset-badges">
          <span class="asset-chip" data-asset="auto_rickshaw.glb">auto_rickshaw.glb</span>
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

    // =========================================================================
    // 1. BLENDER MCP GLB ASSET LOADER (HTTP + Embedded Gzip Binary Fallback)
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
    // 2. WEB AUDIO API SYNTHESIZER (City Drone, Tuk-Tuk, Beep-Beep, Rain Noise)
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
        // Nonlinear brass/reed horn saturation curve (gives authentic Indian auto horn bite!)
        const samples = 1024;
        const curve = new Float32Array(samples);
        for (let i = 0; i < samples; i++) {
          const x = (i * 2) / samples - 1;
          curve[i] = Math.tanh(x * 3.4) + 0.12 * Math.sin(x * Math.PI * 3);
        }
        this.hornShaper = this.ctx.createWaveShaper();
        this.hornShaper.curve = curve;
        this.hornShaper.oversample = '2x';

        // Nasal horn bell formant filter + under-flyover street slapback echo
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
          // Authentic Bengaluru Bajaj RE Auto-Rickshaw Horn:
          // Dual-reed discordant brass/bulb horn ("PA-PA-PAAARP!") with air-pressure pitch envelope & 50Hz diaphragm rattle!
          const bursts = [
            { offset: 0.00, dur: 0.095, pitchMult: 1.00, peakGain: 0.28 },
            { offset: 0.115, dur: 0.095, pitchMult: 1.03, peakGain: 0.30 },
            { offset: 0.230, dur: 0.230, pitchMult: 0.99, peakGain: 0.34 }
          ];
          const baseF1 = 442 + (Math.random() - 0.5) * 14; // Primary brass reed
          const baseF2 = baseF1 * 1.254;                   // Dissonant major-third twin reed (~554 Hz)
          const baseF3 = baseF1 * 2.0;                     // Nasal bell harmonic (~884 Hz)
          const subBulb = baseF1 * 0.5;                    // Rubber bulb air-cavity thump (~221 Hz)

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

            // Air-pressure squeeze bend: swells up +7% on attack, then droops -4% on release
            o1.frequency.setValueAtTime(f1 * 0.94, start);
            o1.frequency.linearRampToValueAtTime(f1 * 1.06, start + 0.022);
            o1.frequency.exponentialRampToValueAtTime(f1 * 0.97, end);

            o2.frequency.setValueAtTime(f2 * 0.94, start);
            o2.frequency.linearRampToValueAtTime(f2 * 1.065, start + 0.022);
            o2.frequency.exponentialRampToValueAtTime(f2 * 0.97, end);

            o3.frequency.setValueAtTime(f3, start);
            oSub.frequency.setValueAtTime(subBulb, start);

            // 52Hz mechanical horn diaphragm rattle FM modulation
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

        // BMTC Bus deep dual-air horn or Scooter quick piezo beep
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
    // 3. DIFFICULTY PROFILES (Two-Way Traffic + Jaywalkers + Glitch Bounce)
    // =========================================================================
    const GRAVITY_PROFILES = {
      low: {
        id: 'low',
        trafficCount: 12,
        jaywalkerCount: 5,
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
    // 4. THREE.JS SCENE, GOLDEN-HOUR SKY, LIGHTING & CAMERA
    // =========================================================================
    const canvas = document.getElementById('game-canvas');
    const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, powerPreference: 'high-performance' });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.25;

    const scene = new THREE.Scene();
    // Warm Bengaluru Golden-Hour / Dusk Horizon Sky (NOT pitch black!)
    const drySkyColor = new THREE.Color(0x283e66);
    const rainSkyColor = new THREE.Color(0x162238);
    scene.background = drySkyColor.clone();
    scene.fog = new THREE.FogExp2(0x283e66, 0.0045);

    const camera = new THREE.PerspectiveCamera(58, window.innerWidth / window.innerHeight, 0.1, 420);
    camera.position.set(0, 4.2, 7.8);

    const hemiLight = new THREE.HemisphereLight(0x9ec5ff, 0x3d352e, 1.65);
    scene.add(hemiLight);

    const sunLight = new THREE.DirectionalLight(0xfff0d4, 2.6);
    sunLight.position.set(35, 55, 30);
    sunLight.castShadow = true;
    sunLight.shadow.mapSize.set(2048, 2048);
    sunLight.shadow.camera.near = 1;
    sunLight.shadow.camera.far = 180;
    const d = 48;
    sunLight.shadow.camera.left = -d;
    sunLight.shadow.camera.right = d;
    sunLight.shadow.camera.top = d;
    sunLight.shadow.camera.bottom = -d;
    scene.add(sunLight);

    // =========================================================================
    // 5. HIGHWAY, CONTINUOUS UNBROKEN NAMMA METRO VIADUCT, TREES & LANDMARKS
    // =========================================================================
    const ROAD_WIDTH = 22.8; // 6 lanes * 3.8m
    const LANES = [-9.5, -5.7, -1.9, 1.9, 5.7, 9.5];
    const CORRIDOR_LENGTH = 360;

    // Realistic Grey Asphalt Road Surface
    const roadMat = new THREE.MeshStandardMaterial({
      color: 0x2b303c,
      roughness: 0.72,
      metalness: 0.10
    });
    const roadMesh = new THREE.Mesh(new THREE.PlaneGeometry(ROAD_WIDTH, CORRIDOR_LENGTH * 1.6), roadMat);
    roadMesh.rotation.x = -Math.PI / 2;
    roadMesh.position.set(0, 0, -CORRIDOR_LENGTH * 0.35);
    roadMesh.receiveShadow = true;
    scene.add(roadMesh);

    // Raised Sidewalk / Urban Boulevard Ground
    const groundMat = new THREE.MeshStandardMaterial({ color: 0x384152, roughness: 0.88 });
    const groundMesh = new THREE.Mesh(new THREE.PlaneGeometry(240, CORRIDOR_LENGTH * 1.6), groundMat);
    groundMesh.rotation.x = -Math.PI / 2;
    groundMesh.position.set(0, -0.04, -CORRIDOR_LENGTH * 0.35);
    groundMesh.receiveShadow = true;
    scene.add(groundMesh);

    // Scrolling Corridor Segments (6m each) — Includes Unbroken Namma Metro Viaduct on Right!
    const scrollingStrips = [];
    const whiteDashMat = new THREE.MeshBasicMaterial({ color: 0xf1f5f9 });
    const yellowLineMat = new THREE.MeshBasicMaterial({ color: 0xffd000 });
    const kerbYellowMat = new THREE.MeshStandardMaterial({ color: 0xffd000, roughness: 0.45 });
    const kerbBlackMat = new THREE.MeshStandardMaterial({ color: 0x1e2430, roughness: 0.65 });
    const concreteMat = new THREE.MeshStandardMaterial({ color: 0x94a3b8, roughness: 0.75 });
    const metroPurpleMat = new THREE.MeshStandardMaterial({
      color: 0x7c3aed,
      roughness: 0.35,
      emissive: 0x4c1d95,
      emissiveIntensity: 0.25
    });
    const railMetalMat = new THREE.MeshStandardMaterial({ color: 0x64748b, metalness: 0.8, roughness: 0.3 });
    const treeTrunkMat = new THREE.MeshStandardMaterial({ color: 0x5c4033, roughness: 0.9 });
    const treeLeafMat = new THREE.MeshStandardMaterial({ color: 0x2d6a4f, roughness: 0.75 });
    const gulmoharLeafMat = new THREE.MeshStandardMaterial({ color: 0x40916c, roughness: 0.7 });

    const dashGeo = new THREE.BoxGeometry(0.16, 0.02, 2.8);
    const kerbGeo = new THREE.BoxGeometry(0.55, 0.26, 6.02);
    // Unbroken 6.05m Viaduct Deck Segment at X = +18.5 so the Metro Line is 100% continuous!
    const viaductDeckGeo = new THREE.BoxGeometry(6.8, 1.1, 6.06);
    const viaductWallGeo = new THREE.BoxGeometry(0.26, 1.15, 6.06);
    const viaductPierGeo = new THREE.CylinderGeometry(0.95, 1.05, 7.6, 12);
    const viaductCapGeo = new THREE.BoxGeometry(5.8, 1.1, 2.0);

    const METRO_X = 18.5;

    for (let z = 36; z > -CORRIDOR_LENGTH + 36; z -= 6) {
      const segIdx = Math.round(Math.abs(z) / 6);
      const row = new THREE.Group();
      row.position.z = z;

      // Lane Divider Dashes between the 6 lanes
      for (const lx of [-7.6, -3.8, 0.0, 3.8, 7.6]) {
        if (lx === 0.0) {
          // Double yellow center median line
          const cl = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.02, 6.02), yellowLineMat);
          cl.position.set(0, 0.01, 0);
          row.add(cl);
        } else if (segIdx % 2 === 0) {
          const dash = new THREE.Mesh(dashGeo, whiteDashMat);
          dash.position.set(lx, 0.01, 0);
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

      // Painted White Zebra Crossings at key pedestrian crossing intervals (including z = -18m)
      if (segIdx % 14 === 3) {
        const zebraGeo = new THREE.BoxGeometry(0.95, 0.022, 3.8);
        for (let zx = -9.6; zx <= 9.6; zx += 1.6) {
          if (Math.abs(zx) < 0.5) continue;
          const stripe = new THREE.Mesh(zebraGeo, whiteDashMat);
          stripe.position.set(zx, 0.012, 0);
          row.add(stripe);
        }
      }

      // CONTINUOUS UNBROKEN NAMMA METRO ELEVATED VIADUCT along X = +18.5!
      const vDeck = new THREE.Mesh(viaductDeckGeo, concreteMat);
      vDeck.position.set(METRO_X, 8.2, 0);
      vDeck.receiveShadow = true;
      const vWallL = new THREE.Mesh(viaductWallGeo, metroPurpleMat);
      vWallL.position.set(METRO_X - 3.3, 9.1, 0);
      const vWallR = new THREE.Mesh(viaductWallGeo, metroPurpleMat);
      vWallR.position.set(METRO_X + 3.3, 9.1, 0);
      row.add(vDeck, vWallL, vWallR);

      // Concrete Viaduct Pier every 18m (3 segments)
      if (segIdx % 3 === 0) {
        const pier = new THREE.Mesh(viaductPierGeo, concreteMat);
        pier.position.set(METRO_X, 3.8, 0);
        const cap = new THREE.Mesh(viaductCapGeo, concreteMat);
        cap.position.set(METRO_X, 7.3, 0);
        row.add(pier, cap);
      }

      // Lush Bengaluru Rain Trees along Left Boulevard & Streetlamps every 24m
      if (segIdx % 4 === 0) {
        const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.28, 0.38, 3.6, 8), treeTrunkMat);
        trunk.position.set(-ROAD_WIDTH / 2 - 3.8, 1.8, 0);
        const crown1 = new THREE.Mesh(new THREE.SphereGeometry(2.6, 10, 8), segIdx % 8 === 0 ? treeLeafMat : gulmoharLeafMat);
        crown1.scale.set(1.2, 0.65, 1.2);
        crown1.position.set(-ROAD_WIDTH / 2 - 3.8, 4.3, 0);
        row.add(trunk, crown1);
      }

      scene.add(row);
      scrollingStrips.push(row);
    }

    // Dynamic Scrolling Bangalore Landmarks (Silk Board Gantry, Vidhana Soudha, Metro Station + Continuous Train)
    const landmarkInstances = [];
    let continuousMetroTrain = null;

    function spawnLandmarksFromGLB() {
      // 1. Massive "Silk Board" Highway Green Sign spanning directly over the 6-lane road
      for (const zPos of [-65, -245]) {
        const silk = loadedTemplates['silk_board_sign.glb'].clone(true);
        silk.position.set(0, 0, zPos);
        scene.add(silk);
        landmarkInstances.push({
          mesh: silk,
          type: 'SILK BOARD FLYOVER GANTRY'
        });
      }

      // 2. Vidhana Soudha Grand Facade along the Left Boulevard Vista
      for (const zPos of [-135, -315]) {
        const vidhana = loadedTemplates['vidhana_soudha.glb'].clone(true);
        vidhana.position.set(-32, 0, zPos);
        vidhana.rotation.y = Math.PI * 0.42;
        scene.add(vidhana);
        landmarkInstances.push({
          mesh: vidhana,
          type: 'VIDHANA SOUDHA GRAND FACADE'
        });
      }

      // 3. Namma Metro Station seamlessly aligned onto the continuous viaduct at X = METRO_X
      const metro = loadedTemplates['metro_station.glb'].clone(true);
      metro.position.set(METRO_X, 0, -185);
      // Extract the Purple Line Train so it can ride continuously along the entire 360m viaduct!
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
        type: 'NAMMA METRO PURPLE LINE STATION'
      });
    }

    // =========================================================================
    // 6. REALISTIC ASPHALT POTHOLES (Broken Crater + Puddle + Traffic Cone)
    // =========================================================================
    const potholes = [];
    const potholeGroup = new THREE.Group();
    scene.add(potholeGroup);

    const potholeRimMat = new THREE.MeshStandardMaterial({ color: 0x1b1e26, roughness: 0.92 });
    const potholeWaterMat = new THREE.MeshStandardMaterial({
      color: 0x1e293b,
      roughness: 0.08,
      metalness: 0.65
    });
    const potholeGlowMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.55 });
    const coneOrangeMat = new THREE.MeshStandardMaterial({ color: 0xf97316, roughness: 0.4 });
    const coneWhiteMat = new THREE.MeshStandardMaterial({ color: 0xf8fafc, roughness: 0.3 });

    function rebuildPotholes(count) {
      while (potholeGroup.children.length > 0) {
        potholeGroup.remove(potholeGroup.children[0]);
      }
      potholes.length = 0;

      for (let i = 0; i < count; i++) {
        const g = new THREE.Group();
        // Jagged 7-sided dark asphalt crater rim
        const rim = new THREE.Mesh(new THREE.CylinderGeometry(1.55, 1.75, 0.06, 7), potholeRimMat);
        rim.position.y = 0.02;
        // Glossy rainwater puddle inside crater
        const puddle = new THREE.Mesh(new THREE.CylinderGeometry(1.25, 1.25, 0.07, 10), potholeWaterMat);
        puddle.position.y = 0.025;
        // Subtle gravity-glitch shimmer ring inside crater
        const anomalyRing = new THREE.Mesh(new THREE.RingGeometry(0.95, 1.12, 16), potholeGlowMat);
        anomalyRing.rotation.x = -Math.PI / 2;
        anomalyRing.position.y = 0.065;

        // BBMP Orange-and-White Traffic Cone at edge of pothole
        const cone = new THREE.Mesh(new THREE.ConeGeometry(0.22, 0.65, 10), coneOrangeMat);
        cone.position.set(1.45, 0.32, 0.4);
        const coneBand = new THREE.Mesh(new THREE.CylinderGeometry(0.11, 0.16, 0.18, 10), coneWhiteMat);
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
    // 7. PLAYER AUTO-RICKSHAW & GROUNDED LANE TRAFFIC WITH DETACHABLE WHEELS
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
      hornCooldown: 0
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

    // Grounded Lane-Based NPC Traffic Pool
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
        callouts: ['🚌 BMTC 500D SILK BOARD!', '📢 SIDE KODI! HEAVY BUS!']
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
        callouts: ['🛺 ONDU SECOND ANNA!', '💸 METER ONE-AND-HALF!']
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
          laneIdx = 3 + Math.floor(Math.random() * 3); // Right-side oncoming lanes (3, 4, 5)
        } else if (forceOncoming === false) {
          laneIdx = Math.floor(Math.random() * 3);     // Left-side forward lanes (0, 1, 2)
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

    // Left-Hand Lanes (0, 1, 2) drive FORWARD (-Z); Right-Hand Lanes (3, 4, 5) drive ONCOMING (+Z)!
    const HERO_SLOTS = [
      { type: 'techie', laneIdx: 0, z: -10.5 },
      { type: 'bmtc', laneIdx: 1, z: -14.5 },
      { type: 'swiggy', laneIdx: 2, z: -18.5 },
      { type: 'npc_auto', laneIdx: 3, z: -13.0 },
      { type: 'bmtc', laneIdx: 4, z: -22.0 },
      { type: 'zepto', laneIdx: 5, z: -11.0 },
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
      const isOncoming = laneIdx >= 3; // Right side of yellow median = Oncoming traffic!
      const laneX = LANES[laneIdx];
      const rowIdx = Math.floor(slotIndex / LANES.length);
      const zOffset = hero ? hero.z : -26 - rowIdx * 22 - (slotIndex % 3) * 6;

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
    // 7B. SUDDEN BENGALURU JAYWALKER PEDESTRIANS (Crossing Road + Stop Hand!)
    // =========================================================================
    const jaywalkers = [];
    const JAYWALKER_SHIRT_COLORS = [0xf97316, 0x06b6d4, 0xec4899, 0xeab308, 0x22c55e, 0xa855f7];
    const JAYWALKER_CALLOUTS = [
      '✋ "ONDU SECOND ANNA!" CROSSING!',
      '🚶‍♂️ SUDDEN JAYWALKER ON ROAD!',
      '✋ "WAIT MAADI!" STOP HAND!',
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

      // First two jaywalkers are already mid-crossing right in front of the player!
      let startX, startZ, dirX, state;
      if (index === 0) {
        startX = -3.8;
        startZ = -17.5;
        dirX = 1;
        state = 'crossing';
      } else if (index === 1) {
        startX = 3.6;
        startZ = -32.0;
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
    // 8. COMIC CALLOUTS & INPUT CONTROLS
    // =========================================================================
    const calloutLayer = document.getElementById('callout-layer');
    let lastCalloutTime = 0;

    function spawnComicCallout(worldPos, text, bgColor = '#ffd000') {
      const now = performance.now();
      if (now - lastCalloutTime < 220) return;
      lastCalloutTime = now;

      const proj = worldPos.clone().add(new THREE.Vector3(0, 2.0, 0)).project(camera);
      if (proj.z > 1) return;
      const x = (proj.x * 0.5 + 0.5) * window.innerWidth;
      const y = (-proj.y * 0.5 + 0.5) * window.innerHeight;

      const el = document.createElement('div');
      el.className = 'comic-pop';
      el.textContent = text;
      el.style.left = `${Math.min(window.innerWidth - 130, Math.max(130, x))}px`;
      el.style.top = `${Math.min(window.innerHeight - 90, Math.max(90, y))}px`;
      el.style.backgroundColor = bgColor;
      calloutLayer.appendChild(el);
      setTimeout(() => el.remove(), 1150);
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
      spawnComicCallout(player.pos, '📯 PA-PA-PAAARP! SIDE KODI!', '#ffd000');

      // Same-direction vehicles ahead yield slightly when honked at
      trafficPool.forEach((v) => {
        const dz = Math.abs(v.pos.z - player.pos.z);
        const dx = v.pos.x - player.pos.x;
        if (!v.isOncoming && dz < 16 && Math.abs(dx) < 4.5 && v.type !== 'bmtc') {
          const shiftDir = dx >= 0 ? 1 : -1;
          v.targetLaneX = THREE.MathUtils.clamp(v.targetLaneX + shiftDir * 3.8, LANES[0], LANES[2]);
        }
      });

      // Jaywalkers scurry faster across the road and wave their Stop Hand when honked at!
      jaywalkers.forEach((p) => {
        const dz = p.pos.z - player.pos.z;
        if (dz < 2 && dz > -34 && p.state === 'crossing') {
          p.speedBoost = 1.85;
          spawnComicCallout(p.pos, '🏃‍♂️ "AYYO! WAIT MAADI ANNA!"', '#fb923c');
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
      reattachAllPlayerWheels();

      rainActive = false;
      rainIntensity = 0.0;
      weatherTimer = currentProfile.rainCycleDuration;
      updateWeatherBanner();

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
    // 9. SIMULATION, TWO-WAY TRAFFIC & SUDDEN JAYWALKER PHYSICS LOOP
    // =========================================================================
    let cameraShake = 0;
    const clock = new THREE.Clock();

    function updateSimulation(dt, elapsed) {
      if (player.hornCooldown > 0) player.hornCooldown -= dt;

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
      roadMat.roughness = 0.72 - rainIntensity * 0.56;
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

      // Gravity pulls vehicle cleanly back to the road (y = 0)
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

      // 3. Seamless Scrolling Corridor, Continuous Viaduct & Continuous Metro Train
      const scrollStep = player.forwardSpeed * dt;
      scrollingStrips.forEach((row) => {
        row.position.z += scrollStep;
        if (row.position.z > 36) {
          row.position.z -= CORRIDOR_LENGTH;
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
      landmarkInstances.forEach((lm) => {
        lm.mesh.position.z += scrollStep;
        if (lm.mesh.position.z > 60) {
          lm.mesh.position.z -= CORRIDOR_LENGTH;
        }
        const distAhead = -lm.mesh.position.z;
        if (distAhead > -10 && distAhead < nearestDist) {
          nearestDist = distAhead;
          nearestName = lm.type;
        }
      });
      document.getElementById('hud-landmark').textContent =
        `${nearestName} • ${Math.max(0, Math.round(nearestDist))}m`;

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
              spawnComicCallout(player.pos, '🕳️ POTHOLE GRAVITY GLITCH!', '#38bdf8');
            }
          }
        }
      });

      // 5. Sudden Road-Crossing Bengaluru Jaywalkers (Wait/Stop Hand Gesture + Walk Cycle)
      for (let i = 0; i < jaywalkers.length; i++) {
        const p = jaywalkers[i];
        if (p.hitCooldown > 0) p.hitCooldown -= dt;
        p.pos.z += scrollStep;

        const distAhead = -p.pos.z;
        // Suddenly dart onto the road when the player approaches!
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

          // Articulated walking legs + swinging cloth bag + waving "Ondu Second" Stop Hand!
          const swing = Math.sin(p.walkPhase) * 0.62;
          if (p.legL) p.legL.rotation.x = swing;
          if (p.legR) p.legR.rotation.x = -swing;
          if (p.armL) p.armL.rotation.x = -swing * 0.7;
          if (p.armR) p.armR.rotation.z = Math.sin(p.walkPhase * 1.4) * 0.22;

          // Reached opposite sidewalk
          if ((p.dirX > 0 && p.pos.x > ROAD_WIDTH / 2 + 1.0) || (p.dirX < 0 && p.pos.x < -ROAD_WIDTH / 2 - 1.0)) {
            p.state = 'crossed';
            if (p.legL) p.legL.rotation.x = 0;
            if (p.legR) p.legR.rotation.x = 0;
          }
        }

        // Gravity recovery if bounced
        if (p.pos.y > 0 || p.vy !== 0) {
          p.vy -= currentProfile.gravityReturn * dt;
          p.pos.y += p.vy * dt;
          if (p.pos.y <= 0) {
            p.pos.y = 0;
            p.vy = 0;
          }
        }

        // Check collision between Player Auto and Jaywalker
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
          spawnComicCallout(p.pos, '🤸 "AYYO! NODKONDU HOGI ANNA!"', '#ff3b5c');
        }

        if (p.pos.z > 20) {
          resetJaywalkerToKerb(p);
        }
      }

      // 6. Two-Way Grounded Lane Traffic AI (Left Side Forward -Z, Right Side Oncoming +Z)
      for (let i = 0; i < trafficPool.length; i++) {
        const v = trafficPool[i];
        if (v.hitCooldown > 0) v.hitCooldown -= dt;

        const minLane = v.isOncoming ? 3 : 0;
        const maxLane = v.isOncoming ? 5 : 2;

        // Smart forward lane check within same-direction lanes
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

        // Hyper-delivery Zepto/Blinkit riders weave across their side's lanes
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

        // Smooth lane centering
        const laneErr = v.targetLaneX - v.pos.x;
        v.vel.x += laneErr * 7.5 * dt;
        v.vel.x *= Math.exp(-4.2 * dt);

        // Gravity returns NPC vehicles cleanly to the road (y = 0)
        v.vel.y -= currentProfile.gravityReturn * dt;
        if (v.pos.y <= 0) {
          v.pos.y = 0;
          v.vel.y = 0;
        }

        // Smoothly recover Z speed back to cruise speed (negative for forward, positive for oncoming)
        const targetVelZ = v.isOncoming ? v.baseSpeed * 0.42 : -v.baseSpeed;
        v.vel.z += (targetVelZ - v.vel.z) * dt * 2.5;

        // Subtle, realistic tilt into lane changes + 180-deg rotation for oncoming right-side traffic!
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
            ? `🚨 WRONG-SIDE HEAD-ON! ${v.spec.callouts[0]}`
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

      // 8. Smooth Chase Camera & HUD Updates
      if (cameraShake > 0) cameraShake = Math.max(0, cameraShake - dt * 1.8);
      const shakeX = (Math.random() - 0.5) * cameraShake;
      const shakeY = (Math.random() - 0.5) * cameraShake;

      camera.position.x += (player.pos.x * 0.58 - camera.position.x) * dt * 7.5 + shakeX;
      camera.position.y += (3.85 + player.pos.y * 0.45 - camera.position.y) * dt * 6.5 + shakeY;
      camera.position.z = 7.2;
      camera.lookAt(player.pos.x * 0.75, 1.25 + player.pos.y * 0.3, -14);

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

      renderer.render(scene, camera);
    }

    window.addEventListener('resize', () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
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
        updateSimulation(0.05, 0.2);
        gamePaused = false;
      } else {
        applyGravityProfile('medium', false);
        updateSimulation(0.05, 0.2);
        if (!modal.open) modal.showModal();
        gamePaused = true;
      }
      renderer.render(scene, camera);
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
    print(f"Wrote {out_file} ({os.path.getsize(out_file)} bytes)")

if __name__ == "__main__":
    main()
