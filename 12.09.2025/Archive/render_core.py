# render_core.py
import os
import sys

WIDTH, HEIGHT = 80, 24
BUFFER_SIZE = WIDTH * HEIGHT
SCREEN = [" " for _ in range(BUFFER_SIZE)]

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def reset_buffer():
    global SCREEN
    SCREEN = [" " for _ in range(BUFFER_SIZE)]

def index(x, y):
    return y * WIDTH + x

def draw_point(x, y, char=" "):
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        SCREEN[index(x, y)] = char

def draw_line(x1, y1, x2, y2, char=" "):
    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy))
    if steps == 0:
        draw_point(x1, y1, char)
        return
    x_inc = dx / steps
    y_inc = dy / steps
    x, y = x1, y1
    for _ in range(steps):
        draw_point(int(round(x)), int(round(y)), char)
        x += x_inc
        y += y_inc

def draw_text(x, y, text):
    for i, ch in enumerate(text):
        draw_point(x + i, y, ch)

def render():
    clear_screen()
    for y in range(HEIGHT):
        row = SCREEN[y * WIDTH : (y + 1) * WIDTH]
        print("".join(row))
