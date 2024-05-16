import drawsvg as svg

from .base_cards import BaseCards
from .base_card import PortraitCard
from .utils import mm_to_px


class CutTemplate(PortraitCard):
    BORDER_COLOR = "black"
    BORDER_WIDTH = 1
    RADIUS = mm_to_px(4)

    def _render(self, count: int):
        yield svg.Rectangle(0, 0, self.CARD_WIDTH, self.CARD_HEIGHT,
                            rx=self.RADIUS, ry=self.RADIUS,
                            stroke=self.BORDER_COLOR, fill="none", stroke_width=self.BORDER_WIDTH)


class CutTemplates(BaseCards):
    CONFIG_FILE = "./config/cut_templates.yaml"
    CARD_CLASS = CutTemplate
    ROWS, COLS = 4, 2
