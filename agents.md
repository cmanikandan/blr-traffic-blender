# AGENTS.md — Ondu Second: Bangalore Gravity Glitch

This document provides context, architectural conventions, coordinate systems, and build workflows for AI coding agents working on **Ondu Second: Bangalore Gravity Glitch**.

---

## 1. Project Overview

**Ondu Second: Bangalore Gravity Glitch** is a self-contained 3D WebGL (Three.js) arcade traffic game set on a bustling 6-lane Bengaluru highway corridor alongside the elevated Namma Metro Purple Line viaduct, Vidhana Soudha, and the Silk Board flyover gantry.

### Key Gameplay Pillars
- **Player Vehicle**: Authentic Bengaluru Bajaj RE Auto-Rickshaw (canary-yellow canopy `#FFD000` + emerald-green lower chassis `#009A44`) with 3 independent wheels that can snap off on heavy impacts and be repaired with `R`.
- **Two-Way Indian Traffic**:
  - **Left Side (`LANES[0..2]` at `x = -9.5, -5.7, -1.9`)**: Drives **forward** (`-Z`, same direction as the player).
  - **Right Side (`LANES[3..5]` at `x = +1.9, +5.7, +9.5`)**: Drives **oncoming** (`+Z`, rotated `180°` with front windshields and headlights facing the camera).
- **Sudden Road-Crossing Jaywalkers**: Pedestrians (`pedestrian_jaywalker.glb`) waiting along the kerbs and zebra crossings who suddenly dart across the road as the player approaches, raising the iconic Bengaluru *"Ondu Second / Stop Hand"* gesture while carrying a cloth `jhola` bag.
- **Dynamic Hazards & Controlled Gravity Glitch**:
  - Magnetic BBMP potholes (dark asphalt craters with rainwater puddles, orange-and-white traffic cones, and cyan gravity rings) pull nearby vehicles laterally and trigger a controlled low-G bounce.
  - Sudden monsoon downpours reduce tire grip to `0%` (hydroplaning drift) and activate a 1,600-streak 3D rain particle system.
- **Procedural Web Audio Engine**: Zero external audio files. Synthesizes a continuous ambient city drone, speed-modulated 2-stroke auto *"tuk-tuk"* engine, pink-noise monsoon downpour layer, and a multi-harmonic **3-burst Bengaluru Auto-Rickshaw reed/bulb horn (`"PA-PA-PAAARP!"`)** with nonlinear waveshaper saturation, diaphragm rattle modulation, and under-flyover slapback echo.

---

## 2. Repository Structure

```text
blr-traffic-blender/
├── agents.md                  # Agent architecture, conventions & build instructions
├── build_assets_blender.py    # Blender Python (bpy) procedural 3D asset generator
├── build_game_html.py         # Compiler that embeds assets/*.glb into index.html
├── index.html                 # Unified playable 3D WebGL game (Three.js + Web Audio + HUD)
├── assets/                    # Exported Blender .glb binary 3D models
│   ├── auto_rickshaw.glb
│   ├── bmtc_bus.glb
│   ├── commuter_techie.glb
│   ├── delivery_blinkit.glb
│   ├── delivery_swiggy.glb
│   ├── delivery_zepto.glb
│   ├── metro_station.glb
│   ├── pedestrian_jaywalker.glb
│   ├── silk_board_sign.glb
│   └── vidhana_soudha.glb
└── *.glb                      # Root-level copies of the 10 .glb models for direct relative fetch
```

> **Important**: Never edit `index.html` directly if you plan to re-run `build_game_html.py`. Always make HTML/CSS/JS changes inside `build_game_html.py` and run `python3 build_game_html.py` to regenerate `index.html`.

---

## 3. Blender MCP & 3D Asset Conventions (`build_assets_blender.py`)

All 10 `.glb` models are procedurally modeled in Blender (`bpy`) and exported with `export_yup=True` and `export_apply=True`.

### Coordinate System Mapping (Blender $\rightarrow$ Three.js)
- **Blender `+Y`** $\rightarrow$ **Three.js `-Z`** (Forward, driving away from the chase camera).
- **Blender `-Y`** $\rightarrow$ **Three.js `+Z`** (Rear, facing the chase camera at `z = +7.2`).
- **Blender `+Z`** $\rightarrow$ **Three.js `+Y`** (Vertical Up; `z = 0` in Blender is the road surface `y = 0` in Three.js).
- **Blender `+X`** $\rightarrow$ **Three.js `+X`** (Right lateral axis).

### Mandatory Scene-Graph Naming & Pivot Rules
1. **Detachable Vehicle Wheels (`Wheel_*`)**:
   - Every vehicle exports wheels as separate child mesh objects of the root empty (`Wheel_Front`, `Wheel_Rear_L`, `Wheel_Rear_R`, `Wheel_FL`, `Wheel_FR`, `Wheel_RL`, `Wheel_RR`).
   - **Crucial Pivot Rule**: Build wheel cylinders at `(0, 0, 0)`, join with `apply_loc=False`, and then set `wheel.location = (x, y, radius)` before parenting to `root`. This keeps each wheel's origin at its axle center so `w.node.rotation.x` spins smoothly in Three.js without eccentric vertical bouncing.
2. **Articulated Jaywalker Pedestrian (`pedestrian_jaywalker.glb`)**:
   - Child nodes `Leg_L` and `Leg_R` have their local origins at the hip (`z = 0.78`), and `Arm_L` / `Arm_R` have their local origins at the shoulder (`z = 1.32`), built with `apply_loc=False`.
   - The torso mesh is named `Ped_Torso` so Three.js can clone its material and tint jaywalkers with diverse Indian street outfit colors.
3. **Namma Metro Station & Train (`metro_station.glb`)**:
   - Includes a child object named `Metro_Train` which Three.js detaches at runtime (`scene.attach(continuousMetroTrain)`) so the Purple Line train glides continuously along the entire 360m unbroken viaduct at `X = +18.5`.
4. **ACES Filmic Tone Mapping & Emission Strengths**:
   - Three.js renders with `THREE.ACESFilmicToneMapping` (`toneMappingExposure = 1.25`).
   - Keep `emission_strength` in Blender between `0.5` and `1.2` for colored lights (`taillight`, `amber_glow`). Values above `2.5` will clip and desaturate into white under ACES Filmic tone mapping.

---

## 4. Build, Run & Verification Workflow

### Step 1: Regenerate 3D `.glb` Assets via Blender MCP
If you modify `build_assets_blender.py`, execute it against the running Blender MCP server (`127.0.0.1:9876`, TCP JSON command `{"type": "execute_code", "params": {"code": "..."}}`):

```bash
python3 -c '
import json, socket
with open("build_assets_blender.py") as f:
    code = f.read()
s = socket.create_connection(("127.0.0.1", 9876), timeout=30)
s.sendall(json.dumps({"type": "execute_code", "params": {"code": code}}).encode())
print(s.recv(65536).decode())
s.close()
'
```

### Step 2: Compile `index.html`
After updating `build_game_html.py` or re-exporting `.glb` assets:

```bash
python3 build_game_html.py
```

This compresses all `assets/*.glb` files into base64-gzipped payloads inside `EMBEDDED_GLB_GZ` and writes `index.html`.

### Step 3: Serve Locally & Verify Visually
Start a local HTTP server:

```bash
python3 -m http.server 8765
```

 URL query parameters supported by `index.html` for automated testing and headless browser screenshots:
- `http://localhost:8765/index.html` — Opens the native `<dialog id="gravity-modal">` difficulty selector.
- `http://localhost:8765/index.html?autostart=low` — Boots directly into **Low (Cubbon Park Morning)** mode.
- `http://localhost:8765/index.html?autostart=medium` — Boots directly into **Medium (Indiranagar 6 PM Rush)** mode.
- `http://localhost:8765/index.html?autostart=complex&rain=1&snapwheel=1` — Boots directly into **Complex (Silk Board 8 PM Gridlock)** mode with active monsoon rain (`0%` tire grip) and a snapped wheel.
