import drawsvg as svg

from ecogame.utils import mm_to_px
from ecogame.base_card import BaseCard
from ecogame.utils import mm_to_px
from ecogame.base_cards import BaseCards


class DisasterDie(BaseCard):
    SIZES = [25, 19, 16, 12]  # in mm.
    WIDTH, HEIGHT = mm_to_px(SIZES[0]), mm_to_px(SIZES[0])
    MARGIN_LEFT, MARGIN_RIGHT = mm_to_px(0), mm_to_px(0)
    MARGIN_TOP, MARGIN_BOTTOM = mm_to_px(0), mm_to_px(0)
    INNER_WIDTH = WIDTH - MARGIN_LEFT - MARGIN_RIGHT
    INNER_HEIGHT = HEIGHT - MARGIN_TOP - MARGIN_BOTTOM
    ROWS, COLS = 6, 6

    def _render(self, pips: int, size: int):
        yield svg.Image(0, 0, size, size, path=f"./images/dice-{pips}.png", embed=True)

    @property
    def width(self):
        return self._config["size"]

    @property
    def height(self):
        return self._config["size"]


class DisasterDice(BaseCards):
    CONFIG_FILE = "./config/disaster_dice.yaml"
    CARD_CLASS = DisasterDie

    def _add_cards(self, config):
        for size in self.CARD_CLASS.SIZES:
            for dice_config in config:
                self._cards.append(self.CARD_CLASS(size=mm_to_px(size), **dice_config))
