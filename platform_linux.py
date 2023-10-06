import math
import re
import subprocess
import time

import numpy as np

from platform import Platform

import Xlib.XK
from Xlib import X, protocol
from Xlib.display import Display


class Linux(Platform):

    def __init__(self):
        # initialized in wait_until_application_handle
        self._window = None

    def wait_until_application_handle(self):
        # This function gets called every frame to check whether the window handle is still valid (i.e. if the
        #  program has been closed) to handle closing & reopening of Holocure.
        # This is not necessarily the smartest idea on Linux because we have to recursive loop over all windows to find
        #  the correct one.
        # So assume the window will be valid indefinitely.
        if self._window:
            return

        # The actual visible Holocure window might be nested in any number of parent windows depending on the
        # compositor. We henceforth have to search recursively.
        disp = Display()
        def search_holocure_window(window):
            name = window.get_wm_name()
            classs = window.get_wm_class()
            if name == "HoloCure" and classs == ("steam_app_2420510", "steam_app_2420510"):
                self._window = window
                return

            for child in window.query_tree().children:
                search_holocure_window(child)

        search_holocure_window(disp.screen().root)

    def get_holocure_bounds(self):
        # Absolute position of the window doesn't matter because we can screenshot HoloCure seperately. We only store
        #  width and height
        geometry = self._window.get_geometry()
        w, h = geometry.width, geometry.height
        return 0, 0, w, h

    def press_key(self, key):
        if key == "enter":
            key = "Return"
        # TODO: temporary hack, but handling holocure keys -> platform keys should be done in the platform module as
        #  well in the future, i.e. have a map like the one in send_input.py for windows.

        disp = Display()
        the_root = disp.screen().root

        event = protocol.event.KeyPress(
            time=X.CurrentTime,
            root=the_root, window=self._window, same_screen=0, child=X.NONE,
            root_x=0, root_y=0, event_x=0, event_y=0,
            state=0, detail=disp.keysym_to_keycode(Xlib.XK.string_to_keysym(key))
        )
        disp.send_event(self._window, event, propagate=True)
        disp.sync()

        # we need to wait at least a frame between press and release to make sure holocure picks up the input
        time.sleep(0.03)

        event = protocol.event.KeyRelease(
            time=X.CurrentTime,
            root=the_root, window=self._window, same_screen=0, child=X.NONE,
            root_x=0, root_y=0, event_x=0, event_y=0,
            state=0, detail=disp.keysym_to_keycode(Xlib.XK.string_to_keysym(key))
        )
        disp.send_event(self._window, event, propagate=True)
        disp.sync()

    def holocure_screenshot(self, roi=None):
        raw = self._window.get_image(*roi, X.ZPixmap, 0xffffffff)
        return np.frombuffer(raw.data, dtype=np.uint8).reshape((roi[3], roi[2], 4))[:, :, :3]

    def config_file_path(self):
        # If you have custom keybinds, remove None and add the path of the settings.json file between double qoutes.
        # Example:
        # return "/home/anton/.var/app/com.valvesoftware.Steam/data/Steam/steamapps/compatdata/2420510/pfx/drive_c/users/steamuser/AppData/Local/HoloCure/settings.json"
        return None

    def offset(self, fish_count):
        # 0 pixels at 0 fish, -15 pixels at speed 7
        return math.floor(-15 * min(fish_count, 70) / 70)
