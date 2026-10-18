# AGENTS.md — Ondu Second: Bangalore Gravity Glitch (Pro Edition)

This document provides context, architectural conventions, coordinate systems, and build workflows for AI coding agents working on **Ondu Second: Bangalore Gravity Glitch**.

---

## 1. Project Overview

**Ondu Second: Bangalore Gravity Glitch** is a self-contained 3D WebGL (Three.js r170) arcade traffic game set on a bustling 6-lane Bengaluru highway corridor alongside the elevated Namma Metro Purple Line viaduct, Vidhana Soudha, and the Silk Board flyover gantry.

### Key Gameplay Pillars
- **Player Vehicle**: Authentic Bengaluru Bajaj RE Auto-Rickshaw (canary-yellow canopy `#FFD000` + emerald-green lower chassis `#009A44` + bilingual rear hood stencil) with 3 independent wheels that can snap off on heavy impacts and be repaired with `R`.
- **Bilingual Kannada + English Hoardings & Gantries (60:40 Rule)**:
  - 8 procedural canvas-textured roadside commercial hoardings (Rameshwaram Cafe, Namma Yatri, KMF Nandini, Namma Metro, Mysore Sandal Soap, BTP Alert, Zepto/Blinkit, Vidyarthi Bhavan) and 2 overhead National Highway gantries (`SILK BOARD JUNCTION` and `HEBBAL FLYOVER`) displaying bold Kannada (`ಕನ್ನಡ`) primary headlines above English subtitles.
- **Bengaluru Traffic Police (BTP) Sudden License Check (`traffic_police.glb`)**:
  - Articulated BTP officer in white pith helmet, lime-green hi-vis reflective vest, khaki uniform, aviator sunglasses, and red LED baton standing beside a bilingual BTP checkpost barricade with flashing red/blue strobes.
  - Blows a synthesized pea-whistle (`playPoliceWhistle`) and steps out into the lane (`#hud-cop-alert`). Players can press **`L`** (or click **`🪪 Show DL [L]`**) to verify their DigiLocker DL & RC for `+₹100`, swerve to evade (`+₹60`), or get busted with a `-₹100` e-Challan fine on collision.
- **Occasional Darting Stray Dog (`stray_dog.glb`)**:
  - Articulated Indian Pariah Dog (Indie dog) with 4 galloping legs (`Dog_Leg_FL`, `Dog_Leg_FR`, `Dog_Leg_RL`, `Dog_Leg_RR`) and curled tail that suddenly darts across the highway with a double-bark (`playDogBark`).
  - Honking (`H`) makes the dog bolt 2x faster; jumping cleanly over the dog with `SPACE` awards a `+₹75` Good Boy Hop Bonus.
- **Two-Way Indian Traffic & Sudden Jaywalkers**:
  - **Left Side (`LANES[0..2]` at `x = -9.5, -5.7, -1.9`)**: Drives **forward** (`-Z`, same direction as the player).
  - **Right Side (`LANES[3..5]` at `x = +1.9, +5.7, +9.5`)**: Drives **oncoming** (`+Z`, rotated `180°`).
  - **Jaywalkers (`pedestrian_jaywalker.glb`)**: Cross the highway raising the *"Ondu Second!"* stop hand.
- **Procedural Web Audio Engine**: Zero external audio files. Synthesizes ambient city drone, 2-stroke auto *"tuk-tuk"* engine, pink-noise monsoon downpour layer, 3-burst Bengaluru Auto-Rickshaw reed/bulb horn (`"PA-PA-PAAARP!"`), BTP police pea-whistle & siren, DigiLocker verification chime, and Indie stray dog double-bark.

---

## 2. Repository Structure

```text
blr-traffic-blender/
├── README.md                  # Full documentation, screenshots & controls
├── agents.md                  # Agent architecture, conventions & build instructions
├── build_assets_blender.py    # Blender Python (bpy) procedural 3D asset generator (12 models)
├── build_game_html.py         # Compiler that embeds assets/*.glb into index.html
├── index.html                 # Unified playable 3D WebGL game (Three.js + Web Audio + HUD)
├── screenshots/               # AAA hero banner, Blender studio render & live WebGL screenshots
│   ├── pro_hero_banner.jpg
│   ├── blender_assets_upgraded.png
│   ├── gameplay_medium_clear.png
│   ├── gameplay_action.png
│   ├── gameplay_peak_hour.png
│   └── gameplay_menu.png
├── assets/                    # Exported Blender .glb binary 3D models (12 total)
│   ├── auto_rickshaw.glb
│   ├── bmtc_bus.glb
│   ├── commuter_techie.glb
│   ├── delivery_blinkit.glb
│   ├── delivery_swiggy.glb
│   ├── delivery_zepto.glb
│   ├── metro_station.glb
│   ├── pedestrian_jaywalker.glb
│   ├── silk_board_sign.glb
│   ├── stray_dog.glb
│   ├── traffic_police.glb
│   └── vidhana_soudha.glb
└── *.glb                      # Root-level copies of the 12 .glb models for direct relative fetch
```

> **Important**: Never edit `index.html` directly if you plan to re-run `build_game_html.py`. Always make HTML/CSS/JS changes inside `build_game_html.py` and run `python3 build_game_html.py` to regenerate `index.html`.

---

## 3. Blender & 3D Asset Conventions (`build_assets_blender.py`)

All 12 `.glb` models are procedurally modeled in Blender (`bpy`) and exported with `export_yup=True` and `export_apply=True`.

### Coordinate System Mapping (Blender $\rightarrow$ Three.js)
- **Blender `+Y`** $\rightarrow$ **Three.js `-Z`** (Forward, driving away from the chase camera).
- **Blender `-Y`** $\rightarrow$ **Three.js `+Z`** (Rear, facing the chase camera at `z = +7.2`).
- **Blender `+Z`** $\rightarrow$ **Three.js `+Y`** (Vertical Up; `z = 0` in Blender is the road surface `y = 0` in Three.js).
- **Blender `+X`** $\rightarrow$ **Three.js `+X`** (Right lateral axis).

### Mandatory Scene-Graph Naming & Pivot Rules
1. **Detachable Vehicle Wheels (`Wheel_*`)**:
   - Every vehicle exports wheels as separate child mesh objects of the root empty (`Wheel_Front`, `Wheel_Rear_L`, `Wheel_Rear_R`, `Wheel_FL`, `Wheel_FR`, `Wheel_RL`, `Wheel_RR`).
   - Build wheel cylinders at `(0, 0, 0)`, join with `apply_loc=False`, and then set `wheel.location = (x, y, radius)` before parenting to `root`.
2. **Articulated Jaywalker (`pedestrian_jaywalker.glb`) & BTP Traffic Cop (`traffic_police.glb`)**:
   - Jaywalker child nodes: `Leg_L`, `Leg_R`, `Arm_L`, `Arm_R`, `Ped_Torso`.
   - BTP Traffic Cop child nodes: `Cop_Leg_L`, `Cop_Leg_R` (pivoted at hip `z = 0.78`), `Cop_Arm_L`, `Cop_Arm_R` (pivoted at shoulder `z = 1.34`, holding glowing red LED baton), `Cop_Torso`.
3. **Articulated Indie Stray Dog (`stray_dog.glb`)**:
   - Child nodes `Dog_Leg_FL`, `Dog_Leg_FR`, `Dog_Leg_RL`, `Dog_Leg_RR` have pivots at shoulder/hip height (`z = 0.34`) so `rotation.x` animates a realistic 4-leg bounding gallop cycle in Three.js.
   - Body mesh is named `Dog_Body` to support coat color variations.

---

## 4. Build, Run & Verification Workflow

### Step 1: Regenerate 12 3D `.glb` Assets & Showcase Render in Blender
```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python build_assets_blender.py
```

### Step 2: Compile `index.html`
```bash
python3 build_game_html.py
```

### Step 3: Serve Locally & Verify Visually
```bash
python3 -m http.server 8765
```
Query parameters supported by `index.html`:
- `?autostart=low|medium|complex` — Boots directly into the specified difficulty profile.
- `&rain=1` — Activates monsoon downpour (`0%` tire grip).
- `&snapwheel=1` — Snaps off one player wheel at boot.
- `&copcheck=1` — Triggers an immediate BTP Traffic Police license checkpost ahead.
- `&hop=1` — Launches the player auto into a mid-air Gravity Hop with active comic callout bubbles.
