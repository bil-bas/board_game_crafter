import drawsvg as svg

from ecogame.utils import mm_to_px
from ecogame.base_card import PortraitCard
from .base_cards import BaseCards


class PlayerCard(PortraitCard):
    NAME_Y = mm_to_px(45)
    VALUES_Y = mm_to_px(46)
    IMAGE_SIZE = mm_to_px(30), mm_to_px(30)
    VALUE_MARGIN = mm_to_px(0)
    FONT_HEIGHT_TITLE = 22
    BACK_LABEL = "Player"

    def _render_front(self, name: str, image: str, initial: hash, income: hash, flavour: str):
        # Image.
        yield self._image((self.WIDTH - self.IMAGE_SIZE[0]) // 2, self.MARGIN_TOP, self.IMAGE_SIZE[0],
                          image)

        # # Initial prosperity
        yield from self._value(f"{initial['prosperity']}$", self.FONT_HEIGHT_COST,
                               self.MARGIN_LEFT, self.MARGIN_TOP)

        # Initial pollution
        yield from self._value(f"{initial['pollution']}P", self.FONT_HEIGHT_COST,
                               self.WIDTH - self.MARGIN_RIGHT, self.MARGIN_TOP, right_justify=True)

        # Name
        yield svg.Text(name, self.FONT_HEIGHT_TITLE, self.WIDTH // 2, self.NAME_Y, font_weight="bold",
                       text_anchor="middle")

        # Production: Productivity and Pollution
        yield from self._value(f"+{income['prosperity']}$",
                               self.FONT_HEIGHT_VALUE,
                               self.MARGIN_LEFT + self.VALUE_MARGIN, self.VALUES_Y)

        yield from self._value(f"+{income['pollution']}P", self.FONT_HEIGHT_VALUE,
                               self.WIDTH - self.MARGIN_RIGHT - self.VALUE_MARGIN, self.VALUES_Y,
                               right_justify=True)

        if flavour:
            yield self._wrap(flavour, self.FONT_HEIGHT_FLAVOUR,
                             self.MARGIN_LEFT, self.HEIGHT - self.MARGIN_BOTTOM, 30, valign="bottom")


class PlayerCards(BaseCards):
    CONFIG_FILE = "./config/player_cards.yaml"
    CARD_CLASS = PlayerCard
