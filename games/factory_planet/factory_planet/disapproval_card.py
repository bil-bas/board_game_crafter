import drawsvg as svg

from board_game_crafter.utils import mm_to_px
from board_game_crafter.base_components import BaseComponents
from .game_card import GameCard


class DisapprovalCard(GameCard):
    TITLE_Y = mm_to_px(10)
    TEXT_Y = mm_to_px(20)
    BACK_IMAGE = "disapproval"
    BACK_LABEL = "Disapproval"
    BACK_BACKGROUND_COLOR = "grey"

    def _render_front(self, title: str, text: str):
        # Title
        yield svg.Text(title, self.FONT_HEIGHT_TITLE, self.WIDTH // 2, self.TITLE_Y, font_weight="bold",
                       text_anchor="middle", font_family=self.FONT_FAMILY_TITLE)

        yield self._wrap(text, self.FONT_HEIGHT_TEXT, self.margin_left, self.TEXT_Y, width=self.WRAP_WIDTH)


class DisapprovalCards(BaseComponents):
    CONFIG_FILE = "disapproval_cards.yaml"
    CARD_CLASS = DisapprovalCard
