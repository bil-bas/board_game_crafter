import drawsvg as svg

from board_game_crafter.utils import mm_to_px
from board_game_crafter.base_card import LandscapeCardMixin
from board_game_crafter.base_components import BaseComponents
from .game_card import GameCard


class BuyCard(LandscapeCardMixin, GameCard):
    CENTER_ICON_SIZE = 32, 32
    IMAGE_SIZE = mm_to_px(14), mm_to_px(14)
    VALUE_MARGIN = mm_to_px(8)
    TITLE_Y = mm_to_px(28)
    VALUES_Y = mm_to_px(30)
    CENTER_ICON_Y = VALUES_Y + 8
    TEXT_Y = mm_to_px(39)
    BACK_LABEL = "Improvement"

    def _render_front(self, title: str, cost: str = "", image: str = "", text: str = "",
                      left_value: str = "", center_icon: str = "", right_value: str = "", flavour: str = "",
                      keywords: list = None):
        # Cost
        yield from self._value(cost, self.FONT_HEIGHT_COST, self.margin_left, self.margin_top)

        if image:
            yield self._image((self.width - self.IMAGE_SIZE[0]) // 2, self.margin_top, self.IMAGE_SIZE[0], image)

        if keywords:
            yield svg.Text("\n".join(keywords), self.FONT_HEIGHT_KEYWORDS, self.width - self.margin_right,
                           self.margin_top, font_family=self.FONT_FAMILY, text_anchor="end",
                           dominant_baseline="hanging")

        # Title
        yield svg.Text(title, self.FONT_HEIGHT_TITLE, self.WIDTH // 2, self.TITLE_Y, font_weight="bold",
                       text_anchor="middle", font_family=self.FONT_FAMILY)

        if text:
            yield self._wrap(text.strip(), self.FONT_HEIGHT_TEXT, self.margin_left, self.TEXT_Y, width=0,
                             valign="middle")

        if left_value:
            yield from self._value(left_value, self.FONT_HEIGHT_VALUE, self.margin_left + self.VALUE_MARGIN,
                                   self.VALUES_Y)

        if center_icon:
            yield self._image((self.WIDTH - self.CENTER_ICON_SIZE[0]) // 2, self.CENTER_ICON_Y,
                              self.CENTER_ICON_SIZE[0], center_icon)

        if right_value:
            x = self.WIDTH - self.margin_right - self.VALUE_MARGIN
            yield from self._value(right_value, self.FONT_HEIGHT_VALUE, x, self.VALUES_Y, right_justify=True)

        if flavour:
            yield self._wrap(flavour, self.FONT_HEIGHT_FLAVOUR,
                             self.margin_left, self.HEIGHT - self.margin_bottom, 45, valign="bottom")


class BuyCards(BaseComponents):
    CARD_CLASS = BuyCard
    CONFIG_FILE = "buy_cards.yaml"

    COLS, ROWS = 4, 2
