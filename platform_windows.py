import ctypes
import os
import time
from pathlib import Path

import cv2
import numpy as np
import win32con
import win32gui
import win32ui

from platform import Platform
from send_input import press


class Windows(Platform):

    def __init__(self):
        self.handle = None,
        self.window = None

        # disable program DPI scaling - affects screen capture
        ctypes.windll.shcore.SetProcessDpiAwareness(2)

    def wait_until_application_handle(self):
        while True:
            hwndMain = win32gui.FindWindow("YYGameMakerYY", "HoloCure")
            if hwndMain != 0:
                break

            time.sleep(1)

        self.handle = hwndMain,
        self.window = win32gui.CreateWindowFromHandle(hwndMain)

    def config_file_path(self):
        path = f"{Path.home()}/AppData/Local/HoloCure/settings.json"
        if os.path.isfile(path):
            return path

        return None

    def get_holocure_bounds(self):
        if not self.handle:
            return None
        left, right, top, bottom = win32gui.GetClientRect(self.handle)
        return left, right, right - left, bottom - top

    def holocure_screenshot(self, roi):
        if not self.handle:
            return

        return capture_game(self.handle, *roi)

    def press_key(self, key):
        if not self.window:
            return

        press(self.window, "enter")


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
