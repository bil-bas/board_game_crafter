import drawsvg as svg

from .base_cards import BaseCards
from .base_card import PortraitCard
from .utils import mm_to_px


class CardCutTemplate(PortraitCard):
    BORDER_COLOR = "black"
    BORDER_WIDTH = 1
    RADIUS = mm_to_px(4)

    def _render(self):
        yield svg.Rectangle(0, 0, self.WIDTH, self.HEIGHT,
                            rx=self.RADIUS, ry=self.RADIUS,
                            stroke=self.BORDER_COLOR, fill="none", stroke_width=self.BORDER_WIDTH)


class CardCutTemplates(BaseCards):
    CONFIG_FILE = "./config/card_cut_templates.yaml"
    CARD_CLASS = CardCutTemplate
