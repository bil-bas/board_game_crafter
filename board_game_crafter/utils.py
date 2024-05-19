import os

DEFAULT_DPI = 96

MM_TO_PX_96DPI = 3.7795275591


def mm_to_px(mm: float) -> float:
    return round(mm * MM_TO_PX_96DPI)


A4_WIDTH, A4_HEIGHT = mm_to_px(210), mm_to_px(297)
LINE_WIDTH = 2

_game_name = None


def image_path(name):
    return os.path.join(f"./games/{_game_name}/images/", name)


def config_path(name):
    return os.path.join(f"./games/{_game_name}/config/", name)


def output_path(name):
    return os.path.join(f"./output/{_game_name}/", name)


def set_game_name(name: str):
    global _game_name
    _game_name = name
