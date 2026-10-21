# AGENTS.md — Ondu Second: Namma Auto Traffic (Ultra-HD Pro Edition)

This document provides context, architectural conventions, coordinate systems, and build workflows for AI coding agents working on **Ondu Second: Namma Auto Traffic**.

---

## 1. Project Overview

**Ondu Second: Namma Auto Traffic** is a self-contained Ultra-HD 3D WebGL2 (Three.js r170) arcade traffic game featuring two distinct Bengaluru street environments:
1. **Old Bengaluru Narrow Gullies (`old_blr`, `0.5 km`)**: A tight **`9.6m` 2-lane bazaar street** (`CHICKPET → MALLESHWARAM`) lined with 2-storey Mangalore clay-tile heritage shopfronts, wooden verandah pillars, marigold & jasmine flower vendor carts, overhead festival marigold & mango-leaf toranas, and Chickpet/Malleshwaram bazaar archway gates (no wide buses).
2. **6-Lane Highway Corridor (`low` = `1.2 km`, `medium` = `1.8 km`, `complex` = `2.5 km`)**: A `22.8m` 6-lane highway alongside the elevated Namma Metro Purple Line viaduct, Vidhana Soudha, and NH-44 Silk Board / Hebbal flyover gantries.

### Key Gameplay & Engineering Pillars
- **Fictitious Branding Only**: The player drives the emerald-and-canary **Vayuputra RE Compact (`ವಾಯುಪುತ್ರ`)** Auto-Rickshaw (`auto_rickshaw.glb`). Never use real-world auto manufacturer trademarks.
- **100% Grounded Vehicle Physics**: All vehicles stay strictly grounded (`pos.y = 0`). `SPACE` triggers a grounded **Vayuputra Turbo Gap Boost** (`turboBoostTimer`) rather than vertical jumping.
- **Ultra-HD 4x MSAA WebGL2 Pipeline & 2K Procedural Textures**:
  - `renderer.setPixelRatio(MAX_DPR)` (`up to 2.5`), `4096×4096` PCFSoftShadowMap, and a multi-sampled `WebGLRenderTarget(..., { samples: 4, type: THREE.HalfFloatType })` passed into `EffectComposer`.
  - All procedural `CanvasTexture` surfaces pass through `finalizeHDTexture()` (`LinearMipmapLinearFilter` + `maxAnisotropy`), including `2048×1024` illustrated Kannada + English hoardings, `2048×2048` bump-mapped asphalt, and `2048×1024` dusk sky dome.
- **Interactive BTP Red/Yellow/Green Traffic Signal Junctions**:
  - Overhead & roadside BTP traffic signal gantries with live countdown timers and painted white road stop lines (dynamically scaled for both `22.8m` highway and `9.6m` gully widths).
  - Brake to **`0 KM/H`** before the stop line using **`S`**, **`ArrowDown`**, or **`B`** (Handbrake) on Red for `+₹100` (`+250 PTS`), and press **`W`** / **`SPACE`** on Green to accelerate. Jumping Red triggers a `-₹150` camera challan.
- **BTP Sudden License Check (`traffic_police.glb`) & Darting Indie Stray Dogs (`stray_dog.glb`)**:
  - Press **`L`** to verify DigiLocker DL & RC (`+₹100`), swerve (`+₹60`), or take a `-₹100` challan on collision.
  - Stray dogs bolt across lanes with a synthesized double-bark (`+₹75` clean swerve bonus).
- **Dual Camera Views & Viral PNG Fare Receipt**:
  - Toggle between **3rd-Person Chase (`chase`)** and **1st-Person Vayuputra RE Dash Cam (`dashcam`)** via **`V`**.
  - Finite trips conclude with a **Final Trip Scoreboard**, `localStorage` Top-5 Leaderboard, and downloadable **`800×980` Thermal PNG Fare Receipt**.

---

## 2. Repository Structure

```text
blr-traffic-blender/
├── README.md                  # Full documentation, 2K/Retina HD screenshots & controls
├── agents.md                  # Agent architecture, coordinate conventions & build workflow
├── build_assets_blender.py    # Blender Python (bpy) procedural 3D asset generator (12 models + 2560x1440 QHD render)
├── build_game_html.py         # Compiler that embeds assets/*.glb into index.html
├── index.html                 # Unified playable 3D WebGL2 game (Three.js + Web Audio + HUD)
├── screenshots/               # 2K HD key art banners, 2560x1440 Blender render & 2880x1800 Retina WebGL screenshots
│   ├── old_blr_gully_banner.jpg
│   ├── pro_hero_banner.jpg
│   ├── blender_assets_upgraded.png
│   ├── gameplay_old_blr.png
│   ├── gameplay_old_blr_dashcam.png
│   ├── gameplay_menu.png
│   ├── gameplay_action.png
│   ├── gameplay_redlight.png
│   ├── gameplay_dashcam.png
│   ├── gameplay_medium_clear.png
│   ├── gameplay_peak_hour.png
│   └── gameplay_scoreboard.png
├── assets/                    # Exported Blender .glb binary 3D models (12 total)
└── *.glb                      # Root-level copies of the 12 .glb models for direct relative fetch
```

> **Important**: Never edit `index.html` directly. Always edit `build_game_html.py` and run `python3 build_game_html.py` to regenerate `index.html`.

---

## 3. Blender & Three.js Coordinate Conventions

All 12 `.glb` models are procedurally modeled in Blender (`bpy`) and exported with `export_yup=True` and `export_apply=True`.

### Coordinate System Mapping (Blender $\rightarrow$ Three.js)
- **Blender `+Y`** $\rightarrow$ **Three.js `-Z`** (Forward, facing away from the chase camera).
- **Blender `-Y`** $\rightarrow$ **Three.js `+Z`** (Rear, facing toward the chase camera).
- **Blender `+Z`** $\rightarrow$ **Three.js `+Y`** (Vertical Up; `y = 0` is the asphalt road surface).
- **Blender `+X`** $\rightarrow$ **Three.js `+X`** (Right lateral axis).

### Critical Character Heading Rule (`pedestrian_jaywalker.glb`, `stray_dog.glb`, `traffic_police.glb`)
Because characters face `+Y` in Blender (`(0, 0, -1)` in Three.js), rotating around `+Y` by `yaw` produces a forward world vector of `(-sin(yaw), 0, -cos(yaw))`:
- Moving **Left-to-Right (`+X`, `dirX > 0`)** requires **negative yaw** (`-Math.PI * 0.54`, handled by `getJaywalkerForwardYaw(dirX)`).
- Moving **Right-to-Left (`-X`, `dirX < 0`)** requires **positive yaw** (`+Math.PI * 0.54`).
- Inverting this sign causes characters to moonwalk backwards!

---

## 4. Build, Run & Retina HD Screenshot Workflow

### Step 1: Regenerate 12 `.glb` Models & `2560×1440` Studio Render
```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python build_assets_blender.py
```

### Step 2: Compile `index.html`
```bash
python3 build_game_html.py
```

### Step 3: Serve & Capture `2880×1800` Retina HD Screenshots (macOS Metal WebGL)
Always omit `--disable-gpu` and pass `--use-angle=metal --force-device-scale-factor=2`:
```bash
python3 -m http.server 8765 --bind 127.0.0.1 &
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --use-angle=metal --enable-webgl --ignore-gpu-blocklist \
  --window-size=1440,900 --force-device-scale-factor=2 --hide-scrollbars \
  --virtual-time-budget=4200 \
  --screenshot=screenshots/gameplay_old_blr.png \
  "http://127.0.0.1:8765/index.html?autostart=old_blr&view=chase&jaywalker=1"
```

Supported URL query parameters:
- `?autostart=old_blr|low|medium|complex` — Boots directly into the selected route (`old_blr` = `0.5 km` narrow gullies).
- `&view=chase|dashcam` — Selects 3rd-person Chase or 1st-person Vayuputra RE Dash Cam POV.
- `&redlight=1` — Stages an active BTP Red-Light Signal Junction ahead (`0 KM/H` stop).
- `&copcheck=1` — Stages an immediate BTP Traffic Police license checkpost ahead.
- `&jaywalker=1` — Stages a forward-walking pedestrian mid-crossing ahead.
- `&rain=1` — Activates monsoon downpour (`0%` tire grip).
- `&gameover=1` — Opens the Final Trip Scoreboard & Receipt modal immediately.
