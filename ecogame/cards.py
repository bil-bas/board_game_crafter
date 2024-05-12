import os
import glob

from PIL import Image, ImageDraw

from ecogame.utils import mm_to_px, Font
from ecogame.base_cards import BaseCards


class Cards(BaseCards):
    CARD_WIDTH, CARD_HEIGHT = mm_to_px(88.9), mm_to_px(63.5)
    MARGIN_LEFT, MARGIN_RIGHT = mm_to_px(7), mm_to_px(7)
    MARGIN_TOP, MARGIN_BOTTOM = mm_to_px(5), mm_to_px(5)

    CENTER_ICON_SIZE = 32, 32
    IMAGE_SIZE = 60, 60
    COST_ICON_SIZE = 22, 22

    INNER_WIDTH = CARD_WIDTH - MARGIN_LEFT - MARGIN_RIGHT
    INNER_HEIGHT = CARD_HEIGHT - MARGIN_TOP - MARGIN_BOTTOM
    VALUE_MARGIN = mm_to_px(8)
    TITLE_Y = mm_to_px(20)
    VALUES_Y = mm_to_px(30)
    CENTER_ICON_Y = VALUES_Y + 8
    FLAVOUR_Y = mm_to_px(45)

    COLS, ROWS = 2, 4
    CONFIG_FILE = "./cards.yaml"

    def generate(self, config: hash, show_border: bool, show_count: bool) -> list:
        for card_config in config:
            count = card_config.get("count", 1)
            card = self._card(show_border=show_border, show_count=show_count, **card_config)
            for _ in range(count):
                yield card

    def _card(self, show_border: bool, show_count: bool, title: str, cost: str, image: str = "", text: str = "",
              left_value: str = "", center_icon: str = "", right_value: str = "", flavour: str = "",
              keywords: list = None, count: int = 1):

        card = Image.new("RGBA", (self.CARD_WIDTH, self.CARD_HEIGHT), self.BACKGROUND_COLOR)
        draw = ImageDraw.Draw(card)

        if cost.endswith("$"):
            cost = cost[:-1]
            sized_image = self._images["prosperity"].resize(self.COST_ICON_SIZE, Image.Resampling.LANCZOS)
            card.paste(sized_image, (self.MARGIN_LEFT + (32 if "/" in cost else 15), self.MARGIN_TOP), mask=sized_image)
        else:
            assert cost == "Starting"

        self._font.text(draw, (self.MARGIN_LEFT, self.MARGIN_TOP), str(cost), color=self.INK_COLOR,
                        size=self.FONT_HEIGHT_COST)

        if image:
            sized_image = self._images[image].resize(self.IMAGE_SIZE, Image.Resampling.LANCZOS)
            card.paste(sized_image, ((self.CARD_WIDTH - self.IMAGE_SIZE[0]) // 2, self.MARGIN_TOP), mask=sized_image)

        if keywords:
            self._font.text(draw, (self.CARD_WIDTH - self.MARGIN_RIGHT, self.MARGIN_TOP), "\n".join(keywords),
                            anchor="ra", color=self.INK_COLOR, size=self.FONT_HEIGHT_KEYWORDS)

        self._font.text(draw, (self.CARD_WIDTH // 2, self.TITLE_Y), title, color=self.INK_COLOR,
                        size=self.FONT_HEIGHT_TITLE, anchor="ma")

        if text:
            self._font.text(draw, (self.MARGIN_LEFT, self.VALUES_Y), text, color=self.INK_COLOR,
                            size=self.FONT_HEIGHT_TEXT)

        if left_value:
            left_value = self.unit_icon(card, left_value, (self.MARGIN_LEFT + self.VALUE_MARGIN + 25,
                                                           self.VALUES_Y))
            self._font.text(draw, (self.MARGIN_LEFT + self.VALUE_MARGIN, self.VALUES_Y), left_value,
                            color=self.INK_COLOR,
                            size=self.FONT_HEIGHT_VALUE)

        if center_icon:
            sized_image = self._images[center_icon].resize(self.CENTER_ICON_SIZE, Image.Resampling.LANCZOS)
            card.paste(sized_image, box=((self.CARD_WIDTH - self.CENTER_ICON_SIZE[0]) // 2, self.CENTER_ICON_Y),
                       mask=sized_image)

        if right_value:
            x = self.CARD_WIDTH - self.MARGIN_RIGHT - self.VALUE_MARGIN - self.UNIT_SIZE[0]
            right_value = self.unit_icon(card, right_value, (x, self.VALUES_Y))

            self._font.text(draw, (self.CARD_WIDTH - self.MARGIN_RIGHT - self.VALUE_MARGIN, self.VALUES_Y),
                            right_value, color=self.INK_COLOR, size=self.FONT_HEIGHT_VALUE, anchor="ra")

        if flavour:
            self._font.text(draw, (self.MARGIN_LEFT, self.CARD_HEIGHT - self.MARGIN_BOTTOM), flavour,
                            color=self.INK_COLOR, size=self.FONT_HEIGHT_FLAVOUR, wrap_width=44, anchor="ld")

        if show_count and count != 1:
            self._font.text(draw, (self.CARD_WIDTH - self.MARGIN_RIGHT, self.CARD_HEIGHT - self.MARGIN_BOTTOM),
                            str(count), color=self.INK_COLOR, size=self.FONT_HEIGHT_COUNT, anchor="rd")

        if show_border:
            draw.rectangle((0, 0, self.CARD_WIDTH - 1, self.CARD_HEIGHT - 1), outline=(210, 210, 210, 255))

        return card
