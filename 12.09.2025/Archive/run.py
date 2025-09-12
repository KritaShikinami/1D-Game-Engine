# run.py
import os
import time
from render_core import WIDTH, HEIGHT, reset_buffer, draw_line, draw_text, draw_point, render

if os.name == 'nt':
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

def main():
    i = 0
    while True:
        i += 1
        hide_cursor()
        reset_buffer()
        draw_line(0, HEIGHT - 1, WIDTH - 1, HEIGHT - 1, "░")
        draw_text(2, 1, f"SIERRA ENGINE - V0.1.1")
        draw_point(20 + i, 22, "●")
        render()
        time.sleep(0.1)

if __name__ == "__main__":
    os.system("mode con: cols=81 lines=25")
    main()
