import ctypes
import json
import os
from pathlib import Path
from sys import platform
import time
import traceback

import cv2
import numpy as np
import win32con, win32gui, win32ui

from imgproc import templates, masks
from send_input import press


def main() -> None:
    """Entry point for the program."""
    print("Welcome to Automated HoloCure Fishing!")
    print("Please open holocure, go to Holo House, and start fishing!")
    print("You can do other tasks as long as HoloCure window isn't minimised.")
    print("it works even if it's in the background!")
    # disable program DPI scaling so OpenCV debug shows at correct size
    if platform == "win32":
        errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(2)
    # first time config load, but we check every second to see if it's changed
    keybinds = get_config()
    one_second_timer = time.time()
    # Big loopy boi:
    while True:
        #   1. Use computer vision to get information about the game
        #   2. Calculate what inputs to send
        #   3. Send the inputs to the game
        last_time = time.time()
        # update the config once a second :)
        if last_time - one_second_timer > 1:
            keybinds = get_config()
            one_second_timer = last_time
        # find the window every loop - a bit ugly but we can handle the game
        # closing and opening this way (theres probably a better way though)
        hwndMain = win32gui.FindWindow("YYGameMakerYY", "HoloCure")
        if hwndMain == 0:
            time.sleep(1)
            continue
        img_src = capture_game(hwndMain)
        if img_src is None:  # skip if we can't find the window (e.g. its minimised)
            continue
        # used to send input - a bit wasteful to call every loop though...
        win = win32ui.CreateWindowFromHandle(hwndMain)

        # resize the window down to 640x360
        # so the rest of the code is resolution-invariant
        img_src = cv2.resize(img_src, (640, 360), interpolation=cv2.INTER_NEAREST)
        cv2.namedWindow("Source", cv2.WINDOW_NORMAL)
        cv2.imshow("Source", img_src)
        cv2.resizeWindow("Source", 1280, 720)

        # maths time
        # look for rhythm game arrows first
        # spacebar first
        res = cv2.matchTemplate(
            img_src[244 : 244 + 17, 379 + 2 : 409],
            templates["space"],
            cv2.TM_SQDIFF,
            mask=masks["space"],
        )
        min_val, _, _, _ = cv2.minMaxLoc(res)
        # arbitrary magic number, gets stuck if mouse hovering over button
        if min_val < 1000:
            press(win, keybinds["space"])

        # left/right
        for key in ("left", "right"):
            res = cv2.matchTemplate(
                img_src[243 : 243 + 19, 379:409],
                templates[key],
                cv2.TM_SQDIFF,
                mask=masks[key],
            )
            min_val, _, _, _ = cv2.minMaxLoc(res)
            # arbitrary magic number, gets stuck if mouse hovering over button
            if min_val < 1000:
                press(win, keybinds[key])
                break

        # up/down
        for key in ("up", "down"):
            res = cv2.matchTemplate(
                img_src[242 : 242 + 21, 379 + 1 : 409],
                templates[key],
                cv2.TM_SQDIFF,
                mask=masks[key],
            )
            min_val, _, _, _ = cv2.minMaxLoc(res)
            # arbitrary magic number, gets stuck if mouse hovering over button
            if min_val < 1000:
                press(win, keybinds[key])
                break

        # look for "ok" button and press enter if so
        res = cv2.matchTemplate(
            img_src[251 : 251 + 29, 276 : 276 + 89],
            templates["ok"],
            cv2.TM_SQDIFF,
            mask=masks["ok"],
        )
        min_val, _, _, _ = cv2.minMaxLoc(res)
        # arbitrary magic number, handles the mouse being over the OK button
        if min_val < 60_000_000:
            press(win, "enter")
            time.sleep(0.05)
            press(win, "enter")

        # debug to see how fast the loop runs
        elapsed = time.time() - last_time
        fps = 1 / elapsed
        print(f"FPS: {round(fps, 2):06.2f}" + "-" * round(fps / 10))
        cv2.waitKey(1)


def get_config():
    """Load game configuration and return a table."""
    # TODO: maybe only read if the file is modified
    SETTINGS_PATH = f"{Path.home()}/AppData/Local/HoloCure/settings.json"
    with open(SETTINGS_PATH) as config_file:
        config = json.load(config_file)
        keybinds = config.get("theButtons")
        if keybinds:
            return {
                "space": keybinds[0].lower(),
                "left": keybinds[2].lower(),
                "right": keybinds[3].lower(),
                "up": keybinds[4].lower(),
                "down": keybinds[5].lower(),
            }
        return {
            "space": "space",
            "left": "a",
            "right": "d",
            "up": "w",
            "down": "s",
        }


def capture_game(hwnd):
    """Get a screenshot of the given window.

    Works even if the is behind other windows but not minimised.

    From https://stackoverflow.com/a/62293979
    and https://stackoverflow.com/q/40098142
    and https://stackoverflow.com/a/68310347"""
    # TODO: can probably refactor this as a class to avoid calling
    # constructors/destructors all the time
    left, top, right, bottom = win32gui.GetClientRect(hwnd)
    # left and top are usually 0, 0 but just to be safe :)
    width, height = right - left, bottom - top
    # calculate offset (e.g. from title bar, window borders)
    left, top, *_ = win32gui.GetWindowRect(hwnd)
    offset_left, offset_top = win32gui.ScreenToClient(hwnd, (left, top))
    # if the window is minimised, return a black rectangle
    if width == 0 or height == 0:
        return None
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, width, height)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt(
        (0, 0), (width, height), dcObj, (-offset_left, -offset_top), win32con.SRCCOPY
    )

    im = dataBitMap.GetBitmapBits(True)
    img = np.frombuffer(im, dtype=np.uint8).reshape((height, width, 4))
    converted = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)

    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())
    return converted


if __name__ == "__main__":
    main()
