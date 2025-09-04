import os, time

WIDTH, HEIGHT = 80, 24
BUFFER_SIZE = WIDTH * HEIGHT
os.system("mode con: cols=81 lines=25")

SCREEN = [" " for _ in range(BUFFER_SIZE)]

if os.name == 'nt':
    import msvcrt
    import ctypes

    class _CursorInfo(ctypes.Structure):
        _fields_ = [("size", ctypes.c_int),
                    ("visible", ctypes.c_byte)]

def hide_cursor():
    if os.name == 'nt':
        ci = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = False
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
    elif os.name == 'posix':
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

def show_cursor():
    if os.name == 'nt':
        ci = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = True
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
    elif os.name == 'posix':
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def reset_buffer():
    global SCREEN
    SCREEN = [" " for _ in range(BUFFER_SIZE)]

def index(x, y):
    return y * WIDTH + x

def draw_point(x, y, char=""):
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        SCREEN[index(x, y)] = char

def draw_line(x1, y1, x2, y2, char=""):
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

# --- Ana döngü ---
def main():
    i = 0
    while True:
        i = i + 1
        hide_cursor()
        reset_buffer()
        draw_line(0, HEIGHT - 1, WIDTH - 1, HEIGHT - 1, "░")
        draw_text(2, 1, f"SIERRA ENGINE - V0.1.1")
        
        #Kodlar ve işlemler bundan sonra başlayabilir
        
        draw_point(20 + i, 22, "●")

        render()
        time.sleep(0.1)

main()
