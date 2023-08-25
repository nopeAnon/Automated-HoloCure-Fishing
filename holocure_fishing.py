import ctypes
import json
from math import floor
from pathlib import Path
from sys import platform
import time

import cv2
import numpy as np
import win32con, win32gui, win32ui

from imgproc import templates, masks
from send_input import press

DEBUG = False


def main() -> None:
    """Entry point for the program."""
    print("Welcome to Automated HoloCure Fishing!")
    print("Please open HoloCure, go to Holo House, and start fishing!")
    print("You can do other tasks as long as the HoloCure window isn't minimised.")
    print("It works even if the game is in the background!")
    # disable program DPI scaling - affects screen capture
    if platform == "win32":
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    # first time config load, but we check every second to see if it's changed
    keybinds = get_config()
    one_second_timer = time.perf_counter()
    counter = 0
    # Region of Interest - we only need this area of the screen
    BASE_ROI = (276, 242, 133, 38)  # left, top, right, bottom
    # Big loopy boi:
    while True:
        #   1. Use computer vision to get information about the game
        #   2. Use OpenCV template matching to check which button to press
        #   3. Send the inputs to the game
        last_time = time.perf_counter()
        # update the config once a second :)
        if last_time - one_second_timer > 1:
            keybinds = get_config()
            one_second_timer = last_time
        # find the window every loop - a bit ugly, but we can handle the game
        # closing and opening this way (there's probably a better way though)
        hwndMain = win32gui.FindWindow("YYGameMakerYY", "HoloCure")
        if hwndMain == 0:
            time.sleep(1)
            continue
        # capture only the area we need for image processing
        left, top, right, bottom = win32gui.GetClientRect(hwndMain)
        width, height = right - left, bottom - top
        if width == 0 or height == 0:  # skip if window minimised
            continue
        scale = round(height / 360)
        roi = np.multiply(scale, BASE_ROI)
        img_src = capture_game(hwndMain, *roi)
        # used to send input - a bit wasteful to call every loop though...
        win = win32ui.CreateWindowFromHandle(hwndMain)

        # resize the image down to 360p equivalent
        # so the rest of the code is resolution-invariant
        img_src = cv2.resize(
            img_src,
            dsize=None,
            fx=1 / scale,
            fy=1 / scale,
            interpolation=cv2.INTER_NEAREST,
        )
        if DEBUG:
            cv2.namedWindow("Source", cv2.WINDOW_NORMAL)
            cv2.imshow("Source", img_src)
            cv2.resizeWindow("Source", img_src.shape[1] * 2, img_src.shape[0] * 2)

        # maths time
        # look for rhythm game arrows first
        for key in ("space", "left", "right", "up", "down"):
            h, w, _ = templates[key].shape
            # offset so all templates line up properly
            h_offset = 10 - floor(h / 2)
            w_offset = 10 - floor(w / 2)
            res = cv2.matchTemplate(
                img_src[h_offset: h_offset + h, 103 + w_offset: 133],
                templates[key],
                cv2.TM_SQDIFF,
                mask=masks[key],
            )
            min_val, _, _, _ = cv2.minMaxLoc(res)
            # arbitrary magic number, gets stuck if mouse hovering over button
            if min_val < 1000:
                press(win, keybinds[key])
                time.sleep(0.2)
                break

        # look for "ok" button and press enter if so
        h, w, _ = templates["ok"].shape
        res = cv2.matchTemplate(
            img_src[9: 9 + h, 0:w],
            templates["ok"],
            cv2.TM_SQDIFF,
            mask=masks["ok"],
        )
        min_val, _, _, _ = cv2.minMaxLoc(res)
        # arbitrary magic number, handles the mouse hovering over the OK button
        if min_val < 60_000_000:
            press(win, "enter")
            time.sleep(0.01)
            press(win, "enter")
            time.sleep(0.01)
            press(win, "enter")
            time.sleep(0.01)
            press(win, "enter")
            time.sleep(0.01)
            press(win, "enter")
            time.sleep(0.01)
            press(win, "enter")
            counter += 1
            print("Fishing count: ", counter)


        elapsed = time.perf_counter() - last_time
        # debug to see how fast the loop runs
        if DEBUG:
            fps = 1 / elapsed
            print(f"FPS: {round(fps, 2):06.2f}" + "-" * round(fps / 10))
            cv2.waitKey(1)

        # slow the loop down to 100Hz max
        if elapsed < 0.01:
            time.sleep(0.01 - elapsed)


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


def capture_game(hwnd, left: int, top: int, width: int, height: int):
    """Get a screenshot of the given window.

    Works even if target hwnd is behind other windows, but not minimised.

    From https://stackoverflow.com/a/62293979
    and https://stackoverflow.com/q/40098142
    and https://stackoverflow.com/a/68310347"""
    # TODO: can probably refactor this as a class to avoid calling
    # constructors/destructors all the time
    # calculate offset (e.g. from title bar, window borders)
    offset_left, offset_top, *_ = win32gui.GetWindowRect(hwnd)
    offset_left, offset_top = win32gui.ScreenToClient(hwnd, (offset_left, offset_top))
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, width, height)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt(
        (0, 0),
        (width, height),
        dcObj,
        (left - offset_left, top - offset_top),
        win32con.SRCCOPY,
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
