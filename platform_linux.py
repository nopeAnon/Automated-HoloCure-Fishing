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
        self._bounds = None

        # initialized in holocure screenshot
        self._image = None

    def wait_until_application_handle(self):
        # this function gets called every frame to check whether the window handle is still valid (i.e. if the
        #  program has been closed) to handle closing & reopening of Holocure.
        # This is a bad idea on linux because the only way to get a valid window id for Holocure is by using a seperate
        #  xwininfo program that needs to be called as a subprocess. This adds frametime which slows the entire program
        #  down.
        # So we assume the first Holocure window we find will be valid indefinitely. If the user closes Holocure, the
        #  script will have to be restarted.
        if self._window:
            return

        while True:
            try:
                out = subprocess.check_output(["xwininfo", "-name", "HoloCure"], universal_newlines=True)
                break
            except subprocess.CalledProcessError:
                time.sleep(5)

        window_id_hex = re.search(r'Window id: (0x[0-9a-fA-F]+)', out)
        window_id_decimal = int(window_id_hex.group(1), 16)

        disp = Display()
        self._window = disp.create_resource_object("window", int(window_id_decimal))

    def get_holocure_bounds(self):
        # this function gets called every frame to check whether the window has been moved / changed resolution.
        # Similar problems to wait_until_application_handle.
        # once we find valid bounds, assume they'll be valid indefinitely.
        # Note: the x & y position doesn't actually matter because we take screenshots relatively, only changing
        #       resolution will break the script.
        if self._bounds:
            return self._bounds

        xwin_out = subprocess.run(["xwininfo", "-name", "HoloCure"], capture_output=True, text=True).stdout

        geometry_pattern = re.compile(r'-geometry (\d+)x(\d+)\+(\d+)\+(\d+)')
        geometry_match = geometry_pattern.search(xwin_out)

        self._bounds = (int(geometry_match.group(3)), int(geometry_match.group(4)), int(geometry_match.group(1)), int(
            geometry_match.group(2)))
        return self._bounds

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
        width, height = self._bounds[2], self._bounds[3]
        raw = self._window.get_image(0, 0, width, height, X.ZPixmap, 0xffffffff)
        # numpy magic trick
        self._image = np.frombuffer(raw.data, dtype=np.uint8).reshape((height, width, 4))[:, :, :3]

        return self._image[roi[1]:roi[1] + roi[3], roi[0]:roi[0] + roi[2], :]

    def config_file_path(self):
        # If you have custom keybinds, remove None and add the path of the settings.json file between double qoutes.
        # Example:
        # return "/home/anton/.var/app/com.valvesoftware.Steam/data/Steam/steamapps/compatdata/2420510/pfx/drive_c/users/steamuser/AppData/Local/HoloCure/settings.json"
        return None

    def offset(self, fish_count):
        # 0 pixels at 0 fish, -17 pixels at speed 7
        return np.floor(-17 * min(fish_count, 70) / 70)
