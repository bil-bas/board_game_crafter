from PIL import Image, ImageDraw

from ecogame.utils import mm_to_px
from ecogame.base_cards import BaseCards, LandscapeCards


class Cards(LandscapeCards, BaseCards):
    CENTER_ICON_SIZE = 32, 32
    IMAGE_SIZE = 60, 60
    COST_ICON_SIZE = 22, 22
    VALUE_MARGIN = mm_to_px(8)
    TITLE_Y = mm_to_px(20)
    VALUES_Y = mm_to_px(30)
    CENTER_ICON_Y = VALUES_Y + 8
    FLAVOUR_Y = mm_to_px(45)
    TEXT_Y = mm_to_px(37)

    CONFIG_FILE = "./config/cards.yaml"

    def generate(self, config: hash, show_border: bool, show_count: bool) -> list:
        for card_config in config:
            count = card_config.get("count", 1)
            card = self._card(show_border=show_border, show_count=show_count, **card_config)
            for _ in range(count):
                yield card

    def _card(self, show_border: bool, show_count: bool, title: str, cost: str = "", image: str = "", text: str = "",
              left_value: str = "", center_icon: str = "", right_value: str = "", flavour: str = "",
              keywords: list = None, count: int = 1):

        card = Image.new("RGBA", (self.CARD_WIDTH, self.CARD_HEIGHT), self.BACKGROUND_COLOR)
        draw = ImageDraw.Draw(card)

        self._value(card, draw, (self.MARGIN_LEFT, self.MARGIN_TOP), cost,
                    size=self.FONT_HEIGHT_COST)

        if image:
            sized_image = self._image(image, self.IMAGE_SIZE)
            card.paste(sized_image, ((self.CARD_WIDTH - self.IMAGE_SIZE[0]) // 2, self.MARGIN_TOP), mask=sized_image)

        if keywords:
            for i, keyword in enumerate(keywords):
                self._font.text(draw, (self.CARD_WIDTH - self.MARGIN_RIGHT,
                                       self.MARGIN_TOP + (self.FONT_HEIGHT_KEYWORDS + 2) * i),
                                keyword, anchor="ra", color=self.INK_COLOR, size=self.FONT_HEIGHT_KEYWORDS)

        self._font.text(draw, (self.CARD_WIDTH // 2, self.TITLE_Y), title, color=self.INK_COLOR,
                        size=self.FONT_HEIGHT_TITLE, anchor="ma")

        if text:
            self._font.text(draw, (self.MARGIN_LEFT, self.TEXT_Y), text.strip(), color=self.INK_COLOR,
                            size=self.FONT_HEIGHT_TEXT, anchor="lm")

        if left_value:
            self._value(card, draw,
                        (self.MARGIN_LEFT + self.VALUE_MARGIN, self.VALUES_Y),
                        left_value,
                        size=self.FONT_HEIGHT_VALUE)

        if center_icon:
            sized_image = self._image(center_icon, self.CENTER_ICON_SIZE)
            card.paste(sized_image, box=((self.CARD_WIDTH - self.CENTER_ICON_SIZE[0]) // 2, self.CENTER_ICON_Y),
                       mask=sized_image)

        if right_value:
            x = self.CARD_WIDTH - self.MARGIN_RIGHT - self.VALUE_MARGIN
            self._value(card, draw, (x, self.VALUES_Y), right_value, size=self.FONT_HEIGHT_VALUE,
                        right_justify=True)

        if flavour:
            self._font.text(draw, (self.MARGIN_LEFT, self.CARD_HEIGHT - self.MARGIN_BOTTOM), flavour,
                            color=self.INK_COLOR, size=self.FONT_HEIGHT_FLAVOUR, wrap_width=44, anchor="ld")

        if show_count and count != 1:
            self._font.text(draw, (self.CARD_WIDTH - self.MARGIN_RIGHT, self.CARD_HEIGHT - self.MARGIN_BOTTOM),
                            str(count), color=self.INK_COLOR, size=self.FONT_HEIGHT_COUNT, anchor="rd")

        if show_border:
            draw.rectangle((0, 0, self.CARD_WIDTH - 1, self.CARD_HEIGHT - 1), outline=(210, 210, 210, 255))

        return card
