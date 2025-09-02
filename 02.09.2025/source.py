import math, random

SURFACE_TYPES = {
    "ASFALT": {
        "friction": 0.15,
        "line_color": (100, 100, 100)   # gri
    },
    "BUZ": {
        "friction": 0.05,
        "line_color": (173, 216, 230)   # açık camgöbeği
    },
    "KUM": {
        "friction": 0.30,
        "line_color": (245, 222, 179)   # bej
    },
    "CIM": {
        "friction": 0.25,
        "line_color": (34, 139, 34)     # yeşil
    }
}

def Friction(q, m, a, g):
    if (m * a) > (q * m * g):
        x_v = (m * a) - (q * m * g)
        return x_v
    else:
        x_v = (q * m * g) - (m * a)
        return x_v        

def collision(m1, m2, v1i, v2i, type):
    print("\nCalculating...")
    if type == 1:
        v1f = ((m1 + m2) * v1i + 2 * m2 * v2i) / (m1 + m2)
        v2f = ((m1 + m2) * v2i + 2 * m1 * v1i) / (m1 + m2)
        print("\nElastic Collision Results:")
        print(f"Final velocity of object 1 (v1f): {v1f} m/s")
        print(f"Final velocity of object 2 (v2f): {v2f} m/s")
    else:
        vf = (m1 * v1i + m2 * v2i) / (m1 + m2)
        print("\nInelastic Collision Result:")
        print(f"Final shared velocity (vf): {vf} m/s")
    print("Done.")

# Halen daha deneme aşamasında, çeşitli hatalar oluşabilir.

class Perlin1D:
    def __init__(self, seed=0):
        rng = random.Random(seed)
        p = list(range(256))
        rng.shuffle(p)
        self.perm = p + p  # wrap için iki kez

    @staticmethod
    def fade(t):  # 6t^5 - 15t^4 + 10t^3
        return t*t*t*(t*(t*6 - 15) + 10)

    @staticmethod
    def lerp(a, b, t):
        return a + t*(b - a)

    def grad(self, h, x):           # 1D: +x veya -x
        return x if (h & 1) == 0 else -x

    def noise(self, x):
        xi0 = math.floor(x) & 255   # sol ızgara noktası
        xi1 = (xi0 + 1) & 255       # sağ ızgara noktası

        xf0 = x - math.floor(x)     # sola uzaklık
        xf1 = xf0 - 1.0             # sağa uzaklık (x - (i+1))

        g0 = self.perm[xi0]
        g1 = self.perm[xi1]

        d0 = self.grad(g0, xf0)
        d1 = self.grad(g1, xf1)

        u = self.fade(xf0)
        return self.lerp(d0, d1, u)  # ~[-1,1]

def fbm1d(noise_fn, x, octaves=5, lacunarity=2.0, gain=0.5):
    amp, freq = 1.0, 1.0
    total = norm = 0.0
    for _ in range(octaves):
        total += amp * noise_fn(x * freq)
        norm += amp
        amp *= gain
        freq *= lacunarity
    return total / norm if norm else 0.0

def __main__ ():
    p = Perlin1D(seed=42)
    val = p.noise(3.25)            # tek oktav Perlin
    val_fbm = fbm1d(p.noise, 3.25, octaves=6)
    print(f" {p} \n {val} \n {val_fbm}")

__main__()
