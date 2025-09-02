import pygame
import sys
import source

pygame.init()

WIDTH, HEIGHT = 1000, 600
INFO_PANEL_WIDTH = 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
ikon = pygame.image.load("Assets/Logo.fw.png")
pygame.display.set_icon(ikon)
pygame.display.set_caption("SIERRA ENGINE")

WHITE = (255, 255, 255)
RED   = (255, 0, 0)
GRAY  = (40, 40, 40)
BG_COLOR = (20, 20, 20)

clock = pygame.time.Clock()
FPS = 60

m = 10
a = 2
g = 9.81

# --- Dünya parametreleri ---
BLOCK_SIZE = 50
WORLD_LENGTH = 500
line_y = HEIGHT // 2
box_width, box_height = 50, 50

perlin = source.Perlin1D(seed=42)
world = []
for i in range(WORLD_LENGTH):
    noise_val = source.fbm1d(perlin.noise, i * 0.1, octaves=4)
    surface = source.surface_from_noise(noise_val)
    world.append(surface)

camera_x = 0
player_x = WIDTH // 2
player_y = line_y - box_height

current_surface = world[0]
q = source.SURFACE_TYPES[current_surface]["friction"]
line_color = source.SURFACE_TYPES[current_surface]["line_color"]
box_speed = source.Friction(q, m, a, g)

font = pygame.font.Font("Assets/Font3.ttf", 20)

with open("dunya.txt", "w", encoding="utf-8") as f:
    for i in range(WORLD_LENGTH):
        noise_val = source.fbm1d(perlin.noise, i * 0.1, octaves=4)
        surface_type = source.surface_from_noise(noise_val)
        f.write(f"{i}: {surface_type}\n")

print("Dünya haritası 'dunya.txt' dosyasına kaydedildi.")

# --- Oyun döngüsü ---
running = True
while running:
    clock.tick(FPS)
    screen.fill(BG_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Tuşlar ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        camera_x -= box_speed
    if keys[pygame.K_RIGHT]:
        camera_x += box_speed

    # Kamera sınırları
    camera_x = max(0, min(camera_x, WORLD_LENGTH * BLOCK_SIZE - (WIDTH - INFO_PANEL_WIDTH)))

    # --- Oyuncunun altındaki zemin ---
    player_block_index = int((camera_x + player_x) // BLOCK_SIZE)
    if 0 <= player_block_index < len(world):
        current_surface = world[player_block_index]
        q = source.SURFACE_TYPES[current_surface]["friction"]
        line_color = source.SURFACE_TYPES[current_surface]["line_color"]
        box_speed = source.Friction(q, m, a, g)

    # --- Dünya çizimi ---
    start_block = int(camera_x // BLOCK_SIZE)
    end_block = start_block + int((WIDTH - INFO_PANEL_WIDTH) // BLOCK_SIZE) + 2

    for i in range(start_block, min(end_block, WORLD_LENGTH)):
        surface_type = world[i]
        color = source.SURFACE_TYPES[surface_type]["line_color"]
        x_pos = (i * BLOCK_SIZE) - camera_x
        pygame.draw.rect(screen, color, (x_pos, line_y, BLOCK_SIZE, BLOCK_SIZE))

    pygame.draw.rect(screen, RED, (player_x, player_y, box_width, box_height))

    pygame.draw.rect(screen, GRAY, (WIDTH - INFO_PANEL_WIDTH, 0, INFO_PANEL_WIDTH, HEIGHT))

    info_texts = [
        f"KUTLE: {m} kg",
        f"HIZ: {box_speed:.2f} px/frame",
        f"SURTUNME: {q}",
        f"IVME: {a} m/s^2",
        f"YERCEKIMI: {g} m/s^2",
        f"ZEMIN: {current_surface.upper()}",
        "=================================",
        "ZEMIN TURLERI",
        "ASFALT - BUZ",
        "KUM - CIM",
        "=================================",
        "SIERRA ENGINE V1.0",
        "OPEN WORLD"
    ]

    for i, text in enumerate(info_texts):
        txt_surface = font.render(text, True, WHITE)
        screen.blit(txt_surface, (WIDTH - INFO_PANEL_WIDTH + 20, 20 + i * 30))

    pygame.display.flip()

pygame.quit()
sys.exit()
