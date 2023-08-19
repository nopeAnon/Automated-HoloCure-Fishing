#! C:\Users\minec\Documents\Python\holocure-fishing\fishing\Scripts\python.exe
import pyautogui
import time
import win32api, win32con, win32gui, win32ui
from threading import Thread
import threading

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
    'z':0x5A
}

stop_thread = threading.Event()

def press(button_key):
    print("pressing ", button_key)
    hwndMain = win32gui.FindWindow(None, "HoloCure")
    win = win32ui.CreateWindowFromHandle(hwndMain)
    win.SendMessage(win32con.WM_KEYDOWN, button[button_key], 0)
    time.sleep(0.01)
    win.SendMessage(win32con.WM_KEYUP, button[button_key], 0)


def continue_fishing():
    while not stop_thread.is_set():
        if pyautogui.locateOnScreen("./img/ok.png", confidence=0.6):
            press('j')
            time.sleep(0.01)
            press('j')
        time.sleep(0.5)


def fishing():
    hit_area = None
    while True:
        if not hit_area:
            hit_area = pyautogui.locateOnScreen("./img/box.png", confidence=0.6)
            print("Finding...")
            print(hit_area)

        if hit_area:
            pic = pyautogui.screenshot(region=(hit_area.left+15, hit_area.top+30, 1, hit_area.height-30))
            # right = 45, 236, 43
            # up = 225, 50, 50
            # e = 174, 49, 208
            # l = 246, 198, 67
            # d = 52,144,245


            w, h = pic.size

            press_button = ""
            
            for x in range(0, h):
                r,g,b = pic.getpixel((0,x))

                # enter
                # if (r,g,b) == (174, 49, 208):
                if r in range(172, 176) and g in range(47, 51) and b in range(206, 210):
                    press_button = 'j'
                    break

                # left
                # if (r,g,b) == (246, 198, 67):
                elif r in range(242, 250) and g in range(194, 202) and b in range(63, 71):
                    press_button = 'a'
                    break

                # right
                # if (r,g,b) == (45, 236, 43):
                elif r in range(43, 47) and g in range(234, 238) and b in range(41, 45):
                    press_button = 'd'
                    break
                
                # down
                # if (r,g,b) == (52,144,245):
                elif r in range(50, 54) and g in range(142, 146) and b in range(243, 247):
                    press_button = 's'
                    break

                # up
                # if (r,g,b) == (225, 50, 50):
                elif r in range(223, 227) and g in range(48, 52) and b in range(48, 52):
                    press_button = 'w'
                    break

            if press_button:
                press(press_button)

                

t1 = Thread(target=continue_fishing)

try:
    t1.start()
    fishing()
except(KeyboardInterrupt, SystemExit):
    stop_thread.set()
    t1.join()



            

    # time.sleep(0.1)