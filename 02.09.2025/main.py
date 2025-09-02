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

line_y = HEIGHT // 2
line_thickness = 10
box_width, box_height = 50, 50
box_x = (WIDTH - INFO_PANEL_WIDTH) // 2 - box_width // 2
box_y = line_y - box_height

m = 10
a = 2
g = 9.81

current_surface = "ASFALT"
q = source.SURFACE_TYPES[current_surface]["friction"]
line_color = source.SURFACE_TYPES[current_surface]["line_color"]
box_speed = source.Friction(q, m, a, g)

font = pygame.font.Font("Assets/Font3.ttf", 20)

running = True
while running:
    clock.tick(FPS)
    screen.fill(BG_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                current_surface = "ASFALT"
            elif event.key == pygame.K_2:
                current_surface = "BUZ"
            elif event.key == pygame.K_3:
                current_surface = "KUM"
            elif event.key == pygame.K_4:
                current_surface = "CIM"

            q = source.SURFACE_TYPES[current_surface]["friction"]
            line_color = source.SURFACE_TYPES[current_surface]["line_color"]
            box_speed = source.Friction(q, m, a, g)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        box_x -= box_speed
    if keys[pygame.K_RIGHT]:
        box_x += box_speed

    max_x = WIDTH - INFO_PANEL_WIDTH - box_width
    box_x = max(0, min(max_x, box_x))

    pygame.draw.line(screen, line_color, (0, line_y), (WIDTH - INFO_PANEL_WIDTH, line_y), line_thickness)
    pygame.draw.rect(screen, RED, (box_x, box_y, box_width, box_height))

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
        "1: ASFALT",
        "2: BUZ",
        "3: KUM",
        "4: CIM",
        "=================================",
        "SIERRA ENGINE V0.6"
    ]

    for i, text in enumerate(info_texts):
        txt_surface = font.render(text, True, WHITE)
        screen.blit(txt_surface, (WIDTH - INFO_PANEL_WIDTH + 20, 20 + i * 30))

    pygame.display.flip()

pygame.quit()
sys.exit()
