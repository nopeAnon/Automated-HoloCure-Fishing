"""Contains constants and functions for image processing."""

import cv2

raw = dict(
    ok=cv2.imread("./img/360p/ok.png", cv2.IMREAD_UNCHANGED),
    box=cv2.imread("./img/360p/box.png", cv2.IMREAD_UNCHANGED),
    space=cv2.imread("./img/360p/space.png", cv2.IMREAD_UNCHANGED),
    left=cv2.imread("./img/360p/left.png", cv2.IMREAD_UNCHANGED),
    right=cv2.imread("./img/360p/right.png", cv2.IMREAD_UNCHANGED),
    up=cv2.imread("./img/360p/up.png", cv2.IMREAD_UNCHANGED),
    down=cv2.imread("./img/360p/down.png", cv2.IMREAD_UNCHANGED),
)

templates = {}
for name, img in raw.items():
    templates[name] = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

masks = {}
for name, img in raw.items():
    masks[name] = cv2.extractChannel(img, 3)
