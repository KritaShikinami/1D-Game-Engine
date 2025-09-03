import pygame, sys
import source

pygame.init()

WIDTH, HEIGHT = 1000, 600
INFO_PANEL_WIDTH = 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SIERRA ENGINE")

WHITE = (255, 255, 255)
GRAY  = (40, 40, 40)
BG_COLOR = (20, 20, 20)

clock = pygame.time.Clock()
FPS = 60

line_y = HEIGHT // 2
line_thickness = 10

# Fizik parametreleri
m, a, g = 10, 2, 9.81
current_surface = "TAS"
q = source.SURFACE_TYPES[current_surface]["friction"]
line_color = source.SURFACE_TYPES[current_surface]["line_color"]
box_speed = source.Friction(q, m, a, g)

# Kutular
box1 = source.Box(200, line_y-50, 50, 50, (255,0,0), m, speed=box_speed)
box2 = source.Box(600, line_y-50, 50, 50, (0,0,255), 15, speed=0)

font = pygame.font.Font("Assets/Font3.ttf", 20)

running = True
while running:
    clock.tick(FPS)
    screen.fill(BG_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1: current_surface = "TAS"
            elif event.key == pygame.K_2: current_surface = "BUZ"
            elif event.key == pygame.K_3: current_surface = "KUM"
            elif event.key == pygame.K_4: current_surface = "CIM"

            q = source.SURFACE_TYPES[current_surface]["friction"]
            line_color = source.SURFACE_TYPES[current_surface]["line_color"]
            box1.speed = source.Friction(q, m, a, g)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        box1.rect.x -= box1.speed
    if keys[pygame.K_RIGHT]:
        box1.rect.x += box1.speed

    # Kutuları hareket ettir
    box1.move()
    box2.move()

    # Çarpışma kontrolü (source'dan geliyor)
    box1.speed, box2.speed = source.check_collision(
        box1.rect, box2.rect,
        box1.mass, box2.mass,
        box1.speed, box2.speed
    )

    # Çizimler
    pygame.draw.line(screen, line_color, (0, line_y), (WIDTH - INFO_PANEL_WIDTH, line_y), line_thickness)
    box1.draw(screen)
    box2.draw(screen)
    pygame.draw.rect(screen, GRAY, (WIDTH - INFO_PANEL_WIDTH, 0, INFO_PANEL_WIDTH, HEIGHT))

    info_texts = [
        f"KUTLE1: {box1.mass} kg",
        f"KUTLE2: {box2.mass} kg",
        f"HIZ1: {box1.speed:.2f} px/frame",
        f"HIZ2: {box2.speed:.2f} px/frame",
        f"SURTUNME: {q}",
        f"IVME: {a} m/s^2",
        f"YERCEKIMI: {g} m/s^2",
        f"ZEMIN: {current_surface.upper()}",
    ]

    for i, text in enumerate(info_texts):
        txt_surface = font.render(text, True, WHITE)
        screen.blit(txt_surface, (WIDTH - INFO_PANEL_WIDTH + 20, 20 + i * 25))

    pygame.display.flip()

pygame.quit()
sys.exit()
