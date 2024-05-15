import drawsvg as svg

from ecogame.utils import mm_to_px
from ecogame.base_card import BaseCard


class DisasterDie(BaseCard):
    SIZES = [25, 19, 16, 12]  # in mm.
    CARD_WIDTH, CARD_HEIGHT = mm_to_px(SIZES[0]), mm_to_px(SIZES[0])
    MARGIN_LEFT, MARGIN_RIGHT = mm_to_px(0), mm_to_px(0)
    MARGIN_TOP, MARGIN_BOTTOM = mm_to_px(0), mm_to_px(0)
    INNER_WIDTH = CARD_WIDTH - MARGIN_LEFT - MARGIN_RIGHT
    INNER_HEIGHT = CARD_HEIGHT - MARGIN_TOP - MARGIN_BOTTOM
    ROWS, COLS = 6, 6

    def _render(self, pips: int, size: int, count: int = 1):
        yield svg.Image(0, 0, size, size, path=f"./images/dice-{pips}.png", embed=True)

    @property
    def width(self):
        return self._config["size"]

    @property
    def height(self):
        return self._config["size"]