"""
send_input.py

Contains constants and functions for sending input.
"""

import time

import win32con

BUTTON = {
    "0": 0x30,
    "1": 0x31,
    "2": 0x32,
    "3": 0x33,
    "4": 0x34,
    "5": 0x35,
    "6": 0x36,
    "7": 0x37,
    "8": 0x38,
    "9": 0x39,
    "a": 0x41,
    "b": 0x42,
    "c": 0x43,
    "d": 0x44,
    "e": 0x45,
    "f": 0x46,
    "g": 0x47,
    "h": 0x48,
    "i": 0x49,
    "j": 0x4A,
    "k": 0x4B,
    "l": 0x4C,
    "m": 0x4D,
    "n": 0x4E,
    "o": 0x4F,
    "p": 0x50,
    "q": 0x51,
    "r": 0x52,
    "s": 0x53,
    "t": 0x54,
    "u": 0x55,
    "v": 0x56,
    "w": 0x57,
    "x": 0x58,
    "y": 0x59,
    "z": 0x5A,
    "space": 0x20,
    "enter": 0x0D,
    "left": 0x25,
    "up": 0x26,
    "right": 0x27,
    "down": 0x28,
    "shift": 0x10,
    "ctrl": 0x11,
}


def press(win, button_key: str):
    """Send button press to the target window."""
    print("Pressing " + button_key)
    button_key = button_key.lower()
    win.SendMessage(win32con.WM_KEYDOWN, BUTTON[button_key], 0)
    time.sleep(0.015)
    win.SendMessage(win32con.WM_KEYUP, BUTTON[button_key], 0)
