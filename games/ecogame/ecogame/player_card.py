import drawsvg as svg

from board_game_crafter.utils import mm_to_px
from board_game_crafter.base_card import PortraitCardMixin
from board_game_crafter.base_components import BaseComponents
from .game_card import GameCard


class PlayerCard(PortraitCardMixin, GameCard):
    NAME_Y = mm_to_px(45)
    VALUES_Y = mm_to_px(46)
    IMAGE_SIZE = mm_to_px(30), mm_to_px(30)
    VALUE_MARGIN = mm_to_px(0)
    FONT_HEIGHT_TITLE = 22
    BACK_LABEL = "Player"
    BACK_BACKGROUND_COLOR = "pink"

    def _render_front(self, name: str, image: str, initial: hash, income: hash, flavour: str):
        # Image.
        yield self._image((self.width - self.IMAGE_SIZE[0]) // 2, self.margin_top, self.IMAGE_SIZE[0],
                          image)

        # # Initial prosperity
        yield from self._value(f"{initial['prosperity']}$", self.FONT_HEIGHT_COST,
                               self.margin_left, self.margin_top)

        # Initial pollution
        yield from self._value(f"{initial['pollution']}P", self.FONT_HEIGHT_COST,
                               self.WIDTH - self.margin_right, self.margin_top, right_justify=True)

        # Name
        yield svg.Text(name, self.FONT_HEIGHT_TITLE, self.WIDTH // 2, self.NAME_Y, font_weight="bold",
                       text_anchor="middle")

        # Production: Productivity and Pollution
        yield from self._value(f"+{income['prosperity']}$",
                               self.FONT_HEIGHT_VALUE,
                               self.margin_left + self.VALUE_MARGIN, self.VALUES_Y)

        yield from self._value(f"+{income['pollution']}P", self.FONT_HEIGHT_VALUE,
                               self.width - self.margin_right - self.VALUE_MARGIN, self.VALUES_Y,
                               right_justify=True)

        if flavour:
            yield self._wrap(flavour, self.FONT_HEIGHT_FLAVOUR,
                             self.margin_left, self.height - self.margin_bottom, 30, valign="bottom")


class PlayerCards(BaseComponents):
    CONFIG_FILE = "player_cards.yaml"
    CARD_CLASS = PlayerCard
