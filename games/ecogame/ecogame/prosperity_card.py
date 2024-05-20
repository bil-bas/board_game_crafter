import drawsvg as svg

from board_game_crafter.utils import mm_to_px
from board_game_crafter.base_card import LandscapeCardMixin
from board_game_crafter.base_components import BaseComponents
from .game_card import GameCard


class ProsperityCard(LandscapeCardMixin, GameCard):
    TABLE_ROW_HEIGHT = mm_to_px(13.5)
    TABLE_COL_WIDTH = mm_to_px(16.5)
    CIRCLE_RADIUS = mm_to_px(6)
    CIRCLE_COLOR = "gold"
    CONNECTOR_WIDTH = mm_to_px(4)
    FONT_HEIGHT_TABLE = 18
    BACK_LABEL = "Prosperity"
    BACK_BACKGROUND_COLOR = "gold"
    NUM_COLS, NUM_ROWS = 5, 4

    def _render_front(self):
        x, y = self.margin_left + self.CIRCLE_RADIUS, self.margin_top + self.CIRCLE_RADIUS
        table = svg.Group(transform=f"translate({x}, {y})")
        table.extend(self._table())
        yield table

    def _table(self):
        right = (self.NUM_COLS - 1) * self.TABLE_COL_WIDTH
        # 4-5
        yield svg.Line(right, self.TABLE_ROW_HEIGHT * 0, right, self.TABLE_ROW_HEIGHT * 1,
                       stroke_width=self.CONNECTOR_WIDTH, stroke=self.CIRCLE_COLOR)
        # 9-10
        yield svg.Line(0, self.TABLE_ROW_HEIGHT * 1, 0, self.TABLE_ROW_HEIGHT * 2,
                       stroke_width=self.CONNECTOR_WIDTH, stroke=self.CIRCLE_COLOR)
        # 14-15
        yield svg.Line(right, self.TABLE_ROW_HEIGHT * 2, right, self.TABLE_ROW_HEIGHT * 3,
                       stroke_width=self.CONNECTOR_WIDTH, stroke=self.CIRCLE_COLOR)

        for row in range(self.NUM_ROWS):
            y = self.TABLE_ROW_HEIGHT * (self.NUM_ROWS - row - 1)
            yield svg.Line(self.margin_left, y, (self.NUM_COLS - 1) * self.TABLE_COL_WIDTH, y,
                           stroke_width=self.CONNECTOR_WIDTH, stroke=self.CIRCLE_COLOR)
            for col in range(self.NUM_COLS):
                x = self.TABLE_COL_WIDTH * (col if row % 2 == 0 else (self.NUM_COLS - col - 1))

                yield svg.Circle(x, y, self.CIRCLE_RADIUS, fill=self.CIRCLE_COLOR)
                yield svg.Text(str(col + row * 5), self.FONT_HEIGHT_TABLE, x, y, font_weight="bold",
                               text_anchor="middle", dominant_baseline="middle")


class ProsperityCards(BaseComponents):
    CARD_CLASS = ProsperityCard
    CONFIG_FILE = "prosperity_cards.yaml"

    COLS, ROWS = 4, 2
