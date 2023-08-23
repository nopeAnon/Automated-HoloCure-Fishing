import pyautogui
import time
import json
import win32con, win32gui, win32ui
from pathlib import Path
import os
import traceback
from PIL import Image
import cv2 as cv
import numpy as np
import mss.tools

dir_path = os.path.dirname(os.path.realpath(__file__))
debug = False

def getconfig():
    with open(f"{Path.home()}/AppData/Local/HoloCure/settings.json") as config_file:
        config = json.load(config_file)
        keybinds = config.get("theButtons")
        resolution = config.get("Resolution")
        if keybinds:
            print("found keybinds")
            return keybinds, resolution
        return ['z', 'x', 'a', 'd', 'w', 's', 0.0]


# Config
keybinds, resolution = getconfig()
SPACE, _, LEFT, RIGHT, UP, DOWN = keybinds
needles = {"up": UP, "down": DOWN, "left": LEFT, "right": RIGHT, "space": SPACE}
res = "INVALID RESOLUTION"
pre_left_offset = 0
pre_top_offset = 0
pre_width = 100
pre_height = 100
hitbox_left_offset = 0
hitbox_top_offset = 0
hitbox_width = 100
hitbox_height = 100

if resolution == 1.0:
    pre_left_offset = -120
    pre_top_offset = 23
    pre_width = 133
    pre_height = 52
    hitbox_left_offset = -17
    hitbox_top_offset = -3 
    hitbox_width = 83
    hitbox_height = 87
    res = "720p"
elif resolution == 2.0:
    pre_left_offset = -180
    pre_top_offset = 34
    pre_width = 200
    pre_height = 78
    hitbox_left_offset = -25
    hitbox_top_offset = -5
    hitbox_width = 125
    hitbox_height = 130
    res = "1080p"

print(f"{res} mode set")

print("Preloading Images...")
images_name = list(needles.keys()) + ["ok", "box"]
images = {name:cv.imread(f"{dir_path}/img/{res}/{name}.png", cv.IMREAD_UNCHANGED) for name in images_name}

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
    'left':0x25,
    'up':0x26,
    'right':0x27,
    'down':0x28,
    'shift':0x10,
    'ctrl':0x11

}

win = None

def press(button_key: str):
    button_key = button_key.lower()
    win.SendMessage(win32con.WM_KEYDOWN, button[button_key], 0)
    time.sleep(0.05)
    win.SendMessage(win32con.WM_KEYUP, button[button_key], 0)
    time.sleep(0.05)

# clear debug folder if present
if os.path.exists(f"{dir_path}/debug"):
    for f in os.listdir(f"{dir_path}/debug"):
        os.remove(f"{dir_path}/debug/{f}")

def _pil_frombytes(im):
    return Image.frombytes('RGB', im.size, im.bgra, 'raw', 'BGRX').tobytes()

i = 0
# for debuggin if enabled
def debug_screenshot(img, debug_title=f"{i}_screen.png"):
    global i
    if not debug:
        return
    os.makedirs(f"{dir_path}/debug", exist_ok=True)
    mss.tools.to_png(_pil_frombytes(img), img.size, output=f"{dir_path}/debug/{i}_{debug_title}.png")
    i += 1

def locate(sct, needle, region=None, mon=1, confidence=0.8, method=cv.TM_CCOEFF_NORMED, debug_title="screen"):
    add_left = 0
    add_top = 0
    
    if not region:
        region = sct.monitors[mon]
    else:
        add_left = region[0]
        add_top = region[1]

    img = sct.grab(region)
    res = cv.matchTemplate(np.array(img), needle, method)
    if debug:
        global i
        debug_screenshot(img, debug_title=debug_title)
        i += 1
    _,_,_, max_loc = cv.minMaxLoc(res)
    h, w, _ = needle.shape
    if (res >= confidence).any():
        return (max_loc[0]+add_left, max_loc[1]+add_top, max_loc[0]+add_left+w, max_loc[1]+add_top+h)
    return None

max_retry = 50

def fishing():
    print("Welcome to Automated HoloCure Fishing!")
    print("Please open holocure, go to holo house, and start fishing!")
    print("Please don't move/close/minimize the holocure window.")
    print("You can do other tasks as long as holocure window is visible.")
    print("However, doing heavy tasks may affect the program's ability to fish.")
    print("===============")
    hit_area = None
    
    pre_region = None
    
    region = None
    
    prepared = None
    
    retry = max_retry

    # Specify which monitor has the holocure window. Monitor count starts at 1. So if you want monitor 2, mon=2
    monitor = 1

    hwndMain = win32gui.FindWindow(None, "HoloCure")

    global win

    with mss.mss() as sct:
        while True:
            if not hwndMain:
                print("\rHolocure window not found! Trying again in 5 seconds...", end="")
                time.sleep(5)
                hwndMain = win32gui.FindWindow(None, "HoloCure")
            elif hwndMain and not win:
                print("Holocure window found!")
                win = win32ui.CreateWindowFromHandle(hwndMain)

            # check for a hit_area inidcating a running minigame
            if not hit_area:
                prepared = None
                # scan for "ok" box in case fishing has to continue
                if locate(sct, images["ok"], confidence=0.6, mon=monitor, debug_title="finding_ok"):
                    print("continue fishing...")
                    press('enter')
                    time.sleep(0.05)
                    press('enter')
                    time.sleep(0.5)
                else:
                    # scan for hit region once on full screen and later only near the old region to save scan time between button presses
                    hit_area = locate(sct, images["box"], region=region, confidence=0.5, mon=monitor, debug_title="finding_hit_area")
                if hit_area:
                    print("found hit area!")
                    print(hit_area)
                    # changed to bbox region. See https://chayanvinayak.blogspot.com/2013/03/bounding-box-in-pilpython-image-library.html
                    pre_region = (hit_area[0]+pre_left_offset, hit_area[1]+pre_top_offset, hit_area[0]+pre_left_offset+pre_width, hit_area[1]+pre_top_offset+pre_height)
                    region = (hit_area[0]+hitbox_left_offset, hit_area[1]+hitbox_top_offset, hit_area[0]+hitbox_left_offset+hitbox_width, hit_area[1]+hitbox_top_offset+hitbox_height)
                    if debug:
                        print(f"pre_region: {pre_region}")
                        print(f"region: {region}")
                        debug_screenshot(sct.grab((pre_region)), debug_title="scanbox")
                        debug_screenshot(sct.grab((pre_region)), debug_title="hitbox")
            elif retry > 0:
                # we found a running hit area
                
                retry -= 1
                if not prepared:
                    # take a picture of the area before the hit area
                    # try to find a needle in advance
                    for needle in needles.items():
                        if locate(sct, images[needle[0]], region=pre_region, confidence=0.7, mon=monitor, debug_title=f"scanning_{needle[0]}") is not None:
                            print(f"prepare {needle[0]}")
                            prepared = needle
                            debug_screenshot(sct.grab((pre_region)), debug_title=f"prepare_{prepared[0]}")
                            retry = max_retry
                            break
                else:
                    # take a picture of the hit area and wait for the prepared needle to arrive
                    # pic = pyautogui.screenshot(region=region)
                    if locate(sct, images[prepared[0]], region=region, confidence=0.6, mon=monitor, debug_title=f"waiting_{prepared[0]}") is not None:
                        # needle arrived
                        print(f"pressing {prepared[0]}")
                        debug_screenshot(sct.grab((region)), debug_title=f"hit_{prepared[0]}")
                        press(prepared[1])
                        # reset prepared needle
                        prepared = None
                        # check if hit area is still present to continue minigame
                        hit_area = locate(sct, images["box"], region=region, confidence=0.5, mon=monitor, debug_title="finding_hit_area")
            else:
                retry = max_retry
                hit_area = locate(sct, images["box"], region=region, confidence=0.5, mon=monitor, debug_title="finding_hit_area")



try:
    fishing()
except(KeyboardInterrupt, SystemExit):
    pass
except Exception as e:
        traceback.print_exc()

    
