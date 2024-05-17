import drawsvg as svg

from .disaster_die import DisasterDie, DisasterDice
from .utils import mm_to_px


class DieCutTemplate(DisasterDie):
    BORDER_COLOR = "black"
    BORDER_WIDTH = 1
    RADIUS = mm_to_px(2)

    def _render_front(self, size_mm: int, pips: int = None):
        yield svg.Rectangle(0, 0, self.width, self.height,
                            rx=self.RADIUS, ry=self.RADIUS,
                            stroke=self.BORDER_COLOR, fill="none", stroke_width=self.BORDER_WIDTH)

    @property
    def size_mm(self):
        return self._config["size_mm"]


class DieCutTemplates(DisasterDice):
    CONFIG_FILE = "./config/die_cut_templates.yaml"
    CARD_CLASS = DieCutTemplate
    COLS, ROWS = 6, 1
