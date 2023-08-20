import pyautogui
import time
import json
import win32con, win32gui, win32ui
from threading import Thread
import threading
from pathlib import Path
import os

dir_path = os.path.dirname(os.path.realpath(__file__))


def getconfig():
    with open(f"{Path.home()}/AppData/Local/HoloCure/settings.json") as config_file:
        config = json.load(config_file)
        keybinds = config.get("theButtons")
        if keybinds:
            return keybinds
        return ['z', 'x', 'a', 'd', 'w', 's']


# Config
SPACE, _, LEFT, RIGHT, UP, DOWN = getconfig()
up_color = (225, 50, 50)
down_color = (52,144,245)
left_color = (246, 198, 67)
right_color = (45, 236, 43)
space_color = (174, 49, 208)
color_tolerance = 3

space_r_range = range(space_color[0]-color_tolerance, space_color[0]+color_tolerance)
space_g_range = range(space_color[1]-color_tolerance, space_color[1]+color_tolerance)
space_b_range = range(space_color[2]-color_tolerance, space_color[2]+color_tolerance)

up_r_range = range(up_color[0]-color_tolerance, up_color[0]+color_tolerance)
up_g_range = range(up_color[1]-color_tolerance, up_color[1]+color_tolerance)
up_b_range = range(up_color[2]-color_tolerance, up_color[2]+color_tolerance)

down_r_range = range(down_color[0]-color_tolerance, down_color[0]+color_tolerance)
down_g_range = range(down_color[1]-color_tolerance, down_color[1]+color_tolerance)
down_b_range = range(down_color[2]-color_tolerance, down_color[2]+color_tolerance)

left_r_range = range(left_color[0]-color_tolerance, left_color[0]+color_tolerance)
left_g_range = range(left_color[1]-color_tolerance, left_color[1]+color_tolerance)
left_b_range = range(left_color[2]-color_tolerance, left_color[2]+color_tolerance)

right_r_range = range(right_color[0]-color_tolerance, right_color[0]+color_tolerance)
right_g_range = range(right_color[1]-color_tolerance, right_color[1]+color_tolerance)
right_b_range = range(right_color[2]-color_tolerance, right_color[2]+color_tolerance)




button = {
    '0':0x30,
    '1':0x31,
    '2':0x32,
    '3':0x33,
    '4':0x34,
    '5':0x35,
    '6':0x36,
    '7':0x37,
    '8':0x38,
    '9':0x39,
    'a':0x41,
    'b':0x42,
    'c':0x43,
    'd':0x44,
    'e':0x45,
    'f':0x46,
    'g':0x47,
    'h':0x48,
    'i':0x49,
    'j':0x4A,
    'k':0x4B,
    'l':0x4C,
    'm':0x4D,
    'n':0x4E,
    'o':0x4F,
    'p':0x50,
    'q':0x51,
    'r':0x52,
    's':0x53,
    't':0x54,
    'u':0x55,
    'v':0x56,
    'w':0x57,
    'x':0x58,
    'y':0x59,
    'z':0x5A,
    'space':0x20,
    'enter':0x0D,
}

stop_thread = threading.Event()

def press(button_key: str):
    button_key = button_key.lower()
    print("pressing ", button_key)
    hwndMain = win32gui.FindWindow(None, "HoloCure")
    win = win32ui.CreateWindowFromHandle(hwndMain)
    win.SendMessage(win32con.WM_KEYDOWN, button[button_key], 0)
    time.sleep(0.05)
    win.SendMessage(win32con.WM_KEYUP, button[button_key], 0)
    time.sleep(0.05)


def continue_fishing():
    while not stop_thread.is_set():
        if pyautogui.locateOnScreen(f"{dir_path}/img/ok.png", confidence=0.6):
            press('enter')
            press('enter')
        time.sleep(0.5)

def fishing():
    print("Welcome to Automated HoloCure Fishing!")
    print("Please open holocure, go to holo house, and start fishing!")
    hit_area = None
    region = None
    # i = 0
    while True:
        if not hit_area:
            hit_area = pyautogui.locateOnScreen(f"{dir_path}/img/box.png", confidence=0.6)
            if hit_area:
                print("Found Area!")
                print(hit_area)
                print("Please don't move/close/minimize the holocure window.")
                print("You can do other tasks as long as holocure window is visible.")
                print("However, doing heavy tasks may affect the program's ability to fish.")
                region = (hit_area.left+14, hit_area.top+24, hit_area.width-16, hit_area.height-30)

        if hit_area and region:
            pic = pyautogui.screenshot(region=region)
            # UP = 225, 50, 50
            # DOWN = 52,144,245
            # LEFT = 246, 198, 67
            # RIGHT = 45, 236, 43
            # SPACE = 174, 49, 208

            w, h = pic.size

            press_button = ""
            for x in range(0, w, 2):
                if press_button: break
                for y in range(0, h):
                    r,g,b = pic.getpixel((x,y))

                    # SPACE
                    if r in space_r_range and g in space_g_range and b in space_b_range:
                        press_button = SPACE

                    # left
                    elif r in left_r_range and g in left_g_range and b in left_b_range:
                        press_button = LEFT

                    # right
                    elif r in right_r_range and g in right_g_range and b in right_b_range:
                        press_button = RIGHT
                    
                    # down
                    elif r in down_r_range and g in down_g_range and b in down_b_range:
                        press_button = DOWN

                    # up
                    elif r in up_r_range and g in up_g_range and b in up_b_range:
                        press_button = UP

                    if press_button:
                        press(press_button)
                        # pyautogui.screenshot(f"Screen_{i}.png", region=region)
                        # i += 1
                        break

                

t1 = Thread(target=continue_fishing)

try:
    t1.start()
    fishing()
except(KeyboardInterrupt, SystemExit):
    stop_thread.set()
    t1.join()
