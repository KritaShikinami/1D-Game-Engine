import pygame
import random
import math

# --- Pygame Başlat ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sıvı Sürtünme Simülasyonu")
clock = pygame.time.Clock()

# --- Renkler ---
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
LIGHT_BLUE = (173, 216, 230)
GRAY = (100, 100, 100)

# --- Sıvı Parametreleri (örnek: HONEY) ---
LIQUID = {
    "scale": 2.50e-2,
    "activation": 1200.0,
    "correction_coefficient": 160
}
T = 298  # sıcaklık (Kelvin)

# --- Nesne Parametreleri ---
object_radius = 20
object_x = 100
object_y = 100
object_mass = 5.0
object_velocity = 0.0
gravity = 9.81

# --- Sıvı Alanı ---
water_rect = pygame.Rect(0, 400, WIDTH, 200)

# --- Sıçrama Efekti ---
def draw_splash(x, y):
    for _ in range(5):
        offset = random.randint(-15, 15)
        pygame.draw.circle(screen, LIGHT_BLUE, (x + offset, y - 5), 4)

# --- Sıvı Sürtünme Fonksiyonu ---
def liquid_friction(s, a, c, t, m, v):
    p = s * (10 ** (a / t - c))
    f = (m * v) - p
    return f

# --- Ana Döngü ---
running = True
was_in_water = False

while running:
    dt = clock.tick(60) / 1000.0  # saniye cinsinden zaman adımı

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Arkaplan
    screen.fill(WHITE)

    # Sıvı alanı çiz
    pygame.draw.rect(screen, BLUE, water_rect)

    # Nesne çiz
    pygame.draw.circle(screen, GRAY, (int(object_x), int(object_y)), object_radius)

    # Fizik: yerçekimi etkisi
    object_velocity += gravity * dt
    object_y += object_velocity * dt

    # Sıvıya giriş kontrolü
    object_rect = pygame.Rect(object_x - object_radius, object_y - object_radius,
                              object_radius * 2, object_radius * 2)

    if object_rect.colliderect(water_rect):
        if not was_in_water:
            draw_splash(int(object_x), water_rect.top)
            was_in_water = True

        # Sıvı sürtünmesi uygula
        f = liquid_friction(LIQUID["scale"], LIQUID["activation"],
                            LIQUID["correction_coefficient"], T,
                            object_mass, object_velocity)
        net_acc = f / object_mass
        object_velocity -= net_acc * dt

    pygame.display.flip()

pygame.quit()
