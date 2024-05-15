import drawsvg as svg

from .utils import mm_to_px
from .base_card import LandscapeCard


class Card(LandscapeCard):
    CENTER_ICON_SIZE = 32, 32
    IMAGE_SIZE = mm_to_px(14), mm_to_px(14)
    VALUE_MARGIN = mm_to_px(8)
    TITLE_Y = mm_to_px(28)
    VALUES_Y = mm_to_px(30)
    CENTER_ICON_Y = VALUES_Y + 8
    TEXT_Y = mm_to_px(39)

    # show_count
    def _render(self, title: str, cost: str = "", image: str = "", text: str = "",
                left_value: str = "", center_icon: str = "", right_value: str = "", flavour: str = "",
                keywords: list = None, count: int = 1):
        # Cost
        yield from self._value(cost, self.FONT_HEIGHT_COST, self.MARGIN_LEFT, self.MARGIN_TOP)

        if image:
            yield self._image((self.CARD_WIDTH - self.IMAGE_SIZE[0]) // 2, self.MARGIN_TOP, self.IMAGE_SIZE[0], image)

        if keywords:
            yield svg.Text("\n".join(keywords), self.FONT_HEIGHT_KEYWORDS, self.CARD_WIDTH - self.MARGIN_RIGHT,
                           self.MARGIN_TOP, text_anchor="end", dominant_baseline="hanging")

        # Title
        yield svg.Text(title, self.FONT_HEIGHT_TITLE, self.CARD_WIDTH // 2, self.TITLE_Y, font_weight="bold",
                       text_anchor="middle")

        if text:
            yield self._wrap(text.strip(), self.FONT_HEIGHT_TEXT, self.MARGIN_LEFT, self.TEXT_Y, width=0,
                             valign="middle")

        if left_value:
            yield from self._value(left_value, self.FONT_HEIGHT_VALUE, self.MARGIN_LEFT + self.VALUE_MARGIN, self.VALUES_Y)

        if center_icon:
            yield self._image((self.CARD_WIDTH - self.CENTER_ICON_SIZE[0]) // 2, self.CENTER_ICON_Y,
                              self.CENTER_ICON_SIZE[0], center_icon)

        if right_value:
            x = self.CARD_WIDTH - self.MARGIN_RIGHT - self.VALUE_MARGIN
            yield from self._value(right_value, self.FONT_HEIGHT_VALUE, x, self.VALUES_Y, right_justify=True)

        if flavour:
            yield self._wrap(flavour, self.FONT_HEIGHT_FLAVOUR,
                             self.MARGIN_LEFT, self.CARD_HEIGHT - self.MARGIN_BOTTOM, 45, valign="bottom")

        # if show_count and count != 1:
        #     self._font.text(draw, (self.CARD_WIDTH - self.MARGIN_RIGHT, self.CARD_HEIGHT - self.MARGIN_BOTTOM),
        #                     str(count), color=self.INK_COLOR, size=self.FONT_HEIGHT_COUNT, anchor="rd")
