import math, random, pygame

# --- Zemin tipleri ---
SURFACE_TYPES = {
    "ALUMINUM": {
        "friction": 0.35,
        "line_color": (200, 200, 200),
        "durability": 0.70
    },
    "ALUMINUM-PLATE": {
        "friction": 0.40,
        "line_color": (180, 180, 180),
        "durability": 0.85
    },
    "STEEL": {
        "friction": 0.45,
        "line_color": (160, 160, 160),
        "durability": 0.95
    },
    "STEEL-PLATE": {
        "friction": 0.50,
        "line_color": (140, 140, 140),
        "durability": 0.90
    },
    "STAINLESS-STEEL": {
        "friction": 0.40,
        "line_color": (180, 180, 180),
        "durability": 0.98
    },
    "STAINLESS-STEEL-PLATE": {
        "friction": 0.45,
        "line_color": (160, 160, 160),
        "durability": 0.95
    },
    "COPPER": {
        "friction": 0.55,
        "line_color": (184, 115, 51),
        "durability": 0.80
    },
    "COPPER-PLATE": {
        "friction": 0.60,
        "line_color": (160, 90, 40),
        "durability": 0.85
    },
    "LEAD": {
        "friction": 0.65,
        "line_color": (105, 105, 105),
        "durability": 0.60
    },
    "LEAD-PLATE": {
        "friction": 0.70,
        "line_color": (85, 85, 85),
        "durability": 0.65
    },    
    "BRICK": {
        "friction": 0.65,
        "line_color": (187, 34, 34),
        "durability": 0.75
    },    
    "ASPHALT": {
        "friction": 0.70,
        "line_color": (50, 50, 50),
        "durability": 0.85
    },
    "CONCRETE": {
        "friction": 0.55,
        "line_color": (128, 128, 128),
        "durability": 0.90
    },
    "SAND": {
        "friction": 0.45,
        "line_color": (194, 178, 128),
        "durability": 0.25
    },
    "DIRT": {
        "friction": 0.50,
        "line_color": (101, 67, 33),
        "durability": 0.40
    },
    "GLASS": {
        "friction": 0.35,
        "line_color": (251, 206, 235),
        "durability": 0.50
    },
    "PLASTIC": {
        "friction": 0.20,
        "line_color": (255, 255, 255),
        "durability": 0.60
    },
    "MARBLE": {
        "friction": 0.30,
        "line_color": (220, 220, 220),
        "durability": 0.90
    }
}

OBJECT_TYPES = {
    "HIGHWAYMAN": {
            "durability": 1000,
            "weight": 1500,
            "max_speed": 200,
            "wheel_friction": 0.50
    }
}

CHARACTER_TYPES = {
    "TESTSUBJECT01": {
        "speed": 1,
        "size": 32,
        "walk_sequence": ["Assets/Arts/default_character_sprite_1.png",
                          "Assets/Arts/default_character_sprite_2.png",
                          "Assets/Arts/default_character_sprite_3.png",
                          "Assets/Arts/default_character_sprite_2.png"],
        "frame_delay": 15,
        "head_hp": 100,
        "body_hp": 100,
        "leg_hp": 100,
        "arm_hp": 100
    }
}

COLOR_TYPES = {
    "SILVER": (192, 192, 192),
    "GRAY": (128, 128, 128),
    "DARK_GRAY": (64, 64, 64),
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
    "RED": (255, 0, 0),
    "DARK_RED": (139, 0, 0),
    "ORANGE": (255, 165, 0),
    "BROWN": (101, 67, 33),
    "DARK_BROWN": (80, 40, 20),
    "YELLOW": (255, 255, 0),
    "GOLD": (255, 215, 0),
    "LIGHT_YELLOW": (255, 255, 153),
    "GREEN": (0, 128, 0),
    "DARK_GREEN": (0, 100, 0),
    "LIME": (50, 205, 50),
    "BLUE": (0, 0, 255),
    "NAVY": (0, 0, 128),
    "SKY_BLUE": (135, 206, 235),
    "CYAN": (0, 255, 255),
    "TEAL": (0, 128, 128),
    "PURPLE": (128, 0, 128),
    "VIOLET": (238, 130, 238),
    "MAGENTA": (255, 0, 255),
    "PINK": (255, 192, 203),
    "ROSE": (255, 102, 204),
    "BEIGE": (245, 245, 220),
    "SAND": (194, 178, 128),
    "MARBLE": (220, 220, 220),
    "COPPER": (184, 115, 51),
    "BRICK": (187, 34, 34),
    "GLASS": (251, 206, 235)
}

LIQUID_TYPES = {
    "WATER": {
        "scale": 2.41e-5,
        "activation": 247.8,
        "correction_coefficient": 140
    },
    "ETHANOL": {
        "scale": 1.20e-4,
        "activation": 420.0,
        "correction_coefficient": 140
    },
    "METHANOL": {
        "scale": 7.20e-5,
        "activation": 370.0,
        "correction_coefficient": 145
    },
    "GLYCERIN": {
        "scale": 1.10e-2,
        "activation": 900.0,
        "correction_coefficient": 150
    },
    "HONEY": {
        "scale": 2.50e-2,
        "activation": 1200.0,
        "correction_coefficient": 160
    },
    "ENG_OIL_O": {
        "scale": 3.50e-3,
        "activation": 700.0,
        "correction_coefficient": 160
    },
    "ENG_OIL_S": {
        "scale": 1.80e-3,
        "activation": 600.0,
        "correction_coefficient": 160
    }
}

# --- Fizik fonksiyonları ---
def Friction(q, m, a, g):
    if (m * a) > (q * m * g):
        return (m * a) - (q * m * g)
    else:
        return (q * m * g) - (m * a)

def collision(m1, m2, v1, v2, type):
    if (type == 1):
        v1f = ((m1 - m2) / (m1 + m2)) * v1 + (2 * m2 / (m1 + m2)) * v2
        v2f = (2 * m1 / (m1 + m2)) * v1 + ((m2 - m1) / (m1 + m2)) * v2
        return v1f, v2f
    elif (type == 0):
        return ((m1 * v1) + (m2 * v2)) / (m1 + m2)
    else:
        return "ERROR 1: Parametreler yanlış (Muhtemel 'TYPE' girdisi)"

def collision_result(v1d, v2d, v1m, v2m, v1f, v2f, vf, type):
    if (type == 1):
        return v1f, v2f
    elif (type == 0):
        if (v1m == v2m):
            energy = 0.5 * v1m * (vf ** 2)
            damage_v1 = energy * (1 - v1d)
            damage_v2 = energy * (1 - v2d)
            return damage_v1, damage_v2
        else:
            energy = 0.5 * ((v1m + v2m) / 2) * (vf ** 2)
            energy = 0.5 * v1m * (vf ** 2)
            damage_v1 = energy * (1 - v1d)
            damage_v2 = energy * (1 - v2d)
            return damage_v1, damage_v2
    else:
        return "ERROR 2: Parametreler yanlış (Muhtemel 'TYPE' girdisi)"

def check_collision(box1, box2, m1, m2, v1, v2):
    if box1.colliderect(box2):
        return collision(m1, m2, v1, v2)
    return v1, v2

def liquid_friction(s, a, c, t, m, ac):
    p = s * (10 ** (a / t - c))
    f = (m * ac) - p
    return f

# --- Karakter Oluşturucu ---

def create_character(character_type, start_x, start_y, CHARACTER_TYPES):
    data = CHARACTER_TYPES[character_type]
    return {
        "type": character_type,
        "x": start_x,
        "y": start_y,
        "size": data["size"],
        "speed": data["speed"],
        "walk_frames": [pygame.image.load(path).convert_alpha() for path in data["walk_sequence"]],
        "frame_delay": data["frame_delay"],
        "current_frame": 0,
        "frame_timer": 0,
        "facing_left": False,
        "hp": {
            "head": data["head_hp"],
            "body": data["body_hp"],
            "leg": data["leg_hp"],
            "arm": data["arm_hp"]
        }
    }

# --- Çizim işlemleri ---

def draw_world(screen, background_tile, surface_color, BLOCK_SIZE, TOP_HEIGHT, WORLD_BLOCKS, WINDOW_WIDTH, camera_x, player):
    start_tile_x = camera_x // BLOCK_SIZE
    offset_x = -(camera_x % BLOCK_SIZE)
    for y in range(0, TOP_HEIGHT, BLOCK_SIZE):
        for x in range(-BLOCK_SIZE, WINDOW_WIDTH + BLOCK_SIZE, BLOCK_SIZE):
            world_tile_x = start_tile_x + (x // BLOCK_SIZE)
            if 0 <= world_tile_x < WORLD_BLOCKS:
                screen.blit(background_tile, (x + offset_x, y))
    pygame.draw.line(screen, surface_color, (0, player["y"] + player["size"] + 2), (WINDOW_WIDTH, player["y"] + player["size"] + 2), 2)

def draw_player(screen, player, camera_x):
    screen_x = player["x"] - camera_x
    sprite = pygame.transform.scale(player["walk_frames"][player["current_frame"]], (player["size"], player["size"]))
    if player["facing_left"]:
        sprite = pygame.transform.flip(sprite, True, False)
    screen.blit(sprite, (screen_x, player["y"]))

def draw_info_panel(screen, info_panel_bg, font, TOP_HEIGHT, surface_type, surface_data, player):
    screen.blit(info_panel_bg, (0, TOP_HEIGHT))
    info_text = f"ZEMIN: {surface_type}  SURTUNME: {surface_data['friction']}  DAYANIKLILIK: {surface_data['durability']}"
    text_surface = font.render(info_text, True, (37, 228, 6))
    hp_text = f"HP - BAS: {player['hp']['head']}  GOVDE: {player['hp']['body']}  BACAK: {player['hp']['leg']}  KOL: {player['hp']['arm']}"
    hp_surface = font.render(hp_text, True, (37, 228, 6))
    screen.blit(text_surface, (10, TOP_HEIGHT + 20))
    screen.blit(hp_surface, (10, TOP_HEIGHT + 50))

# --- Debug Mode ---

def draw_debug_info(screen, font, player, camera_x, fps):
    debug_lines = [
        f"DEBUG MODE",
        f"Camera X: {camera_x:.2f}",
        f"Player X: {player['x']:.2f}",
        f"Player Y: {player['y']:.2f}",
        f"Facing Left: {player['facing_left']}",
        f"Current Frame: {player['current_frame']}",
        f"FPS: {fps:.1f}"
    ]
    y_offset = 10
    for line in debug_lines:
        text_surface = font.render(line, True, (255, 255, 0))
        screen.blit(text_surface, (10, y_offset))
        y_offset += 15

# --- Örnek bir kod ---
def example1():
    A_surface = "STEEL"
    B_surface = "STELL"
    Z_surface = "ASPHALT"

    A_durability = SURFACE_TYPES[A_surface]["durability"]
    B_durability = SURFACE_TYPES[B_surface]["durability"]

    A_mass = 10  # kg
    B_mass = 10  # kg
    A_velocity = 2  # m/s
    B_velocity = 0  # m/s

    collision_type = 0

    vf = collision(A_mass, B_mass, A_velocity, B_velocity, collision_type)

    damage_A, damage_B = collision_result(
        A_durability, B_durability,
        A_mass, B_mass,
        None, None,  # Elastik olmayan çarpışmada v1f, v2f kullanılmıyor
        vf,
        collision_type
    )

    print("Çarpışma Sonucu")
    print(f"Ortak hız: {vf:.2f} m/s")
    print("\n=========== [A] =============\n")
    print(f"A objesi hasar: {damage_A:.2f}")
    if (damage_A - A_durability) < A_durability:
        print("A objesinin dayanıklılığı azaldı.")
    print(f"A Dayanıklılığı: {A_durability - damage_A}")
    print("\n=========== [B] =============\n")
    print(f"B objesi hasar: {damage_B:.2f}")
    if (damage_B - B_durability) < B_durability:
        print("B objesinin dayanıklılığı azaldı.")
    print(f"B Dayanıklılığı: {B_durability - damage_B}")

def example2():
    object_mass = 5.0   # kg
    object_velocity = 10.0  # m/s (başlangıç hızı)

    liquid = "HONEY"
    s = LIQUID_TYPES[liquid]["scale"]
    a = LIQUID_TYPES[liquid]["activation"]
    c = LIQUID_TYPES[liquid]["correction_coefficient"]

    # Sıcaklık (298 K ~ 25°C)
    T = 298  

    f = liquid_friction(s, a, c, T, object_mass, object_velocity)

    net_acc = f / object_mass

    #(basit: v' = v - net_acc*Δt, burada Δt=1s alalım)
    new_velocity = object_velocity - net_acc * 1  

    print(f"Sıvı: {liquid}")
    print(f"Başlangıç hızı: {object_velocity:.2f} m/s")
    print(f"Sürtünme kuvveti: {f:.4f} N")
    print(f"Net ivme: {net_acc:.4f} m/s²")
    print(f"1 saniye sonraki hız: {new_velocity:.2f} m/s")

def __main__ ():
    #print("\n============[ ORN1 ]=============\n")
    #example1()
    #print("\n============[ ORN2 ]=============\n")
    #example2()
    print("SIERRA ENGINE IS RUNNED SUCCESFULLY.")

__main__()
