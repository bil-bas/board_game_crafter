import textwrap

from PIL import ImageFont

MM_TO_PX = 3.7795275591


def mm_to_px(mm: float) -> int:
    return round(mm * MM_TO_PX)


A4_WIDTH, A4_HEIGHT = mm_to_px(210), mm_to_px(297)
LINE_WIDTH = 2


class Font:
    def __init__(self, font_name):
        self._font_name = font_name
        self._fonts = {}

    def text(self, draw, pos, text: str, color: tuple, size: int, anchor: str = None, wrap_width: int = None):

        if wrap_width is not None:
            text = textwrap.fill(text, wrap_width)

        if size not in self._fonts:
            self._fonts[size] = ImageFont.truetype(f"./fonts/{self._font_name}.ttf", size)
        font = self._fonts[size]

        draw.text(pos, text, fill=color, font=font, anchor=anchor)
