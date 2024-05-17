import drawsvg as svg

from ecogame.utils import mm_to_px
from ecogame.base_card import BaseCard
from ecogame.base_cards import BaseCards


class DisasterDie(BaseCard):
    SIZES = [25, 19, 16, 12]  # in mm.
    WIDTH, HEIGHT = mm_to_px(SIZES[0]), mm_to_px(SIZES[0])
    MARGIN_LEFT, MARGIN_RIGHT = mm_to_px(0), mm_to_px(0)
    MARGIN_TOP, MARGIN_BOTTOM = mm_to_px(0), mm_to_px(0)
    INNER_WIDTH = WIDTH - MARGIN_LEFT - MARGIN_RIGHT
    INNER_HEIGHT = HEIGHT - MARGIN_TOP - MARGIN_BOTTOM
    COLS, ROWS = 6, 1

    def _render_front(self, size_mm: float, pips: int) -> None:
        yield svg.Image(0, 0, self.width, self.height, path=f"./images/dice-{pips}.png", embed=True)

    @property
    def width(self) -> float:
        return mm_to_px(self._config["size_mm"])

    @property
    def height(self) -> float:
        return mm_to_px(self._config["size_mm"])


class DisasterDice(BaseCards):
    CONFIG_FILE = "./config/disaster_dice.yaml"
    CARD_CLASS = DisasterDie

    def _add_cards(self, config: hash):
        for size_mm in self.CARD_CLASS.SIZES:
            for dice_config in config:
                self._cards.append(self.CARD_CLASS(size_mm=size_mm, **dice_config))
