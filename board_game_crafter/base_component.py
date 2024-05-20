import textwrap

import drawsvg as svg

from .utils import mm_to_px


class Face:
    FRONT = "front"
    BACK = "Back"
    TEMPLATE = "template"

    ALL = [FRONT, BACK, TEMPLATE]


class BaseComponent:
    WIDTH, HEIGHT = None, None
    COLS, ROWS = None, None
    FONT_FAMILY_BODY, FONT_FAMILY_TITLE = "serif", "sans"

    BLEED_MARGIN = mm_to_px(2)
    MARGIN_LEFT = MARGIN_RIGHT = MARGIN_TOP = MARGIN_BOTTOM = MARGIN = None

    ROTATE = False

    TEMPLATE_RADIUS = mm_to_px(4)
    TEMPLATE_COLOR = "black"
    TEMPLATE_THICKNESS = 1

    def __init__(self, **config: hash):
        self._count = config.pop("count", 1)
        self._config = config
        self._is_blank = self._config.pop("is_blank", False)

    def _wrap(self, text: str, size: int, x: float, y: float, width: int, valign: str = "top",
              font_family: str = None) -> svg.Text:
        if font_family is None:
            font_family = self.FONT_FAMILY_BODY

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
            raise ValueError(f"Bad valign: {valign}")

        return svg.Text("\n".join(lines), size, x, y + offset, font_family=font_family)

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
        raise NotImplementedError

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

    @property
    def margin_top(self) -> float:
        return self.MARGIN_TOP or self.MARGIN

    @property
    def margin_left(self) -> float:
        return self.MARGIN_LEFT or self.MARGIN

    @property
    def margin_right(self) -> float:
        return self.MARGIN_RIGHT or self.MARGIN

    @property
    def margin_bottom(self) -> float:
        return self.MARGIN_BOTTOM or self.MARGIN

    @property
    def inner_width(self) -> float:
        return self.width - self.margin_left - self.margin_right

    @property
    def inner_height(self) -> float:
        return self.height - self.margin_top - self.margin_bottom

    @property
    def bleed_width(self) -> float:
        return self.width + self.BLEED_MARGIN * 2

    @property
    def bleed_height(self) -> float:
        return self.height + self.BLEED_MARGIN * 2
