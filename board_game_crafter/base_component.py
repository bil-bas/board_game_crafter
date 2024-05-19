import textwrap

import drawsvg as svg

from .utils import mm_to_px, image_path


class Face:
    FRONT = "front"
    BACK = "Back"
    TEMPLATE = "template"

    ALL = [FRONT, BACK, TEMPLATE]


class BaseComponent:
    FONT_HEIGHT_TITLE = 24
    FONT_HEIGHT_VALUE = 34
    FONT_HEIGHT_TEXT = 20
    FONT_HEIGHT_KEYWORDS = 12
    FONT_HEIGHT_FLAVOUR = 12
    FONT_HEIGHT_COST = 18
    FONT_HEIGHT_COUNT = 12

    UNIT_SIZE = FONT_HEIGHT_VALUE, FONT_HEIGHT_VALUE
    TEXT_ICON_SPACING = 2

    WIDTH, HEIGHT = None, None
    COLS, ROWS = None, None

    BLEED_MARGIN = mm_to_px(1.5)
    BLEED_WIDTH = BLEED_HEIGHT = None
    MARGIN_LEFT = MARGIN_RIGHT = MARGIN_TOP = MARGIN_BOTTOM = None
    INNER_WIDTH = INNER_HEIGHT = None
    BACK_LABEL = "Improvement"

    ROTATE = False

    BACK_BORDER_COLOR = "#555555"  # Dark grey
    BACK_BACKGROUND_COLOR = "#F2EBE3"  # Ivory
    BACK_BORDER_WIDTH = mm_to_px(10)
    BACK_FONT_HEIGHT_TITLE = 32
    BACK_FONT_HEIGHT_TYPE = 20

    TEMPLATE_RADIUS = mm_to_px(4)
    TEMPLATE_COLOR = "black"
    TEMPLATE_THICKNESS = 1

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

    def _wrap(self, text: str, size: int, x: int, y: int, width: int, valign: str = "top") -> svg.Text:
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
    def _image(x: float, y: float, size: float, name: str) -> svg.Image:
        return svg.Image(x, y, size, size, path=image_path(f"{name}.png"), embed=True)

    @property
    def count(self) -> int:
        return self._count

    def render(self, face: str):
        if self._is_blank:
            return

        if face == Face.FRONT:
            yield from self._render_front(**self._config)
        elif face == Face.BACK:
            yield from self._render_back(**self._config)
        elif face == Face.TEMPLATE:
            yield from self._render_template(**self._config)
        else:
            raise RuntimeError(f"Unknown face: {face}")

    def _render_front(self, **config):
        raise NotImplementedError

    def _render_back(self, **config):
        yield svg.Rectangle(-self.BLEED_MARGIN, -self.BLEED_MARGIN, self.BLEED_WIDTH, self.BLEED_HEIGHT,
                            fill=self.BACK_BORDER_COLOR, stroke="none")

        yield svg.Rectangle(self.MARGIN_LEFT, self.MARGIN_TOP, self.INNER_WIDTH, self.INNER_HEIGHT,
                            stroke="none", fill=self.BACK_BACKGROUND_COLOR)

        yield svg.Text("ECOGAME", self.BACK_FONT_HEIGHT_TITLE, self.width / 2, self.height / 2,
                       center=True)

        yield svg.Text(self.BACK_LABEL, self.BACK_FONT_HEIGHT_TYPE, self.width / 2, self.height / 2 + 40,
                       center=True)

    def _render_template(self, **config) -> None:
        yield svg.Rectangle(0, 0, self.width, self.height,
                            rx=self.TEMPLATE_RADIUS, ry=self.TEMPLATE_RADIUS,
                            stroke=self.TEMPLATE_COLOR, fill="none", stroke_width=self.TEMPLATE_THICKNESS)

    @property
    def width(self) -> float:
        return self.WIDTH

    @property
    def height(self) -> float:
        return self.HEIGHT
