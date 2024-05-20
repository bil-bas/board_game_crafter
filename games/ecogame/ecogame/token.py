import drawsvg as svg

from board_game_crafter.utils import mm_to_px
from board_game_crafter.base_component import BaseComponent
from board_game_crafter.base_components import BaseComponents


class Token(BaseComponent):
    WIDTH, HEIGHT = mm_to_px(15), mm_to_px(15)
    FONT_SIZE_TITLE = 10
    FONT_SIZE_MODIFIER = 15
    COLS, ROWS = 7, 10
    TEMPLATE_RADIUS = WIDTH / 2  # Circle!

    def _render_front(self, name: int, back_modifier: int = None):
        yield svg.Text(name, self.FONT_SIZE_TITLE, self.width * 0.5, self.height * 0.5, text_anchor="middle",
                       dominant_baseline="middle", font_family=self.FONT_SIZE_TITLE)

    def _render_back(self, name: int, back_modifier: int = None):
        yield svg.Text(name, self.FONT_SIZE_TITLE, self.width * 0.5, self.height * 0.5, text_anchor="middle",
                       dominant_baseline="middle", font_family=self.FONT_SIZE_TITLE)

        if back_modifier is not None:
            yield svg.Text(f"+{back_modifier}", self.FONT_SIZE_MODIFIER, self.width * 0.5, self.height * 0.8,
                           text_anchor="middle", font_family=self.FONT_SIZE_TITLE)




class Tokens(BaseComponents):
    CARD_CLASS = Token
    CONFIG_FILE = "tokens.yaml"
