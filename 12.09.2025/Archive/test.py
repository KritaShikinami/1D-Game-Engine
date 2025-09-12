# main.py
import pygame, math
from source import SkeletonCharacter, StatusPanel

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18)

def draw_line(surface, start, end, color, width):
    pygame.draw.line(surface, color, start, end, width)

def draw_circle(surface, position, radius, color):
    pygame.draw.circle(surface, color, position, radius)

def draw_text(surface, text, position, font, color):
    label = font.render(text, True, color)
    surface.blit(label, position)

# Karakter oluştur
character = SkeletonCharacter((400, 200))
character.add_part("Head", (0, -50), 20, math.pi / 2)
character.add_part("Torso", (0, 0), 60, math.pi / 2)
character.add_part("Left Arm", (-30, 0), 40, math.pi / 3)
character.add_part("Right Arm", (30, 0), 40, 2 * math.pi / 3)
character.add_part("Left Leg", (-15, 60), 50, math.pi / 2)
character.add_part("Right Leg", (15, 60), 50, math.pi / 2)

# Panel oluştur
panel = StatusPanel(character)

# Ana döngü
running = True
while running:
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    character.render(screen, draw_line, draw_circle)
    panel.render(screen, draw_text, font, (20, 480))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
