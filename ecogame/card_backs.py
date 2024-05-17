import drawsvg as svg

from .utils import mm_to_px
from .base_card import LandscapeCard
from .base_cards import BaseCards


class CardBack(LandscapeCard):
    BORDER_COLOR = "black"
    BACKGROUND_COLOR = "white"
    BORDER_WIDTH = mm_to_px(10)
    FONT_HEIGHT_TITLE = 46
    FONT_HEIGHT_TYPE = 24

    def _render(self, card_type: str = ""):
        yield svg.Rectangle(-self.BLEED_MARGIN, -self.BLEED_MARGIN, self.BLEED_WIDTH, self.BLEED_HEIGHT,
                            fill=self.BORDER_COLOR, stroke="none")

        yield svg.Rectangle(self.MARGIN_LEFT, self.MARGIN_TOP, self.INNER_WIDTH, self.INNER_HEIGHT,
                            stroke="none", fill=self.BACKGROUND_COLOR)

        yield svg.Text("ECOGAME", self.FONT_HEIGHT_TITLE, self.WIDTH / 2, self.HEIGHT / 2,
                       center=True)

        if card_type:
            yield svg.Text(card_type, self.FONT_HEIGHT_TYPE, self.WIDTH / 2, self.HEIGHT / 2 + 40,
                           center=True)


class CardBacks(BaseCards):
    CARD_CLASS = CardBack
    CONFIG_FILE = "./config/card_backs.yaml"
