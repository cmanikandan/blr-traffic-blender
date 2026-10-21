# 🤖 agents.md — AI Coding Agent Guide (`Ondu Second: Namma Auto Traffic`)

> **Built End-to-End with [Google Antigravity](https://antigravity.google/) & [Google Gemini Models](https://deepmind.google/technologies/gemini/)**  
> This repository is designed for seamless autonomous iteration by **[Google Antigravity](https://antigravity.google/)**, **Gemini CLI**, and MCP-enabled AI coding agents powered by **[Google Gemini models](https://ai.google.dev/)**. Read this file completely before modifying 3D assets, game physics, textures, or documentation.

---

## 1. Agentic Architecture & Multi-Agent Roles

This project was autonomously architected, modeled in 3D, textured, synthesized, and visually verified using **Google Antigravity** + **Google Gemini** across four specialized agent responsibilities:

| Agent Role | Scope & Files Owned | Primary Tools / Stack |
| :--- | :--- | :--- |
| **🎨 3D Blender Asset Agent** | Procedural PBR geometry, detachable wheel hierarchies, character limb pivots, and QHD studio showcase renders in [`build_assets_blender.py`](build_assets_blender.py) → `assets/*.glb`. | Blender 5.x (`bpy`) + [Blender MCP](https://github.com/ahujasid/blender-mcp) (`127.0.0.1:9876`) or headless `--background` CLI |
| **🏎️ WebGL2 Simulation & Physics Agent** | Three.js r170 4x MSAA HDR pipeline, `old_blr` narrow-gully vs 6-lane highway topology, BTP Red-Light signals, Dash Cam POV, and grounded physics in [`build_game_html.py`](build_game_html.py). | Three.js `r170`, `EffectComposer`, `UnrealBloomPass`, `WebGLRenderTarget` (`HalfFloatType`, `samples: 4`) |
| **🪧 Kannada Cultural & Audio Agent** | 2K (`2048×1024`) illustrated Kannada + English (`60:40`) hoardings, Chickpet/Malleshwaram bazaar signage, Web Audio synthesizer, and thermal PNG receipt generator in [`build_game_html.py`](build_game_html.py). | HTML5 2D Canvas (`Noto Sans Kannada` / `Tunga`), Web Audio API (`AudioContext` oscillators & noise buffers) |
| **🔍 Visual QA & Release Agent** | Metal-accelerated Retina (`2880×1800`) headless Chrome screenshot verification, zero-trademark / zero-secret audits, [`README.md`](README.md), and [`LICENSE`](LICENSE) (MIT). | Headless Chrome (`--use-angle=metal --force-device-scale-factor=2`), `sips`, Git |

---

## 2. Non-Negotiable Guardrails & Cultural Authenticity Rules

Every agent modifying this codebase **MUST** enforce these five rules without exception:

1. **Single Source of Truth (`build_game_html.py` → `index.html`)**:
   - **NEVER** edit [`index.html`](index.html) directly—it is a compiled artifact embedding all 12 gzip-compressed base64 `.glb` models.
   - Always edit [`build_game_html.py`](build_game_html.py) and run `python3 build_game_html.py` to regenerate [`index.html`](index.html).
2. **Fictitious Vehicle Branding Only (Zero Real Trademarks)**:
   - The player vehicle is the fictitious emerald-and-canary **`Vayuputra RE Compact (ವಾಯುಪುತ್ರ)`** (`KA-01-AG-9999`).
   - Verify zero occurrences of real auto-manufacturer trademarks before committing (`grep -ri "bajaj" . --exclude-dir=.git` must return 0 matches).
3. **100% Grounded Vehicle Physics (`pos.y === 0`)**:
   - Autos, buses, and scooters **never fly or jump vertically**. Keep `player.pos.y = 0` and NPC `v.pos.y = 0` at all times.
   - Pressing `SPACE` triggers a grounded **⚡ Vayuputra Turbo Gap Boost** (`player.turboBoostTimer`), never an airborne hop.
4. **Authentic Bengaluru Cultural Details**:
   - Commercial hoardings and Old Bengaluru bazaar shopboards follow Bengaluru's **60% Kannada (`ಕನ್ನಡ`) : 40% English** signage standard.
   - Key art and character depictions must reflect authentic local Bengaluru street culture (e.g., bareheaded local Bengaluru *"Auto Anna"* in a collared khaki uniform shirt `ಖಾಕಿ ಅಂಗಿ`, BTP officers in white pith helmets and lime-green reflective vests, and terracotta Indian Pariah / Indie street dogs).
5. **Permissive Open-Source Licensing ([`LICENSE`](LICENSE))**:
   - All code, procedural `.glb` models, shaders, and documentation remain compatible with the repository's **[MIT License](LICENSE)**. Never bundle proprietary fonts, copyrighted audio clips, or unattributed third-party meshes.

---

## 3. Repository Structure

```text
blr-traffic-blender/
├── LICENSE                    # Permissive MIT License
├── README.md                  # User documentation, 2K/Retina HD screenshots & quick-start guide
├── agents.md                  # AI Coding Agent instructions, guardrails & build/QA workflows
├── build_assets_blender.py    # Blender Python (bpy) procedural 3D asset generator (12 PBR models + 2560x1440 render)
├── build_game_html.py         # Master game source & compiler that embeds assets/*.glb into index.html
├── index.html                 # Compiled zero-install playable 3D WebGL2 bundle (~642 KB)
├── screenshots/               # 2K HD key art banners, 2560x1440 Blender render & 2880x1800 Retina WebGL captures
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
├── assets/                    # Canonical exported Blender .glb binary 3D models (12 total)
└── *.glb                      # Root-level copies of the 12 .glb models for direct relative HTTP fetch
```

---

## 4. Route Topologies & Core Gameplay Systems

### Four Finite Bengaluru Route Profiles (`GRAVITY_PROFILES`)
| Profile Key | Route Name | Road Width & Lanes | Distance | Special Rules |
| :--- | :--- | :--- | :---: | :--- |
| **`old_blr`** | `ಹಳೆಯ ಬೆಂಗಳೂರು ಗಲ್ಲಿ \| Old Bengaluru Gullies` (`Chickpet → Malleshwaram`) | **`9.6m` narrow 2-lane gully** (`GULLY_LANES = [-3.1, -1.35, 1.35, 3.1]`) | `0.5 KM` | `isNarrowGully: true`, `busRatio: 0.0` (no BMTC buses), 2-storey Mangalore clay-tile shops, flower carts, overhead marigold toranas, `1.8x` heritage fare rate |
| **`low`** | `ಕಬ್ಬನ್ ಪಾರ್ಕ್ ಬೆಳಿಗ್ಗೆ \| Cubbon Park Morning` (`MG Road → Cubbon Park`) | `22.8m` 6-lane highway (`LANES = [-9.5, -5.7, -1.9, 1.9, 5.7, 9.5]`) | `1.2 KM` | Calm morning traffic, `1.0x` base fare rate |
| **`medium`** | `ಇಂದಿರಾನಗರ ಸಂಜೆ ರಶ್ \| Indiranagar 6 PM Rush` (`Silk Board → Indiranagar`) | `22.8m` 6-lane highway | `1.8 KM` | Default balanced rush with BMTC 500D buses, BTP signals & cop checks, `1.5x` fare rate |
| **`complex`** | `ಸಿಲ್ಕ್ ಬೋರ್ಡ್ ಟ್ರಾಫಿಕ್ \| Silk Board 8 PM Gridlock` (`Electronic City → Hebbal`) | `22.8m` 6-lane highway | `2.5 KM` | Dense peak-hour gridlock + frequent monsoon hydroplaning (`0%` tire grip), `2.5x`–`3.8x` surge |

- **Two-Way Left-Hand Indian Traffic**:
  - Negative `X` lanes (`index < lanes.length / 2`) drive **forward (`-Z`)** with the player.
  - Positive `X` lanes (`index >= lanes.length / 2`) drive **oncoming (`+Z`)**, rotated `Math.PI`.
- **Interactive BTP Red-Light Signal Junctions**:
  - Players stop at `0 KM/H` before the white stop line using `S`, `ArrowDown`, or `B` (Handbrake latch) on Red (`+₹100` / `+250 PTS` bonus) and press `W` / `SPACE` on Green to accelerate. Jumping Red triggers a `-₹150` camera challan.

---

## 5. Blender 3D & Three.js Coordinate Conventions

All 12 `.glb` models in [`build_assets_blender.py`](build_assets_blender.py) export with `export_yup=True` and `export_apply=True`.

### Axis Mapping (Blender $\rightarrow$ glTF / Three.js)
- **Blender `+Y`** $\rightarrow$ **Three.js `-Z`** (Forward, away from chase camera).
- **Blender `-Y`** $\rightarrow$ **Three.js `+Z`** (Rear, toward chase camera).
- **Blender `+Z`** $\rightarrow$ **Three.js `+Y`** (Vertical Up; `y = 0` is the asphalt surface).
- **Blender `+X`** $\rightarrow$ **Three.js `+X`** (Right lateral axis).

### Critical Character Forward-Yaw Rule (`getJaywalkerForwardYaw`)
Because `pedestrian_jaywalker.glb`, `stray_dog.glb`, and `traffic_police.glb` are modeled facing **`+Y` in Blender** (`(0, 0, -1)` in Three.js), rotating around `+Y` by `yaw` yields world forward vector `(-sin(yaw), 0, -cos(yaw))`:
- Crossing **Left-to-Right (`+X`, `dirX > 0`)** **MUST** use **negative yaw** (`-Math.PI * 0.54`).
- Crossing **Right-to-Left (`-X`, `dirX < 0`)** **MUST** use **positive yaw** (`+Math.PI * 0.54`).
- Never invert this sign—positive yaw with `+X` velocity makes pedestrians moonwalk backwards!

### Mandatory Scene-Graph Node Names
- **Detachable Vehicle Wheels**: `Wheel_Front`, `Wheel_Rear_L`, `Wheel_Rear_R` (3-wheelers) and `Wheel_FL`, `Wheel_FR`, `Wheel_RL`, `Wheel_RR` (4-wheelers), built at origin before setting `.location = (x, y, radius)`.
- **Jaywalker (`pedestrian_jaywalker.glb`)**: `Leg_L`, `Leg_R`, `Arm_L`, `Arm_R`, `Ped_Torso`.
- **BTP Officer (`traffic_police.glb`)**: `Cop_Leg_L`, `Cop_Leg_R`, `Cop_Arm_L`, `Cop_Arm_R` (with red LED baton), `Cop_Torso`.
- **Indie Stray Dog (`stray_dog.glb`)**: `Dog_Leg_FL`, `Dog_Leg_FR`, `Dog_Leg_RL`, `Dog_Leg_RR`, `Dog_Body`.

---

## 6. Build, Verification & Retina HD Screenshot Workflow

### Step 1: Rebuild All 12 PBR `.glb` Assets & `2560×1440` Showcase Render
Via headless Blender CLI:
```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python build_assets_blender.py
```
*(Or via an active Blender MCP socket on `127.0.0.1:9876` by running `python3 build_assets_blender.py`.)*

### Step 2: Compile `index.html` & Run Static Audits
```bash
python3 build_game_html.py
grep -ri "bajaj" . --exclude-dir=.git && exit 1 || echo "Zero trademark leaks"
```

### Step 3: Capture `2880×1800` Retina HD WebGL Screenshots (macOS Metal GPU)
Never pass `--disable-gpu` (which forces blank or fallback WebGL frames). Always serve over HTTP and enable Metal + `2x` device scale factor:
```bash
python3 -m http.server 8765 --bind 127.0.0.1 >/dev/null 2>&1 &
SRV_PID=$!
trap "kill $SRV_PID 2>/dev/null || true" EXIT
sleep 1

"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --use-angle=metal --enable-webgl --ignore-gpu-blocklist \
  --window-size=1440,900 --force-device-scale-factor=2 --hide-scrollbars \
  --virtual-time-budget=4200 \
  --screenshot="screenshots/gameplay_old_blr.png" \
  "http://127.0.0.1:8765/index.html?autostart=old_blr&view=chase&jaywalker=1"
```

### Deterministic URL Query Parameters for Automated Agent QA
- `?autostart=old_blr|low|medium|complex` — Skips modal and boots directly into the chosen route (`old_blr` = `0.5 km` narrow gullies).
- `&view=chase|dashcam` — Boots in 3rd-person Chase view or 1st-person Vayuputra RE Dash Cam POV.
- `&redlight=1` — Stages an active BTP Red-Light Signal Junction ahead with the auto braked at `0 KM/H`.
- `&copcheck=1` — Stages an immediate BTP Traffic Police whistle & DigiLocker DL check ahead.
- `&jaywalker=1` — Stages a forward-walking pedestrian mid-crossing right in front of the auto.
- `&rain=1` — Enables monsoon downpour + `0%` tire grip hydroplaning.
- `&snapwheel=1` — Detaches one player wheel at boot to test `[R]` wheel repair.
- `&gameover=1` — Opens the Final Trip Scoreboard & Thermal PNG Fare Receipt generator immediately.
