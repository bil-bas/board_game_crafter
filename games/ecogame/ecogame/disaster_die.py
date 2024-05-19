import drawsvg as svg

from board_game_crafter.utils import mm_to_px, image_path
from board_game_crafter.base_component import BaseComponent
from board_game_crafter.base_components import BaseComponents


class DisasterDie(BaseComponent):
    WIDTH, HEIGHT = mm_to_px(50), mm_to_px(50)
    MARGIN_LEFT, MARGIN_RIGHT = mm_to_px(0), mm_to_px(0)
    MARGIN_TOP, MARGIN_BOTTOM = mm_to_px(0), mm_to_px(0)
    INNER_WIDTH = WIDTH - MARGIN_LEFT - MARGIN_RIGHT
    INNER_HEIGHT = HEIGHT - MARGIN_TOP - MARGIN_BOTTOM
    COLS, ROWS = 6, 1
    TEMPLATE_RADIUS = mm_to_px(6)

    def _render_front(self, size_mm: float, pips: int) -> None:
        yield svg.Image(0, 0, self.width, self.height, path=image_path(f"dice-{pips}.png"), embed=True)

    @property
    def width(self) -> float:
        return mm_to_px(self._config["size_mm"])

    @property
    def height(self) -> float:
        return mm_to_px(self._config["size_mm"])

    @property
    def size_mm(self):
        return self._config["size_mm"]


class DisasterDice(BaseComponents):
    CONFIG_FILE = "disaster_dice.yaml"
    CARD_CLASS = DisasterDie
    SIZES = [25, 19, 16, 12]  # in mm.
