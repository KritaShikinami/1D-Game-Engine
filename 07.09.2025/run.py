import pygame
import sys
from source import SURFACE_TYPES, CHARACTER_TYPES, create_character, draw_world, draw_player, draw_info_panel, draw_debug_info

# --- Ayarlar ---
BLOCK_SIZE = 32
WORLD_BLOCKS = 500
WORLD_WIDTH = BLOCK_SIZE * WORLD_BLOCKS
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
TOP_HEIGHT = 300
BOTTOM_HEIGHT = 100
FPS = 60

pygame.init()
icon = pygame.image.load("Assets/Arts/logo.png")
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("SIERRA ENGINE")

background_tile = pygame.image.load("Assets/Arts/background.png").convert()
info_panel_bg = pygame.image.load("Assets/Arts/panel_information.png").convert()

try:
    font = pygame.font.Font("Assets/Font/Font.ttf", 10)
except FileNotFoundError:
    print("font.ttf bulunamadı, varsayılan font kullanılacak.")
    font = pygame.font.SysFont(None, 24)

surface_type = "STEEL"
surface_data = SURFACE_TYPES[surface_type]
surface_color = surface_data["line_color"]

player = create_character(
    "TESTSUBJECT01",
    BLOCK_SIZE * 10,
    TOP_HEIGHT // 2 - CHARACTER_TYPES["TESTSUBJECT01"]["size"] // 2,
    CHARACTER_TYPES
)

camera_x = 0

def update_player(char, keys):
    moving = False
    if keys[pygame.K_LEFT]:
        char["x"] = max(0, char["x"] - char["speed"])
        moving = True
        char["facing_left"] = True
    if keys[pygame.K_RIGHT]:
        char["x"] = min(WORLD_WIDTH - char["size"], char["x"] + char["speed"])
        moving = True
        char["facing_left"] = False

    if moving:
        char["frame_timer"] += 1
        if char["frame_timer"] >= char["frame_delay"]:
            char["frame_timer"] = 0
            char["current_frame"] = (char["current_frame"] + 1) % len(char["walk_frames"])
    else:
        char["current_frame"] = 0

def main():
    DEBUG_MODE = True
    
    global camera_x
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        update_player(player, keys)
        camera_x = max(0, min(player["x"] - WINDOW_WIDTH / 4, WORLD_WIDTH - WINDOW_WIDTH))

        draw_world(screen, background_tile, surface_color, BLOCK_SIZE, TOP_HEIGHT, WORLD_BLOCKS, WINDOW_WIDTH, camera_x, player)
        draw_player(screen, player, camera_x)
        draw_info_panel(screen, info_panel_bg, font, TOP_HEIGHT, surface_type, surface_data, player)
        if DEBUG_MODE:
            draw_debug_info(screen, font, player, camera_x, clock.get_fps())

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
