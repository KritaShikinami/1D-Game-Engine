import pygame
import sys
from source import (
    SURFACE_TYPES,
    CHARACTER_TYPES,
    create_character,
    create_npc,
    update_npc_passive,
    update_npc_aggressive,
    draw_world,
    draw_player,
    draw_npc,
    draw_info_panel,
    draw_debug_info,
    is_hit_by_mouse,
    get_cursor_type
)

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
pygame.mouse.set_visible(False)

icon = pygame.image.load("Assets/Arts/logo.png")
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("SIERRA ENGINE")

# --- Cursor görselleri ---
normal_cursor_img = pygame.image.load("Assets/Arts/normal_cursor.png").convert_alpha()
attack_cursor_img = pygame.image.load("Assets/Arts/attack_cursor.png").convert_alpha()

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

# Oyuncu
player = create_character(
    "TESTSUBJECT01-GUN",
    BLOCK_SIZE * 10,
    TOP_HEIGHT // 2 - CHARACTER_TYPES["TESTSUBJECT01-GUN"]["size"] // 2,
    CHARACTER_TYPES
)
player["firing"] = False
player["total_hp"] = 100

# NPC'ler
npc_passive = create_npc(
    "TESTSUBJECT01",
    BLOCK_SIZE * 20,
    TOP_HEIGHT // 2 - CHARACTER_TYPES["TESTSUBJECT01"]["size"] // 2,
    CHARACTER_TYPES
)

npc_aggressive = create_npc(
    "TESTSUBJECT01",
    BLOCK_SIZE * 30,
    TOP_HEIGHT // 2 - CHARACTER_TYPES["TESTSUBJECT01"]["size"] // 2,
    CHARACTER_TYPES,
    aggressive=True
)

camera_x = 0


def update_player(char, keys):
    if char.get("firing", False):
        char["frame_timer"] += 1
        if char["frame_timer"] >= char["frame_delay"]:
            char["frame_timer"] = 0
            char["current_frame"] += 1
            if char["current_frame"] >= len(char["walk_frames"]):
                char["type"] = "TESTSUBJECT01-GUN"
                char["walk_frames"] = [
                    pygame.image.load(path).convert_alpha()
                    for path in CHARACTER_TYPES["TESTSUBJECT01-GUN"]["walk_sequence"]
                ]
                char["frame_delay"] = CHARACTER_TYPES["TESTSUBJECT01-GUN"]["frame_delay"]
                char["current_frame"] = 0
                char["frame_timer"] = 0
                char["firing"] = False
        return

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


def draw_cursor(screen, mouse_pos, entities, camera_x):
    cursor_type = get_cursor_type(mouse_pos, entities, camera_x)
    cursor_img = attack_cursor_img if cursor_type == "attack" else normal_cursor_img
    screen.blit(cursor_img, (mouse_pos[0] - 8, mouse_pos[1] - 8))

def handle_click(mouse_pos, entities, camera_x):
    for npc in entities:
        if not npc["dead"] and is_hit_by_mouse(mouse_pos, npc, camera_x):
            npc["total_hp"] -= 50

            # Agresif NPC'ye ilk vurulduğunda silahını çıkarsın
            if npc.get("aggressive", False) and npc["type"] not in ("TESTSUBJECT01-GUN", "TESTSUBJECT01-FIRING"):
                npc["type"] = "TESTSUBJECT01-GUN"
                npc["walk_frames"] = [
                    pygame.image.load(path).convert_alpha()
                    for path in CHARACTER_TYPES["TESTSUBJECT01-GUN"]["walk_sequence"]
                ]
                npc["frame_delay"] = CHARACTER_TYPES["TESTSUBJECT01-GUN"]["frame_delay"]
                npc["current_frame"] = 0
                npc["frame_timer"] = 0

            if npc["total_hp"] <= 0:
                npc["dead"] = True
                npc["type"] = "TESTSUBJECT01-DEATH"
                npc["walk_frames"] = [
                    pygame.image.load(path).convert_alpha()
                    for path in CHARACTER_TYPES["TESTSUBJECT01-DEATH"]["walk_sequence"]
                ]
                npc["current_frame"] = 0
                npc["frame_timer"] = 0
                npc["frame_delay"] = CHARACTER_TYPES["TESTSUBJECT01-DEATH"]["frame_delay"]


def main():
    DEBUG_MODE = True
    global camera_x

    npcs = [npc_passive, npc_aggressive]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                handle_click(event.pos, npcs, camera_x)

                if not player.get("firing", False):
                    player["type"] = "TESTSUBJECT01-FIRING"
                    player["walk_frames"] = [
                        pygame.image.load(path).convert_alpha()
                        for path in CHARACTER_TYPES["TESTSUBJECT01-FIRING"]["walk_sequence"]
                    ]
                    player["frame_delay"] = CHARACTER_TYPES["TESTSUBJECT01-FIRING"]["frame_delay"]
                    player["current_frame"] = 0
                    player["frame_timer"] = 0
                    player["firing"] = True

        keys = pygame.key.get_pressed()
        update_player(player, keys)
        camera_x = max(0, min(player["x"] - WINDOW_WIDTH / 4, WORLD_WIDTH - WINDOW_WIDTH))

        draw_world(screen, background_tile, surface_color, BLOCK_SIZE, TOP_HEIGHT, WORLD_BLOCKS, WINDOW_WIDTH, camera_x, player)
        draw_player(screen, player, camera_x)

        for npc in npcs:
            if npc["dead"]:
                if npc["current_frame"] < len(npc["walk_frames"]) - 1:
                    npc["frame_timer"] += 1
                    if npc["frame_timer"] >= npc["frame_delay"]:
                        npc["frame_timer"] = 0
                        npc["current_frame"] += 1
            else:
                if npc.get("aggressive", False):
                    update_npc_aggressive(npc, player, WORLD_WIDTH)
                else:
                    update_npc_passive(npc, WORLD_WIDTH)

            draw_npc(screen, npc, camera_x)

        draw_info_panel(screen, info_panel_bg, font, TOP_HEIGHT, surface_type, surface_data, player)

        mouse_pos = pygame.mouse.get_pos()
        draw_cursor(screen, mouse_pos, npcs, camera_x)

        if DEBUG_MODE:
            draw_debug_info(screen, font, player, camera_x, clock.get_fps())

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
