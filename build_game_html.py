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
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>ಒಂದು ಸೆಕೆಂಡ್ | Ondu Second: Namma Auto Traffic — Vayuputra RE 3D WebGL Arcade</title>
  <meta name="description" content="Drive the Vayuputra RE Compact (ವಾಯುಪುತ್ರ) Auto-Rickshaw through 6-lane Bengaluru traffic with BTP Red-Light Signal stops, sudden cop checks, darting Indie stray dogs, and configurable Dash Cam POV!">
  <meta property="og:title" content="ಒಂದು ಸೆಕೆಂಡ್ | Ondu Second: Namma Auto Traffic (Pro 3D WebGL Edition)">
  <meta property="og:description" content="Navigate Silk Board & Indiranagar in a Vayuputra RE Auto-Rickshaw! Obey BTP Red-Light Signals, flash your DigiLocker DL to cops, dodge Indie stray dogs, and share your Namma Auto Fare Receipt!">
  <meta property="og:type" content="website">
  <meta property="og:image" content="screenshots/pro_hero_banner.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="ಒಂದು ಸೆಕೆಂಡ್ | Ondu Second: Namma Auto Traffic (3D WebGL)">
  <meta name="twitter:description" content="Can you survive Silk Board rush hour in a Vayuputra RE Auto? Play free in your browser with Chase & Dash Cam POV!">
  <meta name="twitter:image" content="screenshots/pro_hero_banner.jpg">
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

    .tool-btn.action-pill {
      background: rgba(255, 255, 255, 0.07);
      border-color: rgba(255, 255, 255, 0.14);
    }

    .tool-btn.action-pill:hover {
      border-color: var(--auto-yellow);
    }

    .tool-btn.active-mode,
    .tool-btn.action-pill.active-mode {
      background: var(--auto-yellow);
      color: #0b0e14;
      border-color: var(--auto-yellow);
      font-weight: 900;
      box-shadow: 0 2px 10px rgba(255, 208, 0, 0.35);
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
      width: min(1160px, 95vw);
      max-height: 94vh;
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
      padding: 18px 24px;
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
      font-size: 1.55rem;
      font-weight: 900;
      letter-spacing: -0.01em;
      color: #ffffff;
    }

    .modal-lead {
      color: #94a3b8;
      font-size: 0.84rem;
      line-height: 1.42;
      margin-top: 4px;
    }

    .mode-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
      gap: 12px;
      margin: 12px 0;
    }

    .mode-card {
      background: rgba(30, 41, 59, 0.68);
      border: 1.5px solid rgba(255, 255, 255, 0.12);
      border-radius: 16px;
      padding: 14px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 12px;
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
      font-size: 0.64rem;
      font-weight: 800;
      letter-spacing: 0.07em;
      text-transform: uppercase;
      padding: 3px 8px;
      border-radius: 6px;
      margin-bottom: 6px;
    }

    .tag-oldblr { background: rgba(249, 115, 22, 0.22); color: #fdba74; border: 1px solid rgba(251, 146, 60, 0.42); }
    .tag-low { background: rgba(34, 197, 94, 0.18); color: #4ade80; }
    .tag-med { background: rgba(255, 208, 0, 0.18); color: #ffd000; }
    .tag-complex { background: rgba(255, 59, 92, 0.2); color: #fb7185; }

    .mode-card h2 {
      font-size: 1.02rem;
      font-weight: 800;
      color: #ffffff;
      margin-bottom: 4px;
    }

    .mode-desc {
      font-size: 0.75rem;
      color: #cbd5e1;
      line-height: 1.38;
      margin-bottom: 8px;
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

    /* Trip Progress Strip inside Auto Fare Unit */
    .trip-progress-strip {
      margin-top: 6px;
      padding-top: 6px;
      border-top: 1px solid rgba(255, 255, 255, 0.1);
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .trip-progress-label {
      display: flex;
      justify-content: space-between;
      font-size: 0.63rem;
      font-weight: 800;
      color: #fde047;
      letter-spacing: 0.04em;
    }

    .trip-bar-track {
      width: 100%;
      height: 6px;
      background: rgba(255, 255, 255, 0.14);
      border-radius: 99px;
      overflow: hidden;
    }

    .trip-bar-fill {
      height: 100%;
      width: 0%;
      background: linear-gradient(90deg, #ffd000, #22c55e);
      transition: width 0.15s linear;
    }

    /* Camera Selector Bar inside Start Modal */
    .camera-config-bar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 10px;
      margin: 12px 0 4px 0;
      padding: 10px 14px;
      border-radius: 12px;
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid rgba(255, 208, 0, 0.35);
    }

    .camera-config-title {
      font-size: 0.78rem;
      font-weight: 800;
      color: #fde047;
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }

    .camera-config-btns {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }

    .cam-opt-btn {
      background: rgba(30, 41, 59, 0.9);
      color: #cbd5e1;
      border: 1.5px solid rgba(255, 255, 255, 0.16);
      border-radius: 9px;
      padding: 6px 12px;
      font-size: 0.75rem;
      font-weight: 800;
      cursor: pointer;
      transition: all 0.15s ease;
    }

    .cam-opt-btn.active-cam {
      background: var(--auto-yellow);
      color: #090d16;
      border-color: #ffffff;
      box-shadow: 0 0 12px rgba(255, 208, 0, 0.45);
    }

    /* =========================================================================
       AUTO-RICKSHAW DASH CAM / COCKPIT POV OVERLAY
       ========================================================================= */
    #dashcam-overlay {
      position: fixed;
      inset: 0;
      pointer-events: none;
      z-index: 6;
      display: none;
      overflow: hidden;
      --steer-deg: 0deg;
      --wiper-deg: -42deg;
    }

    #dashcam-overlay.active {
      display: block;
    }

    /* Top Rexine Canopy & Yellow Windshield Arch */
    .dashcam-top-canopy {
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 54px;
      background: linear-gradient(180deg, #111318 0%, #1e222d 72%, #ffd000 72%, #d9a700 100%);
      border-bottom: 4px solid #090d16;
      box-shadow: 0 10px 28px rgba(0, 0, 0, 0.65);
    }

    /* Left & Right Yellow-Green Auto Windshield A-Pillars */
    .dashcam-pillar-left,
    .dashcam-pillar-right {
      position: absolute;
      top: 48px;
      bottom: 0;
      width: 38px;
      background: linear-gradient(180deg, #ffd000 0%, #e5b800 55%, #009a44 55%, #007633 100%);
      border-right: 4px solid #090d16;
      box-shadow: 8px 0 24px rgba(0, 0, 0, 0.55);
    }

    .dashcam-pillar-right {
      right: 0;
      border-right: none;
      border-left: 4px solid #090d16;
      box-shadow: -8px 0 24px rgba(0, 0, 0, 0.55);
    }

    /* Hanging Mysuru Mallige (Jasmine Garland) & Nimbu-Mirchi Charm */
    .dashcam-garland {
      position: absolute;
      top: 46px;
      left: 50%;
      transform-origin: top center;
      transform: translateX(-50%) rotate(calc(var(--steer-deg) * -0.8));
      display: flex;
      flex-direction: column;
      align-items: center;
      transition: transform 0.08s linear;
    }

    .garland-strands {
      font-size: 1.25rem;
      line-height: 0.95;
      letter-spacing: 2px;
      filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.65));
      text-align: center;
    }

    .garland-tag {
      margin-top: 2px;
      background: rgba(9, 13, 22, 0.85);
      border: 1px solid rgba(255, 208, 0, 0.65);
      color: #fde047;
      font-size: 0.62rem;
      font-weight: 900;
      padding: 2px 8px;
      border-radius: 99px;
      letter-spacing: 0.05em;
    }

    /* Dash Cam REC Timestamp OSD Badge */
    .dashcam-rec-osd {
      position: absolute;
      bottom: 176px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(9, 13, 22, 0.85);
      border: 1.5px solid rgba(239, 68, 68, 0.75);
      border-radius: 99px;
      padding: 5px 14px;
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
      font-size: 0.70rem;
      font-weight: 800;
      color: #f8fafc;
      display: flex;
      align-items: center;
      gap: 8px;
      letter-spacing: 0.05em;
      box-shadow: 0 8px 20px rgba(0, 0, 0, 0.55);
    }

    .rec-dot {
      width: 9px;
      height: 9px;
      border-radius: 50%;
      background: #ef4444;
      box-shadow: 0 0 8px #ef4444;
      animation: blink-rec 1s infinite;
    }

    @keyframes blink-rec {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.2; }
    }

    /* Center Windshield Wiper Blade */
    .dashcam-wiper {
      position: absolute;
      top: 52px;
      left: 50%;
      width: 5px;
      height: 290px;
      background: linear-gradient(180deg, #0f172a, #334155);
      transform-origin: top center;
      transform: translateX(-50%) rotate(var(--wiper-deg));
      border-radius: 4px;
      opacity: 0.55;
    }

    /* Bottom Auto Dashboard Cowling & Steering Handlebar */
    .dashcam-bottom-dash {
      position: absolute;
      bottom: 84px;
      left: 50%;
      transform: translateX(-50%);
      width: min(680px, 72vw);
      height: 80px;
      background: linear-gradient(180deg, #009a44 0%, #00682d 38%, #111827 38%, #090d16 100%);
      border-top: 4px solid #ffd000;
      border-left: 4px solid #090d16;
      border-right: 4px solid #090d16;
      border-radius: 36px 36px 0 0;
      box-shadow: 0 -10px 30px rgba(0, 0, 0, 0.75);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: flex-start;
      padding-top: 8px;
    }

    .dashcam-handlebar {
      width: 340px;
      height: 18px;
      background: linear-gradient(90deg, #1e293b 0 18%, #cbd5e1 18% 82%, #1e293b 82% 100%);
      border: 2px solid #090d16;
      border-radius: 99px;
      transform: rotate(var(--steer-deg));
      transition: transform 0.06s linear;
      box-shadow: 0 6px 14px rgba(0, 0, 0, 0.6);
      position: relative;
    }

    .dashcam-dash-label {
      margin-top: 8px;
      font-size: 0.68rem;
      font-weight: 900;
      color: #fde047;
      letter-spacing: 0.08em;
    }

    /* =========================================================================
       END-OF-TRIP SCOREBOARD MODAL (<dialog id="score-modal">)
       ========================================================================= */
    dialog#score-modal {
      margin: auto;
      width: min(740px, 93vw);
      max-height: 94vh;
      overflow-y: auto;
      background: linear-gradient(160deg var(--in-oklab), rgba(15, 23, 42, 0.98), rgba(9, 13, 24, 0.99));
      color: #f8fafc;
      border: 2.5px solid #ffd000;
      border-radius: 22px;
      padding: 0;
      box-shadow: 0 28px 75px rgba(0, 0, 0, 0.85);
    }

    dialog#score-modal .modal-inner {
      padding: 16px 24px;
    }

    dialog#score-modal::backdrop {
      background: rgba(6, 10, 20, 0.78);
      backdrop-filter: blur(8px);
    }

    .score-hero-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
      margin: 10px 0;
      padding: 12px 18px;
      border-radius: 14px;
      background: rgba(30, 41, 59, 0.75);
      border: 1px solid rgba(255, 208, 0, 0.35);
    }

    .score-big-num {
      font-size: 2.15rem;
      font-weight: 900;
      color: #ffd000;
      font-variant-numeric: tabular-nums;
      line-height: 1.05;
    }

    .score-rank-pill {
      display: inline-block;
      margin-top: 4px;
      background: rgba(34, 197, 94, 0.2);
      border: 1px solid #4ade80;
      color: #86efac;
      font-size: 0.74rem;
      font-weight: 900;
      padding: 3px 11px;
      border-radius: 99px;
      letter-spacing: 0.05em;
    }

    .score-breakdown-table {
      width: 100%;
      border-collapse: collapse;
      margin: 8px 0 12px 0;
      font-size: 0.80rem;
    }

    .score-breakdown-table th,
    .score-breakdown-table td {
      padding: 7px 10px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      text-align: left;
    }

    .score-breakdown-table th {
      color: #94a3b8;
      font-size: 0.70rem;
      text-transform: uppercase;
      letter-spacing: 0.06em;
    }

    .score-breakdown-table td:last-child,
    .score-breakdown-table th:last-child {
      text-align: right;
      font-variant-numeric: tabular-nums;
      font-weight: 800;
    }

    .score-actions {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
    }

    .score-actions .launch-btn {
      flex: 1;
      min-width: 155px;
    }

    .score-actions .secondary-btn {
      background: rgba(30, 41, 59, 0.95);
      color: #f8fafc;
      border: 1.5px solid rgba(255, 208, 0, 0.55);
    }

    .score-actions .share-receipt-btn {
      background: linear-gradient(135deg, #22c55e, #16a34a);
      color: #052e16;
      border: 1.5px solid #86efac;
      box-shadow: 0 4px 16px rgba(34, 197, 94, 0.35);
    }

    /* BTP Traffic Signal Junction HUD Banner */
    .signal-alert-banner {
      display: none;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      padding: 8px 14px;
      border-radius: 12px;
      background: linear-gradient(90deg, rgba(15, 23, 42, 0.96), rgba(30, 41, 59, 0.96));
      border: 2px solid #ef4444;
      color: #ffffff;
      box-shadow: 0 10px 28px rgba(0, 0, 0, 0.65);
    }

    .signal-alert-banner.visible {
      display: flex;
    }

    .signal-lights-mini {
      display: flex;
      gap: 6px;
      background: #090d16;
      padding: 5px 8px;
      border-radius: 999px;
      border: 1px solid rgba(255, 255, 255, 0.18);
    }

    .sig-dot {
      width: 14px;
      height: 14px;
      border-radius: 50%;
      opacity: 0.22;
      transition: opacity 0.15s, box-shadow 0.15s;
    }

    .sig-dot.red { background: #ff2a2a; }
    .sig-dot.yellow { background: #ffd000; }
    .sig-dot.green { background: #10f560; }

    .sig-dot.active {
      opacity: 1;
      box-shadow: 0 0 12px currentColor;
    }

    .signal-timer-box {
      font-family: ui-monospace, 'SFMono-Regular', Menlo, monospace;
      font-size: 1.05rem;
      font-weight: 900;
      padding: 3px 9px;
      border-radius: 8px;
      background: #090d16;
      color: #ff4d4d;
      border: 1.5px solid rgba(255, 255, 255, 0.2);
      min-width: 56px;
      text-align: center;
    }

    .signal-action-btn {
      background: #ffd000;
      color: #090d16;
      border: none;
      border-radius: 8px;
      padding: 6px 11px;
      font-size: 0.72rem;
      font-weight: 900;
      text-transform: uppercase;
      cursor: pointer;
      white-space: nowrap;
    }

    /* Responsive On-Screen Touch / Arcade Control Bar */
    .touch-controls-bar {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      background: var(--hud-bg);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      border: 1.5px solid rgba(255, 208, 0, 0.42);
      border-radius: 16px;
      padding: 8px 12px;
      box-shadow: 0 12px 32px rgba(0, 0, 0, 0.55);
      pointer-events: auto;
      user-select: none;
      -webkit-user-select: none;
    }

    .touch-btn {
      appearance: none;
      border: 1.5px solid rgba(255, 255, 255, 0.18);
      background: rgba(30, 41, 59, 0.92);
      color: #f8fafc;
      border-radius: 10px;
      padding: 8px 12px;
      font-size: 0.74rem;
      font-weight: 900;
      letter-spacing: 0.03em;
      cursor: pointer;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 2px;
      min-width: 58px;
      transition: transform 0.08s, background 0.12s, border-color 0.12s;
      touch-action: manipulation;
    }

    .touch-btn span.sub-key {
      font-size: 0.58rem;
      color: #94a3b8;
      font-family: ui-monospace, monospace;
    }

    .touch-btn:active,
    .touch-btn.pressed {
      transform: scale(0.95);
      background: var(--auto-yellow);
      color: #090d16;
      border-color: #ffffff;
    }

    .touch-btn.brake-btn {
      background: rgba(153, 27, 27, 0.9);
      border-color: #f87171;
      color: #fef2f2;
    }

    .touch-btn.brake-btn.active-brake {
      background: #ef4444;
      color: #ffffff;
      box-shadow: 0 0 14px rgba(239, 68, 68, 0.75);
    }

    .touch-btn.go-btn {
      background: rgba(6, 95, 70, 0.92);
      border-color: #34d399;
      color: #ecfdf5;
    }

    .leaderboard-strip {
      background: rgba(15, 23, 42, 0.78);
      border: 1px solid rgba(255, 208, 0, 0.28);
      border-radius: 12px;
      padding: 10px 14px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      font-size: 0.76rem;
    }

    .leaderboard-strip strong {
      color: var(--auto-yellow);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    .leaderboard-badges {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }

    .lb-pill {
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.14);
      border-radius: 8px;
      padding: 4px 9px;
      font-family: ui-monospace, monospace;
      font-size: 0.7rem;
      color: #e2e8f0;
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

    @media (max-width: 920px) {
      .controls-card {
        display: none;
      }
      .hud-bottom-row {
        justify-content: center;
        flex-wrap: wrap;
        gap: 10px;
      }
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
      <!-- Top-Left: Authentic Bengaluru Auto Digital Fare Meter + Trip Destination Progress -->
      <div class="auto-fare-unit interactive">
        <div class="meter-header">
          <span>ನಮ್ಮ ಆಟೋ • VAYUPUTRA RE</span>
          <span class="meter-status-dot" id="surge-badge">1.0x HIRE</span>
        </div>
        <div class="meter-screen">
          <div class="fare-digits" id="hud-fare">₹30.00</div>
          <div class="fare-sub" id="hud-dist">0.0 / 1.8 KM</div>
        </div>
        <div class="trip-progress-strip">
          <div class="trip-progress-label">
            <span id="hud-trip-title">🏁 TRIP TO INDIRANAGAR</span>
            <span id="hud-trip-pct">0%</span>
          </div>
          <div class="trip-bar-track">
            <div class="trip-bar-fill" id="hud-trip-fill"></div>
          </div>
        </div>
        <div class="dl-status-strip">
          <span>🪪 DIGILOCKER DL &amp; RC</span>
          <span class="dl-badge" id="hud-dl-status">VALID • PRESS [L]</span>
        </div>
      </div>

      <!-- Top-Center: Bilingual (Kannada + English) National Highway Sign, Traffic Signal & BTP Cop Alert -->
      <div class="highway-sign-cluster">
        <div class="nh-sign-board">
          <span class="nh-shield">NH 44</span>
          <div class="nh-text-stack">
            <span class="nh-kn" id="hud-landmark-kn">ಸಿಲ್ಕ್ ಬೋರ್ಡ್ ಮೇಲ್ಸೇತುವೆ • 45m</span>
            <span class="nh-en" id="hud-landmark">SILK BOARD FLYOVER GANTRY • 45m</span>
          </div>
        </div>

        <!-- Interactive BTP Red-Light Traffic Signal Banner -->
        <div class="signal-alert-banner interactive" id="hud-signal-banner">
          <div class="signal-lights-mini" aria-hidden="true">
            <span class="sig-dot red active" id="hud-sig-red"></span>
            <span class="sig-dot yellow" id="hud-sig-yellow"></span>
            <span class="sig-dot green" id="hud-sig-green"></span>
          </div>
          <div class="cop-alert-text">
            <span class="cop-alert-kn" id="hud-sig-kn">🚦 ಕೆಂಪು ಸಿಗ್ನಲ್! ನಿಲ್ಲಿಸಿ! (RED SIGNAL AHEAD — STOP BEFORE LINE!)</span>
            <span class="cop-alert-en" id="hud-sig-en">HOLD [S] OR PRESS [B] TO STOP • PRESS [W] WHEN GREEN (+₹100 BONUS)</span>
          </div>
          <span class="signal-timer-box" id="hud-sig-timer">05s</span>
          <button type="button" class="signal-action-btn" id="btn-sig-brake-start">🛑 STOP [B]</button>
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
      <nav class="top-toolbar interactive" aria-label="Game Mode, Camera View and Audio Controls">
        <div class="mode-segmented">
          <button type="button" class="tool-btn" data-quick-mode="old_blr">🏘️ Old Blr (0.5km)</button>
          <button type="button" class="tool-btn" data-quick-mode="low">Low</button>
          <button type="button" class="tool-btn active-mode" data-quick-mode="medium">Medium</button>
          <button type="button" class="tool-btn" data-quick-mode="complex">Peak Hour</button>
        </div>
        <button type="button" class="tool-btn action-pill" id="btn-camera-toggle">🎥 View: Chase [V]</button>
        <button type="button" class="tool-btn action-pill" id="btn-signal-test">🚦 Red Light</button>
        <button type="button" class="tool-btn action-pill" id="btn-handbrake">🛑 Brake [B]</button>
        <button type="button" class="tool-btn action-pill" id="btn-horn-test">📯 Horn</button>
        <button type="button" class="tool-btn action-pill" id="btn-cop-test">👮 Cop Check</button>
        <button type="button" class="tool-btn action-pill" id="btn-rain-toggle">🌧️ Rain</button>
        <button type="button" class="tool-btn action-pill" id="btn-end-trip">🏁 End Trip</button>
        <button type="button" class="tool-btn action-pill" id="btn-audio-toggle">🔊 Audio</button>
        <button type="button" class="tool-btn action-pill" id="btn-open-modal">⚙️ Menu</button>
      </nav>
    </header>

    <footer class="hud-bottom-row">
      <!-- Bottom-Left: Controls Guide -->
      <div class="controls-card interactive">
        <span class="key-item"><kbd>W</kbd><kbd>A</kbd><kbd>S</kbd><kbd>D</kbd> Steer, Stop &amp; Start</span>
        <span class="key-item"><kbd>B</kbd> Handbrake Stop / Release</span>
        <span class="key-item"><kbd>V</kbd> Dash Cam / Chase View</span>
        <span class="key-item"><kbd>SPACE</kbd> Start / Turbo Boost</span>
        <span class="key-item"><kbd>H</kbd> Horn</span>
        <span class="key-item"><kbd>L</kbd> Show DL</span>
      </div>

      <!-- Bottom-Center: Interactive On-Screen Touch & Mouse Driving Controls -->
      <div class="touch-controls-bar interactive" id="touch-controls-bar" role="group" aria-label="On-Screen Driving and Signal Stop/Start Controls">
        <button type="button" class="touch-btn" id="tbtn-left">
          <span>◀ LEFT</span>
          <span class="sub-key">[A / ←]</span>
        </button>
        <button type="button" class="touch-btn" id="tbtn-right">
          <span>RIGHT ▶</span>
          <span class="sub-key">[D / →]</span>
        </button>
        <button type="button" class="touch-btn brake-btn" id="tbtn-brake">
          <span id="tbtn-brake-label">🛑 STOP</span>
          <span class="sub-key">[S / B]</span>
        </button>
        <button type="button" class="touch-btn go-btn" id="tbtn-go">
          <span>🟢 GO / START</span>
          <span class="sub-key">[W / ↑]</span>
        </button>
        <button type="button" class="touch-btn" id="tbtn-horn">
          <span>📯 HORN</span>
          <span class="sub-key">[H]</span>
        </button>
        <button type="button" class="touch-btn" id="tbtn-dl">
          <span>🪪 SHOW DL</span>
          <span class="sub-key">[L]</span>
        </button>
      </div>

      <!-- Bottom-Right: Speedometer, Grip & 3-Wheel Status -->
      <div class="speed-cluster interactive">
        <div class="speed-row">
          <div>
            <span class="speed-num" id="hud-speed">65</span>
            <span class="speed-unit">KM/H</span>
          </div>
          <span class="alt-badge" id="hud-alt">🎥 CHASE VIEW</span>
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

  <!-- 3D Viewport & Configurable First-Person Auto Dash Cam Cockpit Overlay -->
  <main>
    <canvas id="game-canvas" aria-label="Ondu Second 3D Bangalore Traffic Viewport"></canvas>
    <div id="dashcam-overlay" aria-hidden="true">
      <div class="dashcam-top-canopy"></div>
      <div class="dashcam-pillar-left"></div>
      <div class="dashcam-pillar-right"></div>
      <div class="dashcam-wiper" id="dashcam-wiper"></div>
      <div class="dashcam-garland">
        <div class="garland-strands">🌼🌿🍋🌶️🌿🌼</div>
        <div class="garland-tag">ನಮ್ಮ ಬೆಂಗಳೂರು ಆಟೋ • ವಾಯುಪುತ್ರ</div>
      </div>
      <div class="dashcam-rec-osd">
        <span class="rec-dot"></span>
        <span id="dashcam-osd-text">REC • KA-01-AG-9999 VAYUPUTRA RE DASHCAM • 4K HDR 60FPS</span>
      </div>
      <div class="dashcam-bottom-dash">
        <div class="dashcam-handlebar"></div>
        <div class="dashcam-dash-label">🛺 VAYUPUTRA RE COCKPIT • ವಾಯುಪುತ್ರ • PRESS [V] FOR CHASE VIEW</div>
      </div>
    </div>
    <div id="callout-layer" aria-hidden="true"></div>
  </main>

  <!-- Native Modal Dialog: Difficulty, Camera View & Route Menu -->
  <dialog id="gravity-modal" aria-labelledby="modal-title">
    <div class="hazard-trim"></div>
    <div class="modal-inner">
      <div class="modal-top">
        <span class="modal-badge">ನಮ್ಮ ಬೆಂಗಳೂರು • VAYUPUTRA RE (ವಾಯುಪುತ್ರ) HD TRAFFIC EDITION</span>
      </div>
      <h1 id="modal-title">ಒಂದು ಸೆಕೆಂಡ್ | ONDU SECOND: NAMMA AUTO TRAFFIC</h1>
      <p class="modal-lead">
        Drive the iconic emerald-and-canary <strong>Vayuputra RE Compact (ವಾಯುಪುತ್ರ)</strong> Auto-Rickshaw through <strong>Old Bengaluru narrow gullies</strong> or wide highways! Stop at <strong>BTP Red-Light Signal Junctions</strong> (<kbd>S</kbd> or <kbd>B</kbd>) and start on Green (<kbd>W</kbd>), read <strong>HD Kannada + English hoardings</strong>, flash your <strong>DigiLocker DL</strong>, and dodge darting <strong>Indie stray dogs</strong>!
      </p>

      <!-- User-Configurable Camera Perspective Selector -->
      <div class="camera-config-bar">
        <span class="camera-config-title">🎥 Camera Perspective (Configurable Anytime with [V]):</span>
        <div class="camera-config-btns">
          <button type="button" class="cam-opt-btn active-cam" data-set-cam="chase">🎥 Regular Chase View (3rd Person)</button>
          <button type="button" class="cam-opt-btn" data-set-cam="dashcam">🛺 Vayuputra RE Dash Cam View (Driver Cockpit POV)</button>
        </div>
      </div>

      <div class="mode-grid">
        <article class="mode-card" data-mode="old_blr">
          <div>
            <span class="mode-tag tag-oldblr">Heritage • Narrow Gully (0.5 KM)</span>
            <h2>ಹಳೆಯ ಬೆಂಗಳೂರು ಗಲ್ಲಿ | Old Bengaluru Gullies</h2>
            <p class="mode-desc">
              Short 0.5 KM squeeze through narrow Chickpet &amp; Malleshwaram bazaar lanes! Mangalore-tiled silk &amp; filter-kaapi shops, flower stalls, overhead marigold toranas, shoppers &amp; stray dogs.
            </p>
            <ul class="mode-stats">
              <li><strong>Trip Distance:</strong> 0.5 KM (Chickpet → Malleshwaram)</li>
              <li><strong>Narrow Lane:</strong> 2-Lane Heritage Gully • 11 Vehicles • 1 Signal</li>
              <li><strong>Hazards:</strong> 7 Bazaar Shoppers • 4 Stray Dogs • 1 Beat Cop</li>
            </ul>
          </div>
          <button type="button" class="launch-btn" data-select-mode="old_blr">Start 0.5 KM Gully Trip</button>
        </article>

        <article class="mode-card" data-mode="low">
          <div>
            <span class="mode-tag tag-low">Low • Easy Route (1.2 KM)</span>
            <h2>ಕಬ್ಬನ್ ಪಾರ್ಕ್ ಬೆಳಿಗ್ಗೆ | Cubbon Park Morning</h2>
            <p class="mode-desc">
              Cruising morning ride with HD bilingual Kannada hoardings, BTP traffic signal junctions, occasional stray dogs &amp; jaywalkers, and friendly BTP patrol checkposts.
            </p>
            <ul class="mode-stats">
              <li><strong>Trip Distance:</strong> 1.2 KM (MG Road → Cubbon Park)</li>
              <li><strong>Traffic &amp; Signals:</strong> 12 Grounded Vehicles • 2 Traffic Signals</li>
              <li><strong>Hazards:</strong> 5 Jaywalkers • 3 Stray Dogs • 1 BTP Cop</li>
            </ul>
          </div>
          <button type="button" class="launch-btn" data-select-mode="low">Start 1.2 KM Trip</button>
        </article>

        <article class="mode-card selected" data-mode="medium">
          <div>
            <span class="mode-tag tag-med">Medium • Normal Route (1.8 KM)</span>
            <h2>ಇಂದಿರಾನಗರ ಸಂಜೆ ರಶ್ | Indiranagar 6 PM Rush</h2>
            <p class="mode-desc">
              Bustling evening rush with BTP Red-Light Signal Junctions, oncoming BMTC 500D buses, sudden BTP license stops, darting Indie stray dogs, and Zepto/Blinkit cut-offs.
            </p>
            <ul class="mode-stats">
              <li><strong>Trip Distance:</strong> 1.8 KM (Silk Board → Indiranagar)</li>
              <li><strong>Traffic &amp; Signals:</strong> 20 Grounded Vehicles • 2 Traffic Signals</li>
              <li><strong>Hazards:</strong> 8 Jaywalkers • 5 Stray Dogs • 2 BTP Cops</li>
            </ul>
          </div>
          <button type="button" class="launch-btn" data-select-mode="medium">Start 1.8 KM Trip</button>
        </article>

        <article class="mode-card" data-mode="complex">
          <div>
            <span class="mode-tag tag-complex">Complex • Peak Hour (2.5 KM)</span>
            <h2>ಸಿಲ್ಕ್ ಬೋರ್ಡ್ ಟ್ರಾಫಿಕ್ | Silk Board 8 PM Gridlock</h2>
            <p class="mode-desc">
              Full Silk Board peak-hour madness! Red-light camera junctions, non-stop BMTC convoys, aggressive BTP e-Challan nakabandis, pack of darting stray dogs, and monsoon hydroplaning.
            </p>
            <ul class="mode-stats">
              <li><strong>Trip Distance:</strong> 2.5 KM (Electronic City → Hebbal)</li>
              <li><strong>Traffic &amp; Signals:</strong> 30 Dense Vehicles • 3 Traffic Signals</li>
              <li><strong>Hazards:</strong> 12 Jaywalkers • 7 Stray Dogs • 3 BTP Cops</li>
            </ul>
          </div>
          <button type="button" class="launch-btn" data-select-mode="complex">Start 2.5 KM Trip</button>
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

  <!-- Native Modal Dialog: End-of-Trip Scoreboard, Viral Fare Receipt & Local Leaderboard -->
  <dialog id="score-modal" aria-labelledby="score-modal-title">
    <div class="hazard-trim"></div>
    <div class="modal-inner">
      <div class="modal-top">
        <span class="modal-badge" id="score-route-badge">🏁 ನಮ್ಮ ಆಟೋ ಮೀಟರ್ ರಸೀದಿ • VAYUPUTRA RE TRIP RECEIPT</span>
      </div>
      <h1 id="score-modal-title">🏁 ಪ್ರಯಾಣ ಮುಕ್ತಾಯ! | TRIP COMPLETED — FINAL SCOREBOARD</h1>
      <p class="modal-lead" id="score-modal-subtitle">
        You navigated Bengaluru traffic in your Vayuputra RE and reached your destination! Download your thermal fare receipt PNG or share your score:
      </p>

      <div class="score-hero-row">
        <div>
          <div style="font-size: 0.72rem; font-weight: 800; color: #94a3b8; text-transform: uppercase;">Final Driver Score</div>
          <div class="score-big-num" id="score-total-pts">2,450 PTS</div>
          <span class="score-rank-pill" id="score-rank-badge">🏆 S-RANK • ನಮ್ಮ ಆಟೋ ರಾಜ (BENGALURU AUTO LEGEND)</span>
        </div>
        <div style="text-align: right;">
          <div style="font-size: 0.72rem; font-weight: 800; color: #94a3b8; text-transform: uppercase;">Final Auto Meter Fare</div>
          <div class="score-big-num" style="color: #4ade80;" id="score-total-fare">₹385.00</div>
          <div style="font-size: 0.75rem; color: #cbd5e1; font-weight: 700;" id="score-dist-summary">Distance: 1.8 / 1.8 KM</div>
        </div>
      </div>

      <table class="score-breakdown-table">
        <thead>
          <tr>
            <th>Scoring Category</th>
            <th>Count / Details</th>
            <th>Fare / Score Impact</th>
          </tr>
        </thead>
        <tbody id="score-breakdown-body">
        </tbody>
      </table>

      <!-- Persistent Local High-Score Leaderboard Strip -->
      <div class="leaderboard-strip">
        <strong>🏆 Local Top Runs (KA-01 Hall of Fame):</strong>
        <div class="leaderboard-badges" id="score-leaderboard-list">
          <span class="lb-pill">#1 2,450 PTS • ₹385</span>
        </div>
      </div>

      <div class="score-actions">
        <button type="button" class="launch-btn share-receipt-btn" id="btn-download-receipt">🧾 Download Fare Receipt PNG</button>
        <button type="button" class="launch-btn secondary-btn" id="btn-share-score">📤 Share Challenge Text</button>
        <button type="button" class="launch-btn" id="btn-score-replay">🔄 Play Again (New Trip)</button>
        <button type="button" class="launch-btn secondary-btn" id="btn-score-switch-cam">🎥 Switch View &amp; Replay</button>
        <button type="button" class="launch-btn secondary-btn" id="btn-score-menu">⚙️ Change Route</button>
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
    // 3. DIFFICULTY & ROUTE PROFILES (Finite Trips + Two-Way Traffic + Cops + Stray Dogs)
    // =========================================================================
    const GRAVITY_PROFILES = {
      old_blr: {
        id: 'old_blr',
        isNarrowGully: true,
        roadWidth: 9.6,
        cruiseSpeed: 19.5,
        routeTitle: 'CHICKPET → MALLESHWARAM',
        shieldCode: 'BLR 02',
        targetDistanceKm: 0.5,
        trafficCount: 11,
        signalCount: 1,
        jaywalkerCount: 7,
        dogCount: 4,
        copCount: 1,
        busRatio: 0.0,
        deliveryRatio: 0.50,
        deliverySpeedMult: 1.12,
        cutOffAggression: 0.42,
        potholeCount: 4,
        potholePullStrength: 13.0,
        potholeRadius: 3.3,
        rainCycleDuration: 26,
        rainStormDuration: 7,
        fareRateMult: 1.8
      },
      low: {
        id: 'low',
        isNarrowGully: false,
        roadWidth: 22.8,
        cruiseSpeed: 30,
        routeTitle: 'MG ROAD → CUBBON PARK',
        shieldCode: 'NH 44',
        targetDistanceKm: 1.2,
        trafficCount: 12,
        signalCount: 2,
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
        fareRateMult: 1.0
      },
      medium: {
        id: 'medium',
        isNarrowGully: false,
        roadWidth: 22.8,
        cruiseSpeed: 32,
        routeTitle: 'SILK BOARD → INDIRANAGAR',
        shieldCode: 'NH 44',
        targetDistanceKm: 1.8,
        trafficCount: 20,
        signalCount: 2,
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
        fareRateMult: 1.5
      },
      complex: {
        id: 'complex',
        isNarrowGully: false,
        roadWidth: 22.8,
        cruiseSpeed: 34,
        routeTitle: 'ELECTRONIC CITY → HEBBAL',
        shieldCode: 'NH 44',
        targetDistanceKm: 2.5,
        trafficCount: 30,
        signalCount: 3,
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
        fareRateMult: 2.5
      }
    };

    let currentProfile = GRAVITY_PROFILES.medium;

    // =========================================================================
    // 4. ULTRA-HD THREE.JS SCENE, 4X MSAA HDR COMPOSER, PMREM & 4K SHADOWS
    // =========================================================================
    const canvas = document.getElementById('game-canvas');
    const MAX_DPR = Math.min(window.devicePixelRatio || 1, 2.5);
    const renderer = new THREE.WebGLRenderer({
      canvas,
      antialias: true,
      powerPreference: 'high-performance'
    });
    renderer.setPixelRatio(MAX_DPR);
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 0.98;

    function finalizeHDTexture(canvasEl, repeatX = 1, repeatY = 1) {
      const tex = new THREE.CanvasTexture(canvasEl);
      tex.colorSpace = THREE.SRGBColorSpace;
      tex.generateMipmaps = true;
      tex.minFilter = THREE.LinearMipmapLinearFilter;
      tex.magFilter = THREE.LinearFilter;
      tex.anisotropy = renderer.capabilities.getMaxAnisotropy();
      if (repeatX !== 1 || repeatY !== 1) {
        tex.wrapS = THREE.RepeatWrapping;
        tex.wrapT = THREE.RepeatWrapping;
        tex.repeat.set(repeatX, repeatY);
      }
      return tex;
    }

    const scene = new THREE.Scene();
    const drySkyColor = new THREE.Color(0x1b2b48);
    const gullySkyColor = new THREE.Color(0x282138);
    const rainSkyColor = new THREE.Color(0x0d1524);
    scene.background = drySkyColor.clone();
    scene.fog = new THREE.FogExp2(0x1b2b48, 0.0034);

    // PMREM Metallic & Glass Reflections (Pro-Game PBR Lighting)
    const pmremGenerator = new THREE.PMREMGenerator(renderer);
    scene.environment = pmremGenerator.fromScene(new RoomEnvironment(), 0.035).texture;
    scene.environmentIntensity = 0.32;

    const camera = new THREE.PerspectiveCamera(58, window.innerWidth / window.innerHeight, 0.1, 440);
    camera.position.set(0, 4.2, 7.8);

    // Hardware 4x MSAA + HalfFloat HDR Post-Processing Composer for Razor-Sharp HD Edges
    const msaaRenderTarget = new THREE.WebGLRenderTarget(
      Math.floor(window.innerWidth * MAX_DPR),
      Math.floor(window.innerHeight * MAX_DPR),
      {
        samples: 4,
        type: THREE.HalfFloatType,
        colorSpace: THREE.SRGBColorSpace
      }
    );
    const composer = new EffectComposer(renderer, msaaRenderTarget);
    composer.setPixelRatio(MAX_DPR);
    composer.setSize(window.innerWidth, window.innerHeight);
    composer.addPass(new RenderPass(scene, camera));
    const bloomPass = new UnrealBloomPass(
      new THREE.Vector2(window.innerWidth * MAX_DPR, window.innerHeight * MAX_DPR),
      0.14, // subtle crisp HDR glow
      0.28,
      0.94  // high threshold so text & hoardings stay razor-sharp!
    );
    composer.addPass(bloomPass);
    composer.addPass(new OutputPass());

    const hemiLight = new THREE.HemisphereLight(0xa5cbff, 0x3b2f26, 0.98);
    scene.add(hemiLight);

    const sunLight = new THREE.DirectionalLight(0xffe8c2, 1.9);
    sunLight.position.set(34, 58, 28);
    sunLight.castShadow = true;
    sunLight.shadow.mapSize.set(4096, 4096);
    sunLight.shadow.camera.near = 1;
    sunLight.shadow.camera.far = 185;
    const d = 42;
    sunLight.shadow.camera.left = -d;
    sunLight.shadow.camera.right = d;
    sunLight.shadow.camera.top = d;
    sunLight.shadow.camera.bottom = -d;
    sunLight.shadow.bias = -0.0003;
    sunLight.shadow.normalBias = 0.018;
    scene.add(sunLight);

    // Procedural 2K HD Bengaluru Golden-Hour / Dusk Horizon Sky Dome
    function createSkyDomeTexture() {
      const c = document.createElement('canvas');
      c.width = 2048;
      c.height = 1024;
      const ctx = c.getContext('2d');
      const grad = ctx.createLinearGradient(0, 0, 0, 1024);
      grad.addColorStop(0.0, '#091024');
      grad.addColorStop(0.32, '#16274c');
      grad.addColorStop(0.46, '#3b4e7d');
      grad.addColorStop(0.515, '#e6844e');
      grad.addColorStop(0.545, '#f6b26b');
      grad.addColorStop(0.585, '#2b354f');
      grad.addColorStop(1.0, '#111827');
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, 2048, 1024);

      // Crisp twilight stars near upper sky
      for (let s = 0; s < 140; s++) {
        const sx = Math.random() * 2048;
        const sy = Math.random() * 340;
        const sr = 0.7 + Math.random() * 1.4;
        ctx.fillStyle = `rgba(255, 250, 240, ${0.25 + Math.random() * 0.55})`;
        ctx.beginPath();
        ctx.arc(sx, sy, sr, 0, Math.PI * 2);
        ctx.fill();
      }

      // Layered golden-hour clouds near horizon
      for (let i = 0; i < 65; i++) {
        const cx = Math.random() * 2048;
        const cy = 310 + Math.random() * 210;
        const rw = 100 + Math.random() * 260;
        const rh = 14 + Math.random() * 36;
        const cg = ctx.createRadialGradient(cx, cy, 4, cx, cy, rw);
        cg.addColorStop(0, 'rgba(255, 205, 148, 0.20)');
        cg.addColorStop(0.55, 'rgba(232, 132, 88, 0.09)');
        cg.addColorStop(1, 'rgba(255, 196, 138, 0.0)');
        ctx.fillStyle = cg;
        ctx.beginPath();
        ctx.ellipse(cx, cy, rw, rh, 0, 0, Math.PI * 2);
        ctx.fill();
      }
      return finalizeHDTexture(c);
    }

    const skyDome = new THREE.Mesh(
      new THREE.SphereGeometry(380, 40, 24),
      new THREE.MeshBasicMaterial({ map: createSkyDomeTexture(), side: THREE.BackSide, fog: false })
    );
    scene.add(skyDome);

    // =========================================================================
    // 5. 2K HD PBR ASPHALT HIGHWAY, NARROW OLD BENGALURU GULLIES & HD HOARDINGS
    // =========================================================================
    const ROAD_WIDTH = 22.8; // 6-lane highway * 3.8m
    const GULLY_ROAD_WIDTH = 9.6; // Narrow 2-lane Old Bengaluru bazaar gully!
    const LANES = [-9.5, -5.7, -1.9, 1.9, 5.7, 9.5];
    const GULLY_LANES = [-3.1, -1.35, 1.35, 3.1]; // 2 tight forward streams + 2 tight oncoming streams
    const CORRIDOR_LENGTH = 360;

    function getActiveRoadWidth() {
      return currentProfile && currentProfile.isNarrowGully ? GULLY_ROAD_WIDTH : ROAD_WIDTH;
    }

    function getActiveLanes() {
      return currentProfile && currentProfile.isNarrowGully ? GULLY_LANES : LANES;
    }

    function createAsphaltTextures() {
      const c = document.createElement('canvas');
      c.width = 2048;
      c.height = 2048;
      const ctx = c.getContext('2d');
      ctx.fillStyle = '#232834';
      ctx.fillRect(0, 0, 2048, 2048);

      const bumpCanvas = document.createElement('canvas');
      bumpCanvas.width = 1024;
      bumpCanvas.height = 1024;
      const bctx = bumpCanvas.getContext('2d');
      bctx.fillStyle = '#808080';
      bctx.fillRect(0, 0, 1024, 1024);

      // High-definition micro-aggregate tarmac grain & tar seal lines
      for (let i = 0; i < 65000; i++) {
        const x = Math.random() * 2048;
        const y = Math.random() * 2048;
        const v = 26 + Math.floor(Math.random() * 34);
        ctx.fillStyle = `rgb(${v}, ${v + 3}, ${v + 9})`;
        ctx.fillRect(x, y, 2, 2);
        if (i < 28000) {
          const bv = 105 + Math.floor(Math.random() * 50);
          bctx.fillStyle = `rgb(${bv},${bv},${bv})`;
          bctx.fillRect(x * 0.5, y * 0.5, 2, 2);
        }
      }

      // Subtle glossy tire wear tracks down each lane
      for (let lane = 0; lane < 6; lane++) {
        const lx = ((lane + 0.5) / 6) * 2048;
        for (const wheelOffset of [-64, 64]) {
          const tg = ctx.createLinearGradient(lx + wheelOffset - 44, 0, lx + wheelOffset + 44, 0);
          tg.addColorStop(0, 'rgba(15, 18, 25, 0)');
          tg.addColorStop(0.5, 'rgba(13, 16, 23, 0.44)');
          tg.addColorStop(1, 'rgba(15, 18, 25, 0)');
          ctx.fillStyle = tg;
          ctx.fillRect(lx + wheelOffset - 44, 0, 88, 2048);
        }
      }

      const colorMap = finalizeHDTexture(c, 1, 28);
      const bumpMap = new THREE.CanvasTexture(bumpCanvas);
      bumpMap.wrapS = THREE.RepeatWrapping;
      bumpMap.wrapT = THREE.RepeatWrapping;
      bumpMap.repeat.set(2, 56);
      bumpMap.anisotropy = renderer.capabilities.getMaxAnisotropy();
      return { colorMap, bumpMap };
    }

    const asphaltMaps = createAsphaltTextures();
    const roadMat = new THREE.MeshStandardMaterial({
      map: asphaltMaps.colorMap,
      bumpMap: asphaltMaps.bumpMap,
      bumpScale: 0.016,
      color: 0xdce2ec,
      roughness: 0.66,
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
    // 5B. 2K ULTRA-HD ILLUSTRATED BILINGUAL (KANNADA + ENGLISH) HOARDINGS
    // =========================================================================
    const BILINGUAL_HOARDING_ADS = [
      {
        artType: 'dosa',
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
        artType: 'auto',
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
        artType: 'milk',
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
        artType: 'metro',
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
        artType: 'sandal',
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
        artType: 'btp',
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
        artType: 'delivery',
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
        artType: 'dosa',
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

    function drawHoardingVectorIllustration(ctx, artType, cx, cy, borderCol, accentCol) {
      ctx.save();
      // Glowing circular medallion backdrop on right side of hoarding
      const rad = ctx.createRadialGradient(cx, cy, 24, cx, cy, 195);
      rad.addColorStop(0, 'rgba(255,255,255,0.22)');
      rad.addColorStop(0.7, 'rgba(0,0,0,0.28)');
      rad.addColorStop(1, 'rgba(0,0,0,0.48)');
      ctx.fillStyle = rad;
      ctx.beginPath();
      ctx.arc(cx, cy, 185, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = borderCol;
      ctx.lineWidth = 6;
      ctx.stroke();

      if (artType === 'dosa') {
        // Banana leaf
        ctx.fillStyle = '#15803d';
        ctx.beginPath();
        ctx.ellipse(cx, cy + 34, 145, 76, -0.08, 0, Math.PI * 2);
        ctx.fill();
        // Crispy golden masala dosa cone/roll
        const dg = ctx.createLinearGradient(cx - 125, cy - 10, cx + 125, cy + 45);
        dg.addColorStop(0, '#f59e0b');
        dg.addColorStop(0.5, '#fbbf24');
        dg.addColorStop(1, '#b45309');
        ctx.fillStyle = dg;
        ctx.beginPath();
        ctx.moveTo(cx - 130, cy + 36);
        ctx.lineTo(cx + 120, cy - 18);
        ctx.lineTo(cx + 132, cy + 38);
        ctx.closePath();
        ctx.fill();
        // Melting white butter dollop + chutney bowls
        ctx.fillStyle = '#fef9c3';
        ctx.beginPath();
        ctx.arc(cx - 6, cy + 14, 18, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = '#f8fafc';
        ctx.beginPath();
        ctx.arc(cx - 58, cy + 68, 22, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = '#dc2626';
        ctx.beginPath();
        ctx.arc(cx, cy + 74, 22, 0, Math.PI * 2);
        ctx.fill();
        // Brass Filter Kaapi Davara-Tumbler + rising steam
        ctx.fillStyle = '#eab308';
        ctx.fillRect(cx + 55, cy - 82, 46, 58);
        ctx.beginPath();
        ctx.ellipse(cx + 78, cy - 22, 36, 12, 0, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = 'rgba(255,255,255,0.75)';
        ctx.lineWidth = 4;
        for (const sx of [cx + 66, cx + 86]) {
          ctx.beginPath();
          ctx.moveTo(sx, cy - 92);
          ctx.quadraticCurveTo(sx - 10, cy - 115, sx + 6, cy - 135);
          ctx.stroke();
        }
      } else if (artType === 'auto') {
        // Stylized Emerald & Canary Vayuputra RE Auto Emblem
        ctx.fillStyle = '#ffd000';
        ctx.beginPath();
        ctx.roundRect(cx - 95, cy - 88, 190, 74, 26);
        ctx.fill();
        ctx.fillStyle = '#009a44';
        ctx.beginPath();
        ctx.roundRect(cx - 102, cy - 18, 204, 86, 18);
        ctx.fill();
        ctx.fillStyle = '#38bdf8';
        ctx.beginPath();
        ctx.roundRect(cx - 72, cy - 68, 144, 48, 10);
        ctx.fill();
        ctx.fillStyle = '#fef08a';
        ctx.beginPath();
        ctx.arc(cx, cy + 24, 20, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = '#0f172a';
        ctx.beginPath();
        ctx.arc(cx - 74, cy + 76, 24, 0, Math.PI * 2);
        ctx.arc(cx + 74, cy + 76, 24, 0, Math.PI * 2);
        ctx.fill();
      } else if (artType === 'metro') {
        // Sleek Namma Metro Purple Train Front
        ctx.fillStyle = '#e2e8f0';
        ctx.beginPath();
        ctx.roundRect(cx - 88, cy - 105, 176, 185, 34);
        ctx.fill();
        ctx.fillStyle = '#7c3aed';
        ctx.fillRect(cx - 88, cy - 2, 176, 36);
        ctx.fillStyle = '#0f172a';
        ctx.beginPath();
        ctx.roundRect(cx - 68, cy - 82, 136, 66, 14);
        ctx.fill();
        ctx.fillStyle = '#fde047';
        ctx.beginPath();
        ctx.arc(cx - 52, cy + 54, 14, 0, Math.PI * 2);
        ctx.arc(cx + 52, cy + 54, 14, 0, Math.PI * 2);
        ctx.fill();
      } else {
        // Golden Heritage Crest / Emblem
        ctx.fillStyle = accentCol;
        ctx.beginPath();
        ctx.arc(cx, cy, 108, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = '#090d16';
        ctx.beginPath();
        ctx.arc(cx, cy, 82, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = borderCol;
        ctx.font = '900 72px "Noto Sans Kannada", "Inter", sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        const glyph = artType === 'milk' ? 'ನಂದಿನಿ' : artType === 'sandal' ? '೧೯೧೬' : artType === 'btp' ? 'BTP' : '10m';
        ctx.fillText(glyph, cx, cy + 4);
      }
      ctx.restore();
    }

    function createBilingualHoardingTexture(ad) {
      const c = document.createElement('canvas');
      c.width = 2048;
      c.height = 1024;
      const ctx = c.getContext('2d');
      ctx.scale(2, 2); // Author in crisp 1024x512 coordinates rendered at true 2048x1024 2K HD!

      const grad = ctx.createLinearGradient(0, 0, 1024, 512);
      grad.addColorStop(0, ad.bgTop);
      grad.addColorStop(1, ad.bgBot);
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, 1024, 512);

      // Subtle glossy studio spotlight sheen
      const sheen = ctx.createLinearGradient(0, 0, 620, 512);
      sheen.addColorStop(0, 'rgba(255,255,255,0.10)');
      sheen.addColorStop(0.45, 'rgba(255,255,255,0.02)');
      sheen.addColorStop(1, 'rgba(0,0,0,0.18)');
      ctx.fillStyle = sheen;
      ctx.fillRect(0, 0, 1024, 512);

      // Outer & inner neon border
      ctx.strokeStyle = ad.border;
      ctx.lineWidth = 12;
      ctx.strokeRect(14, 14, 996, 484);
      ctx.strokeStyle = 'rgba(255,255,255,0.32)';
      ctx.lineWidth = 3;
      ctx.strokeRect(28, 28, 968, 456);

      // Draw HD Vector Artwork Medallion on Right Side (x = 805, y = 278)
      drawHoardingVectorIllustration(ctx, ad.artType, 812, 284, ad.border, ad.accent);

      // Top 60% Kannada Header Pill
      ctx.fillStyle = ad.border;
      ctx.beginPath();
      ctx.roundRect(48, 44, 470, 48, 10);
      ctx.fill();
      ctx.fillStyle = '#090d16';
      ctx.font = '900 23px "Noto Sans Kannada", "Inter", sans-serif';
      ctx.fillText(ad.badge, 66, 76);

      // 60:40 Rule Tag on top-right
      ctx.fillStyle = 'rgba(9,13,22,0.68)';
      ctx.beginPath();
      ctx.roundRect(720, 42, 256, 44, 8);
      ctx.fill();
      ctx.strokeStyle = 'rgba(255,255,255,0.3)';
      ctx.lineWidth = 2;
      ctx.stroke();
      ctx.fillStyle = '#ffffff';
      ctx.font = '800 19px "Inter", sans-serif';
      ctx.fillText('ಕನ್ನಡ 60% • HD ULTRA', 740, 70);

      // Prominent Kannada Headline (60% Primary Display)
      ctx.save();
      ctx.fillStyle = ad.accent;
      ctx.shadowColor = 'rgba(0,0,0,0.75)';
      ctx.shadowBlur = 12;
      ctx.font = '900 54px "Noto Sans Kannada", "Arial Unicode MS", sans-serif';
      ctx.fillText(ad.knTitle, 48, 178, 560);

      // Kannada Sub-headline
      ctx.fillStyle = '#ffffff';
      ctx.font = '700 28px "Noto Sans Kannada", "Arial Unicode MS", sans-serif';
      ctx.fillText(ad.knSub, 48, 236, 560);
      ctx.restore();

      // Divider rule
      ctx.strokeStyle = ad.border;
      ctx.lineWidth = 4;
      ctx.beginPath();
      ctx.moveTo(48, 274);
      ctx.lineTo(604, 274);
      ctx.stroke();

      // English Headline (40% Secondary Display)
      ctx.fillStyle = '#ffffff';
      ctx.font = '900 40px "Inter", -apple-system, sans-serif';
      ctx.fillText(ad.enTitle, 48, 344, 560);

      // English Sub-headline
      ctx.fillStyle = '#e2e8f0';
      ctx.font = '800 22px "Inter", -apple-system, sans-serif';
      ctx.fillText(ad.enSub, 48, 404, 560);

      return finalizeHDTexture(c);
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

      return finalizeHDTexture(c);
    }

    // Build Scrolling Corridor Segments (6m each) — Highway + Narrow Old Bengaluru Gully Support
    const scrollingStrips = [];
    const highwayOnlyObjects = [];
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

      const hwySubGroup = new THREE.Group();
      row.add(hwySubGroup);
      highwayOnlyObjects.push(hwySubGroup);

      // Center Yellow Divider (shared by both 6-lane highway and 2-lane narrow Old Bengaluru gully!)
      const cl = new THREE.Mesh(new THREE.BoxGeometry(0.20, 0.022, 6.02), yellowLineMat);
      cl.position.set(0, 0.012, 0);
      row.add(cl);

      // Outer 6-lane Highway Dashes
      for (const lx of [-7.6, -3.8, 3.8, 7.6]) {
        if (segIdx % 2 === 0) {
          const dash = new THREE.Mesh(dashGeo, whiteDashMat);
          dash.position.set(lx, 0.012, 0);
          hwySubGroup.add(dash);
        }
      }

      // Yellow-and-Black Highway Kerbs
      const kMat = segIdx % 2 === 0 ? kerbYellowMat : kerbBlackMat;
      const kerbL = new THREE.Mesh(kerbGeo, kMat);
      kerbL.position.set(-ROAD_WIDTH / 2 - 0.28, 0.13, 0);
      const kerbR = new THREE.Mesh(kerbGeo, kMat);
      kerbR.position.set(ROAD_WIDTH / 2 + 0.28, 0.13, 0);
      hwySubGroup.add(kerbL, kerbR);

      // Painted White Zebra Crossings on Highway
      if (segIdx % 14 === 3) {
        const zebraGeo = new THREE.BoxGeometry(0.95, 0.024, 3.8);
        for (let zx = -9.6; zx <= 9.6; zx += 1.6) {
          if (Math.abs(zx) < 0.5) continue;
          const stripe = new THREE.Mesh(zebraGeo, whiteDashMat);
          stripe.position.set(zx, 0.014, 0);
          hwySubGroup.add(stripe);
        }
      }

      // Continuous Unbroken Namma Metro Elevated Viaduct along X = +18.5 (Highway modes)
      const vDeck = new THREE.Mesh(viaductDeckGeo, concreteMat);
      vDeck.position.set(METRO_X, 8.2, 0);
      vDeck.receiveShadow = true;
      const vWallL = new THREE.Mesh(viaductWallGeo, metroPurpleMat);
      vWallL.position.set(METRO_X - 3.3, 9.1, 0);
      const vWallR = new THREE.Mesh(viaductWallGeo, metroPurpleMat);
      vWallR.position.set(METRO_X + 3.3, 9.1, 0);
      hwySubGroup.add(vDeck, vWallL, vWallR);

      if (segIdx % 3 === 0) {
        const pier = new THREE.Mesh(viaductPierGeo, concreteMat);
        pier.position.set(METRO_X, 3.8, 0);
        const cap = new THREE.Mesh(viaductCapGeo, concreteMat);
        cap.position.set(METRO_X, 7.3, 0);
        hwySubGroup.add(pier, cap);
      }

      // Lush Bengaluru Rain Trees & Warm LED Highway Streetlamps
      if (segIdx % 5 === 0) {
        const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.28, 0.38, 3.6, 8), treeTrunkMat);
        trunk.position.set(-ROAD_WIDTH / 2 - 11.2, 1.8, 0);
        const crown1 = new THREE.Mesh(new THREE.SphereGeometry(2.6, 12, 10), segIdx % 10 === 0 ? treeLeafMat : gulmoharLeafMat);
        crown1.scale.set(1.25, 0.68, 1.25);
        crown1.position.set(-ROAD_WIDTH / 2 - 11.2, 4.6, 0);
        hwySubGroup.add(trunk, crown1);

        const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.13, 7.5, 8), poleMetalMat);
        pole.position.set(-ROAD_WIDTH / 2 - 1.2, 3.75, 2.2);
        const arm = new THREE.Mesh(new THREE.BoxGeometry(1.8, 0.10, 0.10), poleMetalMat);
        arm.position.set(-ROAD_WIDTH / 2 - 0.4, 7.4, 2.2);
        const bulb = new THREE.Mesh(new THREE.BoxGeometry(0.55, 0.08, 0.24), lampBulbMat);
        bulb.position.set(-ROAD_WIDTH / 2 + 0.2, 7.34, 2.2);
        hwySubGroup.add(pole, arm, bulb);
      }

      scene.add(row);
      scrollingStrips.push(row);
    }

    // =========================================================================
    // 5C. NEW! OLD BENGALURU NARROW HERITAGE GULLY (CHICKPET / MALLESHWARAM 0.5KM)
    // =========================================================================
    const oldBlrGullyGroup = new THREE.Group();
    oldBlrGullyGroup.visible = false;
    scene.add(oldBlrGullyGroup);
    const gullyScrollingRows = [];
    const gullyLandmarkInstances = [];

    const OLD_BLR_SHOPS = [
      {
        bg: '#7c2d12',
        border: '#fbbf24',
        kn: 'ಚಿಕ್ಕಪೇಟೆ ರೇಷ್ಮೆ ಸೀರೆ ಮಂದಿರ',
        en: 'CHICKPET KANCHIPURAM SILKS • ESTD 1928',
        wallHex: 0xd97706
      },
      {
        bg: '#14532d',
        border: '#fde047',
        kn: 'ಮಲ್ಲೇಶ್ವರಂ ಹೂವಿನ ಮಾರುಕಟ್ಟೆ',
        en: 'MALLESHWARAM JASMINE & MARIGOLD BAZAAR',
        wallHex: 0xb45309
      },
      {
        bg: '#1e3a8a',
        border: '#38bdf8',
        kn: 'ಶ್ರೀ ರಾಘವೇಂದ್ರ ಫಿಲ್ಟರ್ ಕಾಫಿ',
        en: 'HERITAGE DEGREE FILTER KAAPI & BENNE DOSA',
        wallHex: 0xeab308
      },
      {
        bg: '#581c87',
        border: '#f472b6',
        kn: 'ಬಳೇಪೇಟೆ ಬಳೆ ಮತ್ತು ಅಲಂಕಾರ',
        en: 'BALEPET GLASS BANGLES & KUMKUM EMPORIUM',
        wallHex: 0x9a3412
      },
      {
        bg: '#3f6212',
        border: '#bef264',
        kn: 'ಅವೆನ್ಯೂ ರಸ್ತೆ ಪುಸ್ತಕ ಬಜಾರ್',
        en: 'AVENUE ROAD RARE BOOKS & STATIONERY',
        wallHex: 0x0f766e
      },
      {
        bg: '#7f1d1d',
        border: '#fde68a',
        kn: 'ಗಾಂಧಿ ಬಜಾರ್ ಮಸಾಲೆ ಭಂಡಾರ',
        en: 'GANDHI BAZAAR SPICES, AGARBATTI & SANDAL',
        wallHex: 0xc2410c
      }
    ];

    function createHeritageShopSignTexture(shop) {
      const c = document.createElement('canvas');
      c.width = 1024;
      c.height = 256;
      const ctx = c.getContext('2d');
      ctx.fillStyle = shop.bg;
      ctx.fillRect(0, 0, 1024, 256);
      ctx.strokeStyle = shop.border;
      ctx.lineWidth = 12;
      ctx.strokeRect(10, 10, 1004, 236);
      ctx.strokeStyle = 'rgba(255,255,255,0.35)';
      ctx.lineWidth = 3;
      ctx.strokeRect(22, 22, 980, 212);

      ctx.fillStyle = '#fde047';
      ctx.font = '900 54px "Noto Sans Kannada", "Inter", sans-serif';
      ctx.fillText(shop.kn, 42, 114, 940);

      ctx.fillStyle = '#ffffff';
      ctx.font = '800 32px "Inter", sans-serif';
      ctx.fillText(shop.en, 42, 192, 940);
      return finalizeHDTexture(c);
    }

    function createHeritageArchBannerTexture(knText, enText) {
      const c = document.createElement('canvas');
      c.width = 1536;
      c.height = 320;
      const ctx = c.getContext('2d');
      const g = ctx.createLinearGradient(0, 0, 0, 320);
      g.addColorStop(0, '#7c2d12');
      g.addColorStop(1, '#431407');
      ctx.fillStyle = g;
      ctx.fillRect(0, 0, 1536, 320);
      ctx.strokeStyle = '#ffd000';
      ctx.lineWidth = 14;
      ctx.strokeRect(12, 12, 1512, 296);

      ctx.fillStyle = '#fde047';
      ctx.font = '900 66px "Noto Sans Kannada", "Inter", sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(knText, 768, 138, 1440);
      ctx.fillStyle = '#ffffff';
      ctx.font = '900 40px "Inter", sans-serif';
      ctx.fillText(enText, 768, 236, 1440);
      return finalizeHDTexture(c);
    }

    function buildOldBengaluruNarrowGullies() {
      const shopTextures = OLD_BLR_SHOPS.map((s) => createHeritageShopSignTexture(s));
      const graniteFootpathMat = new THREE.MeshStandardMaterial({ color: 0x64748b, roughness: 0.85 });
      const mangaloreTileMat = new THREE.MeshStandardMaterial({ color: 0x991b1b, roughness: 0.62 });
      const woodPillarMat = new THREE.MeshStandardMaterial({ color: 0x451a03, roughness: 0.78 });
      const windowLitMat = new THREE.MeshBasicMaterial({ color: 0xfef08a });
      const marigoldMat = new THREE.MeshBasicMaterial({ color: 0xf97316 });
      const jasmineMat = new THREE.MeshBasicMaterial({ color: 0xfef9c3 });
      const mangoLeafMat = new THREE.MeshStandardMaterial({ color: 0x15803d, roughness: 0.6 });

      const footpathGeo = new THREE.BoxGeometry(5.6, 0.28, 12.04);
      const gullyKerbGeo = new THREE.BoxGeometry(0.38, 0.30, 12.04);
      const shopBodyGeo = new THREE.BoxGeometry(4.2, 6.4, 11.4);
      const roofAwningGeo = new THREE.BoxGeometry(2.4, 0.22, 11.6);
      const upperRoofGeo = new THREE.ConeGeometry(3.4, 1.5, 4);

      for (let z = 36; z > -CORRIDOR_LENGTH + 36; z -= 12) {
        const segIdx = Math.round(Math.abs(z) / 12);
        const gRow = new THREE.Group();
        gRow.position.z = z;

        // Raised Granite Stone Bazaar Footpaths hugging the narrow 9.6m lane (X = ±4.8m edge!)
        const kMat = segIdx % 2 === 0 ? kerbYellowMat : kerbBlackMat;
        for (const side of [-1, 1]) {
          const kerb = new THREE.Mesh(gullyKerbGeo, kMat);
          kerb.position.set(side * (GULLY_ROAD_WIDTH / 2 + 0.19), 0.15, 0);
          const fp = new THREE.Mesh(footpathGeo, graniteFootpathMat);
          fp.position.set(side * (GULLY_ROAD_WIDTH / 2 + 2.95), 0.14, 0);
          fp.receiveShadow = true;
          gRow.add(kerb, fp);

          // 2-Storey Old Bengaluru Heritage Shopfront right alongside the narrow gully (X = ±7.8m)
          const shopIdx = (segIdx + (side > 0 ? 3 : 0)) % OLD_BLR_SHOPS.length;
          const shopCfg = OLD_BLR_SHOPS[shopIdx];
          const wallMat = new THREE.MeshStandardMaterial({ color: shopCfg.wallHex, roughness: 0.78 });
          const bldg = new THREE.Mesh(shopBodyGeo, wallMat);
          bldg.position.set(side * 7.85, 3.2, 0);
          bldg.castShadow = true;
          bldg.receiveShadow = true;
          gRow.add(bldg);

          // Sloped Red Mangalore Clay-Tile Verandah Awning overhanging the footpath
          const awning = new THREE.Mesh(roofAwningGeo, mangaloreTileMat);
          awning.position.set(side * 5.65, 3.15, 0);
          awning.rotation.z = side * 0.28;
          gRow.add(awning);

          // Pitched Mangalore-Tile Top Roof
          const topRoof = new THREE.Mesh(upperRoofGeo, mangaloreTileMat);
          topRoof.position.set(side * 7.85, 7.15, 0);
          topRoof.rotation.y = Math.PI / 4;
          topRoof.scale.set(1.0, 1.0, 2.35);
          gRow.add(topRoof);

          // Carved Wooden Verandah Pillars & Glowing Upper-Storey Louvered Windows
          for (const pz of [-4.2, 0, 4.2]) {
            const pillar = new THREE.Mesh(new THREE.CylinderGeometry(0.11, 0.13, 3.0, 8), woodPillarMat);
            pillar.position.set(side * 5.25, 1.5, pz);
            gRow.add(pillar);

            const win = new THREE.Mesh(new THREE.PlaneGeometry(0.95, 1.35), windowLitMat);
            win.position.set(side * 5.72, 4.9, pz);
            win.rotation.y = side > 0 ? -Math.PI / 2 : Math.PI / 2;
            gRow.add(win);
          }

          // Crisp HD Bilingual Kannada + English Shop Signboard facing oncoming driver & gully!
          const signMesh = new THREE.Mesh(
            new THREE.BoxGeometry(0.14, 1.25, 5.2),
            new THREE.MeshBasicMaterial({ map: shopTextures[shopIdx] })
          );
          signMesh.position.set(side * 5.52, 3.85, 0);
          // Also add an angled projecting shop flag-sign so driver reads it straight ahead down the narrow lane!
          const flagSign = new THREE.Mesh(
            new THREE.PlaneGeometry(3.2, 0.85),
            new THREE.MeshBasicMaterial({ map: shopTextures[shopIdx], side: THREE.DoubleSide })
          );
          flagSign.position.set(side * 5.05, 4.15, 3.6);
          flagSign.rotation.y = side * 0.22;
          gRow.add(signMesh, flagSign);

          // Roadside Flower & Fruit Bazaar Basket Stalls (Marigold & Mysuru Mallige Jasmine!)
          if ((segIdx + (side > 0 ? 1 : 0)) % 2 === 0) {
            const cart = new THREE.Mesh(new THREE.BoxGeometry(0.95, 0.75, 1.8), woodPillarMat);
            cart.position.set(side * 5.38, 0.62, -2.2);
            const mHeap = new THREE.Mesh(new THREE.SphereGeometry(0.42, 10, 8), marigoldMat);
            mHeap.scale.set(1.0, 0.65, 1.2);
            mHeap.position.set(side * 5.35, 1.12, -2.55);
            const jHeap = new THREE.Mesh(new THREE.SphereGeometry(0.38, 10, 8), jasmineMat);
            jHeap.scale.set(1.0, 0.65, 1.1);
            jHeap.position.set(side * 5.35, 1.10, -1.80);
            gRow.add(cart, mHeap, jHeap);
          }
        }

        // Overhead Festival Marigold & Mango-Leaf Torana String Lights spanning the Narrow Gully!
        if (segIdx % 2 === 0) {
          const wire = new THREE.Mesh(new THREE.BoxGeometry(10.8, 0.05, 0.05), woodPillarMat);
          wire.position.set(0, 6.15, 0);
          gRow.add(wire);
          for (let tx = -4.5; tx <= 4.5; tx += 0.9) {
            const sag = Math.cos((tx / 4.8) * (Math.PI * 0.5)) * 0.38;
            const bulbMat = Math.abs(Math.round(tx * 2)) % 2 === 0 ? marigoldMat : jasmineMat;
            const garland = new THREE.Mesh(new THREE.SphereGeometry(0.16, 8, 8), bulbMat);
            garland.position.set(tx, 6.12 - sag, 0);
            const leaf = new THREE.Mesh(new THREE.ConeGeometry(0.10, 0.28, 6), mangoLeafMat);
            leaf.position.set(tx + 0.42, 6.04 - sag, 0);
            leaf.rotation.x = Math.PI;
            gRow.add(garland, leaf);
          }
        }

        // Intimate Overhanging Rain-Tree Boughs shading the Old Bengaluru Gully
        if (segIdx % 3 === 1) {
          for (const side of [-1, 1]) {
            const canopy = new THREE.Mesh(new THREE.SphereGeometry(2.3, 12, 10), side < 0 ? treeLeafMat : gulmoharLeafMat);
            canopy.scale.set(1.35, 0.62, 1.25);
            canopy.position.set(side * 5.6, 7.6, 2.5);
            gRow.add(canopy);
          }
        }

        oldBlrGullyGroup.add(gRow);
        gullyScrollingRows.push(gRow);
      }

      // Heritage Old Bengaluru Bazaar Archway Landmarks (Chickpet & Malleshwaram)
      const gullyArches = [
        {
          zPos: -38,
          kn: 'ಚಿಕ್ಕಪೇಟೆ ಪೇಟೆ ದ್ವಾರ • ರೇಷ್ಮೆ ಬಜಾರ್',
          en: 'CHICKPET HERITAGE BAZAAR GATE'
        },
        {
          zPos: -195,
          kn: 'ಮಲ್ಲೇಶ್ವರಂ 8ನೇ ಅಡ್ಡರಸ್ತೆ • ಹೂವಿನ ಬಜಾರ್',
          en: 'MALLESHWARAM 8TH CROSS FLOWER MARKET'
        }
      ];
      gullyArches.forEach((cfg) => {
        const arch = new THREE.Group();
        const pillarGeo = new THREE.BoxGeometry(0.65, 6.8, 0.65);
        const pL = new THREE.Mesh(pillarGeo, mangaloreTileMat);
        pL.position.set(-5.15, 3.4, 0);
        const pR = new THREE.Mesh(pillarGeo, mangaloreTileMat);
        pR.position.set(5.15, 3.4, 0);
        const bannerTex = createHeritageArchBannerTexture(cfg.kn, cfg.en);
        const beam = new THREE.Mesh(
          new THREE.BoxGeometry(10.9, 1.95, 0.36),
          new THREE.MeshBasicMaterial({ map: bannerTex })
        );
        beam.position.set(0, 6.45, 0);
        arch.add(pL, pR, beam);
        arch.position.set(0, 0, cfg.zPos);
        oldBlrGullyGroup.add(arch);
        gullyLandmarkInstances.push({
          mesh: arch,
          kn: cfg.kn,
          type: cfg.en
        });
      });
    }
    buildOldBengaluruNarrowGullies();

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
        const w = 9.2;
        const h = 4.6;

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

        // Illuminated 2K HD Bilingual Ad Face
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
        g.rotation.y = isLeft ? 0.34 : -0.34;

        hoardingGroup.add(g);
        hoardingInstances.push(g);
      }
    }
    buildBilingualHoardings();

    // Dynamic Scrolling Bangalore Highway Landmarks (Silk Board Gantry, Vidhana Soudha, Metro)
    const highwayLandmarksGroup = new THREE.Group();
    scene.add(highwayLandmarksGroup);
    const landmarkInstances = [];
    let continuousMetroTrain = null;

    function spawnLandmarksFromGLB() {
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

        const frontBoard = new THREE.Mesh(new THREE.PlaneGeometry(19.4, 3.75), signMat);
        frontBoard.position.set(0, 8.85, 0.72);
        silk.add(frontBoard);

        const backBoard = new THREE.Mesh(new THREE.PlaneGeometry(19.4, 3.75), signMat);
        backBoard.position.set(0, 8.85, -0.72);
        backBoard.rotation.y = Math.PI;
        silk.add(backBoard);

        silk.position.set(0, 0, cfg.zPos);
        highwayLandmarksGroup.add(silk);
        landmarkInstances.push({
          mesh: silk,
          kn: cfg.kn,
          type: cfg.en
        });
      });

      for (const zPos of [-135, -315]) {
        const vidhana = loadedTemplates['vidhana_soudha.glb'].clone(true);
        vidhana.position.set(-32, 0, zPos);
        vidhana.rotation.y = Math.PI * 0.42;
        highwayLandmarksGroup.add(vidhana);
        landmarkInstances.push({
          mesh: vidhana,
          kn: 'ವಿಧಾನ ಸೌಧ • ಬೆಂಗಳೂರು',
          type: 'VIDHANA SOUDHA GRAND FACADE'
        });
      }

      const metro = loadedTemplates['metro_station.glb'].clone(true);
      metro.position.set(METRO_X, 0, -185);
      metro.traverse((child) => {
        if (child.name && child.name.startsWith('Metro_Train')) {
          continuousMetroTrain = child;
        }
      });
      if (continuousMetroTrain) {
        highwayLandmarksGroup.attach(continuousMetroTrain);
        continuousMetroTrain.position.set(METRO_X - 1.2, 0, -90);
      }
      highwayLandmarksGroup.add(metro);
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

      const activeLanes = getActiveLanes();
      const isGully = Boolean(currentProfile && currentProfile.isNarrowGully);

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
        if (isGully) g.scale.setScalar(0.76);

        const jitter = isGully ? 0.35 : 0.8;
        const laneX = activeLanes[Math.floor(Math.random() * activeLanes.length)] + (Math.random() - 0.5) * jitter;
        g.position.set(laneX, 0, -35 - i * (CORRIDOR_LENGTH / Math.max(1, count)));
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
    // 7. PLAYER AUTO-RICKSHAW (With HD Bilingual Rear Hood Decal & Grounded Physics)
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
      c.width = 1024;
      c.height = 320;
      const ctx = c.getContext('2d');
      ctx.fillStyle = '#111827';
      ctx.fillRect(0, 0, 1024, 320);
      ctx.strokeStyle = '#ffd000';
      ctx.lineWidth = 16;
      ctx.strokeRect(12, 12, 1000, 296);
      ctx.fillStyle = '#fde047';
      ctx.font = '900 84px "Noto Sans Kannada", "Inter", sans-serif';
      ctx.fillText('ನಮ್ಮ ಬೆಂಗಳೂರು • ಒಂದು ಸೆಕೆಂಡ್', 54, 136);
      ctx.fillStyle = '#4ade80';
      ctx.font = '900 60px "Inter", sans-serif';
      ctx.fillText('VAYUPUTRA RE • KA-01-AG-9999', 54, 248);
      return finalizeHDTexture(c);
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
      dlVerifiedTimer: 0,
      turboBoostTimer: 0,
      handbrakeLatched: false,
      cameraMode: 'chase', // 'chase' | 'dashcam'
      tripFinished: false,
      stats: {
        signalsObeyed: 0,
        signalsJumped: 0,
        copsCleared: 0,
        copsEvaded: 0,
        copsFined: 0,
        dogsDodged: 0,
        closeOvertakes: 0,
        collisions: 0,
        wheelsSnapped: 0
      }
    };

    function resetPlayerStatsAndTrip() {
      const isGully = Boolean(currentProfile && currentProfile.isNarrowGully);
      player.pos.set(isGully ? -1.45 : -1.9, 0, 0);
      player.vel.set(0, 0, 0);
      player.rot.set(0, 0, 0);
      player.forwardSpeed = (currentProfile && currentProfile.cruiseSpeed) || 32;
      player.distanceKm = 0;
      player.fareRupees = 30.0;
      player.wheelRepairTimer = 0;
      player.hornCooldown = 0;
      player.dlVerifiedTimer = 0;
      player.turboBoostTimer = 0;
      player.handbrakeLatched = false;
      player.tripFinished = false;
      player.stats = {
        signalsObeyed: 0,
        signalsJumped: 0,
        copsCleared: 0,
        copsEvaded: 0,
        copsFined: 0,
        dogsDodged: 0,
        closeOvertakes: 0,
        collisions: 0,
        wheelsSnapped: 0
      };
      updateBrakeButtonsUI();
    }

    function createPlayerAuto() {
      if (player.mesh) scene.remove(player.mesh);
      player.mesh = loadedTemplates['auto_rickshaw.glb'].clone(true);
      player.mesh.traverse((c) => {
        if (c.isMesh) {
          c.castShadow = true;
          c.receiveShadow = true;
        }
      });

      // Add HD Bilingual Kannada+English Stencil Plate on Rear Canopy Hood
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
        player.stats.wheelsSnapped++;
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
    // 7B. TWO-WAY GROUNDED LANE TRAFFIC POOL (6-Lane Highway + Narrow Gully)
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
        callouts: ['⚡ ZEPTO 10-MIN CUT-OFF!', '🟢 EXPRESS GROCERY WEAVE!', '💨 MOVE ANNA!']
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
        callouts: ['⚡ BLINKIT INSTANT CUT!', '🟡 10-MIN DELIVERY RUSH!']
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
      return Math.random() < 0.55 ? 'techie' : 'npc_auto';
    }

    function findFreeLaneAndZ(preferBehind = false, forceOncoming = null) {
      const activeLanes = getActiveLanes();
      const halfLanes = Math.floor(activeLanes.length / 2);
      const isGully = Boolean(currentProfile && currentProfile.isNarrowGully);
      const minXGap = isGully ? 1.45 : 2.2;

      for (let attempt = 0; attempt < 24; attempt++) {
        let laneIdx;
        if (forceOncoming === true) {
          laneIdx = halfLanes + Math.floor(Math.random() * halfLanes);
        } else if (forceOncoming === false) {
          laneIdx = Math.floor(Math.random() * halfLanes);
        } else {
          laneIdx = Math.floor(Math.random() * activeLanes.length);
        }
        const isOncoming = laneIdx >= halfLanes;
        const laneX = activeLanes[laneIdx];
        const z = (!isOncoming && preferBehind)
          ? 16 + Math.random() * 18
          : -32 - Math.random() * (CORRIDOR_LENGTH - 65);

        let clear = true;
        for (const other of trafficPool) {
          if (Math.abs(other.pos.x - laneX) < minXGap && Math.abs(other.pos.z - z) < 16.0) {
            clear = false;
            break;
          }
        }
        if (clear) return { laneIdx, laneX, z, isOncoming };
      }
      const fallbackLane =
        forceOncoming === true
          ? halfLanes
          : forceOncoming === false
            ? 0
            : Math.floor(Math.random() * activeLanes.length);
      return {
        laneIdx: fallbackLane,
        laneX: activeLanes[fallbackLane],
        z: -45 - Math.random() * (CORRIDOR_LENGTH - 75),
        isOncoming: fallbackLane >= halfLanes
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

    const GULLY_HERO_SLOTS = [
      { type: 'npc_auto', laneIdx: 0, z: -13.5 },
      { type: 'swiggy', laneIdx: 1, z: -23.0 },
      { type: 'npc_auto', laneIdx: 2, z: -15.5 },
      { type: 'zepto', laneIdx: 3, z: -11.5 },
      { type: 'techie', laneIdx: 2, z: -28.0 },
      { type: 'blinkit', laneIdx: 0, z: -31.5 }
    ];

    function spawnTrafficVehicle(slotIndex, totalSlots) {
      const activeLanes = getActiveLanes();
      const halfLanes = Math.floor(activeLanes.length / 2);
      const isGully = Boolean(currentProfile && currentProfile.isNarrowGully);
      const heroList = isGully ? GULLY_HERO_SLOTS : HERO_SLOTS;
      const hero = slotIndex < heroList.length ? heroList[slotIndex] : null;
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
      const laneIdx = hero ? hero.laneIdx : (slotIndex % activeLanes.length);
      const isOncoming = laneIdx >= halfLanes;
      const laneX = activeLanes[laneIdx];
      const rowIdx = Math.floor(slotIndex / activeLanes.length);
      const zOffset = hero ? hero.z : -30 - rowIdx * 24 - (slotIndex % 3) * 6;

      const speedScale = isGully ? 0.65 : 1.0;
      const baseSpeed = (spec.isHyperDelivery
        ? (28 + Math.random() * 10) * currentProfile.deliverySpeedMult
        : vKey === 'bmtc'
          ? 18 + Math.random() * 4
          : 22 + Math.random() * 6) * speedScale;

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

      const isGully = Boolean(currentProfile && currentProfile.isNarrowGully);
      const speedScale = isGully ? 0.65 : 1.0;
      const spawnBehind = !v.isOncoming && v.spec.isHyperDelivery && Math.random() < 0.35;
      const spot = findFreeLaneAndZ(spawnBehind, v.isOncoming);
      v.laneIdx = spot.laneIdx;
      v.isOncoming = spot.isOncoming;
      v.baseYaw = v.isOncoming ? Math.PI : 0;
      v.targetLaneX = spot.laneX;
      v.pos.set(spot.laneX, 0, spot.z);
      v.baseSpeed = (v.spec.isHyperDelivery
        ? (28 + Math.random() * 10) * currentProfile.deliverySpeedMult
        : v.type === 'bmtc'
          ? 18 + Math.random() * 4
          : 22 + Math.random() * 6) * speedScale;
      const targetVelZ = v.isOncoming ? v.baseSpeed * 0.42 : -v.baseSpeed;
      v.vel.set(0, 0, targetVelZ);
      v.rot.set(0, v.baseYaw, 0);
    }

    // =========================================================================
    // 7C. SUDDEN BENGALURU JAYWALKER PEDESTRIANS (Forward-Walking Orientation!)
    // =========================================================================
    const jaywalkers = [];
    const JAYWALKER_SHIRT_COLORS = [0xf97316, 0x06b6d4, 0xec4899, 0xeab308, 0x22c55e, 0xa855f7];
    const JAYWALKER_CALLOUTS = [
      '✋ "ಒಂದು ಸೆಕೆಂಡ್ ಅಣ್ಣ! ONDU SECOND!"',
      '🚶‍♂️ SUDDEN JAYWALKER ON ROAD!',
      '✋ "ಸ್ವಲ್ಪ ತಡೀರಿ! WAIT MAADI!"',
      '🛍️ BAZAAR SHOPPER CROSSING!'
    ];

    function getJaywalkerForwardYaw(dirX) {
      // In Three.js after Blender export_yup: +Y_blender (pedestrian nose, glasses, toes & stop-palm) -> -Z_threejs (0,0,-1).
      // Rotating (0,0,-1) around +Y by theta gives forward_x = -sin(theta), forward_z = -cos(theta).
      // Therefore dirX > 0 (+X travel) MUST use negative yaw (-0.54*PI) to face +X (+7 deg glance toward oncoming +Z),
      // and dirX < 0 (-X travel) MUST use positive yaw (+0.54*PI) to face -X!
      return dirX > 0 ? -Math.PI * 0.54 : Math.PI * 0.54;
    }

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

      const isGully = Boolean(currentProfile && currentProfile.isNarrowGully);
      const halfRoadW = getActiveRoadWidth() / 2;

      let startX, startZ, dirX, state;
      if (index === 0) {
        startX = isGully ? -1.1 : 0.6;
        startZ = -19.5;
        dirX = 1;
        state = 'crossing';
      } else if (index === 1) {
        startX = isGully ? 2.1 : 3.6;
        startZ = -34.0;
        dirX = -1;
        state = 'crossing';
      } else {
        dirX = index % 2 === 0 ? 1 : -1;
        startX = dirX > 0 ? (-halfRoadW - 0.75) : (halfRoadW + 0.75);
        startZ = -48 - (index - 1) * (CORRIDOR_LENGTH / Math.max(4, total));
        state = 'waiting';
      }

      const yaw = getJaywalkerForwardYaw(dirX);
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
        crossSpeed: (isGully ? 2.85 : 3.6) + (index % 3) * 0.55,
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
      const halfRoadW = getActiveRoadWidth() / 2;
      p.dirX = Math.random() < 0.5 ? 1 : -1;
      p.pos.x = p.dirX > 0 ? (-halfRoadW - 0.75) : (halfRoadW + 0.75);
      p.pos.y = 0;
      p.pos.z -= CORRIDOR_LENGTH + Math.random() * 25;
      p.state = 'waiting';
      p.speedBoost = 1.0;
      p.vy = 0;
      p.warned = false;
      p.triggerDist = 44 + Math.random() * 24;
      if (p.legL) p.legL.rotation.x = 0;
      if (p.legR) p.legR.rotation.x = 0;
      if (p.armL) p.armL.rotation.x = 0;
      p.mesh.rotation.set(0, getJaywalkerForwardYaw(p.dirX), 0);
    }

    // =========================================================================
    // 7D. BENGALURU TRAFFIC POLICE (BTP) SUDDEN LICENSE CHECK ("DL TORSI!")
    // =========================================================================
    const trafficCops = [];

    function createBtpBarricadeTexture() {
      const c = document.createElement('canvas');
      c.width = 1024;
      c.height = 512;
      const ctx = c.getContext('2d');
      ctx.fillStyle = '#1e3a8a';
      ctx.fillRect(0, 0, 1024, 512);
      ctx.strokeStyle = '#ffd000';
      ctx.lineWidth = 24;
      ctx.strokeRect(16, 16, 992, 480);
      ctx.fillStyle = '#fde047';
      ctx.font = '900 72px "Noto Sans Kannada", "Inter", sans-serif';
      ctx.fillText('ಬೆಂಗಳೂರು ಸಂಚಾರ ಪೊಲೀಸ್', 60, 164);
      ctx.fillStyle = '#ffffff';
      ctx.font = '900 60px "Inter", sans-serif';
      ctx.fillText('BENGALURU TRAFFIC POLICE', 56, 280);
      ctx.fillStyle = '#ef4444';
      ctx.fillRect(56, 330, 912, 124);
      ctx.fillStyle = '#ffffff';
      ctx.font = '900 60px "Inter", sans-serif';
      ctx.fillText('STOP • ನಿಲ್ಲಿಸಿ • DL & RC CHECK', 96, 414);
      return finalizeHDTexture(c);
    }

    const btpBarricadeTex = createBtpBarricadeTexture();
    const strobeRedMat = new THREE.MeshBasicMaterial({ color: 0xff1e42 });
    const strobeBlueMat = new THREE.MeshBasicMaterial({ color: 0x2563eb });

    function spawnTrafficCopCheckpost(index, total) {
      const group = new THREE.Group();
      const isGully = Boolean(currentProfile && currentProfile.isNarrowGully);
      const halfRoadW = getActiveRoadWidth() / 2;
      const activeLanes = getActiveLanes();

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
      if (isGully) barricade.scale.setScalar(0.76);
      barricade.position.set(isGully ? -1.1 : -1.75, 0, 0.5);
      group.add(barricade);

      // Place first cop ahead so player sees & experiences the BTP checkpost right away!
      const startZ = index === 0 ? -16.5 : -54 - index * (CORRIDOR_LENGTH / Math.max(2, total));
      const kerbX = -halfRoadW + (isGully ? 0.75 : 1.15);
      const targetLaneIdx = isGully ? 0 : (index === 0 ? 1 : (index % 2 === 0 ? 0 : 1));
      group.position.set(index === 0 ? activeLanes[targetLaneIdx] : kerbX, 0, startZ);
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
        targetX: activeLanes[targetLaneIdx],
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
      const isGully = Boolean(currentProfile && currentProfile.isNarrowGully);
      const activeLanes = getActiveLanes();
      cop.pos.z -= CORRIDOR_LENGTH + Math.random() * 30;
      cop.pos.x = cop.kerbX;
      cop.targetX = isGully ? activeLanes[0] : activeLanes[Math.floor(Math.random() * 2)];
      cop.state = 'waiting';
      cop.whistleBlown = false;
      cop.resolved = false;
      cop.copMesh.rotation.y = Math.PI;
      if (cop.legL) cop.legL.rotation.x = 0;
      if (cop.legR) cop.legR.rotation.x = 0;
    }

    // =========================================================================
    // 7E. SUDDEN DARTING BENGALURU STRAY DOGS (`stray_dog.glb`)
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

      const isGully = Boolean(currentProfile && currentProfile.isNarrowGully);
      const halfRoadW = getActiveRoadWidth() / 2;

      let dirX, startX, startZ, state;
      if (index === 0) {
        dirX = 1;
        startX = isGully ? -1.2 : -0.3;
        startZ = -10.2;
        state = 'darting';
      } else {
        dirX = index % 2 === 0 ? 1 : -1;
        startX = dirX > 0 ? (-halfRoadW - 0.9) : (halfRoadW + 0.9);
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
        runSpeed: (isGully ? 5.2 : 6.4) + (index % 3) * 0.9,
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
      const halfRoadW = getActiveRoadWidth() / 2;
      d.dirX = Math.random() < 0.5 ? 1 : -1;
      d.pos.x = d.dirX > 0 ? (-halfRoadW - 0.9) : (halfRoadW + 0.9);
      d.pos.y = 0;
      d.pos.z -= CORRIDOR_LENGTH + Math.random() * 25;
      d.state = 'waiting';
      d.speedBoost = 1.0;
      d.vy = 0;
      d.barked = false;
      d.hopBonusAwarded = false;
      d.triggerDist = 38 + Math.random() * 24;
      if (d.legFL) d.legFL.rotation.x = 0;
      if (d.legFR) d.legFR.rotation.x = 0;
      if (d.legRL) d.legRL.rotation.x = 0;
      if (d.legRR) d.legRR.rotation.x = 0;
      d.mesh.rotation.set(0, d.dirX > 0 ? -Math.PI * 0.48 : Math.PI * 0.48, 0);
    }

    // =========================================================================
    // 7F. BTP RED-LIGHT TRAFFIC SIGNAL JUNCTIONS (STOP ON RED, GO ON GREEN!)
    // =========================================================================
    const trafficSignals = [];
    const signalRedBulbMat = new THREE.MeshBasicMaterial({ color: 0xff2222 });
    const signalYellowBulbMat = new THREE.MeshBasicMaterial({ color: 0xffd000 });
    const signalGreenBulbMat = new THREE.MeshBasicMaterial({ color: 0x10f560 });
    const signalOffBulbMat = new THREE.MeshBasicMaterial({ color: 0x1e293b });
    const stopLineWhiteMat = new THREE.MeshBasicMaterial({ color: 0xffffff });
    const stopLineRedMat = new THREE.MeshBasicMaterial({ color: 0xef4444 });

    function createSignalSignageTexture() {
      const c = document.createElement('canvas');
      c.width = 1024;
      c.height = 384;
      const ctx = c.getContext('2d');
      ctx.fillStyle = '#0f172a';
      ctx.fillRect(0, 0, 1024, 384);
      ctx.strokeStyle = '#ffd000';
      ctx.lineWidth = 20;
      ctx.strokeRect(12, 12, 1000, 360);
      ctx.fillStyle = '#fde047';
      ctx.font = '900 68px "Noto Sans Kannada", "Inter", sans-serif';
      ctx.fillText('🚦 ಸಂಚಾರ ಸಿಗ್ನಲ್ • ನಿಲ್ಲಿಸಿ', 54, 132);
      ctx.fillStyle = '#ffffff';
      ctx.font = '900 52px "Inter", sans-serif';
      ctx.fillText('BTP SIGNAL • STOP ON RED [S / B]', 54, 236);
      ctx.fillStyle = '#4ade80';
      ctx.font = '800 44px "Inter", sans-serif';
      ctx.fillText('WAIT FOR GREEN [W] (+₹100 BONUS)', 54, 316);
      return finalizeHDTexture(c);
    }

    const signalSignageTex = createSignalSignageTexture();

    function spawnTrafficSignalJunction(index, total) {
      const group = new THREE.Group();
      const isGully = Boolean(currentProfile && currentProfile.isNarrowGully);
      const halfRoadW = getActiveRoadWidth() / 2;

      // 1. Thick Painted White Road Stop Line + Red Hazard Band across Forward Lanes
      const stopLineW = isGully ? 4.6 : 11.0;
      const stopLineX = isGully ? -2.35 : -5.6;
      const stopLine = new THREE.Mesh(new THREE.BoxGeometry(stopLineW, 0.028, 0.75), stopLineWhiteMat);
      stopLine.position.set(stopLineX, 0.015, 0);
      group.add(stopLine);

      const redStopBand = new THREE.Mesh(new THREE.BoxGeometry(stopLineW, 0.024, 0.45), stopLineRedMat);
      redStopBand.position.set(stopLineX, 0.014, 0.72);
      group.add(redStopBand);

      // Zebra stripes immediately ahead of the stop line
      const zGeo = new THREE.BoxGeometry(isGully ? 0.65 : 0.85, 0.025, 2.6);
      const zStart = isGully ? -4.2 : -10.2;
      const zStep = isGully ? 1.15 : 1.55;
      for (let zx = zStart; zx <= -0.6; zx += zStep) {
        const zs = new THREE.Mesh(zGeo, stopLineWhiteMat);
        zs.position.set(zx, 0.015, -2.1);
        group.add(zs);
      }

      // 2. Left Kerb Cantilever Signal Mast + Overhead Horizontal Boom Arm
      const mastX = -halfRoadW - (isGully ? 0.42 : 0.85);
      const mastH = isGully ? 5.8 : 6.8;
      const mast = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.20, mastH, 12), poleMetalMat);
      mast.position.set(mastX, mastH / 2, 0);
      group.add(mast);

      const boomW = isGully ? 4.8 : 8.6;
      const boomY = isGully ? 5.55 : 6.4;
      const boom = new THREE.Mesh(new THREE.BoxGeometry(boomW, 0.20, 0.20), poleMetalMat);
      boom.position.set(mastX + boomW * 0.48, boomY, 0);
      group.add(boom);

      // 3. HD Bilingual BTP Signal Instruction Board on Boom
      const signBoard = new THREE.Mesh(
        new THREE.BoxGeometry(isGully ? 3.2 : 4.4, isGully ? 1.15 : 1.55, 0.14),
        new THREE.MeshBasicMaterial({ map: signalSignageTex })
      );
      signBoard.position.set(isGully ? -2.9 : -5.8, boomY, 0.18);
      group.add(signBoard);

      // 4. Dual Signal Light Heads (Kerb Eye-Level Head + Overhead Cantilever Head)
      const housingMat = new THREE.MeshStandardMaterial({ color: 0x090d16, roughness: 0.4, metalness: 0.6 });
      const redBulbs = [];
      const yellowBulbs = [];
      const greenBulbs = [];

      const headPositions = isGully
        ? [
            { x: mastX, y: 3.4, z: 0.26, scale: 0.88 },
            { x: -1.15, y: 5.25, z: 0.24, scale: 1.05 }
          ]
        : [
            { x: mastX, y: 3.9, z: 0.26, scale: 1.0 },
            { x: -2.2, y: 6.1, z: 0.24, scale: 1.22 }
          ];

      for (const posCfg of headPositions) {
        const head = new THREE.Group();
        const box = new THREE.Mesh(new THREE.BoxGeometry(0.78, 2.15, 0.36), housingMat);
        head.add(box);

        const rBulb = new THREE.Mesh(new THREE.SphereGeometry(0.24, 14, 12), signalRedBulbMat);
        rBulb.position.set(0, 0.62, 0.18);
        const yBulb = new THREE.Mesh(new THREE.SphereGeometry(0.24, 14, 12), signalOffBulbMat);
        yBulb.position.set(0, 0.0, 0.18);
        const gBulb = new THREE.Mesh(new THREE.SphereGeometry(0.24, 14, 12), signalOffBulbMat);
        gBulb.position.set(0, -0.62, 0.18);

        head.add(rBulb, yBulb, gBulb);
        head.position.set(posCfg.x, posCfg.y, posCfg.z);
        head.scale.setScalar(posCfg.scale);
        group.add(head);

        redBulbs.push(rBulb);
        yellowBulbs.push(yBulb);
        greenBulbs.push(gBulb);
      }

      const startZ = index === 0 ? (isGully ? -62 : -78) : -78 - index * (CORRIDOR_LENGTH / Math.max(2, total));
      group.position.set(0, 0, startZ);
      scene.add(group);

      return {
        group,
        pos: group.position,
        redBulbs,
        yellowBulbs,
        greenBulbs,
        phase: 'red', // 'red' | 'yellow' | 'green'
        timer: 6.0,
        armedOnApproach: false,
        stoppedOnRed: false,
        bonusAwarded: false,
        violated: false
      };
    }

    function updateSignalBulbMaterials(sig) {
      const isR = sig.phase === 'red';
      const isY = sig.phase === 'yellow';
      const isG = sig.phase === 'green';
      sig.redBulbs.forEach((b) => {
        b.material = isR ? signalRedBulbMat : signalOffBulbMat;
        b.scale.setScalar(isR ? 1.25 : 0.92);
      });
      sig.yellowBulbs.forEach((b) => {
        b.material = isY ? signalYellowBulbMat : signalOffBulbMat;
        b.scale.setScalar(isY ? 1.25 : 0.92);
      });
      sig.greenBulbs.forEach((b) => {
        b.material = isG ? signalGreenBulbMat : signalOffBulbMat;
        b.scale.setScalar(isG ? 1.25 : 0.92);
      });
    }

    function rebuildTrafficSignals(count) {
      trafficSignals.forEach((s) => scene.remove(s.group));
      trafficSignals.length = 0;
      for (let i = 0; i < count; i++) {
        const sig = spawnTrafficSignalJunction(i, count);
        updateSignalBulbMaterials(sig);
        trafficSignals.push(sig);
      }
    }

    function resetTrafficSignalJunction(sig) {
      sig.pos.z -= CORRIDOR_LENGTH + 20 + Math.random() * 25;
      sig.phase = 'red';
      sig.timer = 6.0;
      sig.armedOnApproach = false;
      sig.stoppedOnRed = false;
      sig.bonusAwarded = false;
      sig.violated = false;
      updateSignalBulbMaterials(sig);
    }

    function triggerRedLightSignalAheadNow(autoBrake = false) {
      audio.init();
      if (trafficSignals.length === 0) return;
      const sig = trafficSignals[0];
      sig.pos.z = -16.5;
      sig.phase = 'red';
      sig.timer = 5.5;
      sig.armedOnApproach = true;
      sig.stoppedOnRed = false;
      sig.bonusAwarded = false;
      sig.violated = false;
      updateSignalBulbMaterials(sig);
      if (autoBrake) {
        player.handbrakeLatched = true;
        player.forwardSpeed = 0;
        updateBrakeButtonsUI();
      }
      spawnComicCallout(
        sig.pos,
        '🚦 ಕೆಂಪು ಸಿಗ್ನಲ್! RED SIGNAL AHEAD — PRESS [B] OR HOLD [S] TO STOP!',
        '#ef4444'
      );
    }

    // =========================================================================
    // 8. POOLED 60FPS COMIC CALLOUTS, LICENSE CHECK, BRAKE/START & TOUCH CONTROLS
    // =========================================================================
    const calloutLayer = document.getElementById('callout-layer');
    let lastCalloutTime = 0;
    const CALLOUT_POOL_SIZE = 8;
    const calloutPool = [];
    let calloutPoolIdx = 0;

    for (let i = 0; i < CALLOUT_POOL_SIZE; i++) {
      const el = document.createElement('div');
      el.className = 'comic-pop';
      el.style.display = 'none';
      calloutLayer.appendChild(el);
      calloutPool.push({ el, timerId: null });
    }

    function spawnComicCallout(worldPos, text, bgColor = '#ffd000') {
      const now = performance.now();
      if (now - lastCalloutTime < 180) return;
      lastCalloutTime = now;

      const proj = worldPos.clone().add(new THREE.Vector3(0, 2.0, 0)).project(camera);
      if (proj.z > 1) return;
      const x = (proj.x * 0.5 + 0.5) * window.innerWidth;
      const y = (-proj.y * 0.5 + 0.5) * window.innerHeight;

      const slot = calloutPool[calloutPoolIdx];
      calloutPoolIdx = (calloutPoolIdx + 1) % CALLOUT_POOL_SIZE;
      if (slot.timerId) clearTimeout(slot.timerId);

      const el = slot.el;
      el.style.display = 'none';
      void el.offsetWidth; // Restart CSS animation cleanly without DOM creation
      el.textContent = text;
      el.style.left = `${Math.min(window.innerWidth - 150, Math.max(150, x))}px`;
      el.style.top = `${Math.min(window.innerHeight - 95, Math.max(95, y))}px`;
      el.style.backgroundColor = bgColor;
      el.style.display = 'block';

      slot.timerId = setTimeout(() => {
        el.style.display = 'none';
      }, 1220);
    }

    function updateBrakeButtonsUI() {
      const isBraking = Boolean(player.handbrakeLatched);
      const hbBtn = document.getElementById('btn-handbrake');
      if (hbBtn) {
        hbBtn.textContent = isBraking ? '🟢 Start [W/B]' : '🛑 Brake [B]';
        hbBtn.classList.toggle('active-mode', isBraking);
      }
      const tBrake = document.getElementById('tbtn-brake');
      const tBrakeLabel = document.getElementById('tbtn-brake-label');
      if (tBrake) tBrake.classList.toggle('active-brake', isBraking);
      if (tBrakeLabel) tBrakeLabel.textContent = isBraking ? '🛑 STOPPED' : '🛑 STOP';

      const sigBtn = document.getElementById('btn-sig-brake-start');
      if (sigBtn) {
        sigBtn.textContent = isBraking ? '🟢 GO / START [W]' : '🛑 STOP [B]';
        sigBtn.style.background = isBraking ? '#4ade80' : '#ffd000';
      }
    }

    function toggleHandbrakeStop() {
      audio.init();
      player.handbrakeLatched = !player.handbrakeLatched;
      updateBrakeButtonsUI();
      if (player.handbrakeLatched) {
        spawnComicCallout(player.pos, '🛑 HANDBRAKE APPLIED — STOPPING AUTO (PRESS [W] TO START)', '#ef4444');
      } else {
        spawnComicCallout(player.pos, '🟢 BRAKE RELEASED — VAYUPUTRA RE MOVING!', '#4ade80');
      }
    }

    function releaseBrakeAndStartMoving() {
      audio.init();
      if (player.handbrakeLatched) {
        player.handbrakeLatched = false;
        updateBrakeButtonsUI();
      }
      if (player.forwardSpeed < 12) {
        player.forwardSpeed = currentProfile && currentProfile.isNarrowGully ? 14 : 18;
      }
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
          player.stats.copsCleared++;
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
      const isGully = Boolean(currentProfile && currentProfile.isNarrowGully);
      const spotX = isGully ? -2.4 : -3.8;
      const cop = trafficCops[0];
      cop.pos.z = -12.5;
      cop.pos.x = spotX;
      cop.targetX = spotX;
      cop.copMesh.rotation.y = Math.PI;
      cop.state = 'stepping_out';
      cop.whistleBlown = true;
      cop.resolved = false;
      audio.playPoliceWhistle(false);
      document.getElementById('hud-cop-alert').classList.add('visible');
      document.getElementById('vignette-fx').classList.add('cop-strobe');
      spawnComicCallout(cop.pos, '👮‍♂️ "ಏಯ್ ಆಟೋ! ಸೈಡ್ ಹಾಕಿ! DL ತೋರಿಸಿ!" [PRESS L]', '#ef4444');
    }

    // User-Configurable Camera View: 'chase' (3rd Person) vs 'dashcam' (Inside Auto Cockpit POV)
    function setCameraMode(mode, showCallout = false) {
      player.cameraMode = mode === 'dashcam' ? 'dashcam' : 'chase';
      const isDash = player.cameraMode === 'dashcam';

      const overlay = document.getElementById('dashcam-overlay');
      if (overlay) overlay.classList.toggle('active', isDash);

      if (player.mesh) {
        player.mesh.visible = !isDash;
      }

      const camBtn = document.getElementById('btn-camera-toggle');
      if (camBtn) {
        camBtn.textContent = isDash ? '🛺 View: Dash Cam [V]' : '🎥 View: Chase [V]';
        camBtn.classList.toggle('active-mode', isDash);
      }

      const altBadge = document.getElementById('hud-alt');
      if (altBadge) {
        altBadge.textContent = isDash ? '🛺 DASH CAM POV' : '🎥 CHASE VIEW';
      }

      document.querySelectorAll('[data-set-cam]').forEach((btn) => {
        btn.classList.toggle('active-cam', btn.dataset.setCam === player.cameraMode);
      });

      camera.fov = isDash ? 66 : 58;
      camera.updateProjectionMatrix();

      if (showCallout) {
        spawnComicCallout(
          player.pos,
          isDash ? '🛺 VAYUPUTRA RE DASH CAM VIEW (COCKPIT POV)' : '🎥 REGULAR CHASE CAMERA VIEW',
          '#38bdf8'
        );
      }
    }

    function toggleCameraMode() {
      setCameraMode(player.cameraMode === 'chase' ? 'dashcam' : 'chase', true);
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
          releaseBrakeAndStartMoving();
          break;
        case 'KeyS':
        case 'ArrowDown':
          keys.down = true;
          updateBrakeButtonsUI();
          break;
        case 'KeyB':
          toggleHandbrakeStop();
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
          releaseBrakeAndStartMoving();
          if (!keys.space && player.turboBoostTimer <= 0) {
            player.turboBoostTimer = 1.6;
            audio.playBeepBeepHorn('auto');
            spawnComicCallout(player.pos, '⚡ VAYUPUTRA TURBO GAP BOOST! (GROUNDED)', '#38bdf8');
          }
          keys.space = true;
          break;
        case 'KeyV':
          toggleCameraMode();
          break;
        case 'KeyG':
          triggerRedLightSignalAheadNow(false);
          break;
        case 'KeyE':
          if (!gamePaused) {
            finishTripAndShowScoreboard('Meter Stopped by Driver');
          }
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
          updateBrakeButtonsUI();
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

    // Wire On-Screen Touch / Mouse Controls for Mobile, Tablet & Desktop Clickers
    function bindHoldButton(btnId, onDown, onUp) {
      const btn = document.getElementById(btnId);
      if (!btn) return;
      const start = (ev) => {
        ev.preventDefault();
        audio.init();
        btn.classList.add('pressed');
        onDown();
      };
      const end = (ev) => {
        ev.preventDefault();
        btn.classList.remove('pressed');
        if (onUp) onUp();
      };
      btn.addEventListener('pointerdown', start);
      btn.addEventListener('pointerup', end);
      btn.addEventListener('pointerleave', end);
      btn.addEventListener('pointercancel', end);
    }

    bindHoldButton('tbtn-left', () => { keys.left = true; }, () => { keys.left = false; });
    bindHoldButton('tbtn-right', () => { keys.right = true; }, () => { keys.right = false; });
    bindHoldButton(
      'tbtn-brake',
      () => {
        keys.down = true;
        player.handbrakeLatched = true;
        updateBrakeButtonsUI();
      },
      () => {
        keys.down = false;
      }
    );
    bindHoldButton(
      'tbtn-go',
      () => {
        keys.up = true;
        releaseBrakeAndStartMoving();
      },
      () => {
        keys.up = false;
      }
    );
    document.getElementById('tbtn-horn')?.addEventListener('click', () => triggerPlayerHorn());
    document.getElementById('tbtn-dl')?.addEventListener('click', () => flashDigiLockerLicenseToCop());
    document.getElementById('btn-handbrake')?.addEventListener('click', () => toggleHandbrakeStop());
    document.getElementById('btn-signal-test')?.addEventListener('click', () => triggerRedLightSignalAheadNow(false));
    document.getElementById('btn-sig-brake-start')?.addEventListener('click', () => {
      if (player.handbrakeLatched || player.forwardSpeed < 3) {
        releaseBrakeAndStartMoving();
      } else {
        player.handbrakeLatched = true;
        updateBrakeButtonsUI();
      }
    });

    function triggerPlayerHorn() {
      if (player.hornCooldown > 0) return;
      player.hornCooldown = 0.28;
      audio.init();
      audio.playBeepBeepHorn('auto');
      spawnComicCallout(player.pos, '📯 ಪಾ-ಪಾ-ಪಾರ್ಪ್! ಸೈಡ್ ಕೊಡಿ! (SIDE KODI!)', '#ffd000');

      const activeLanes = getActiveLanes();
      const halfLanes = Math.floor(activeLanes.length / 2);
      const shiftStep = currentProfile && currentProfile.isNarrowGully ? 1.7 : 3.8;

      // Same-direction vehicles ahead yield slightly when honked at
      trafficPool.forEach((v) => {
        const dz = Math.abs(v.pos.z - player.pos.z);
        const dx = v.pos.x - player.pos.x;
        if (!v.isOncoming && dz < 16 && Math.abs(dx) < 4.5 && v.type !== 'bmtc') {
          const shiftDir = dx >= 0 ? 1 : -1;
          v.targetLaneX = THREE.MathUtils.clamp(
            v.targetLaneX + shiftDir * shiftStep,
            activeLanes[0],
            activeLanes[halfLanes - 1]
          );
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

    // Weather, Modal, Local Leaderboard & End-of-Trip Viral Receipt Controls
    let rainActive = false;
    let rainIntensity = 0.0;
    let weatherTimer = 14.0;
    let lastCompletedTripSummary = null;

    function toggleManualRainStorm() {
      rainActive = !rainActive;
      weatherTimer = rainActive ? currentProfile.rainStormDuration : currentProfile.rainCycleDuration;
      updateWeatherBanner();
    }

    function updateWeatherBanner() {
      document.getElementById('hud-weather-alert').classList.toggle('visible', rainActive);
    }

    const modal = document.getElementById('gravity-modal');
    const scoreModal = document.getElementById('score-modal');
    let gamePaused = true;

    const LEADERBOARD_KEY = 'blr_vayuputra_leaderboard_v1';

    function saveAndRenderLeaderboard(newEntry) {
      let list = [];
      try {
        const raw = localStorage.getItem(LEADERBOARD_KEY);
        if (raw) list = JSON.parse(raw);
      } catch (_) {}

      if (newEntry) {
        list.push(newEntry);
        list.sort((a, b) => b.score - a.score);
        list = list.slice(0, 5);
        try {
          localStorage.setItem(LEADERBOARD_KEY, JSON.stringify(list));
        } catch (_) {}
      }

      const container = document.getElementById('score-leaderboard-list');
      if (!container) return;
      if (list.length === 0) {
        container.innerHTML = '<span class="lb-pill">No trips recorded yet</span>';
        return;
      }
      container.innerHTML = list
        .map(
          (item, idx) =>
            `<span class="lb-pill">#${idx + 1} ${item.score.toLocaleString()} PTS • ₹${item.fare.toFixed(0)} (${item.mode.toUpperCase()})</span>`
        )
        .join('');
    }

    function updateTripProgressHUD() {
      const targetKm = currentProfile.targetDistanceKm || 1.8;
      const pct = Math.min(100, Math.round((player.distanceKm / targetKm) * 100));
      document.documentElement.style.setProperty('--trip-pct', `${pct}%`);
      const titleEl = document.getElementById('hud-trip-title');
      if (titleEl) titleEl.textContent = `🏁 ${currentProfile.routeTitle}`;
      const pctEl = document.getElementById('hud-trip-pct');
      if (pctEl) pctEl.textContent = `${pct}%`;
      const distEl = document.getElementById('hud-dist');
      if (distEl) distEl.textContent = `${player.distanceKm.toFixed(2)} / ${targetKm.toFixed(1)} KM`;
    }

    function finishTripAndShowScoreboard(reason = 'Destination Reached!') {
      player.tripFinished = true;
      gamePaused = true;
      audio.init();
      audio.playLicenseVerified();

      const targetKm = currentProfile.targetDistanceKm || 1.8;
      const distPts = Math.round(player.distanceKm * 600);
      const farePts = Math.round(player.fareRupees * 3.5);
      const sigPts = player.stats.signalsObeyed * 250;
      const copPts = player.stats.copsCleared * 300 + player.stats.copsEvaded * 150;
      const dogPts = player.stats.dogsDodged * 200 + player.stats.closeOvertakes * 80;
      const penaltyPts =
        player.stats.collisions * 75 +
        player.stats.copsFined * 250 +
        player.stats.signalsJumped * 300;
      const totalScore = Math.max(150, distPts + farePts + sigPts + copPts + dogPts - penaltyPts);

      let rankText = '🏆 S-RANK • ನಮ್ಮ ಆಟೋ ರಾಜ (BENGALURU AUTO LEGEND)';
      if (totalScore < 1400) {
        rankText = '🥉 B-RANK • SILK BOARD SURVIVOR (ಸಂಚಾರ ವೀರ)';
      } else if (totalScore < 2200) {
        rankText = '🥇 A-RANK • INDIRANAGAR METER BOSS (ಮೀಟರ್ ಬಾಸ್)';
      }

      lastCompletedTripSummary = {
        routeTitle: currentProfile.routeTitle,
        mode: currentProfile.id,
        reason,
        distanceKm: player.distanceKm,
        targetKm,
        fare: player.fareRupees,
        score: totalScore,
        rankText,
        distPts,
        farePts,
        sigPts,
        copPts,
        dogPts,
        penaltyPts,
        stats: { ...player.stats }
      };

      saveAndRenderLeaderboard({
        score: totalScore,
        fare: player.fareRupees,
        mode: currentProfile.id,
        ts: Date.now()
      });

      document.getElementById('score-route-badge').textContent =
        `🏁 ${currentProfile.routeTitle} • ${reason.toUpperCase()}`;
      document.getElementById('score-total-pts').textContent = `${totalScore.toLocaleString()} PTS`;
      document.getElementById('score-rank-badge').textContent = rankText;
      document.getElementById('score-total-fare').textContent = `₹${player.fareRupees.toFixed(2)}`;
      document.getElementById('score-dist-summary').textContent =
        `Trip Distance: ${player.distanceKm.toFixed(2)} / ${targetKm.toFixed(1)} KM • View: ${player.cameraMode.toUpperCase()}`;

      const tbody = document.getElementById('score-breakdown-body');
      tbody.innerHTML = `
        <tr>
          <td>🛣️ Route Distance Completed (${currentProfile.routeTitle})</td>
          <td>${player.distanceKm.toFixed(2)} / ${targetKm.toFixed(1)} KM</td>
          <td class="pts-pos">+${distPts} PTS</td>
        </tr>
        <tr>
          <td>📟 Vayuputra RE Meter Fare (${currentProfile.fareRateMult.toFixed(1)}x Rate)</td>
          <td>₹${player.fareRupees.toFixed(2)} Collected</td>
          <td class="pts-pos">+${farePts} PTS</td>
        </tr>
        <tr>
          <td>🚦 BTP Red-Light Signal Discipline</td>
          <td>${player.stats.signalsObeyed} Stopped on Red • ${player.stats.signalsJumped} Jumped</td>
          <td class="${sigPts >= player.stats.signalsJumped * 300 ? 'pts-pos' : 'pts-neg'}">+${sigPts} PTS</td>
        </tr>
        <tr>
          <td>👮‍♂️ BTP Traffic Cop License Checks</td>
          <td>${player.stats.copsCleared} DL Verified • ${player.stats.copsEvaded} Dodged</td>
          <td class="pts-pos">+${copPts} PTS</td>
        </tr>
        <tr>
          <td>🐕 Indie Stray Dogs &amp; Traffic Overtakes</td>
          <td>${player.stats.dogsDodged} Dogs Dodged • ${player.stats.closeOvertakes} Overtakes</td>
          <td class="pts-pos">+${dogPts} PTS</td>
        </tr>
        <tr>
          <td>💥 Traffic Bumps &amp; e-Challan Penalties</td>
          <td>${player.stats.collisions} Bumps • ${player.stats.copsFined + player.stats.signalsJumped} Challans</td>
          <td class="${penaltyPts > 0 ? 'pts-neg' : 'pts-pos'}">${penaltyPts > 0 ? '-' + penaltyPts : '0 (CLEAN!)'} PTS</td>
        </tr>
      `;

      document.getElementById('hud-cop-alert').classList.remove('visible');
      document.getElementById('hud-signal-banner').classList.remove('visible');
      document.getElementById('vignette-fx').classList.remove('cop-strobe');

      if (modal.open) modal.close();
      if (!scoreModal.open) scoreModal.showModal();
      scoreModal.scrollTop = 0;
    }

    // Generate & Download Viral Shareable Namma Auto Thermal Fare Receipt PNG
    function downloadTripReceiptPng() {
      const s = lastCompletedTripSummary || {
        routeTitle: currentProfile.routeTitle,
        distanceKm: player.distanceKm,
        targetKm: currentProfile.targetDistanceKm,
        fare: player.fareRupees,
        score: 2550,
        rankText: '🏆 S-RANK • ನಮ್ಮ ಆಟೋ ರಾಜ (BENGALURU AUTO LEGEND)',
        stats: player.stats
      };

      const c = document.createElement('canvas');
      c.width = 800;
      c.height = 980;
      const ctx = c.getContext('2d');

      // Outer Dark Charcoal & Auto Canary Yellow Border
      ctx.fillStyle = '#090d16';
      ctx.fillRect(0, 0, 800, 980);
      ctx.strokeStyle = '#ffd000';
      ctx.lineWidth = 14;
      ctx.strokeRect(18, 18, 764, 944);

      // Top Hazard Banner
      ctx.fillStyle = '#ffd000';
      ctx.fillRect(34, 34, 732, 86);
      ctx.fillStyle = '#090d16';
      ctx.font = '900 32px "Noto Sans Kannada", "Inter", sans-serif';
      ctx.fillText('🛺 ನಮ್ಮ ಬೆಂಗಳೂರು ಆಟೋ ಮೀಟರ್ ರಸೀದಿ • KA-01', 56, 74);
      ctx.font = '900 20px "Inter", sans-serif';
      ctx.fillText('VAYUPUTRA RE COMPACT (ವಾಯುಪುತ್ರ) • OFFICIAL DRIVER SCORE CARD', 56, 105);

      // Route & Vehicle Info Box
      ctx.fillStyle = '#111827';
      ctx.fillRect(42, 142, 716, 130);
      ctx.strokeStyle = 'rgba(255, 208, 0, 0.4)';
      ctx.lineWidth = 2;
      ctx.strokeRect(42, 142, 716, 130);

      ctx.fillStyle = '#fde047';
      ctx.font = '900 28px "Inter", sans-serif';
      ctx.fillText(`ROUTE: ${s.routeTitle}`, 64, 188);
      ctx.fillStyle = '#cbd5e1';
      ctx.font = '700 21px "Inter", monospace';
      ctx.fillText(`VEHICLE: KA-01-AG-9999 (VAYUPUTRA RE) • DIST: ${s.distanceKm.toFixed(2)}/${s.targetKm.toFixed(1)} KM`, 64, 226);
      ctx.fillStyle = '#38bdf8';
      ctx.font = '800 20px "Inter", sans-serif';
      ctx.fillText(s.rankText, 64, 256);

      // Hero Score & Meter Fare Blocks
      ctx.fillStyle = '#052e16';
      ctx.fillRect(42, 292, 348, 140);
      ctx.strokeStyle = '#4ade80';
      ctx.strokeRect(42, 292, 348, 140);
      ctx.fillStyle = '#86efac';
      ctx.font = '800 18px "Inter", sans-serif';
      ctx.fillText('FINAL METER FARE COLLECTED', 64, 328);
      ctx.fillStyle = '#4ade80';
      ctx.font = '900 58px "Inter", monospace';
      ctx.fillText(`₹${s.fare.toFixed(2)}`, 64, 402);

      ctx.fillStyle = '#1e1b4b';
      ctx.fillRect(410, 292, 348, 140);
      ctx.strokeStyle = '#ffd000';
      ctx.strokeRect(410, 292, 348, 140);
      ctx.fillStyle = '#fde047';
      ctx.font = '800 18px "Inter", sans-serif';
      ctx.fillText('FINAL DRIVER SCORE', 432, 328);
      ctx.fillStyle = '#ffffff';
      ctx.font = '900 58px "Inter", monospace';
      ctx.fillText(`${s.score.toLocaleString()} PTS`, 432, 402);

      // Itemized Breakdown Rows
      const rows = [
        ['🚦 Red-Light Signals Obeyed', `${s.stats.signalsObeyed} Stopped (+₹${s.stats.signalsObeyed * 100})`],
        ['👮‍♂️ BTP License Checks Cleared', `${s.stats.copsCleared} Verified • ${s.stats.copsEvaded} Dodged`],
        ['🐕 Indie Stray Dogs Dodged', `${s.stats.dogsDodged} Clean Swerves`],
        ['⚡ Close Traffic Overtakes', `${s.stats.closeOvertakes} Vehicles Passed`],
        ['💥 Bumps & e-Challan Fines', `${s.stats.collisions} Bumps • ${s.stats.copsFined + s.stats.signalsJumped} Challans`]
      ];

      let ry = 485;
      rows.forEach(([label, val]) => {
        ctx.fillStyle = '#1e293b';
        ctx.fillRect(42, ry - 34, 716, 56);
        ctx.fillStyle = '#f8fafc';
        ctx.font = '800 23px "Inter", sans-serif';
        ctx.fillText(label, 64, ry);
        ctx.fillStyle = '#fde047';
        ctx.textAlign = 'right';
        ctx.fillText(val, 736, ry);
        ctx.textAlign = 'left';
        ry += 72;
      });

      // Footer Challenge Call to Action
      ctx.fillStyle = '#ffd000';
      ctx.font = '900 24px "Noto Sans Kannada", "Inter", sans-serif';
      ctx.fillText('ಒಂದು ಸೆಕೆಂಡ್ | ONDU SECOND: BENGALURU TRAFFIC PRO', 42, 885);
      ctx.fillStyle = '#94a3b8';
      ctx.font = '700 18px "Inter", monospace';
      ctx.fillText('Built with Google Antigravity & Gemini • github.com/cmanikandan/blr-traffic-blender', 42, 922);

      const link = document.createElement('a');
      link.download = `vayuputra-auto-receipt-${s.score}pts.png`;
      link.href = c.toDataURL('image/png');
      link.click();
    }

    async function shareTripScoreText() {
      const s = lastCompletedTripSummary || {
        routeTitle: currentProfile.routeTitle,
        fare: player.fareRupees,
        score: 2550,
        stats: player.stats
      };
      const shareText =
        `🛺 I scored ${s.score.toLocaleString()} PTS (Meter Fare ₹${s.fare.toFixed(2)}) driving the Vayuputra RE Auto on ${s.routeTitle} in Ondu Second: Bengaluru Traffic Pro! ` +
        `🚦 ${s.stats.signalsObeyed} Red Lights Obeyed • 👮‍♂️ ${s.stats.copsCleared} BTP Checks Cleared • 🐕 ${s.stats.dogsDodged} Stray Dogs Dodged! ` +
        `Can you beat my meter? https://github.com/cmanikandan/blr-traffic-blender`;

      const shareBtn = document.getElementById('btn-share-score');
      if (navigator.share) {
        try {
          await navigator.share({ title: 'Ondu Second: Vayuputra RE Auto Score', text: shareText });
          return;
        } catch (_) {}
      }
      try {
        await navigator.clipboard.writeText(shareText);
        if (shareBtn) {
          const orig = shareBtn.textContent;
          shareBtn.textContent = '✅ Copied Challenge to Clipboard!';
          setTimeout(() => { shareBtn.textContent = orig; }, 2200);
        }
      } catch (_) {}
    }

    function applyGravityProfile(modeKey, closeDialog = true) {
      currentProfile = GRAVITY_PROFILES[modeKey] || GRAVITY_PROFILES.medium;
      const isGully = Boolean(currentProfile.isNarrowGully);

      document.querySelectorAll('[data-quick-mode]').forEach((btn) => {
        btn.classList.toggle('active-mode', btn.dataset.quickMode === modeKey);
      });
      document.querySelectorAll('.mode-card').forEach((card) => {
        card.classList.toggle('selected', card.dataset.mode === modeKey);
      });

      // Toggle 6-Lane Tech Corridor Highway vs Narrow Old Bengaluru Heritage Gullies (0.5 KM)
      oldBlrGullyGroup.visible = isGully;
      hoardingGroup.visible = !isGully;
      highwayLandmarksGroup.visible = !isGully;
      highwayOnlyObjects.forEach((obj) => {
        obj.visible = !isGully;
      });
      roadMesh.scale.x = isGully ? (GULLY_ROAD_WIDTH / ROAD_WIDTH) : 1.0;

      const nhShieldEl = document.querySelector('.nh-shield');
      if (nhShieldEl) {
        nhShieldEl.textContent = currentProfile.shieldCode || (isGully ? 'BLR 02' : 'NH 44');
      }

      resetPlayerStatsAndTrip();
      rebuildPotholes(currentProfile.potholeCount);
      rebuildTrafficForProfile(currentProfile);
      rebuildTrafficSignals(currentProfile.signalCount || 2);
      rebuildJaywalkers(currentProfile.jaywalkerCount);
      rebuildTrafficCops(currentProfile.copCount);
      rebuildStrayDogs(currentProfile.dogCount);
      reattachAllPlayerWheels();
      setCameraMode(player.cameraMode, false);
      updateTripProgressHUD();

      rainActive = false;
      rainIntensity = 0.0;
      weatherTimer = currentProfile.rainCycleDuration;
      updateWeatherBanner();
      document.getElementById('hud-cop-alert').classList.remove('visible');
      document.getElementById('hud-signal-banner').classList.remove('visible');
      document.getElementById('vignette-fx').classList.remove('cop-strobe');

      if (scoreModal && scoreModal.open) {
        scoreModal.close();
      }
      if (closeDialog && modal.open) {
        modal.close();
      }
      gamePaused = false;
      audio.init();
    }

    function toggleGravityModal() {
      if (scoreModal && scoreModal.open) {
        scoreModal.close();
      }
      if (modal.open) {
        modal.close();
        gamePaused = false;
      } else {
        modal.showModal();
        gamePaused = true;
      }
    }

    modal.addEventListener('close', () => {
      if (!scoreModal.open) {
        gamePaused = false;
      }
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

    document.querySelectorAll('[data-set-cam]').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        setCameraMode(btn.dataset.setCam, false);
      });
    });

    document.getElementById('btn-camera-toggle').addEventListener('click', () => toggleCameraMode());
    document.getElementById('btn-end-trip').addEventListener('click', () => {
      finishTripAndShowScoreboard('Meter Stopped by Driver');
    });
    document.getElementById('btn-download-receipt')?.addEventListener('click', () => downloadTripReceiptPng());
    document.getElementById('btn-share-score')?.addEventListener('click', () => shareTripScoreText());
    document.getElementById('btn-score-replay').addEventListener('click', () => {
      applyGravityProfile(currentProfile.id, true);
    });
    document.getElementById('btn-score-switch-cam').addEventListener('click', () => {
      setCameraMode(player.cameraMode === 'chase' ? 'dashcam' : 'chase', false);
      applyGravityProfile(currentProfile.id, true);
    });
    document.getElementById('btn-score-menu').addEventListener('click', () => {
      if (scoreModal.open) scoreModal.close();
      modal.showModal();
      gamePaused = true;
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
    // 9. SIMULATION, STRICT GROUNDED TRAFFIC, RED-LIGHT SIGNALS, BTP COPS & STRAY DOGS
    // =========================================================================
    let cameraShake = 0;
    const clock = new THREE.Clock();

    // Cached HUD DOM references for 60 FPS zero-overhead updates
    const hudEls = {
      dlStatus: document.getElementById('hud-dl-status'),
      gripText: document.getElementById('hud-grip-text'),
      landmark: document.getElementById('hud-landmark'),
      landmarkKn: document.getElementById('hud-landmark-kn'),
      copAlert: document.getElementById('hud-cop-alert'),
      vignette: document.getElementById('vignette-fx'),
      fare: document.getElementById('hud-fare'),
      surge: document.getElementById('surge-badge'),
      speed: document.getElementById('hud-speed'),
      sigBanner: document.getElementById('hud-signal-banner'),
      sigRed: document.getElementById('hud-sig-red'),
      sigYellow: document.getElementById('hud-sig-yellow'),
      sigGreen: document.getElementById('hud-sig-green'),
      sigKn: document.getElementById('hud-sig-kn'),
      sigEn: document.getElementById('hud-sig-en'),
      sigTimer: document.getElementById('hud-sig-timer')
    };

    function updateSimulation(dt, elapsed) {
      if (player.tripFinished) return;

      const isGully = Boolean(currentProfile.isNarrowGully);
      const activeRoadW = getActiveRoadWidth();
      const halfRoadW = activeRoadW / 2;
      const activeLanes = getActiveLanes();
      const halfLanes = Math.floor(activeLanes.length / 2);

      if (player.hornCooldown > 0) player.hornCooldown -= dt;
      if (player.turboBoostTimer > 0) player.turboBoostTimer -= dt;
      if (player.dlVerifiedTimer > 0) {
        player.dlVerifiedTimer -= dt;
        if (player.dlVerifiedTimer <= 0) {
          hudEls.dlStatus.textContent = 'VALID • PRESS [L]';
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
      const baseDrySky = isGully ? gullySkyColor : drySkyColor;
      scene.background.lerpColors(baseDrySky, rainSkyColor, rainIntensity);
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
      hudEls.gripText.textContent =
        gripPct < 15 ? '0% HYDROPLANING!' : `${gripPct}% DRY ASPHALT`;

      // 2. Vayuputra RE Strictly Grounded Physics + Full 0 KM/H Stop & Start Controls!
      const isBrakingToStop = keys.down || player.handbrakeLatched;
      const cruiseSpeed = currentProfile.cruiseSpeed || 32;
      let targetSpeed = cruiseSpeed;
      if (isBrakingToStop) {
        targetSpeed = 0;
      } else if (player.turboBoostTimer > 0) {
        targetSpeed = isGully ? 36 : 56;
      } else if (keys.up) {
        targetSpeed = isGully ? 29 : 48;
      }
      const accelRate = isBrakingToStop ? 7.2 : 4.2;
      player.forwardSpeed += (targetSpeed - player.forwardSpeed) * Math.min(1, dt * accelRate);
      if (player.forwardSpeed < 0.35 && isBrakingToStop) {
        player.forwardSpeed = 0;
      }
      player.distanceKm += (player.forwardSpeed * dt) / 1000;

      const steerInput = (keys.right ? 1 : 0) - (keys.left ? 1 : 0);
      const attachedWheelCount = player.wheels.filter((w) => w.attached).length;
      const wheelStability = 0.45 + 0.55 * (attachedWheelCount / 3);
      const speedSteerFactor = Math.min(1.0, 0.25 + player.forwardSpeed / 24);

      const steerAccel = ((isGully ? 19 : 24) + (1 - tireGrip) * 8) * wheelStability * speedSteerFactor;
      player.vel.x += steerInput * steerAccel * dt;

      if (attachedWheelCount < 3) {
        player.wheelRepairTimer -= dt;
        if (player.wheelRepairTimer <= 0) reattachAllPlayerWheels();
      }

      const lateralFrictionDamping = 0.65 + tireGrip * 5.5;
      player.vel.x *= Math.exp(-lateralFrictionDamping * dt);

      // Keep Auto strictly planted on the asphalt road (pos.y = 0 always)
      player.pos.x += player.vel.x * dt;
      player.pos.y = 0;
      player.vel.y = 0;

      const maxRoadX = halfRoadW - (isGully ? 0.92 : 1.1);
      if (Math.abs(player.pos.x) > maxRoadX) {
        player.pos.x = Math.sign(player.pos.x) * maxRoadX;
        player.vel.x = -player.vel.x * 0.6;
      }

      const missingWheelTilt = (3 - attachedWheelCount) * 0.10;
      const targetPitch = THREE.MathUtils.clamp(
        (keys.up || player.turboBoostTimer > 0 ? -0.025 : isBrakingToStop && player.forwardSpeed > 2 ? 0.045 : 0),
        -0.12,
        0.12
      );
      const targetYaw = THREE.MathUtils.clamp(-steerInput * 0.10 - player.vel.x * 0.012, -0.32, 0.32);
      const targetRoll = THREE.MathUtils.clamp(-steerInput * 0.11 + missingWheelTilt, -0.25, 0.25);

      player.rot.x += (targetPitch - player.rot.x) * dt * 8.0;
      player.rot.y += (targetYaw - player.rot.y) * dt * 8.0;
      player.rot.z += (targetRoll - player.rot.z) * dt * 8.0;

      if (player.mesh) {
        player.mesh.position.copy(player.pos);
        player.mesh.rotation.copy(player.rot);
        player.mesh.visible = (player.cameraMode === 'chase');
        player.wheels.forEach((w) => {
          if (w.attached) w.node.rotation.x -= (player.forwardSpeed * dt) / 0.28;
        });
      }

      // Update Dash Cam Handlebar & Windshield Wiper CSS Variables
      document.documentElement.style.setProperty('--steer-deg', `${(-steerInput * 14 - player.vel.x * 0.6).toFixed(1)}deg`);
      const wiperAngle = rainActive ? Math.sin(elapsed * 8.0) * 38 : -28;
      document.documentElement.style.setProperty('--wiper-deg', `${wiperAngle.toFixed(1)}deg`);

      // 3. Seamless Scrolling Corridor (6-Lane Tech Corridor OR Narrow Old Bengaluru Gullies!)
      const scrollStep = player.forwardSpeed * dt;
      scrollingStrips.forEach((row) => {
        row.position.z += scrollStep;
        if (row.position.z > 36) {
          row.position.z -= CORRIDOR_LENGTH;
        }
      });

      let nearestDist = Infinity;
      let nearestName = isGully ? 'CHICKPET HERITAGE BAZAAR' : 'SILK BOARD JUNCTION';
      let nearestKn = isGully ? 'ಚಿಕ್ಕಪೇಟೆ ಪೇಟೆ ದ್ವಾರ' : 'ಸಿಲ್ಕ್ ಬೋರ್ಡ್ ಜಂಕ್ಷನ್';

      if (isGully) {
        gullyScrollingRows.forEach((gRow) => {
          gRow.position.z += scrollStep;
          if (gRow.position.z > 36) {
            gRow.position.z -= CORRIDOR_LENGTH;
          }
        });
        gullyLandmarkInstances.forEach((lm) => {
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
      } else {
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
      }

      const distMeters = Math.max(0, Math.round(nearestDist === Infinity ? 120 : nearestDist));
      hudEls.landmark.textContent = `${nearestName} • ${distMeters}m`;
      hudEls.landmarkKn.textContent = `${nearestKn} • ${distMeters}m`;

      // 3B. Interactive BTP Red-Light Traffic Signal Junctions
      let activeSignalForHUD = null;
      for (let i = 0; i < trafficSignals.length; i++) {
        const sig = trafficSignals[i];
        sig.pos.z += scrollStep;
        const distAhead = -sig.pos.z;

        // Arm a fresh Red signal countdown when player approaches within 58m
        if (!sig.armedOnApproach && distAhead < 58 && distAhead > 15) {
          sig.armedOnApproach = true;
          sig.phase = 'red';
          sig.timer = 5.5;
          updateSignalBulbMaterials(sig);
          spawnComicCallout(
            sig.pos,
            '🚦 ಕೆಂಪು ಸಿಗ್ನಲ್! RED SIGNAL AHEAD — HOLD [S] OR PRESS [B] TO STOP!',
            '#ef4444'
          );
        }

        if (sig.armedOnApproach) {
          sig.timer -= dt;
          if (sig.phase === 'red' && sig.timer <= 0) {
            sig.phase = 'yellow';
            sig.timer = 1.0;
            updateSignalBulbMaterials(sig);
          } else if (sig.phase === 'yellow' && sig.timer <= 0) {
            sig.phase = 'green';
            sig.timer = 9.0;
            updateSignalBulbMaterials(sig);
            if (distAhead > -6 && distAhead < 38) {
              audio.playLicenseVerified();
              spawnComicCallout(
                sig.pos,
                '🟢 ಹಸಿರು ಸಿಗ್ನಲ್! GREEN SIGNAL — PRESS [W] OR [SPACE] TO START!',
                '#4ade80'
              );
            }
          }

          // Check if player lawfully stopped before the stop line on Red/Yellow
          if ((sig.phase === 'red' || sig.phase === 'yellow') && distAhead > 0.8 && distAhead < 24 && player.forwardSpeed < 2.2) {
            if (!sig.stoppedOnRed) {
              sig.stoppedOnRed = true;
              sig.bonusAwarded = true;
              player.fareRupees += 100;
              player.stats.signalsObeyed++;
              // Shorten wait time once stopped so gameplay stays snappy!
              if (sig.phase === 'red' && sig.timer > 1.8) {
                sig.timer = 1.8;
              }
              audio.playLicenseVerified();
              spawnComicCallout(
                player.pos,
                '🛑 LAWFUL STOP AT RED SIGNAL! +₹100 BONUS (WAIT FOR GREEN!)',
                '#4ade80'
              );
            }
          }

          // Check if player jumped the Red signal stop line at speed!
          if (sig.phase === 'red' && !sig.stoppedOnRed && !sig.violated && distAhead <= 0.2 && distAhead > -4.5 && player.forwardSpeed > 5.0) {
            sig.violated = true;
            player.stats.signalsJumped++;
            player.fareRupees = Math.max(30, player.fareRupees - 150);
            cameraShake = 0.38;
            audio.playPoliceWhistle(true);
            spawnComicCallout(
              sig.pos,
              '📸 ಕೆಂಪು ಸಿಗ್ನಲ್ ಜಂಪ್! BTP RED-LIGHT CAMERA CHALLAN -₹150!',
              '#ef4444'
            );
          }
        }

        if (distAhead > -4 && distAhead < 62 && !activeSignalForHUD) {
          activeSignalForHUD = { sig, distAhead };
        }

        if (sig.pos.z > 24) {
          resetTrafficSignalJunction(sig);
        }
      }

      if (activeSignalForHUD) {
        const { sig, distAhead } = activeSignalForHUD;
        hudEls.sigBanner.classList.add('visible');
        hudEls.sigRed.classList.toggle('active', sig.phase === 'red');
        hudEls.sigYellow.classList.toggle('active', sig.phase === 'yellow');
        hudEls.sigGreen.classList.toggle('active', sig.phase === 'green');
        const secs = Math.max(0, Math.ceil(sig.timer));
        hudEls.sigTimer.textContent = `${String(secs).padStart(2, '0')}s`;
        hudEls.sigTimer.style.color = sig.phase === 'green' ? '#4ade80' : sig.phase === 'yellow' ? '#ffd000' : '#ff4d4d';
        hudEls.sigBanner.style.borderColor = sig.phase === 'green' ? '#22c55e' : sig.phase === 'yellow' ? '#ffd000' : '#ef4444';

        if (sig.phase === 'green') {
          hudEls.sigKn.textContent = `🟢 ಹಸಿರು ಸಿಗ್ನಲ್! ಮುಂದೆ ಹೋಗಿ! (GREEN LIGHT • ${Math.max(0, Math.round(distAhead))}m)`;
          hudEls.sigEn.textContent = player.forwardSpeed < 5
            ? 'SIGNAL IS GREEN! PRESS [W], [SPACE] OR CLICK [GO / START] TO ACCELERATE!'
            : 'GREEN SIGNAL CLEAR — CRUISING THROUGH JUNCTION';
        } else {
          hudEls.sigKn.textContent = `🚦 ಕೆಂಪು ಸಿಗ್ನಲ್! ನಿಲ್ಲಿಸಿ! (RED SIGNAL ${Math.max(0, Math.round(distAhead))}m — STOP!)`;
          hudEls.sigEn.textContent = sig.stoppedOnRed
            ? '✅ STOPPED AT LINE (+₹100 BONUS) • WAIT FOR GREEN THEN PRESS [W]'
            : 'HOLD [S] OR PRESS [B] TO STOP BEFORE WHITE LINE (+₹100 BONUS)';
        }
      } else {
        hudEls.sigBanner.classList.remove('visible');
      }

      // 4. Realistic Potholes with Lateral Pull & Grounded Suspension Jolt
      potholes.forEach((p) => {
        p.group.position.z += scrollStep;
        p.anomalyRing.rotation.z += dt * 2.5;
        if (p.group.position.z > 20) {
          p.group.position.z -= CORRIDOR_LENGTH;
          p.group.position.x = activeLanes[Math.floor(Math.random() * activeLanes.length)];
        }

        const dx = p.group.position.x - player.pos.x;
        const dz = p.group.position.z - player.pos.z;
        const distSq = dx * dx + dz * dz;
        const pullR = currentProfile.potholeRadius;
        if (distSq < pullR * pullR && player.forwardSpeed > 4) {
          const dist = Math.max(0.5, Math.sqrt(distSq));
          const falloff = 1 - dist / pullR;
          player.vel.x += (dx / dist) * currentProfile.potholePullStrength * falloff * dt;

          if (dist < 1.35 && cameraShake < 0.15) {
            player.forwardSpeed = Math.max(10, player.forwardSpeed * 0.85);
            cameraShake = 0.32;
            audio.playBounceImpact(false);
            spawnComicCallout(player.pos, '🕳️ BBMP POTHOLE SUSPENSION JOLT!', '#38bdf8');
          }
        }
      });

      // 5. Sudden Road-Crossing Bengaluru Jaywalkers (Strictly Grounded & Forward-Walking!)
      for (let i = 0; i < jaywalkers.length; i++) {
        const p = jaywalkers[i];
        if (p.hitCooldown > 0) p.hitCooldown -= dt;
        p.pos.z += scrollStep;
        p.pos.y = 0;

        const distAhead = -p.pos.z;
        if (p.state === 'waiting' && distAhead < p.triggerDist && distAhead > 8) {
          p.state = 'crossing';
          p.mesh.rotation.y = getJaywalkerForwardYaw(p.dirX);
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

          if ((p.dirX > 0 && p.pos.x > halfRoadW + 0.9) || (p.dirX < 0 && p.pos.x < -halfRoadW - 0.9)) {
            p.state = 'crossed';
            if (p.legL) p.legL.rotation.x = 0;
            if (p.legR) p.legR.rotation.x = 0;
            if (p.armL) p.armL.rotation.x = 0;
          }
        }

        const pdx = player.pos.x - p.pos.x;
        const pdz = player.pos.z - p.pos.z;
        if (Math.abs(pdx) < 1.1 && Math.abs(pdz) < 1.15 && p.hitCooldown <= 0 && player.forwardSpeed > 2) {
          p.hitCooldown = 0.8;
          player.stats.collisions++;
          const push = pdx >= 0 ? 1 : -1;
          player.vel.x = push * 10.5;
          p.speedBoost = 1.9;
          cameraShake = 0.35;
          audio.playBeepBeepHorn('auto');
          audio.playBounceImpact(false);
          spawnCollisionSparks(p.pos, 10, 0xfb923c);
          spawnComicCallout(p.pos, '🚶‍♂️ "ಅಯ್ಯೋ! ನೋಡ್ಕೊಂಡು ಹೋಗಿ ಅಣ್ಣ!"', '#ff3b5c');
        }

        if (p.pos.z > 20) {
          resetJaywalkerToKerb(p);
        }
      }

      // 5B. Sudden Bengaluru Traffic Police (BTP) License Check Encounter
      let anyCopAlertActive = false;
      for (let i = 0; i < trafficCops.length; i++) {
        const cop = trafficCops[i];
        cop.pos.z += scrollStep;
        cop.walkPhase += dt * 9.0;

        const strobeToggle = Math.floor(elapsed * 10) % 2 === 0;
        cop.beaconR.scale.setScalar(strobeToggle ? 1.35 : 0.85);
        cop.beaconB.scale.setScalar(strobeToggle ? 0.85 : 1.35);

        const distAhead = -cop.pos.z;

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
          const stepErr = cop.targetX - cop.pos.x;
          cop.pos.x += Math.sign(stepErr) * Math.min(Math.abs(stepErr), 4.2 * dt);
          if (Math.abs(stepErr) > 0.1) {
            cop.copMesh.rotation.y = stepErr > 0 ? -Math.PI * 0.62 : Math.PI * 0.62;
            const swing = Math.sin(cop.walkPhase) * 0.55;
            if (cop.legL) cop.legL.rotation.x = swing;
            if (cop.legR) cop.legR.rotation.x = -swing;
          } else {
            cop.copMesh.rotation.y = Math.PI;
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
            player.stats.copsCleared++;
            audio.playLicenseVerified();
            spawnComicCallout(cop.pos, '🪪 "ಸರಿ ಬಿಡಿ! ಮುಂದೆ ಹೋಗಿ!" (DL VERIFIED! +₹100)', '#4ade80');
          }

          // Check if Cop intercepts Player Auto without showing License!
          const cdx = player.pos.x - cop.pos.x;
          const cdz = player.pos.z - cop.pos.z;
          const interceptWidth = isGully ? 1.65 : 2.25;
          if (!cop.resolved && Math.abs(cdx) < interceptWidth && Math.abs(cdz) < 2.0) {
            cop.resolved = true;
            cop.state = 'fined';
            player.stats.copsFined++;
            player.forwardSpeed = 11.0;
            player.vel.x = (cdx >= 0 ? 1 : -1) * (isGully ? 6.5 : 8.5);
            player.fareRupees = Math.max(30, player.fareRupees - 100);
            cameraShake = 0.42;
            audio.playPoliceWhistle(true);
            spawnCollisionSparks(cop.pos, 14, 0x3b82f6);
            hudEls.dlStatus.textContent = 'e-CHALLAN -₹100!';
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
            player.stats.copsEvaded++;
            player.fareRupees += 60;
            audio.playPoliceWhistle(false);
            spawnComicCallout(
              cop.pos,
              '💨 DODGED BTP CHECKPOST! "ನಿಲ್ಲಿಸಿ! ಕ್ಯಾಮೆರಾ ಚಲನ್!" (+₹60)',
              '#38bdf8'
            );
          }
        } else if (cop.state === 'cleared') {
          const backErr = cop.kerbX - cop.pos.x;
          cop.pos.x += Math.sign(backErr) * Math.min(Math.abs(backErr), 5.0 * dt);
          if (Math.abs(backErr) > 0.1) {
            cop.copMesh.rotation.y = backErr < 0 ? Math.PI * 0.54 : -Math.PI * 0.54;
            const swing = Math.sin(cop.walkPhase) * 0.55;
            if (cop.legL) cop.legL.rotation.x = swing;
            if (cop.legR) cop.legR.rotation.x = -swing;
          } else {
            cop.copMesh.rotation.y = Math.PI;
            if (cop.legL) cop.legL.rotation.x = 0;
            if (cop.legR) cop.legR.rotation.x = 0;
          }
        }

        if (cop.pos.z > 22) {
          resetCopCheckpost(cop);
        }
      }

      hudEls.copAlert.classList.toggle('visible', anyCopAlertActive);
      hudEls.vignette.classList.toggle('cop-strobe', anyCopAlertActive);

      // 5C. Sudden Darting Bengaluru Indie Stray Dogs (Grounded)
      for (let i = 0; i < strayDogs.length; i++) {
        const d = strayDogs[i];
        if (d.hitCooldown > 0) d.hitCooldown -= dt;
        d.pos.z += scrollStep;
        d.pos.y = 0;

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

          const bound = Math.sin(d.gallopPhase) * 0.78;
          if (d.legFL) d.legFL.rotation.x = bound;
          if (d.legFR) d.legFR.rotation.x = Math.sin(d.gallopPhase + 0.6) * 0.78;
          if (d.legRL) d.legRL.rotation.x = -bound;
          if (d.legRR) d.legRR.rotation.x = -Math.sin(d.gallopPhase + 0.6) * 0.78;

          if ((d.dirX > 0 && d.pos.x > halfRoadW + 1.2) || (d.dirX < 0 && d.pos.x < -halfRoadW - 1.2)) {
            d.state = 'crossed';
            if (d.legFL) d.legFL.rotation.x = 0;
            if (d.legFR) d.legFR.rotation.x = 0;
            if (d.legRL) d.legRL.rotation.x = 0;
            if (d.legRR) d.legRR.rotation.x = 0;
          }
        }

        const ddx = player.pos.x - d.pos.x;
        const ddz = player.pos.z - d.pos.z;
        if (Math.abs(ddx) < 1.15 && Math.abs(ddz) < 1.2 && d.hitCooldown <= 0 && player.forwardSpeed > 2) {
          d.hitCooldown = 0.85;
          player.stats.collisions++;
          const push = ddx >= 0 ? 1 : -1;
          player.vel.x = push * 9.0;
          d.speedBoost = 2.2;
          cameraShake = 0.28;
          audio.playDogBark();
          audio.playBounceImpact(false);
          spawnCollisionSparks(d.pos, 8, 0xfde047);
          spawnComicCallout(d.pos, '🐕 "ಬೌ-ಬೌ! BOW-WOW! WATCH IT ANNA!"', '#fb923c');
        } else if (!d.hopBonusAwarded && d.pos.z > 1.5 && Math.abs(ddx) >= 1.15 && Math.abs(ddx) < 5.5) {
          d.hopBonusAwarded = true;
          player.stats.dogsDodged++;
          player.fareRupees += 75;
          audio.playDogBark();
          spawnComicCallout(d.pos, '🐕 CLEAN SWERVE PAST INDIE DOGGO! +₹75 BONUS!', '#4ade80');
        }

        if (d.pos.z > 20) {
          resetStrayDogToKerb(d);
        }
      }

      // 6. Two-Way Strictly Grounded Lane Traffic AI (With Red-Light Queueing!)
      for (let i = 0; i < trafficPool.length; i++) {
        const v = trafficPool[i];
        if (v.hitCooldown > 0) v.hitCooldown -= dt;

        const minLane = v.isOncoming ? halfLanes : 0;
        const maxLane = v.isOncoming ? (activeLanes.length - 1) : (halfLanes - 1);

        // Check if same-direction NPC vehicle should stop behind an active Red/Yellow signal
        let stoppedByRedSignal = false;
        if (!v.isOncoming) {
          for (let s = 0; s < trafficSignals.length; s++) {
            const sig = trafficSignals[s];
            if (sig.phase === 'red' || sig.phase === 'yellow') {
              const distToStopLine = v.pos.z - sig.pos.z; // positive when vehicle is behind stop line (+Z side)
              if (distToStopLine > 2.0 && distToStopLine < 18.0) {
                stoppedByRedSignal = true;
                break;
              }
            }
          }
        }

        for (let j = 0; j < trafficPool.length; j++) {
          if (i === j) continue;
          const other = trafficPool[j];
          if (other.isOncoming !== v.isOncoming) continue;
          const dz = v.isOncoming ? (other.pos.z - v.pos.z) : (v.pos.z - other.pos.z);
          if (dz > 0 && dz < 14 && Math.abs(v.pos.x - other.pos.x) < (isGully ? 1.45 : 2.2)) {
            if (v.baseSpeed > other.baseSpeed && !stoppedByRedSignal) {
              const nextLane = minLane + ((v.laneIdx - minLane + 1) % halfLanes);
              v.laneIdx = nextLane;
              v.targetLaneX = activeLanes[nextLane];
            }
          }
        }

        v.weaveTimer -= dt;
        if (v.spec.isHyperDelivery && v.weaveTimer <= 0 && !stoppedByRedSignal) {
          v.weaveTimer = 1.2 + Math.random() * 1.4;
          if (Math.abs(v.pos.z - player.pos.z) < 38 && Math.random() < currentProfile.cutOffAggression) {
            const shift = Math.random() < 0.5 ? -1 : 1;
            v.laneIdx = THREE.MathUtils.clamp(v.laneIdx + shift, minLane, maxLane);
            v.targetLaneX = activeLanes[v.laneIdx];
          }
        }

        const targetVelZ = stoppedByRedSignal
          ? 0
          : v.isOncoming
            ? v.baseSpeed * 0.42
            : -v.baseSpeed;
        v.vel.z += (targetVelZ - v.vel.z) * dt * (stoppedByRedSignal ? 5.5 : 2.5);

        const relZSpeed = player.forwardSpeed + v.vel.z;
        v.pos.z += relZSpeed * dt;
        v.pos.x += v.vel.x * dt;
        // Strictly grounded on the asphalt road — NO flying autos or vehicles!
        v.pos.y = 0;
        v.vel.y = 0;

        const laneErr = v.targetLaneX - v.pos.x;
        v.vel.x += laneErr * 7.5 * dt;
        v.vel.x *= Math.exp(-4.2 * dt);

        const dirSign = v.isOncoming ? -1 : 1;
        const npcYaw = v.baseYaw + THREE.MathUtils.clamp(-v.vel.x * 0.025 * dirSign, -0.25, 0.25);
        const npcRoll = THREE.MathUtils.clamp(-v.vel.x * 0.03 * dirSign, -0.18, 0.18);
        v.rot.set(0, npcYaw, npcRoll);

        v.mesh.position.copy(v.pos);
        v.mesh.rotation.copy(v.rot);

        const wheelSpinSpeed = Math.abs(v.vel.z);
        v.wheels.forEach((w) => {
          if (w.attached) w.node.rotation.x -= (wheelSpinSpeed * dt) / 0.26;
        });

        // Player <-> NPC Grounded Collision Check
        const hitX = (player.radius + v.spec.radius) * 0.88;
        const hitZ = (1.2 + v.spec.lengthZ * 0.45);
        const dx = player.pos.x - v.pos.x;
        const dz = player.pos.z - v.pos.z;

        if (Math.abs(dx) < hitX && Math.abs(dz) < hitZ && v.hitCooldown <= 0) {
          v.hitCooldown = 0.45;
          player.stats.collisions++;
          const isHyper = v.spec.isHyperDelivery;

          const pushDir = dx >= 0 ? 1 : -1;
          player.vel.x = pushDir * (isHyper ? 13.5 : 9.5);
          v.vel.x = -pushDir * (v.type === 'bmtc' ? 3.0 : 11.0);

          audio.playBeepBeepHorn(v.spec.hornType);
          audio.playBounceImpact(isHyper);
          spawnCollisionSparks(v.pos, isHyper ? 18 : 10, v.spec.colorHex);
          cameraShake = isHyper ? 0.42 : 0.26;

          const bonus = isHyper ? 50 : 25;
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
          if (!v.isOncoming && v.pos.z > 26) {
            player.stats.closeOvertakes++;
          }
          recycleTrafficVehicle(v);
        }
      }

      // 7. Update Detached Wheels & Sparks
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

      // 8. Configurable Camera (Regular Chase View vs First-Person Vayuputra RE Dash Cam View)
      if (cameraShake > 0) cameraShake = Math.max(0, cameraShake - dt * 1.8);
      const shakeX = (Math.random() - 0.5) * cameraShake;
      const shakeY = (Math.random() - 0.5) * cameraShake;

      if (player.cameraMode === 'dashcam') {
        const engineVibY = Math.sin(elapsed * 32) * (player.forwardSpeed > 2 ? 0.006 : 0.002);
        camera.position.x = player.pos.x + shakeX * 0.35;
        camera.position.y = 1.48 + engineVibY + shakeY * 0.35;
        camera.position.z = -0.35;
        camera.lookAt(player.pos.x - steerInput * (isGully ? 1.5 : 2.2), 1.32, -38);
      } else {
        const targetCamY = isGully ? 3.45 : 3.85;
        camera.position.x += (player.pos.x * 0.58 - camera.position.x) * dt * 7.5 + shakeX;
        camera.position.y += (targetCamY - camera.position.y) * dt * 6.5 + shakeY;
        camera.position.z = isGully ? 6.4 : 7.2;
        camera.lookAt(player.pos.x * 0.75, 1.25, -14);
      }

      skyDome.position.x = camera.position.x;

      const surgeMult = (rainActive ? 1.5 : 1.0) * currentProfile.fareRateMult;
      player.fareRupees += (player.forwardSpeed * 0.14 * surgeMult) * dt;
      const speedKmh = Math.round(player.forwardSpeed * 2.1);

      hudEls.fare.textContent = `₹${player.fareRupees.toFixed(2)}`;
      hudEls.surge.textContent =
        rainActive ? `${surgeMult.toFixed(1)}x SURGE` : `${surgeMult.toFixed(1)}x HIRE`;
      hudEls.speed.textContent = String(speedKmh);
      updateTripProgressHUD();

      audio.updateContinuous(speedKmh, rainIntensity, 0);

      // 9. Check if Player Reached Trip Destination!
      if (player.distanceKm >= currentProfile.targetDistanceKm && !player.tripFinished) {
        player.distanceKm = currentProfile.targetDistanceKm;
        updateTripProgressHUD();
        finishTripAndShowScoreboard('Destination Reached!');
      }
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
      const dpr = Math.min(window.devicePixelRatio || 1, 2.5);
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setPixelRatio(dpr);
      renderer.setSize(window.innerWidth, window.innerHeight);
      composer.setPixelRatio(dpr);
      composer.setSize(window.innerWidth, window.innerHeight);
      bloomPass.resolution.set(window.innerWidth * dpr, window.innerHeight * dpr);
    });

    // =========================================================================
    // 10. BOOTSTRAP
    // =========================================================================
    async function bootGame() {
      const params = new URLSearchParams(window.location.search);
      const autoMode = params.get('autostart');
      const viewParam = params.get('view');
      if (viewParam === 'dashcam' || viewParam === 'chase') {
        player.cameraMode = viewParam;
      }

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
        if (viewParam === 'dashcam' || viewParam === 'chase') {
          setCameraMode(viewParam, false);
        }
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
        if (params.get('redlight') === '1') {
          triggerRedLightSignalAheadNow(true);
        }
        if (params.get('jaywalker') === '1' && jaywalkers[0]) {
          const stageForwardJaywalker = () => {
            const jw = jaywalkers[0];
            if (!jw) return;
            jw.dirX = 1;
            jw.state = 'crossing';
            jw.pos.set(-3.2, 0, -13.5);
            jw.mesh.position.copy(jw.pos);
            jw.mesh.rotation.y = getJaywalkerForwardYaw(1);
          };
          stageForwardJaywalker();
          setTimeout(stageForwardJaywalker, 2900);
        }
        if (params.get('action') === '1' || params.get('hop') === '1') {
          player.turboBoostTimer = 1.4;
          setTimeout(() => {
            lastCalloutTime = 0;
            if (trafficCops[0]) {
              spawnComicCallout(trafficCops[0].pos, '👮‍♂️ "ಏಯ್ ಆಟೋ! ಸೈಡ್ ಹಾಕಿ! DL ತೋರಿಸಿ!" [PRESS L]', '#ef4444');
            }
            setTimeout(() => {
              lastCalloutTime = 0;
              if (strayDogs[0]) {
                spawnComicCallout(strayDogs[0].pos, '🐕 "ಬೌ-ಬೌ! BOW-WOW!" +₹75 DOGGO SWERVE!', '#4ade80');
              }
            }, 220);
          }, 2300);
        }
        updateSimulation(0.05, 0.2);
        gamePaused = false;

        if (params.get('gameover') === '1') {
          player.distanceKm = currentProfile.targetDistanceKm;
          player.fareRupees = 485.50;
          player.stats.signalsObeyed = 2;
          player.stats.copsCleared = 2;
          player.stats.copsEvaded = 1;
          player.stats.dogsDodged = 3;
          player.stats.closeOvertakes = 9;
          player.stats.collisions = 1;
          updateTripProgressHUD();
          finishTripAndShowScoreboard('Destination Reached!');
        }
      } else {
        applyGravityProfile('medium', false);
        if (viewParam === 'dashcam' || viewParam === 'chase') {
          setCameraMode(viewParam, false);
        }
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
