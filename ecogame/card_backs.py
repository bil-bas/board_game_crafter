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

    def _render(self, count: int, card_type: str = ""):
        yield svg.Rectangle(0, 0, self.CARD_WIDTH, self.CARD_HEIGHT, fill=self.BORDER_COLOR, stroke="none")
        yield svg.Ellipse(self.CARD_WIDTH // 2, self.CARD_HEIGHT // 2,
                          rx=(self.CARD_WIDTH - self.BORDER_WIDTH) // 2,
                          ry=(self.CARD_HEIGHT - self.BORDER_WIDTH) // 2,
                          stroke="none", fill=self.BACKGROUND_COLOR)

        yield svg.Text("ECOGAME", self.FONT_HEIGHT_TITLE, self.CARD_WIDTH / 2, self.CARD_HEIGHT / 2,
                       center=True)

        if card_type:
            yield svg.Text(card_type, self.FONT_HEIGHT_TYPE, self.CARD_WIDTH / 2, self.CARD_HEIGHT / 2 + 40,
                           center=True)


class CardBacks(BaseCards):
    CARD_CLASS = CardBack
    CONFIG_FILE = "./config/card_backs.yaml"
