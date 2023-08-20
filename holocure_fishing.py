#! C:\Users\minec\Documents\Python\holocure-fishing\fishing\Scripts\python.exe
import pyautogui
import time
import win32con, win32gui, win32ui
from threading import Thread
import threading

# Config

UP = 'w'
DOWN = 's'
LEFT = 'a'
RIGHT = 'd'
SPACE = 'spacebar'



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
    'spacebar':0x20,
    'enter':0x0D,
}

stop_thread = threading.Event()

def press(button_key):
    print("pressing ", button_key)
    hwndMain = win32gui.FindWindow(None, "HoloCure")
    win = win32ui.CreateWindowFromHandle(hwndMain)
    win.SendMessage(win32con.WM_KEYDOWN, button[button_key], 0)
    time.sleep(0.05)
    win.SendMessage(win32con.WM_KEYUP, button[button_key], 0)


def continue_fishing():
    while not stop_thread.is_set():
        if pyautogui.locateOnScreen("./img/ok.png", confidence=0.6):
            press('enter')
            time.sleep(0.1)
            press('enter')
        time.sleep(0.5)


def fishing():
    print("Welcome to Automated HoloCure Fishing!")
    print("Please open holocure, go to holo house, and start fishing!")
    hit_area = None
    # i = 0
    while True:
        if not hit_area:
            hit_area = pyautogui.locateOnScreen("./img/box.png", confidence=0.6)
            if hit_area:
                print("Found Area!")
                print(hit_area)
                print("Please don't move/close/minimize the holocure window.")
                print("You can do other tasks as long as holocure window is visible.")
                print("However, doing heavy tasks may affect the program's ability to fish.")

        if hit_area:
            region = (hit_area.left+14, hit_area.top+24, hit_area.width-16, hit_area.height-30)
            pic = pyautogui.screenshot(region=region)
            # UP = 225, 50, 50
            # DOWN = 52,144,245
            # LEFT = 246, 198, 67
            # RIGHT = 45, 236, 43
            # SPACE = 174, 49, 208

            w, h = pic.size

            press_button = ""
            for x in range(0, w, 3):
                if press_button: break
                for y in range(0, h):
                    r,g,b = pic.getpixel((x,y))

                    # SPACE
                    if r in range(172, 176) and g in range(47, 51) and b in range(206, 210):
                        press_button = SPACE
                        # found = press(SPACE)
                        # break

                    # left
                    elif r in range(242, 250) and g in range(194, 202) and b in range(63, 71):
                        press_button = LEFT
                        # found = press(LEFT)
                        # break

                    # right
                    elif r in range(43, 47) and g in range(234, 238) and b in range(41, 45):
                        press_button = RIGHT
                        # found = press(RIGHT)
                        # break
                    
                    # down
                    elif r in range(50, 54) and g in range(142, 146) and b in range(243, 247):
                        press_button = DOWN
                        # found = press(DOWN)
                        # break

                    # up
                    elif r in range(223, 227) and g in range(48, 52) and b in range(48, 52):
                        press_button = UP
                        # found = press(UP)
                        # break

                    if press_button:
                        press(press_button)
                        # pyautogui.screenshot(f"Screen_{i}.png", region=region)
                        # i += 1
                        break

            # if press_button:
            #     press(press_button)

                

t1 = Thread(target=continue_fishing)

try:
    t1.start()
    fishing()
except(KeyboardInterrupt, SystemExit):
    stop_thread.set()
    t1.join()
