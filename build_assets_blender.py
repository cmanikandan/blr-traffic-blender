import bpy
import math
import os

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(WORKSPACE_DIR, "assets")
SCREENSHOTS_DIR = os.path.join(WORKSPACE_DIR, "screenshots")
os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Scene & Material Helpers
# ---------------------------------------------------------------------------
def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for block in list(bpy.data.meshes):
        if block.users == 0:
            bpy.data.meshes.remove(block)
    for block in list(bpy.data.materials):
        if block.users == 0:
            bpy.data.materials.remove(block)
    for block in list(bpy.data.lights):
        if block.users == 0:
            bpy.data.lights.remove(block)
    for block in list(bpy.data.cameras):
        if block.users == 0:
            bpy.data.cameras.remove(block)

def make_mat(name, color, roughness=0.35, metallic=0.0, emission=None, emission_strength=0.0):
    mat = bpy.data.materials.get(name)
    if mat is None:
        mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = next((n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None)
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (color[0], color[1], color[2], 1.0)
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Metallic"].default_value = metallic
        if "Coat Weight" in bsdf.inputs and roughness < 0.35:
            bsdf.inputs["Coat Weight"].default_value = 0.35
        if emission and emission_strength > 0.0:
            if "Emission Color" in bsdf.inputs:
                bsdf.inputs["Emission Color"].default_value = (emission[0], emission[1], emission[2], 1.0)
            elif "Emission" in bsdf.inputs:
                bsdf.inputs["Emission"].default_value = (emission[0], emission[1], emission[2], 1.0)
            if "Emission Strength" in bsdf.inputs:
                bsdf.inputs["Emission Strength"].default_value = emission_strength
    return mat

def shade_smooth_auto(obj):
    if obj and obj.type == 'MESH' and obj.data:
        for poly in obj.data.polygons:
            poly.use_smooth = True

def add_box(name, size, loc, mat, rot=(0, 0, 0), bevel=0.0, segments=2):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc, rotation=rot)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (size[0], size[1], size[2])
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    if bevel > 0:
        mod = obj.modifiers.new(name="Bevel", type='BEVEL')
        mod.width = bevel
        mod.segments = segments
        bpy.ops.object.modifier_apply(modifier=mod.name)
        shade_smooth_auto(obj)
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)
    return obj

def add_cyl(name, radius, depth, loc, mat, rot=(0, 0, 0), vertices=20):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vertices, radius=radius, depth=depth, location=loc, rotation=rot
    )
    obj = bpy.context.active_object
    obj.name = name
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    shade_smooth_auto(obj)
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)
    return obj

def add_sphere(name, radius, loc, mat, scale=(1, 1, 1), segments=20, ring_count=14):
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=segments, ring_count=ring_count, radius=radius, location=loc
    )
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    shade_smooth_auto(obj)
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)
    return obj

def add_cone(name, r1, r2, depth, loc, mat, rot=(0, 0, 0), vertices=18):
    bpy.ops.mesh.primitive_cone_add(
        vertices=vertices, radius1=r1, radius2=r2, depth=depth, location=loc, rotation=rot
    )
    obj = bpy.context.active_object
    obj.name = name
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    shade_smooth_auto(obj)
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)
    return obj

def join_objects(objs, name, apply_loc=True):
    if not objs:
        return None
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    if len(objs) > 1:
        bpy.ops.object.join()
    joined = bpy.context.active_object
    joined.name = name
    if apply_loc:
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    return joined

def create_wheel(name, loc, radius=0.28, width=0.15, mat_tire=None, mat_rim=None, mat_hub=None, parent=None):
    parts = []
    tire = add_cyl(f"{name}_tire", radius, width, (0, 0, 0), mat_tire, rot=(0, math.pi / 2, 0), vertices=20)
    rim = add_cyl(f"{name}_rim", radius * 0.62, width * 1.06, (0, 0, 0), mat_rim, rot=(0, math.pi / 2, 0), vertices=16)
    hub = add_cyl(f"{name}_hub", radius * 0.30, width * 1.15, (0, 0, 0), mat_hub, rot=(0, math.pi / 2, 0), vertices=12)
    spoke1 = add_box(f"{name}_s1", (width * 1.10, radius * 0.95, radius * 0.16), (0, 0, 0), mat_rim)
    spoke2 = add_box(f"{name}_s2", (width * 1.10, radius * 0.16, radius * 0.95), (0, 0, 0), mat_rim)
    parts.extend([tire, rim, hub, spoke1, spoke2])
    wheel = join_objects(parts, name, apply_loc=False)
    wheel.location = loc
    if parent:
        wheel.parent = parent
    return wheel

def export_hierarchy_glb(root_obj, filename):
    bpy.ops.object.select_all(action='DESELECT')
    def select_tree(o):
        o.select_set(True)
        for ch in o.children:
            select_tree(ch)
    select_tree(root_obj)
    bpy.context.view_layer.objects.active = root_obj

    for path in (os.path.join(ASSETS_DIR, filename), os.path.join(WORKSPACE_DIR, filename)):
        bpy.ops.export_scene.gltf(
            filepath=path,
            export_format='GLB',
            use_selection=True,
            export_yup=True,
            export_apply=True
        )
    print(f"Exported {filename}")

# ---------------------------------------------------------------------------
# Authentic Bengaluru PBR Color Palette
# ---------------------------------------------------------------------------
def init_materials():
    M = {}
    # Authentic Bengaluru Bajaj RE Auto-Rickshaw colors (Automotive Gloss Clearcoat)
    M['auto_green'] = make_mat("Auto_EmeraldGreen", (0.0, 0.54, 0.21), roughness=0.18, metallic=0.22)
    M['auto_yellow'] = make_mat("Auto_CanaryYellow", (1.0, 0.78, 0.0), roughness=0.20, metallic=0.15)
    M['auto_hood_yellow'] = make_mat("Auto_HoodYellow", (0.96, 0.72, 0.02), roughness=0.42, metallic=0.02)
    M['trim_black'] = make_mat("Trim_Black", (0.08, 0.09, 0.11), roughness=0.55)
    M['tire_black'] = make_mat("Tire_Rubber", (0.05, 0.05, 0.06), roughness=0.82)
    M['steel_rim'] = make_mat("Steel_Rim", (0.80, 0.83, 0.88), roughness=0.20, metallic=0.88)
    M['chrome'] = make_mat("Chrome_Metal", (0.95, 0.96, 0.98), roughness=0.10, metallic=0.96)
    M['glass_dark'] = make_mat("Tinted_Glass", (0.10, 0.18, 0.26), roughness=0.08, metallic=0.45)
    M['glass_cyan'] = make_mat("Windshield_Cyan", (0.28, 0.65, 0.85), roughness=0.08, metallic=0.35)
    M['seat_brown'] = make_mat("Rexine_Brown", (0.34, 0.15, 0.05), roughness=0.48)
    M['headlight'] = make_mat("Headlight_Warm", (1.0, 0.97, 0.85), roughness=0.08, emission=(1.0, 0.95, 0.75), emission_strength=1.2)
    M['taillight'] = make_mat("Taillight_Red", (0.94, 0.03, 0.03), roughness=0.15, emission=(0.96, 0.02, 0.02), emission_strength=0.65)
    M['amber_glow'] = make_mat("Indicator_Amber", (1.0, 0.50, 0.0), roughness=0.15, emission=(1.0, 0.45, 0.0), emission_strength=0.65)

    # Delivery & Commuter Colors
    M['swiggy_orange'] = make_mat("Swiggy_Orange", (0.99, 0.36, 0.04), roughness=0.22, emission=(0.99, 0.36, 0.04), emission_strength=0.25)
    M['zepto_green'] = make_mat("Zepto_NeonGreen", (0.10, 0.96, 0.38), roughness=0.20, emission=(0.10, 0.96, 0.38), emission_strength=0.35)
    M['zepto_purple'] = make_mat("Zepto_Purple", (0.32, 0.08, 0.56), roughness=0.24, metallic=0.18)
    M['blinkit_yellow'] = make_mat("Blinkit_Yellow", (1.0, 0.88, 0.02), roughness=0.22, emission=(1.0, 0.86, 0.02), emission_strength=0.30)
    M['scooter_white'] = make_mat("Scooter_PearlWhite", (0.94, 0.96, 0.98), roughness=0.18, metallic=0.25)
    M['scooter_charcoal'] = make_mat("Scooter_Charcoal", (0.16, 0.18, 0.22), roughness=0.26, metallic=0.42)
    M['scooter_teal'] = make_mat("Scooter_ActivaBlue", (0.08, 0.44, 0.68), roughness=0.20, metallic=0.42)
    M['jeans'] = make_mat("Denim_Jeans", (0.13, 0.21, 0.38), roughness=0.68)
    M['techie_shirt'] = make_mat("Techie_SkyShirt", (0.26, 0.60, 0.90), roughness=0.48)
    M['skin'] = make_mat("Skin_Tone", (0.70, 0.46, 0.32), roughness=0.50)

    # Authentic BMTC Bus Colors
    M['bmtc_blue'] = make_mat("BMTC_RoyalBlue", (0.02, 0.36, 0.76), roughness=0.20, metallic=0.22)
    M['bmtc_navy'] = make_mat("BMTC_NavyStripe", (0.01, 0.16, 0.42), roughness=0.25, metallic=0.28)
    M['bmtc_white'] = make_mat("BMTC_IvoryWhite", (0.95, 0.96, 0.98), roughness=0.24, metallic=0.10)

    # Landmarks
    M['granite_light'] = make_mat("Vidhana_Granite", (0.86, 0.83, 0.77), roughness=0.50)
    M['granite_dark'] = make_mat("Vidhana_StoneDark", (0.66, 0.63, 0.57), roughness=0.60)
    M['gold_emblem'] = make_mat("Gold_Dome", (1.0, 0.78, 0.16), roughness=0.18, metallic=0.90, emission=(1.0, 0.72, 0.12), emission_strength=0.9)
    M['tricolor_saffron'] = make_mat("Saffron_Light", (1.0, 0.42, 0.05), roughness=0.35, emission=(1.0, 0.42, 0.05), emission_strength=0.85)
    M['tricolor_green'] = make_mat("IndiaGreen_Light", (0.05, 0.68, 0.22), roughness=0.35, emission=(0.05, 0.68, 0.22), emission_strength=0.85)
    M['metro_concrete'] = make_mat("Viaduct_Concrete", (0.68, 0.70, 0.73), roughness=0.68)
    M['metro_silver'] = make_mat("Metro_Stainless", (0.85, 0.88, 0.92), roughness=0.18, metallic=0.85)
    M['metro_purple'] = make_mat("NammaMetro_Purple", (0.48, 0.14, 0.78), roughness=0.24, emission=(0.48, 0.14, 0.78), emission_strength=0.38)
    M['window_warm'] = make_mat("Lit_Window", (1.0, 0.90, 0.65), roughness=0.15, emission=(1.0, 0.86, 0.55), emission_strength=1.5)
    M['highway_green'] = make_mat("NH_SignGreen", (0.0, 0.38, 0.20), roughness=0.28, metallic=0.15)
    M['sign_white'] = make_mat("Sign_ReflectiveWhite", (0.98, 0.99, 1.0), roughness=0.18, emission=(0.95, 0.98, 1.0), emission_strength=0.5)

    # Bengaluru Traffic Police (BTP) Materials
    M['btp_white'] = make_mat("BTP_ShirtWhite", (0.96, 0.97, 0.99), roughness=0.38)
    M['btp_khaki'] = make_mat("BTP_KhakiPants", (0.66, 0.55, 0.38), roughness=0.55)
    M['btp_neon_vest'] = make_mat("BTP_NeonLimeVest", (0.58, 0.98, 0.08), roughness=0.28, emission=(0.45, 0.92, 0.05), emission_strength=0.32)
    M['btp_baton_red'] = make_mat("BTP_BatonRedGlow", (1.0, 0.08, 0.12), roughness=0.15, emission=(1.0, 0.05, 0.08), emission_strength=1.15)
    M['btp_blue_beacon'] = make_mat("BTP_BlueStrobe", (0.08, 0.45, 1.0), roughness=0.15, emission=(0.08, 0.45, 1.0), emission_strength=1.15)

    # Bengaluru Indie Stray Dog Materials
    M['dog_coat'] = make_mat("Dog_IndieTan", (0.68, 0.40, 0.20), roughness=0.62)
    M['dog_white'] = make_mat("Dog_ChestWhite", (0.94, 0.92, 0.88), roughness=0.58)
    M['dog_snout'] = make_mat("Dog_DarkMuzzle", (0.20, 0.14, 0.11), roughness=0.52)
    M['dog_collar'] = make_mat("Dog_RedCollar", (0.88, 0.12, 0.15), roughness=0.35)
    return M

# ---------------------------------------------------------------------------
# 1. Authentic Bengaluru Auto-Rickshaw (Bajaj RE Compact 4S)
# ---------------------------------------------------------------------------
def build_auto_rickshaw(M):
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
    root = bpy.context.active_object
    root.name = "Auto_Rickshaw"

    parts = []
    parts.append(add_box("floor", (1.24, 2.05, 0.12), (0, -0.04, 0.32), M['trim_black'], bevel=0.02))
    parts.append(add_box("green_tub_rear", (1.22, 1.26, 0.52), (0, -0.46, 0.58), M['auto_green'], bevel=0.09, segments=3))
    parts.append(add_box("front_green", (0.88, 0.62, 0.46), (0, 0.78, 0.54), M['auto_green'], bevel=0.10, segments=3))
    parts.append(add_box("front_mudguard", (0.22, 0.44, 0.14), (0, 1.02, 0.54), M['auto_green'], bevel=0.06, segments=3))
    parts.append(add_box("front_mud_stripe", (0.06, 0.45, 0.15), (0, 1.02, 0.55), M['chrome'], bevel=0.02))

    # Canary Yellow Upper Body Beltline & Front Shield
    parts.append(add_box("front_yellow_shield", (0.94, 0.54, 0.44), (0, 0.76, 0.94), M['auto_yellow'], bevel=0.09, segments=3))
    parts.append(add_box("rear_yellow_belt", (1.38, 1.24, 0.28), (0, -0.46, 0.95), M['auto_yellow'], bevel=0.07, segments=3))
    parts.append(add_box("sill_l", (0.12, 0.75, 0.22), (-0.60, 0.22, 0.42), M['auto_green'], bevel=0.03))
    parts.append(add_box("sill_r", (0.12, 0.75, 0.22), (0.60, 0.22, 0.42), M['auto_green'], bevel=0.03))

    # Bright Yellow Rounded Canopy Hood + Roof Carrier Rack
    parts.append(add_box("canopy_roof_top", (1.34, 1.88, 0.18), (0, -0.08, 1.72), M['auto_hood_yellow'], bevel=0.09, segments=3))
    parts.append(add_box("canopy_rear_back", (1.32, 0.16, 0.68), (0, -0.98, 1.38), M['auto_hood_yellow'], rot=(-0.10, 0, 0), bevel=0.06, segments=3))
    parts.append(add_box("seam_l", (0.05, 1.86, 0.05), (-0.66, -0.08, 1.66), M['trim_black']))
    parts.append(add_box("seam_r", (0.05, 1.86, 0.05), (0.66, -0.08, 1.66), M['trim_black']))
    parts.append(add_box("rear_window", (0.78, 0.06, 0.28), (0, -1.04, 1.44), M['glass_dark'], rot=(-0.10, 0, 0), bevel=0.03))

    # Chrome Roof Carrier Rails (Classic Bengaluru Auto detail)
    parts.append(add_cyl("rack_l", 0.018, 1.20, (-0.52, -0.15, 1.83), M['chrome'], rot=(math.pi / 2, 0, 0), vertices=10))
    parts.append(add_cyl("rack_r", 0.018, 1.20, (0.52, -0.15, 1.83), M['chrome'], rot=(math.pi / 2, 0, 0), vertices=10))

    # Rear Spare Wheel & Engine Door Details
    parts.append(add_cyl("spare_tire", 0.25, 0.13, (0, -1.12, 0.78), M['tire_black'], rot=(math.pi / 2, 0, 0), vertices=18))
    parts.append(add_cyl("spare_hub", 0.15, 0.15, (0, -1.13, 0.78), M['auto_yellow'], rot=(math.pi / 2, 0, 0), vertices=14))
    parts.append(add_box("rear_bumper", (1.38, 0.12, 0.10), (0, -1.12, 0.36), M['chrome'], bevel=0.03))
    parts.append(add_box("mudflap_l", (0.22, 0.03, 0.18), (-0.58, -1.06, 0.25), M['trim_black']))
    parts.append(add_box("mudflap_r", (0.22, 0.03, 0.18), (0.58, -1.06, 0.25), M['trim_black']))
    parts.append(add_box("tl_l", (0.20, 0.06, 0.11), (-0.48, -1.09, 0.54), M['taillight'], bevel=0.02))
    parts.append(add_box("tl_r", (0.20, 0.06, 0.11), (0.48, -1.09, 0.54), M['taillight'], bevel=0.02))
    parts.append(add_box("ind_rl", (0.12, 0.06, 0.11), (-0.32, -1.09, 0.54), M['amber_glow'], bevel=0.02))
    parts.append(add_box("ind_rr", (0.12, 0.06, 0.11), (0.32, -1.09, 0.54), M['amber_glow'], bevel=0.02))
    parts.append(add_box("plate_rear", (0.38, 0.04, 0.12), (-0.42, -1.10, 0.72), M['auto_yellow']))
    parts.append(add_cyl("exhaust_pipe", 0.035, 0.28, (0.46, -1.14, 0.28), M['chrome'], rot=(math.pi / 2, 0, 0), vertices=10))

    # Front Windshield Frame, Glass, Wiper & Pillars
    parts.append(add_box("ws_frame_l", (0.07, 0.07, 0.58), (-0.44, 0.78, 1.40), M['auto_yellow'], rot=(0.20, 0, 0)))
    parts.append(add_box("ws_frame_r", (0.07, 0.07, 0.58), (0.44, 0.78, 1.40), M['auto_yellow'], rot=(0.20, 0, 0)))
    parts.append(add_box("ws_glass", (0.82, 0.04, 0.50), (0, 0.78, 1.40), M['glass_cyan'], rot=(0.20, 0, 0)))
    parts.append(add_box("wiper", (0.03, 0.05, 0.36), (0.04, 0.81, 1.40), M['trim_black'], rot=(0.20, 0.35, 0)))
    parts.append(add_box("mid_pillar_l", (0.06, 0.06, 0.64), (-0.62, -0.05, 1.38), M['trim_black']))
    parts.append(add_box("mid_pillar_r", (0.06, 0.06, 0.64), (0.62, -0.05, 1.38), M['trim_black']))

    # Interior Cushioned Seats, Digital Fare Meter & Driver in Khaki Shirt
    parts.append(add_box("driver_seat", (0.46, 0.40, 0.16), (0, 0.32, 0.72), M['seat_brown'], bevel=0.03))
    parts.append(add_box("pass_seat", (1.16, 0.48, 0.18), (0, -0.50, 0.74), M['seat_brown'], bevel=0.03))
    parts.append(add_box("pass_backrest", (1.16, 0.14, 0.40), (0, -0.78, 1.02), M['seat_brown'], bevel=0.03))
    parts.append(add_box("fare_meter_box", (0.14, 0.12, 0.12), (-0.22, 0.62, 1.02), M['trim_black'], bevel=0.02))
    parts.append(add_box("driver_torso", (0.38, 0.24, 0.46), (0, 0.28, 1.05), M['btp_khaki'], bevel=0.04))
    parts.append(add_sphere("driver_head", 0.15, (0, 0.28, 1.40), M['skin'], segments=14, ring_count=10))

    # Front Iconic Single Round Headlight & Turn Indicators
    parts.append(add_cyl("hl_bezel", 0.14, 0.12, (0, 1.08, 0.76), M['chrome'], rot=(math.pi / 2, 0, 0), vertices=16))
    parts.append(add_cyl("hl_lens", 0.11, 0.05, (0, 1.13, 0.76), M['headlight'], rot=(math.pi / 2, 0, 0), vertices=16))
    parts.append(add_sphere("ind_fl", 0.055, (-0.38, 1.02, 0.88), M['amber_glow'], segments=12, ring_count=8))
    parts.append(add_sphere("ind_fr", 0.055, (0.38, 1.02, 0.88), M['amber_glow'], segments=12, ring_count=8))
    parts.append(add_box("mir_l", (0.14, 0.04, 0.10), (-0.55, 0.76, 1.34), M['chrome']))
    parts.append(add_box("mir_r", (0.14, 0.04, 0.10), (0.55, 0.76, 1.34), M['chrome']))

    body = join_objects(parts, "Body_Chassis", apply_loc=True)
    body.parent = root

    create_wheel("Wheel_Front", (0.0, 1.02, 0.27), radius=0.27, width=0.14,
                 mat_tire=M['tire_black'], mat_rim=M['steel_rim'], mat_hub=M['auto_yellow'], parent=root)
    create_wheel("Wheel_Rear_L", (-0.65, -0.70, 0.28), radius=0.28, width=0.15,
                 mat_tire=M['tire_black'], mat_rim=M['steel_rim'], mat_hub=M['auto_green'], parent=root)
    create_wheel("Wheel_Rear_R", (0.65, -0.70, 0.28), radius=0.28, width=0.15,
                 mat_tire=M['tire_black'], mat_rim=M['steel_rim'], mat_hub=M['auto_green'], parent=root)

    export_hierarchy_glb(root, "auto_rickshaw.glb")
    return root

# ---------------------------------------------------------------------------
# 2. Scooters (Swiggy, Zepto, Blinkit Delivery Riders & IT Techie Commuter)
# ---------------------------------------------------------------------------
def build_scooter_variant(name, filename, body_mat, jacket_mat, cargo_mat, has_cargo_box, is_techie, M):
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
    root = bpy.context.active_object
    root.name = name

    parts = []
    parts.append(add_box(f"{name}_fb", (0.42, 0.85, 0.10), (0, 0.05, 0.26), M['trim_black'], bevel=0.02))
    parts.append(add_box(f"{name}_rs", (0.48, 0.78, 0.42), (0, -0.45, 0.52), body_mat, rot=(0.14, 0, 0), bevel=0.07, segments=3))
    parts.append(add_box(f"{name}_fs", (0.46, 0.26, 0.74), (0, 0.55, 0.62), body_mat, rot=(-0.22, 0, 0), bevel=0.06, segments=3))
    parts.append(add_box(f"{name}_ff", (0.24, 0.36, 0.14), (0, 0.72, 0.38), body_mat, bevel=0.05, segments=2))
    parts.append(add_box(f"{name}_seat", (0.38, 0.72, 0.12), (0, -0.38, 0.76), M['trim_black'], bevel=0.03))
    parts.append(add_cyl(f"{name}_stem", 0.035, 0.35, (0, 0.46, 0.98), M['chrome'], rot=(-0.2, 0, 0), vertices=10))
    parts.append(add_cyl(f"{name}_hbar", 0.025, 0.62, (0, 0.43, 1.12), M['trim_black'], rot=(0, math.pi / 2, 0), vertices=10))
    parts.append(add_sphere(f"{name}_hl", 0.09, (0, 0.52, 1.12), M['headlight'], segments=12, ring_count=10))
    parts.append(add_box(f"{name}_tl", (0.22, 0.06, 0.09), (0, -0.86, 0.62), M['taillight'], bevel=0.02))
    parts.append(add_box(f"{name}_plate", (0.24, 0.03, 0.08), (0, -0.88, 0.46), M['sign_white']))

    torso_tilt = 0.20 if has_cargo_box else 0.08
    parts.append(add_box(f"{name}_leg_l", (0.14, 0.38, 0.14), (-0.14, -0.05, 0.74), M['jeans'], rot=(0.2, 0, 0)))
    parts.append(add_box(f"{name}_leg_r", (0.14, 0.38, 0.14), (0.14, -0.05, 0.74), M['jeans'], rot=(0.2, 0, 0)))
    parts.append(add_box(f"{name}_shin_l", (0.12, 0.12, 0.40), (-0.14, 0.14, 0.50), M['jeans'], rot=(-0.15, 0, 0)))
    parts.append(add_box(f"{name}_shin_r", (0.12, 0.12, 0.40), (0.14, 0.14, 0.50), M['jeans'], rot=(-0.15, 0, 0)))
    parts.append(add_box(f"{name}_torso", (0.42, 0.26, 0.54), (0, -0.18, 1.08), jacket_mat, rot=(torso_tilt, 0, 0), bevel=0.05))
    parts.append(add_cyl(f"{name}_arm_l", 0.055, 0.52, (-0.23, 0.12, 1.18), jacket_mat, rot=(1.15, 0, -0.15), vertices=10))
    parts.append(add_cyl(f"{name}_arm_r", 0.055, 0.52, (0.23, 0.12, 1.18), jacket_mat, rot=(1.15, 0, 0.15), vertices=10))
    parts.append(add_sphere(f"{name}_helmet", 0.19, (0, -0.10, 1.48), cargo_mat if has_cargo_box else M['trim_black'], segments=16, ring_count=12))
    parts.append(add_box(f"{name}_visor", (0.26, 0.10, 0.11), (0, 0.06, 1.48), M['glass_dark'], bevel=0.02))

    if has_cargo_box:
        parts.append(add_box(f"{name}_cargo", (0.60, 0.54, 0.58), (0, -0.64, 1.14), cargo_mat, bevel=0.06, segments=3))
        parts.append(add_box(f"{name}_stripe_b", (0.62, 0.56, 0.07), (0, -0.64, 1.24), M['sign_white']))
        parts.append(add_box(f"{name}_rack", (0.44, 0.48, 0.05), (0, -0.64, 0.83), M['steel_rim']))

    if is_techie:
        parts.append(add_box(f"{name}_backpack", (0.34, 0.18, 0.42), (0, -0.36, 1.12), M['trim_black'], rot=(torso_tilt, 0, 0), bevel=0.05))
        parts.append(add_box(f"{name}_lanyard", (0.14, 0.04, 0.24), (0, -0.04, 1.15), M['bmtc_blue'], rot=(torso_tilt, 0, 0)))
        parts.append(add_box(f"{name}_idcard", (0.09, 0.02, 0.11), (0, -0.02, 1.00), M['sign_white'], rot=(torso_tilt, 0, 0)))

    body = join_objects(parts, "Scooter_Body", apply_loc=True)
    body.parent = root

    create_wheel("Wheel_Front", (0.0, 0.68, 0.24), radius=0.24, width=0.11,
                 mat_tire=M['tire_black'], mat_rim=M['steel_rim'], mat_hub=cargo_mat, parent=root)
    create_wheel("Wheel_Rear", (0.0, -0.58, 0.24), radius=0.24, width=0.12,
                 mat_tire=M['tire_black'], mat_rim=M['steel_rim'], mat_hub=cargo_mat, parent=root)

    export_hierarchy_glb(root, filename)
    return root

# ---------------------------------------------------------------------------
# 3. Authentic BMTC Bus (500D Silk Board - Hebbal Volvo/Suvarna Livery)
# ---------------------------------------------------------------------------
def build_bmtc_bus(M):
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
    root = bpy.context.active_object
    root.name = "BMTC_Bus"

    parts = []
    parts.append(add_box("bus_lower", (2.46, 7.60, 1.25), (0, 0, 1.00), M['bmtc_blue'], bevel=0.09, segments=3))
    parts.append(add_box("bus_belt", (2.48, 7.62, 0.18), (0, 0, 1.62), M['bmtc_navy']))
    parts.append(add_box("bus_upper", (2.44, 7.56, 1.12), (0, 0, 2.22), M['bmtc_white'], bevel=0.07, segments=3))
    parts.append(add_box("bus_roof", (2.38, 7.48, 0.24), (0, 0, 2.86), M['bmtc_blue'], bevel=0.09, segments=3))
    parts.append(add_box("bus_ac", (1.60, 3.10, 0.24), (0, 0.20, 3.06), M['bmtc_white'], bevel=0.07, segments=3))

    # Front Face (+Y in Blender -> -Z Forward in Three.js)
    parts.append(add_box("bus_ws_front", (2.22, 0.08, 0.95), (0, 3.77, 2.18), M['glass_cyan']))
    parts.append(add_box("dest_f_bg", (1.92, 0.10, 0.28), (0, 3.78, 2.76), M['trim_black']))
    parts.append(add_box("dest_f_led", (1.76, 0.12, 0.16), (0, 3.79, 2.76), M['amber_glow']))
    parts.append(add_box("hl_fl", (0.38, 0.08, 0.18), (-0.86, 3.80, 0.78), M['headlight']))
    parts.append(add_box("hl_fr", (0.38, 0.08, 0.18), (0.86, 3.80, 0.78), M['headlight']))
    parts.append(add_box("bumper_f", (2.52, 0.20, 0.24), (0, 3.82, 0.48), M['trim_black'], bevel=0.04))

    # Rear Face (-Y in Blender -> +Z Rear in Three.js)
    parts.append(add_box("bus_ws_rear", (2.06, 0.08, 0.78), (0, -3.77, 2.24), M['glass_dark']))
    parts.append(add_box("dest_r_bg", (1.65, 0.10, 0.26), (0, -3.78, 2.74), M['trim_black']))
    parts.append(add_box("dest_r_led", (1.48, 0.12, 0.15), (0, -3.79, 2.74), M['amber_glow']))
    parts.append(add_box("rear_grille", (1.35, 0.06, 0.52), (0, -3.80, 0.98), M['trim_black']))
    parts.append(add_box("rear_plate", (0.48, 0.06, 0.14), (0, -3.81, 0.62), M['auto_yellow']))
    parts.append(add_box("tl_rl", (0.24, 0.08, 0.42), (-0.98, -3.80, 1.02), M['taillight'], bevel=0.02))
    parts.append(add_box("tl_rr", (0.24, 0.08, 0.42), (0.98, -3.80, 1.02), M['taillight'], bevel=0.02))
    parts.append(add_box("ind_rl", (0.22, 0.08, 0.18), (-0.98, -3.80, 1.36), M['amber_glow'], bevel=0.02))
    parts.append(add_box("ind_rr", (0.22, 0.08, 0.18), (0.98, -3.80, 1.36), M['amber_glow'], bevel=0.02))
    parts.append(add_box("bumper_r", (2.52, 0.20, 0.24), (0, -3.82, 0.48), M['trim_black'], bevel=0.04))

    for i in range(6):
        wy = -2.85 + i * 1.14
        parts.append(add_box(f"win_l_{i}", (0.06, 0.92, 0.78), (-1.21, wy, 2.22), M['glass_dark']))
        parts.append(add_box(f"win_r_{i}", (0.06, 0.92, 0.78), (1.21, wy, 2.22), M['glass_dark']))

    body = join_objects(parts, "Bus_Body", apply_loc=True)
    body.parent = root

    create_wheel("Wheel_FL", (-1.18, 2.25, 0.48), radius=0.48, width=0.26,
                 mat_tire=M['tire_black'], mat_rim=M['steel_rim'], mat_hub=M['bmtc_blue'], parent=root)
    create_wheel("Wheel_FR", (1.18, 2.25, 0.48), radius=0.48, width=0.26,
                 mat_tire=M['tire_black'], mat_rim=M['steel_rim'], mat_hub=M['bmtc_blue'], parent=root)
    create_wheel("Wheel_RL", (-1.18, -2.15, 0.48), radius=0.48, width=0.28,
                 mat_tire=M['tire_black'], mat_rim=M['steel_rim'], mat_hub=M['bmtc_blue'], parent=root)
    create_wheel("Wheel_RR", (1.18, -2.15, 0.48), radius=0.48, width=0.28,
                 mat_tire=M['tire_black'], mat_rim=M['steel_rim'], mat_hub=M['bmtc_blue'], parent=root)

    export_hierarchy_glb(root, "bmtc_bus.glb")
    return root

# ---------------------------------------------------------------------------
# 4. Dynamic Landmark 1: Vidhana Soudha Facade
# ---------------------------------------------------------------------------
def build_vidhana_soudha(M):
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
    root = bpy.context.active_object
    root.name = "Vidhana_Soudha"

    parts = []
    parts.append(add_box("plinth_1", (28.0, 12.0, 1.2), (0, 0, 0.6), M['granite_dark']))
    parts.append(add_box("plinth_2", (26.0, 10.5, 1.2), (0, -0.3, 1.8), M['granite_light']))
    for s in range(6):
        parts.append(add_box(f"step_{s}", (10.5, 3.6 - s * 0.5, 0.35), (0, 4.8 - s * 0.25, 0.2 + s * 0.35), M['granite_light']))

    parts.append(add_box("main_hall", (24.0, 8.2, 7.5), (0, -0.8, 6.1), M['granite_light'], bevel=0.08))
    parts.append(add_box("cornice_1", (25.2, 9.0, 0.65), (0, -0.8, 10.0), M['granite_dark']))
    parts.append(add_box("cornice_2", (24.6, 8.6, 0.55), (0, -0.8, 10.6), M['granite_light']))
    parts.append(add_box("frieze_gold", (11.2, 0.35, 0.55), (0, 3.4, 9.5), M['gold_emblem']))
    parts.append(add_box("glow_saffron", (24.2, 0.15, 0.25), (0, 3.35, 9.9), M['tricolor_saffron']))
    parts.append(add_box("glow_green", (24.2, 0.15, 0.25), (0, 3.35, 2.6), M['tricolor_green']))

    parts.append(add_box("portico_base", (11.5, 3.2, 0.8), (0, 2.2, 2.6), M['granite_dark']))
    parts.append(add_box("portico_roof", (12.0, 3.6, 0.9), (0, 2.2, 9.2), M['granite_dark']))
    for i in range(8):
        px = -4.9 + i * 1.4
        parts.append(add_cyl(f"pillar_{i}", 0.32, 5.8, (px, 3.4, 5.9), M['granite_light'], vertices=14))
        parts.append(add_box(f"cap_{i}", (0.85, 0.85, 0.45), (px, 3.4, 8.6), M['granite_dark']))

    for side in (-1, 1):
        for w in range(4):
            wx = side * (6.8 + w * 1.4)
            for floor_z in (4.5, 7.2):
                parts.append(add_box(f"win_{side}_{w}_{floor_z}", (0.75, 0.2, 1.5), (wx, 3.25, floor_z), M['window_warm']))

    parts.append(add_cyl("central_drum", 3.6, 3.2, (0, -0.5, 12.2), M['granite_light'], vertices=24))
    parts.append(add_cyl("central_rim", 3.9, 0.45, (0, -0.5, 13.8), M['granite_dark'], vertices=24))
    parts.append(add_sphere("central_dome", 3.5, (0, -0.5, 14.2), M['granite_light'], scale=(1.0, 1.0, 1.15), segments=24, ring_count=14))
    parts.append(add_cyl("finial_ped", 0.65, 1.1, (0, -0.5, 18.2), M['gold_emblem'], vertices=14))
    parts.append(add_sphere("finial_top", 0.85, (0, -0.5, 19.1), M['gold_emblem'], scale=(0.8, 0.8, 1.3), segments=14, ring_count=10))

    for cx in (-9.8, 9.8):
        for cy in (-3.2, 1.8):
            parts.append(add_cyl(f"ch_base_{cx}_{cy}", 1.45, 2.2, (cx, cy, 11.8), M['granite_dark'], vertices=14))
            parts.append(add_sphere(f"ch_dome_{cx}_{cy}", 1.4, (cx, cy, 13.0), M['granite_light'], scale=(1.0, 1.0, 1.1), segments=14, ring_count=10))
            parts.append(add_cone(f"ch_sp_{cx}_{cy}", 0.25, 0.02, 0.9, (cx, cy, 14.6), M['gold_emblem'], vertices=10))

    building = join_objects(parts, "Vidhana_Soudha_Mesh", apply_loc=True)
    building.parent = root
    export_hierarchy_glb(root, "vidhana_soudha.glb")
    return root

# ---------------------------------------------------------------------------
# 5. Dynamic Landmark 2: Namma Metro Station Platform & Purple Line Train
# ---------------------------------------------------------------------------
def build_metro_station(M):
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
    root = bpy.context.active_object
    root.name = "Namma_Metro_Station"

    station_parts = []
    for py in (-12.0, 0.0, 12.0):
        station_parts.append(add_cyl(f"metro_pier_{py}", 1.15, 7.2, (0, py, 3.6), M['metro_concrete'], vertices=14))
        station_parts.append(add_box(f"metro_cap_{py}", (7.2, 2.2, 1.3), (0, py, 7.4), M['metro_concrete'], bevel=0.08))

    station_parts.append(add_box("viaduct_deck", (7.8, 36.0, 1.1), (0, 0, 8.4), M['metro_concrete']))
    station_parts.append(add_box("platform_floor", (9.2, 28.0, 0.45), (0, 0, 9.1), M['granite_dark']))
    station_parts.append(add_box("wall_l", (0.25, 36.0, 1.25), (-4.0, 0, 9.5), M['metro_purple']))
    station_parts.append(add_box("wall_r", (0.25, 36.0, 1.25), (4.0, 0, 9.5), M['metro_purple']))

    for ry in range(-12, 13, 4):
        station_parts.append(add_box(f"roof_rib_{ry}", (9.8, 0.35, 0.45), (0, ry, 13.4), M['metro_concrete']))
        station_parts.append(add_cyl(f"st_pil_l_{ry}", 0.18, 4.2, (-3.8, ry, 11.3), M['steel_rim'], vertices=10))
        station_parts.append(add_cyl(f"st_pil_r_{ry}", 0.18, 4.2, (3.8, ry, 11.3), M['steel_rim'], vertices=10))

    station_parts.append(add_box("canopy_center", (6.2, 28.5, 0.35), (0, 0, 13.75), M['metro_silver']))
    station_parts.append(add_box("canopy_wing_l", (2.4, 28.5, 0.28), (-4.0, 0, 13.45), M['metro_purple'], rot=(0, -0.25, 0)))
    station_parts.append(add_box("canopy_wing_r", (2.4, 28.5, 0.28), (4.0, 0, 13.45), M['metro_purple'], rot=(0, 0.25, 0)))
    station_parts.append(add_box("station_light", (1.2, 26.0, 0.12), (0, 0, 13.4), M['headlight']))

    station_mesh = join_objects(station_parts, "Station_Structure", apply_loc=True)
    station_mesh.parent = root

    train_parts = []
    for car_idx, cy in enumerate((-7.2, 0.0, 7.2)):
        train_parts.append(add_box(f"car_body_{car_idx}", (2.65, 6.6, 2.55), (-1.4, cy, 10.65), M['metro_silver'], bevel=0.12))
        train_parts.append(add_box(f"p_stripe_l_{car_idx}", (2.70, 6.58, 0.42), (-1.4, cy, 10.15), M['metro_purple']))
        train_parts.append(add_box(f"p_stripe_u_{car_idx}", (2.68, 6.58, 0.22), (-1.4, cy, 11.72), M['metro_purple']))
        for wy_off in (-2.1, -0.7, 0.7, 2.1):
            train_parts.append(add_box(f"t_win_{car_idx}_{wy_off}", (2.72, 1.0, 0.78), (-1.4, cy + wy_off, 10.95), M['window_warm']))

    train_parts.append(add_box("cab_front_glass", (2.2, 0.12, 0.95), (-1.4, 10.5, 11.0), M['glass_cyan']))
    train_parts.append(add_sphere("cab_hl_l", 0.18, (-2.2, 10.55, 9.85), M['headlight'], segments=10, ring_count=8))
    train_parts.append(add_sphere("cab_hl_r", 0.18, (-0.6, 10.55, 9.85), M['headlight'], segments=10, ring_count=8))
    train_parts.append(add_sphere("cab_tl_l", 0.18, (-2.2, -10.55, 9.85), M['taillight'], segments=10, ring_count=8))
    train_parts.append(add_sphere("cab_tl_r", 0.18, (-0.6, -10.55, 9.85), M['taillight'], segments=10, ring_count=8))

    train_mesh = join_objects(train_parts, "Metro_Train", apply_loc=True)
    train_mesh.parent = root

    export_hierarchy_glb(root, "metro_station.glb")
    return root

# ---------------------------------------------------------------------------
# 6. Dynamic Landmark 3: Massive "Silk Board" Highway Green Sign Gantry
# ---------------------------------------------------------------------------
def build_silk_board_sign(M):
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
    root = bpy.context.active_object
    root.name = "Silk_Board_Sign"

    parts = []
    span_x = 13.2
    for side in (-1, 1):
        px = side * span_x
        parts.append(add_box(f"ped_y_{side}", (1.1, 1.1, 1.6), (px, 0, 0.8), M['auto_yellow']))
        parts.append(add_box(f"ped_b_{side}", (1.14, 1.14, 0.45), (px, 0, 0.95), M['trim_black']))
        parts.append(add_cyl(f"post_f_{side}", 0.24, 9.8, (px, 0.35, 5.2), M['steel_rim'], vertices=12))
        parts.append(add_cyl(f"post_b_{side}", 0.24, 9.8, (px, -0.35, 5.2), M['steel_rim'], vertices=12))

    parts.append(add_cyl("beam_top", 0.22, span_x * 2.08, (0, 0.35, 9.8), M['steel_rim'], rot=(0, math.pi / 2, 0), vertices=12))
    parts.append(add_cyl("beam_bot", 0.22, span_x * 2.08, (0, 0.35, 7.6), M['steel_rim'], rot=(0, math.pi / 2, 0), vertices=12))
    parts.append(add_cyl("beam_back", 0.20, span_x * 2.08, (0, -0.35, 8.7), M['steel_rim'], rot=(0, math.pi / 2, 0), vertices=12))

    for tx in range(-11, 12, 2):
        parts.append(add_box(f"strut_{tx}", (0.12, 0.65, 2.2), (tx, 0.0, 8.7), M['steel_rim'], rot=(0, 0.45 if tx % 4 == 0 else -0.45, 0)))

    board_f = add_box("board_f", (19.6, 0.16, 3.8), (0, -0.52, 8.85), M['highway_green'], bevel=0.04)
    board_b = add_box("board_b", (19.6, 0.16, 3.8), (0, 0.52, 8.85), M['highway_green'], bevel=0.04)
    parts.extend([board_f, board_b])

    for y_face, x_dir in ((-0.62, 1.0), (0.62, -1.0)):
        tag = "f" if y_face < 0 else "b"
        parts.append(add_box(f"border_t_{tag}", (19.2, 0.08, 0.16), (0, y_face, 10.58), M['sign_white']))
        parts.append(add_box(f"border_b_{tag}", (19.2, 0.08, 0.16), (0, y_face, 7.12), M['sign_white']))
        parts.append(add_box(f"border_l_{tag}", (0.16, 0.08, 3.6), (-9.52, y_face, 8.85), M['sign_white']))
        parts.append(add_box(f"border_r_{tag}", (0.16, 0.08, 3.6), (9.52, y_face, 8.85), M['sign_white']))
        parts.append(add_box(f"divider_h_{tag}", (18.8, 0.08, 0.10), (0, y_face, 8.75), M['sign_white']))

        def add_bar(w, h, x, z, yf=y_face, xd=x_dir, t=tag):
            parts.append(add_box(f"let_{t}_{x:.1f}_{z:.1f}", (w, 0.10, h), (x * xd, yf, z), M['sign_white']))

        z0 = 9.68
        add_bar(0.75, 0.18, -6.8, z0 + 0.42); add_bar(0.75, 0.18, -6.8, z0); add_bar(0.75, 0.18, -6.8, z0 - 0.42)
        add_bar(0.18, 0.45, -7.08, z0 + 0.21); add_bar(0.18, 0.45, -6.52, z0 - 0.21)
        add_bar(0.55, 0.18, -5.6, z0 + 0.42); add_bar(0.20, 1.02, -5.6, z0); add_bar(0.55, 0.18, -5.6, z0 - 0.42)
        add_bar(0.20, 1.02, -4.68, z0); add_bar(0.75, 0.18, -4.4, z0 - 0.42)
        add_bar(0.20, 1.02, -3.45, z0)
        parts.append(add_box(f"let_k1_{tag}", (0.68, 0.10, 0.18), (-3.12 * x_dir, y_face, z0 + 0.24), M['sign_white'], rot=(0, -0.58 * x_dir, 0)))
        parts.append(add_box(f"let_k2_{tag}", (0.68, 0.10, 0.18), (-3.12 * x_dir, y_face, z0 - 0.24), M['sign_white'], rot=(0, 0.58 * x_dir, 0)))
        add_bar(0.20, 1.02, -1.32, z0); add_bar(0.72, 0.18, -1.0, z0 + 0.42); add_bar(0.68, 0.16, -1.02, z0)
        add_bar(0.72, 0.18, -1.0, z0 - 0.42); add_bar(0.18, 0.96, -0.70, z0)
        add_bar(0.20, 1.02, 0.05, z0); add_bar(0.20, 1.02, 0.75, z0); add_bar(0.85, 0.18, 0.40, z0 + 0.42); add_bar(0.85, 0.18, 0.40, z0 - 0.42)
        add_bar(0.20, 1.02, 1.45, z0); add_bar(0.20, 1.02, 2.15, z0); add_bar(0.85, 0.18, 1.80, z0 + 0.42); add_bar(0.85, 0.18, 1.80, z0 - 0.05)
        add_bar(0.20, 1.02, 2.85, z0); add_bar(0.75, 0.18, 3.18, z0 + 0.42); add_bar(0.75, 0.18, 3.18, z0 + 0.02)
        add_bar(0.18, 0.52, 3.50, z0 + 0.22); add_bar(0.18, 0.52, 3.42, z0 - 0.24)
        add_bar(0.20, 1.02, 4.25, z0); add_bar(0.72, 0.18, 4.55, z0 + 0.42); add_bar(0.72, 0.18, 4.55, z0 - 0.42); add_bar(0.20, 0.86, 4.92, z0)

        for ax in (-5.8, 0.0, 5.8):
            parts.append(add_box(f"arr_stem_{tag}_{ax}", (0.24, 0.10, 0.72), (ax, y_face, 7.82), M['sign_white']))
            parts.append(add_cone(f"arr_head_{tag}_{ax}", 0.42, 0.02, 0.45, (ax, y_face, 8.32), M['sign_white'], vertices=4))
            parts.append(add_box(f"arr_lbl_{tag}_{ax}", (2.8, 0.08, 0.26), (ax + 2.1 if ax < 0 else ax - 2.1 if ax > 0 else 2.2, y_face, 7.92), M['auto_yellow']))

    for bx in (-7.5, 0.0, 7.5):
        parts.append(add_sphere(f"beacon_{bx}", 0.34, (bx, 0.0, 11.05), M['amber_glow'], segments=12, ring_count=10))

    sign_mesh = join_objects(parts, "Silk_Board_Gantry_Mesh", apply_loc=True)
    sign_mesh.parent = root
    export_hierarchy_glb(root, "silk_board_sign.glb")
    return root

# ---------------------------------------------------------------------------
# 7. Bengaluru Jaywalker Pedestrian (Articulated Limbs + "Stop Hand" Gesture)
# ---------------------------------------------------------------------------
def build_pedestrian_jaywalker(M):
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
    root = bpy.context.active_object
    root.name = "Pedestrian_Jaywalker"

    torso_parts = []
    torso_parts.append(add_box("ped_torso", (0.44, 0.26, 0.62), (0, 0, 1.08), M['swiggy_orange'], bevel=0.05, segments=3))
    torso_parts.append(add_box("ped_collar", (0.46, 0.28, 0.10), (0, 0, 1.38), M['scooter_white'], bevel=0.02))
    torso_parts.append(add_cyl("ped_neck", 0.08, 0.12, (0, 0, 1.46), M['skin'], vertices=12))
    torso_parts.append(add_sphere("ped_head", 0.19, (0, 0, 1.62), M['skin'], segments=16, ring_count=12))
    torso_parts.append(add_sphere("ped_hair", 0.195, (0, -0.02, 1.66), M['trim_black'], scale=(1.02, 1.02, 0.82), segments=16, ring_count=12))
    torso_parts.append(add_box("ped_glasses", (0.24, 0.06, 0.06), (0, 0.17, 1.64), M['trim_black']))

    body = join_objects(torso_parts, "Ped_Torso", apply_loc=True)
    body.parent = root

    leg_l_parts = [
        add_box("leg_l_thigh", (0.16, 0.18, 0.68), (0, 0, -0.34), M['jeans'], bevel=0.03),
        add_box("leg_l_shoe", (0.17, 0.26, 0.12), (0, 0.04, -0.72), M['trim_black'], bevel=0.02)
    ]
    leg_l = join_objects(leg_l_parts, "Leg_L", apply_loc=False)
    leg_l.location = (-0.13, 0, 0.78)
    leg_l.parent = root

    leg_r_parts = [
        add_box("leg_r_thigh", (0.16, 0.18, 0.68), (0, 0, -0.34), M['jeans'], bevel=0.03),
        add_box("leg_r_shoe", (0.17, 0.26, 0.12), (0, 0.04, -0.72), M['trim_black'], bevel=0.02)
    ]
    leg_r = join_objects(leg_r_parts, "Leg_R", apply_loc=False)
    leg_r.location = (0.13, 0, 0.78)
    leg_r.parent = root

    arm_l_parts = [
        add_box("arm_l_limb", (0.12, 0.12, 0.48), (0, 0, -0.22), M['skin'], bevel=0.02),
        add_box("arm_l_bag_handle", (0.04, 0.12, 0.16), (-0.04, 0, -0.48), M['auto_yellow']),
        add_box("arm_l_bag", (0.10, 0.32, 0.34), (-0.06, 0, -0.68), M['auto_yellow'], bevel=0.03)
    ]
    arm_l = join_objects(arm_l_parts, "Arm_L", apply_loc=False)
    arm_l.location = (-0.29, 0, 1.32)
    arm_l.parent = root

    arm_r_parts = [
        add_box("arm_r_upper", (0.12, 0.36, 0.12), (0, 0.16, 0.04), M['skin'], bevel=0.02),
        add_box("arm_r_fore", (0.12, 0.12, 0.28), (0, 0.32, 0.18), M['skin'], bevel=0.02),
        add_box("arm_r_palm", (0.16, 0.06, 0.20), (0, 0.36, 0.34), M['skin'], bevel=0.02)
    ]
    arm_r = join_objects(arm_r_parts, "Arm_R", apply_loc=False)
    arm_r.location = (0.29, 0, 1.32)
    arm_r.parent = root

    export_hierarchy_glb(root, "pedestrian_jaywalker.glb")
    return root

# ---------------------------------------------------------------------------
# 8. NEW! Authentic Bengaluru Traffic Police (BTP) Officer (White Shirt, Khaki
#    Trousers, White Pith Helmet, Neon Reflective Vest, Red LED Baton & e-Challan Machine)
# ---------------------------------------------------------------------------
def build_traffic_police(M):
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
    root = bpy.context.active_object
    root.name = "BTP_Traffic_Police"

    torso_parts = []
    # Crisp White BTP Uniform Shirt + Neon Lime Reflective Safety Vest
    torso_parts.append(add_box("cop_shirt", (0.46, 0.28, 0.64), (0, 0, 1.10), M['btp_white'], bevel=0.05, segments=3))
    torso_parts.append(add_box("cop_vest", (0.48, 0.30, 0.50), (0, 0, 1.12), M['btp_neon_vest'], bevel=0.04, segments=2))
    # Dual Silver Retro-Reflective Vest Strips
    torso_parts.append(add_box("vest_stripe_1", (0.49, 0.31, 0.05), (0, 0, 1.00), M['sign_white']))
    torso_parts.append(add_box("vest_stripe_2", (0.49, 0.31, 0.05), (0, 0, 1.16), M['sign_white']))
    # Black Police Duty Belt + Gold Buckle + Epaulettes
    torso_parts.append(add_box("cop_belt", (0.47, 0.29, 0.08), (0, 0, 0.80), M['trim_black']))
    torso_parts.append(add_box("cop_buckle", (0.10, 0.31, 0.08), (0, 0, 0.80), M['gold_emblem']))
    torso_parts.append(add_box("epaulette_l", (0.14, 0.12, 0.04), (-0.18, 0, 1.43), M['bmtc_navy']))
    torso_parts.append(add_box("epaulette_r", (0.14, 0.12, 0.04), (0.18, 0, 1.43), M['bmtc_navy']))

    # Neck, Head, Mustache, Aviator Sunglasses & Silver Whistle
    torso_parts.append(add_cyl("cop_neck", 0.085, 0.12, (0, 0, 1.48), M['skin'], vertices=12))
    torso_parts.append(add_sphere("cop_head", 0.19, (0, 0, 1.64), M['skin'], segments=16, ring_count=12))
    torso_parts.append(add_box("cop_sunglasses", (0.26, 0.07, 0.07), (0, 0.17, 1.66), M['glass_dark'], bevel=0.01))
    torso_parts.append(add_box("cop_mustache", (0.16, 0.05, 0.035), (0, 0.18, 1.57), M['trim_black'], bevel=0.01))
    torso_parts.append(add_cyl("cop_whistle", 0.025, 0.08, (0.04, 0.22, 1.53), M['chrome'], rot=(math.pi / 2, 0, 0), vertices=10))

    # Iconic Bengaluru Traffic Police White Pith Helmet / Peak Cap with Navy & Red Band + Gold Badge
    torso_parts.append(add_sphere("cop_helmet_dome", 0.215, (0, -0.01, 1.74), M['btp_white'], scale=(1.04, 1.12, 0.78), segments=18, ring_count=12))
    torso_parts.append(add_cyl("cop_helmet_brim", 0.25, 0.035, (0, 0.02, 1.71), M['btp_white'], vertices=18))
    torso_parts.append(add_box("cop_helmet_band", (0.38, 0.40, 0.05), (0, 0.0, 1.74), M['bmtc_navy'], bevel=0.02))
    torso_parts.append(add_box("cop_helmet_badge", (0.08, 0.04, 0.09), (0, 0.21, 1.77), M['gold_emblem']))

    body = join_objects(torso_parts, "Cop_Torso", apply_loc=True)
    body.parent = root

    # Left & Right Khaki Trousers Legs (Pivot at Hip Z = 0.78)
    leg_l = join_objects([
        add_box("cop_leg_l_thigh", (0.17, 0.19, 0.68), (0, 0, -0.34), M['btp_khaki'], bevel=0.03),
        add_box("cop_leg_l_boot", (0.18, 0.27, 0.13), (0, 0.04, -0.72), M['seat_brown'], bevel=0.02)
    ], "Cop_Leg_L", apply_loc=False)
    leg_l.location = (-0.13, 0, 0.78)
    leg_l.parent = root

    leg_r = join_objects([
        add_box("cop_leg_r_thigh", (0.17, 0.19, 0.68), (0, 0, -0.34), M['btp_khaki'], bevel=0.03),
        add_box("cop_leg_r_boot", (0.18, 0.27, 0.13), (0, 0.04, -0.72), M['seat_brown'], bevel=0.02)
    ], "Cop_Leg_R", apply_loc=False)
    leg_r.location = (0.13, 0, 0.78)
    leg_r.parent = root

    # Left Arm holding BTP e-Challan Handheld POS Machine + Receipt Roll
    arm_l = join_objects([
        add_box("cop_sleeve_l", (0.14, 0.14, 0.22), (0, 0.04, -0.08), M['btp_white'], bevel=0.02),
        add_box("cop_arm_l_fore", (0.11, 0.28, 0.11), (0, 0.16, -0.22), M['skin'], bevel=0.02),
        add_box("echallan_device", (0.14, 0.22, 0.06), (0, 0.30, -0.20), M['trim_black'], bevel=0.01),
        add_box("echallan_screen", (0.10, 0.12, 0.02), (0, 0.30, -0.16), M['glass_cyan']),
        add_box("echallan_receipt", (0.09, 0.14, 0.01), (0, 0.42, -0.18), M['sign_white'], rot=(0.35, 0, 0))
    ], "Cop_Arm_L", apply_loc=False)
    arm_l.location = (-0.30, 0, 1.34)
    arm_l.parent = root

    # Right Arm raised waving Red LED Traffic Stop Baton + Stop Hand!
    arm_r = join_objects([
        add_box("cop_sleeve_r", (0.14, 0.20, 0.14), (0, 0.08, 0.04), M['btp_white'], bevel=0.02),
        add_box("cop_arm_r_fore", (0.11, 0.12, 0.30), (0, 0.22, 0.20), M['skin'], bevel=0.02),
        add_cyl("baton_handle", 0.028, 0.16, (0, 0.24, 0.38), M['trim_black'], vertices=10),
        add_cyl("baton_red_led", 0.036, 0.42, (0, 0.24, 0.66), M['btp_baton_red'], vertices=12)
    ], "Cop_Arm_R", apply_loc=False)
    arm_r.location = (0.30, 0, 1.34)
    arm_r.parent = root

    export_hierarchy_glb(root, "traffic_police.glb")
    return root

# ---------------------------------------------------------------------------
# 9. NEW! Authentic Bengaluru Indie Stray Dog (Articulated 4 Legs + Wagging Tail)
# ---------------------------------------------------------------------------
def build_stray_dog(M):
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
    root = bpy.context.active_object
    root.name = "Bengaluru_Stray_Dog"

    body_parts = []
    # Sleek Indie Dog Torso (+Y is forward)
    body_parts.append(add_box("dog_torso", (0.28, 0.68, 0.28), (0, 0.0, 0.44), M['dog_coat'], bevel=0.08, segments=3))
    # White chest blaze
    body_parts.append(add_box("dog_chest_white", (0.22, 0.24, 0.22), (0, 0.26, 0.41), M['dog_white'], bevel=0.05, segments=2))
    # Red Street Dog Collar (BBMP vaccinated Indie!)
    body_parts.append(add_cyl("dog_collar", 0.135, 0.06, (0, 0.31, 0.54), M['dog_collar'], rot=(0.65, 0, 0), vertices=14))
    # Neck & Alert Head
    body_parts.append(add_box("dog_neck", (0.20, 0.20, 0.24), (0, 0.30, 0.56), M['dog_coat'], rot=(-0.45, 0, 0), bevel=0.05))
    body_parts.append(add_box("dog_head", (0.24, 0.26, 0.22), (0, 0.42, 0.68), M['dog_coat'], bevel=0.06, segments=3))
    # Tapered Dark Indie Snout & Wet Black Nose
    body_parts.append(add_box("dog_snout", (0.14, 0.22, 0.13), (0, 0.58, 0.64), M['dog_snout'], bevel=0.04, segments=2))
    body_parts.append(add_sphere("dog_nose", 0.04, (0, 0.69, 0.67), M['trim_black'], segments=10, ring_count=8))
    # Bright Eyes
    body_parts.append(add_sphere("dog_eye_l", 0.026, (-0.08, 0.52, 0.72), M['trim_black'], segments=10, ring_count=8))
    body_parts.append(add_sphere("dog_eye_r", 0.026, (0.08, 0.52, 0.72), M['trim_black'], segments=10, ring_count=8))
    # Perky Pointed Indie Ears
    body_parts.append(add_cone("dog_ear_l", 0.065, 0.01, 0.16, (-0.09, 0.38, 0.84), M['dog_coat'], rot=(0.15, -0.25, 0), vertices=10))
    body_parts.append(add_cone("dog_ear_r", 0.065, 0.01, 0.16, (0.09, 0.38, 0.84), M['dog_coat'], rot=(0.15, 0.25, 0), vertices=10))
    # Classic Upward-Curled Indie Tail
    body_parts.append(add_cyl("dog_tail_1", 0.032, 0.26, (0, -0.38, 0.58), M['dog_coat'], rot=(0.65, 0, 0), vertices=10))
    body_parts.append(add_sphere("dog_tail_tip", 0.035, (0, -0.46, 0.70), M['dog_white'], segments=10, ring_count=8))

    dog_body = join_objects(body_parts, "Dog_Body", apply_loc=True)
    dog_body.parent = root

    # 4 Articulated Legs with shoulder/hip pivots at Z = 0.36 and white socks/paws!
    leg_coords = [
        ("Dog_Leg_FL", (-0.10, 0.24, 0.36)),
        ("Dog_Leg_FR", (0.10, 0.24, 0.36)),
        ("Dog_Leg_RL", (-0.10, -0.24, 0.36)),
        ("Dog_Leg_RR", (0.10, -0.24, 0.36)),
    ]
    for leg_name, loc in leg_coords:
        l_parts = [
            add_box(f"{leg_name}_upper", (0.075, 0.085, 0.26), (0, 0, -0.13), M['dog_coat'], bevel=0.02),
            add_box(f"{leg_name}_sock", (0.070, 0.095, 0.12), (0, 0.01, -0.30), M['dog_white'], bevel=0.02)
        ]
        leg_obj = join_objects(l_parts, leg_name, apply_loc=False)
        leg_obj.location = loc
        leg_obj.parent = root

    export_hierarchy_glb(root, "stray_dog.glb")
    return root

# ---------------------------------------------------------------------------
# Studio Showcase Render for README (`screenshots/blender_assets_upgraded.png`)
# ---------------------------------------------------------------------------
def render_studio_showcase(M, models):
    # Dark reflective studio turntable floor
    floor_mat = make_mat("Studio_Floor", (0.04, 0.06, 0.10), roughness=0.18, metallic=0.45)
    add_box("Studio_Stage", (80.0, 80.0, 0.2), (0, 0, -0.1), floor_mat)

    # Camera is at Y = +9.2 looking towards -Y.
    # Remember: +Y is front of characters/vehicles! So rot_z ~ 0 faces the camera!
    models['auto'].location = (-0.5, 1.8, 0.0)
    models['auto'].rotation_euler = (0, 0, math.radians(-145)) # 3/4 rear-side view showing yellow hood + green chassis + 3 wheels

    models['cop'].location = (1.35, 3.1, 0.0)
    models['cop'].rotation_euler = (0, 0, math.radians(-18)) # Facing camera showing sunglasses, mustache, pith helmet, vest, e-challan & red baton!

    models['dog'].location = (0.15, 3.6, 0.0)
    models['dog'].rotation_euler = (0, 0, math.radians(22)) # Facing camera 3/4 showing snout, ears, red collar, white socks & tail!

    models['ped'].location = (-1.95, 2.9, 0.0)
    models['ped'].rotation_euler = (0, 0, math.radians(18)) # Facing camera showing glasses, jhola bag & "Ondu Second" stop hand!

    models['zepto'].location = (2.85, 1.5, 0.0)
    models['zepto'].rotation_euler = (0, 0, math.radians(-155))

    models['swiggy'].location = (-3.1, 1.3, 0.0)
    models['swiggy'].rotation_euler = (0, 0, math.radians(150))

    models['blinkit'].location = (-4.5, 0.2, 0.0)
    models['blinkit'].rotation_euler = (0, 0, math.radians(30))

    models['techie'].location = (4.3, 0.3, 0.0)
    models['techie'].rotation_euler = (0, 0, math.radians(-28))

    models['bus'].location = (-4.8, -4.8, 0.0)
    models['bus'].rotation_euler = (0, 0, math.radians(-42))

    models['silk_board'].location = (0.0, -11.5, 0.0)
    models['silk_board'].rotation_euler = (0, 0, math.radians(180))
    models['vidhana'].location = (-15.0, -24.0, 0.0)
    models['metro'].location = (13.5, -17.0, 0.0)

    # 3-Point Studio Lighting
    bpy.ops.object.light_add(type='SUN', location=(8, 14, 18), rotation=(math.radians(52), math.radians(12), math.radians(155)))
    sun = bpy.context.active_object
    sun.data.energy = 4.8
    sun.data.color = (1.0, 0.95, 0.88)

    bpy.ops.object.light_add(type='AREA', location=(-6, 8, 5), rotation=(math.radians(65), 0, math.radians(-145)))
    fill = bpy.context.active_object
    fill.data.energy = 420.0
    fill.data.size = 7.0
    fill.data.color = (0.55, 0.80, 1.0)

    bpy.ops.object.light_add(type='AREA', location=(5, 8, 5), rotation=(math.radians(65), 0, math.radians(145)))
    rim = bpy.context.active_object
    rim.data.energy = 480.0
    rim.data.size = 7.0
    rim.data.color = (1.0, 0.82, 0.45)

    if bpy.context.scene.world is None:
        bpy.context.scene.world = bpy.data.worlds.new("StudioWorld")
    bpy.context.scene.world.use_nodes = True
    bg = bpy.context.scene.world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs[0].default_value = (0.06, 0.09, 0.15, 1.0)
        bg.inputs[1].default_value = 1.25

    bpy.ops.object.camera_add(location=(0.0, 8.8, 2.65), rotation=(math.radians(76), 0, math.radians(180)))
    cam = bpy.context.active_object
    cam.data.lens = 35
    bpy.context.scene.camera = cam

    scene = bpy.context.scene
    scene.render.resolution_x = 1600
    scene.render.resolution_y = 900
    scene.render.resolution_percentage = 100
    out_img = os.path.join(SCREENSHOTS_DIR, "blender_assets_upgraded.png")
    scene.render.filepath = out_img
    try:
        bpy.ops.render.render(write_still=True)
        print(f"Rendered studio showcase to {out_img}")
    except Exception as e:
        print(f"Render note: {e}")

def main():
    clear_scene()
    M = init_materials()

    models = {}
    models['auto'] = build_auto_rickshaw(M)
    models['swiggy'] = build_scooter_variant("Delivery_Swiggy", "delivery_swiggy.glb",
                                             M['scooter_white'], M['swiggy_orange'], M['swiggy_orange'], True, False, M)
    models['zepto'] = build_scooter_variant("Delivery_Zepto", "delivery_zepto.glb",
                                            M['zepto_purple'], M['zepto_green'], M['zepto_green'], True, False, M)
    models['blinkit'] = build_scooter_variant("Delivery_Blinkit", "delivery_blinkit.glb",
                                              M['scooter_charcoal'], M['blinkit_yellow'], M['blinkit_yellow'], True, False, M)
    models['techie'] = build_scooter_variant("Commuter_Techie", "commuter_techie.glb",
                                             M['scooter_teal'], M['techie_shirt'], M['steel_rim'], False, True, M)
    models['bus'] = build_bmtc_bus(M)
    models['vidhana'] = build_vidhana_soudha(M)
    models['metro'] = build_metro_station(M)
    models['silk_board'] = build_silk_board_sign(M)
    models['ped'] = build_pedestrian_jaywalker(M)
    models['cop'] = build_traffic_police(M)
    models['dog'] = build_stray_dog(M)

    render_studio_showcase(M, models)
    print("ALL 12 UPGRADED BLENDER GLB ASSETS EXPORTED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
