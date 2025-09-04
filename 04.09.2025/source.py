import math, random

# --- Zemin tipleri ---
SURFACE_TYPES = {
    "STELL": {
        "friction": 0.30,
        "line_color": (192, 192, 192),
        "durability": 0.95
    },
    "STELL-PLATE": {
        "friction": 0.40,
        "line_color": (150, 150, 150),
        "durability": 0.80
    },
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

# --- Örnek bir kod ---
def example():
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

def __main__ ():
    print("\n===========================\n")
    example()
    print("\n===========================\n")

__main__()
