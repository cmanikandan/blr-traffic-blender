# 🛺 ಒಂದು ಸೆಕೆಂಡ್ | Ondu Second: Namma Auto Traffic (Pro Edition)

<p align="center">
  <a href="https://antigravity.google/"><img src="https://img.shields.io/badge/Built_with-Google_Antigravity-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="Built with Google Antigravity" /></a>
  <a href="https://deepmind.google/technologies/gemini/"><img src="https://img.shields.io/badge/Powered_by-Google_Gemini_Models-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white" alt="Powered by Google Gemini Models" /></a>
  <a href="https://www.blender.org/"><img src="https://img.shields.io/badge/3D_Assets-Blender_5.1_PBR_.glb-EA7600?style=for-the-badge&logo=blender&logoColor=white" alt="Blender 5.1 PBR GLB" /></a>
  <a href="https://threejs.org/"><img src="https://img.shields.io/badge/Engine-Three.js_r170_WebGL-000000?style=for-the-badge&logo=threedotjs&logoColor=white" alt="Three.js r170" /></a>
</p>

> **🤖 Created with Google Antigravity & Gemini Models**: This game—including its procedural Blender 3D PBR `.glb` asset pipeline, bilingual Kannada + English canvas texture synthesis, Three.js WebGL shader & post-processing architecture, Web Audio synthesizer, and AAA cover art—was autonomously designed, engineered, and verified using **[Google Antigravity](https://antigravity.google/)**, Google's agentic AI coding & development platform powered by **[Google Gemini models](https://deepmind.google/technologies/gemini/)** ([Gemini API / Google AI for Developers](https://ai.google.dev/)).

<p align="center">
  <img src="screenshots/pro_hero_banner.jpg" alt="Ondu Second: Namma Auto Traffic — AAA Pro Edition Cover Art" width="100%" />
</p>

<p align="center">
  <strong>A self-contained, pro-grade 3D WebGL (Three.js r170) arcade traffic game set on a bustling 6-lane Bengaluru highway corridor alongside the Namma Metro Purple Line viaduct, Vidhana Soudha, and the Silk Board flyover gantry.</strong><br/>
  Featuring <strong>12 procedural PBR 3D <code>.glb</code> models</strong> built in Blender, <strong>user-configurable First-Person Auto Dash Cam &amp; 3rd-Person Chase views</strong>, <strong>100% grounded vehicle physics (zero flying autos)</strong>, <strong>finite route trips with an itemized End-of-Trip Scoreboard</strong>, <strong>Bilingual Kannada + English (60:40) roadside hoardings &amp; highway gantries</strong>, sudden <strong>Bengaluru Traffic Police (BTP) license checks</strong>, and darting <strong>Indie stray dogs</strong>.
</p>

---

## 🎬 Live 3D WebGL Gameplay Preview

### 🛺 User-Configurable Camera Views: Regular Chase View vs. Auto Dash Cam POV (`[V]` Key)

| 🎥 Regular Chase View (3rd-Person Grounded Highway) | 🛺 Auto Dash Cam View (Driver Cockpit POV from Inside the Auto) |
| :---: | :---: |
| ![Regular Chase View](screenshots/gameplay_medium_clear.png) | ![First-Person Auto Dash Cam View](screenshots/gameplay_dashcam.png) |

### 🏁 End-of-Trip Scoreboard, BTP Cop Checks & Monsoon Hydroplaning

| 🏁 Final Trip Scoreboard & Itemized Auto Meter Receipt | 👮‍♂️ Sudden BTP Cop Check & Darting Stray Dog (100% Grounded) |
| :---: | :---: |
| ![End-of-Trip Scoreboard](screenshots/gameplay_scoreboard.png) | ![Grounded Action with BTP Cop & Stray Dog](screenshots/gameplay_action.png) |

| ⛈️ Silk Board 8 PM Peak Hour + Monsoon Hydroplaning (`0%` Grip) | ⚙️ Route, Difficulty & Camera Perspective Selector (`<dialog>`) |
| :---: | :---: |
| ![Silk Board Peak Hour Monsoon Storm](screenshots/gameplay_peak_hour.png) | ![Route & Camera Selector Modal](screenshots/gameplay_menu.png) |

### 🎨 Blender 5.1 Studio Showcase — All 12 Procedural PBR `.glb` Models
![Blender 12 PBR Assets Studio Showcase](screenshots/blender_assets_upgraded.png)

---

## ✨ Key Features in the Pro Edition

### 1. 🎥 User-Configurable Camera Views: First-Person Auto Dash Cam & 3rd-Person Chase (`[V]`)
Switch perspectives anytime during gameplay by pressing **`V`**, clicking **`🎥 View: Chase [V]` / `🛺 View: Dash Cam [V]`** in the top-right toolbar, or choosing your preferred perspective in the Start Menu:
- **🛺 Auto Dash Cam View (Driver Cockpit POV)**: Places the camera directly inside the Bajaj RE Auto-Rickshaw driver's seat looking out through the front windshield. Complete with canary-yellow and emerald-green cabin A-pillars, a steering handlebar that tilts as you steer, a hanging **Mysuru Mallige jasmine garland & nimbu-mirchi (`🍋🌶️`) charm**, an animated windshield wiper that sweeps during monsoon downpours, and a live `🔴 REC • KA-01-AG-9999 AUTO DASHCAM • 1080P 60FPS` OSD.
- **🎥 Regular Chase View (3rd-Person)**: Classic arcade chase camera showcasing your emerald-and-canary Auto-Rickshaw, its bilingual `ನಮ್ಮ ಬೆಂಗಳೂರು • ಒಂದು ಸೆಕೆಂಡ್ / NAMMA BENGALURU • KA-01-AG-9999` rear canopy plate, and all 3 rotating wheels.

---

### 2. 🛞 100% Grounded Realistic Physics & Finite Route Trips with Final Scoreboard
- **Strictly Grounded Vehicles (No Flying Autos)**: Both your player Auto-Rickshaw and all 20–30 two-way NPC vehicles (`auto_rickshaw.glb`, `bmtc_bus.glb`, `delivery_zepto.glb`, `delivery_blinkit.glb`, `delivery_swiggy.glb`, `commuter_techie.glb`) stay 100% planted on the asphalt highway (`pos.y = 0`). Pressing **`SPACE`** triggers a grounded **⚡ Turbo Gap Boost** to surge through tight traffic gaps.
- **Finite Route Trips & End-of-Trip Scoreboard**: Instead of running to perpetuity, every route has a clear destination distance and live progress bar (`🏁 SILK BOARD → INDIRANAGAR`) on your Namma Auto fare meter:
  - **Low (`ಕಬ್ಬನ್ ಪಾರ್ಕ್ ಬೆಳಿಗ್ಗೆ | Cubbon Park Morning`)**: `1.2 KM` Trip (`MG ROAD → CUBBON PARK`)
  - **Medium (`ಇಂದಿರಾನಗರ ಸಂಜೆ ರಶ್ | Indiranagar 6 PM Rush`)**: `1.8 KM` Trip (`SILK BOARD → INDIRANAGAR`)
  - **Complex (`ಸಿಲ್ಕ್ ಬೋರ್ಡ್ ಟ್ರಾಫಿಕ್ | Silk Board 8 PM Gridlock`)**: `2.5 KM` Trip (`ELECTRONIC CITY → HEBBAL`)
- **Itemized Final Fare Receipt & Driver Rank (`<dialog id="score-modal">`)**: Reaching your destination (or pressing **`E`** / clicking **`🏁 End Trip`** anytime) stops the meter and presents your **Final Driver Score**, **Bengaluru Auto Rank (`S-RANK • ನಮ್ಮ ಆಟೋ ರಾಜ`, `A-RANK`, `B-RANK`)**, **Final Meter Fare (`₹`)**, and an itemized breakdown of Distance Completed, Meter Fare, BTP Traffic Cop Checks Cleared/Dodged, Indie Stray Dogs Dodged, Close Overtakes, and Traffic Bumps/Penalties.

---

### 3. 🪧 Authentic Bilingual Kannada + English Hoardings & Highway Gantries (60:40 Rule)
Every roadside billboard, overhead National Highway gantry, BTP police barricade, rear auto canopy stencil, and HUD banner features authentic **Kannada (`ಕನ್ನಡ`) + English** typography following Bengaluru's iconic **60% Kannada : 40% English** commercial signage standard:

| Hoarding / Signage | Primary Kannada (`ಕನ್ನಡ 60%`) | Secondary English (`40%`) |
| :--- | :--- | :--- |
| **The Rameshwaram Cafe** | `ದಿ ರಾಮೇಶ್ವರಂ ಕೆಫೆ • ಶುದ್ಧ ತುಪ್ಪದ ಪುದಿ ಮಸಾಲೆ ದೋಸೆ ಮತ್ತು ಫಿಲ್ಟರ್ ಕಾಫಿ` | `THE RAMESHWARAM CAFE • PURE GHEE PUDI MASALA DOSA & DEGREE FILTER COFFEE` |
| **Namma Yatri Auto App** | `ನಮ್ಮ ಯಾತ್ರಿ ಆಟೋ ಆಪ್ • ಆಟೋ ಚಾಲಕರ ಸ್ವಂತ ಆಪ್ • ಮೀಟರ್ ಮೇಲೆ ₹೨೦ ಬೇಡ!` | `NAMMA YATRI • AUTO APP • 100% DIRECT TO DRIVER • ZERO COMMISSION` |
| **KMF Nandini Dairy** | `ನಂದಿನಿ ತಾಜಾ ಹಾಲು ಮತ್ತು ಸಿಹಿ • ಪ್ರತಿ ದಿನ ಬೆಳಿಗ್ಗೆ ಪರಿಶುದ್ಧ ಹಾಲು, ಮೊಸರು ಮತ್ತು ತುಪ್ಪ` | `KMF NANDINI MILK & MYSORE PAK • GOOD LIFE PURE MILK, CURD & GHEE SWEETS` |
| **Namma Metro Purple Line** | `ನಮ್ಮ ಮೆಟ್ರೋ - ನೇರಳೆ ಮಾರ್ಗ • ವೈಟ್‌ಫೀಲ್ಡ್ ನಿಂದ ಚಲ್ಲಘಟ್ಟ ವರೆಗೆ ಟ್ರಾಫಿಕ್ ಇಲ್ಲದ ಪ್ರಯಾಣ!` | `NAMMA METRO PURPLE LINE • WHITEFIELD TO CHALLAGHATTA • BEAT SILK BOARD RUSH` |
| **Mysore Sandal Soap** | `ಮೈಸೂರು ಸ್ಯಾಂಡಲ್ ಸೋಪ್ • ಶೇಕಡಾ ೧೦೦ ಪರಿಶುದ್ಧ ಶ್ರೀಗಂಧದ ಎಣ್ಣೆಯ ಸೋಪು` | `MYSORE SANDAL SOAP • 100% PURE NATURAL SANDALWOOD OIL • SINCE 1916` |
| **Bengaluru Traffic Police** | `ಸಂಚಾರ ನಿಯಮ ಪಾಲಿಸಿ • ಸುರಕ್ಷಿತವಾಗಿರಿ • ಮುಂದೆ ತಪಾಸಣೆ ಇದೆ • DL, RC ತೋರಿಸಿ!` | `BENGALURU TRAFFIC POLICE ALERT • SUDDEN LICENSE & E-CHALLAN CHECK AHEAD` |
| **Zepto & Blinkit Super Store** | `ಜೆಪ್ಟೊ ಮತ್ತು ಬ್ಲಿಂಕಿಟ್ ಸೂಪರ್ ಸ್ಟೋರ್ • ಕೊತ್ತಂಬರಿ ಸೊಪ್ಪು, ಹಾಲು ೧೦ ನಿಮಿಷದಲ್ಲಿ!` | `ZEPTO & BLINKIT DARK STORE • FRESH CORIANDER, MILK & SNACKS IN 10 MINUTES` |
| **Vidyarthi Bhavan** | `ವಿದ್ಯಾರ್ಥಿ ಭವನ ಮಸಾಲೆ ದೋಸೆ • ಬೆಂಗಳೂರಿನ ಇತಿಹಾಸ ಪ್ರಸಿದ್ಧ ಗರಿಗರಿ ಬೆಣ್ಣೆ ಮಸಾಲೆ ದೋಸೆ` | `VIDYARTHI BHAVAN HERITAGE • LEGENDARY CRISPY BUTTER MASALA DOSA (SINCE 1943)` |
| **NH-44 Overhead Gantries** | `ಸಿಲ್ಕ್ ಬೋರ್ಡ್ ಜಂಕ್ಷನ್ • ಹೊಸೂರು ರಸ್ತೆ` & `ಹೆಬ್ಬಾಳ ಮೇಲ್ಸೇತುವೆ • ಹೊರ ವರ್ತುಲ ರಸ್ತೆ (ORR)` | `SILK BOARD JUNCTION (ELECTRONIC CITY)` & `HEBBAL FLYOVER (KIAL AIRPORT)` |

---

### 4. 👮‍♂️ Sudden Bengaluru Traffic Police (BTP) License Check (`traffic_police.glb`)
- **Roadside BTP Nakabandi & Barricade**: BTP officers wearing the signature **white pith helmet (topi)**, **lime-green high-visibility reflective vest** over khaki uniform, aviator sunglasses, and holding a **glowing red LED traffic baton** wait beside a bilingual `ಬೆಂಗಳೂರು ಸಂಚಾರ ಪೊಲೀಸ್ / BENGALURU TRAFFIC POLICE` steel barricade with flashing red-and-blue strobe beacons.
- **Sudden Whistle & Step-Out**: As your Auto-Rickshaw approaches within range, the cop blows a shrill **pea-whistle (`"PRRREEEET!"`)**, steps into your lane, waves his red LED baton, and shouts:
  > **👮‍♂️ *"ಏಯ್ ಆಟೋ! ಸೈಡ್ ಹಾಕಿ! DL & RC ತೋರಿಸಿ!"* ("Ey Auto! Pull over! Show your License!")**
- **3 Ways to Handle the BTP Cop**:
  1. **Flash DigiLocker License (`L` key or `🪪 Show DL [L]` HUD button)**: Instantly verifies your DL, RC & Green Emission certificate (`"ಸರಿ ಬಿಡಿ! ಮುಂದೆ ಹೋಗಿ!"`), waves the officer back to the kerb, and awards a **`+₹100` Law-Abiding Auto Bonus (`+300 PTS`)**!
  2. **Swerve & Dodge**: Change lanes cleanly around the checkpost (`+₹60` Evasion Bonus / `+150 PTS`).
  3. **Busted (`e-Challan` Fine)**: Colliding with the officer triggers a police siren burst, brakes your auto hard, and deducts a **`-₹100` e-Challan fine (`-250 PTS`)**!

---

### 5. 🐕 Occasional Darting Bengaluru Stray Dog (`stray_dog.glb`)
- **Authentic Indian Pariah Dog (Indie Doggo)**: Procedurally modeled in Blender with a warm terracotta/tawny coat, white paws, alert perked ears, a collar, and the classic **upward-curled Indie tail**.
- **Sudden Road Darting & 4-Leg Gallop Cycle**: Stray dogs wait near roadside stalls and suddenly bolt across the 6-lane highway with a synthesized double-bark (**`"ಬೌ-ಬೌ! BOW-WOW!"`**) and articulated 4-leg bounding animation.
- **Interactive Reactions**:
  - **Blast Auto Horn (`H`)**: The stray dog barks back and sprints **2x faster** to clear your lane!
  - **Clean Swerve Bonus**: Swerving cleanly around a darting Indie dog awards a **`+₹75` Good Boy Bonus (`+200 PTS`)**!

---

## 🎮 Controls

| Key / HUD Button | Action |
| :--- | :--- |
| **`W` / `↑`** | Accelerate / Full Throttle |
| **`S` / `↓`** | Brake / Slow Down |
| **`A` / `D`** or **`←` / `→`** | Steer Left / Right across the 6 lanes |
| **`V`** or **`🎥 View: Chase [V]`** | **Toggle Camera View between Regular 3rd-Person Chase & First-Person Auto Dash Cam POV** |
| **`L`** or **`🪪 Show DL [L]`** | **Flash DigiLocker DL & RC to BTP Traffic Cop (`+₹100` Bonus!)** |
| **`C`** or **`👮 Cop Check`** | Trigger an immediate sudden BTP Traffic Police license check ahead |
| **`SPACE`** | Trigger grounded **⚡ Turbo Gap Boost** |
| **`H`** or **`📯 Horn`** | Blast the **Bengaluru Auto Horn (`"Pa-Pa-Paarp!"`)** — makes jaywalkers & stray dogs scurry |
| **`E`** or **`🏁 End Trip`** | Stop the meter early and open the **Final Trip Scoreboard** |
| **`R`** | Reattach snapped Auto-Rickshaw wheels |
| **`T`** or **`🌧️ Rain`** | Toggle **Monsoon Downpour & Hydroplaning (`0%` Tire Grip + `1.5x` Surge Fare)** |
| **`ESC`** or **`⚙️ Menu`** | Open Route, Difficulty & Camera Perspective Modal (`Low`, `Medium`, `Peak Hour`) |

---

## 🚀 Quick Start & Testing

### Option 1: Open Directly (Zero-Install Single-File Bundle)
Because [`index.html`](index.html) embeds all **12 Blender `.glb` models** as gzip-compressed base64 fallbacks (`DecompressionStream('gzip')`), you can double-click `index.html` directly in Finder/Explorer or run:
```bash
open index.html
```

### Option 2: Run Local HTTP Server
```bash
python3 -m http.server 8765
```
Then open **`http://localhost:8765/index.html`** in Chrome, Edge, Firefox, or Safari.

#### Optional URL Query Parameters for Instant Testing
- `http://localhost:8765/index.html?autostart=medium&view=dashcam&copcheck=1` — Launch directly into **First-Person Auto Dash Cam POV** with an active BTP Traffic Cop checkpost ahead.
- `http://localhost:8765/index.html?autostart=medium&view=chase&action=1` — Launch directly into **Regular 3rd-Person Chase View** with grounded traffic action.
- `http://localhost:8765/index.html?autostart=medium&gameover=1` — Preview the **End-of-Trip Final Scoreboard & Itemized Auto Fare Receipt**.
- `http://localhost:8765/index.html?autostart=complex&rain=1&snapwheel=1&copcheck=1` — Launch directly into **Peak Hour (`ಸಿಲ್ಕ್ ಬೋರ್ಡ್ ಟ್ರಾಫಿಕ್ | Silk Board 8 PM Gridlock`)** with monsoon downpour, hydroplaning, and BTP nakabandi.

---

## 🛠️ Rebuilding 3D Assets & HTML Bundle

1. **Regenerate all 12 PBR `.glb` models & studio showcase render in Blender**:
   ```bash
   /Applications/Blender.app/Contents/MacOS/Blender --background --python build_assets_blender.py
   ```
   *(Or run `python3 build_assets_blender.py` to execute via a running Blender MCP socket on `127.0.0.1:9876` — see [`agents.md`](agents.md) for details.)*

2. **Compile `index.html` from `build_game_html.py` and `assets/*.glb`**:
   ```bash
   python3 build_game_html.py
   ```

---

## 🤖 Built with Google Antigravity & Google Gemini Models

This project was created end-to-end using **[Google Antigravity](https://antigravity.google/)** and **[Google Gemini models](https://deepmind.google/technologies/gemini/)**:
- **[Google Antigravity (`antigravity.google`)](https://antigravity.google/)**: Agentic AI coding environment used to architect the Three.js WebGL simulation, automate Blender 3D asset generation via MCP, synthesize bilingual Kannada + English highway typography, and verify gameplay via headless browser inspection.
- **[Google Gemini Models (`deepmind.google/technologies/gemini`)](https://deepmind.google/technologies/gemini/) & [Google AI for Developers (`ai.google.dev`)](https://ai.google.dev/)**: Multimodal reasoning, procedural 3D geometry scripting (`bpy`), Web Audio synthesis, and generative visual asset creation.
- **[Blender MCP (`github.com/ahujasid/blender-mcp`)](https://github.com/ahujasid/blender-mcp)**: Model Context Protocol integration connecting Google Antigravity and Gemini models to Blender 5.1 for live 3D `.glb` asset authoring.
