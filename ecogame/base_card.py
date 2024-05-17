import textwrap

import drawsvg as svg

from .utils import mm_to_px

GAME_NAME = "Ecogame for E2M"


class BaseCard:
    FONT_HEIGHT_TITLE = 24
    FONT_HEIGHT_VALUE = 34
    FONT_HEIGHT_TEXT = 20
    FONT_HEIGHT_KEYWORDS = 12
    FONT_HEIGHT_FLAVOUR = 12
    FONT_HEIGHT_COST = 18
    FONT_HEIGHT_COUNT = 12

    BACKGROUND_COLOR = (255, 255, 255, 255)
    INK_COLOR = (0, 0, 0, 255)

    UNIT_SIZE = FONT_HEIGHT_VALUE, FONT_HEIGHT_VALUE
    TEXT_ICON_SPACING = 2

    WIDTH, HEIGHT = None, None
    COLS, ROWS = None, None

    BLEED_MARGIN = mm_to_px(1.5)

    ROTATE = False

    def __init__(self, **config: hash):
        self._count = config.pop("count", 1)
        self._config = config
        self._is_blank = self._config.pop("is_blank", False)

    def _value(self, value: str, size: int, x: int, y: int, right_justify: bool = False):
        if value.endswith("P"):
            icon = "pollution"
            value = value[:-1]
        elif value.endswith("$"):
            icon = "prosperity"
            value = value[:-1]
        else:
            icon = None

        if right_justify:
            text_anchor = "end"
            icon_x = x - size
            text_x = icon_x - self.TEXT_ICON_SPACING
        else:
            text_anchor = "start"
            text_x = x
            icon_x = x + len(value) * size * 0.7 + self.TEXT_ICON_SPACING

        yield svg.Text(value, size, text_x, y + size, text_anchor=text_anchor, font_weight="bold")

        if icon:
            yield self._image(icon_x, y + size * 0.2, size * 0.8, icon)

    def _wrap(self, text: str, size: int, x: int, y: int, width: int, valign: str = "top"):
        if width == 0:
            lines = text.split("\n")
        else:
            lines = textwrap.wrap(text, width)

        height = (size + 2) * (len(lines) - 1)

        if valign == "top":
            offset = 0
        elif valign == "middle":
            offset = -height // 2
        elif valign == "bottom":
            offset = -height
        else:
            raise

        return svg.Text("\n".join(lines), size, x, y + offset)

    @staticmethod
    def _image(x, y, size, name):
        return svg.Image(x, y, size, size, path=f"./images/{name}.png", embed=True)

    @property
    def count(self):
        return self._count

    def render(self):
        if self._is_blank:
            return

        yield from self._render(**self._config)

    def _render(self, **config):
        raise NotImplementedError

    @property
    def width(self):
        return self.WIDTH

    @property
    def height(self):
        return self.HEIGHT


class PortraitCard(BaseCard):
    WIDTH, HEIGHT = mm_to_px(63.5), mm_to_px(88.9)
    MARGIN_LEFT, MARGIN_RIGHT = mm_to_px(5), mm_to_px(5)
    MARGIN_TOP, MARGIN_BOTTOM = mm_to_px(5), mm_to_px(5)
    INNER_WIDTH = WIDTH - MARGIN_LEFT - MARGIN_RIGHT
    INNER_HEIGHT = HEIGHT - MARGIN_TOP - MARGIN_BOTTOM
    BLEED_WIDTH = WIDTH + BaseCard.BLEED_MARGIN * 2
    BLEED_HEIGHT = HEIGHT + BaseCard.BLEED_MARGIN * 2
    ROTATE = True
    COLS, ROWS = 2, 4


class LandscapeCard(BaseCard):
    WIDTH, HEIGHT = mm_to_px(88.9), mm_to_px(63.5)
    MARGIN_LEFT, MARGIN_RIGHT = mm_to_px(5), mm_to_px(5)
    MARGIN_TOP, MARGIN_BOTTOM = mm_to_px(5), mm_to_px(5)
    INNER_WIDTH = WIDTH - MARGIN_LEFT - MARGIN_RIGHT
    INNER_HEIGHT = HEIGHT - MARGIN_TOP - MARGIN_BOTTOM
    BLEED_WIDTH = WIDTH + BaseCard.BLEED_MARGIN * 2
    BLEED_HEIGHT = HEIGHT + BaseCard.BLEED_MARGIN * 2
    COLS, ROWS = 2, 4