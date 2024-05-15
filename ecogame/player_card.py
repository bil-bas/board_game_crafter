import drawsvg as svg
from itertools import batched

from ecogame.utils import mm_to_px
from ecogame.base_card import PortraitCard


class PlayerCard(PortraitCard):
    NAME_Y = mm_to_px(45)
    VALUES_Y = mm_to_px(46)
    IMAGE_SIZE = mm_to_px(30), mm_to_px(30)
    VALUE_MARGIN = mm_to_px(0)

    def _render(self, name: str, image: str, initial: hash, income: hash, flavour: str):
        # Image.
        yield self._image((self.CARD_WIDTH - self.IMAGE_SIZE[0]) // 2, self.MARGIN_TOP, self.IMAGE_SIZE[0],
                          image)

        # # Initial prosperity
        yield self._value(f"{initial['prosperity']}$", self.FONT_HEIGHT_COST,
                          self.MARGIN_LEFT, self.MARGIN_TOP)

        # Initial pollution
        yield self._value(f"{initial['pollution']}P", self.FONT_HEIGHT_COST,
                          self.CARD_WIDTH - self.MARGIN_RIGHT, self.MARGIN_TOP, right_justify=True)

        # Name
        yield svg.Text(name, self.FONT_HEIGHT_TITLE, self.CARD_WIDTH // 2, self.NAME_Y, text_anchor="middle")

        # Production: Productivity and Pollution
        yield self._value(f"+{income['prosperity']}$",
                          self.FONT_HEIGHT_VALUE,
                          self.MARGIN_LEFT + self.VALUE_MARGIN, self.VALUES_Y)

        yield self._value(f"+{income['pollution']}P",
                          self.FONT_HEIGHT_VALUE,
                          self.CARD_WIDTH - self.MARGIN_RIGHT - self.VALUE_MARGIN, self.VALUES_Y,
                          right_justify=True)

        if flavour:
            yield self._wrap(flavour, self.FONT_HEIGHT_FLAVOUR,
                             self.MARGIN_LEFT, self.CARD_HEIGHT - self.MARGIN_BOTTOM, 30, valign="bottom")

