import os

DEFAULT_DPI = 96

MM_TO_PX_96DPI = 3.7795275591


def mm_to_px(mm: float) -> float:
    return round(mm * MM_TO_PX_96DPI)


A4_WIDTH, A4_HEIGHT = mm_to_px(210), mm_to_px(297)
LINE_WIDTH = 2


def image_path(name):
    return os.path.join("./games/ecogame/images/", name)


def config_path(name):
    return os.path.join("./games/ecogame/config/", name)