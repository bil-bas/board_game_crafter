
from PIL import Image, ImageDraw

from ecogame.utils import mm_to_px
from ecogame.base_cards import BaseCards


class PlayerCards(BaseCards):
    CARD_WIDTH, CARD_HEIGHT = mm_to_px(63.5 ), mm_to_px(88.9)
    MARGIN_LEFT, MARGIN_RIGHT = mm_to_px(7), mm_to_px(7)
    MARGIN_TOP, MARGIN_BOTTOM = mm_to_px(5), mm_to_px(5)
    INNER_WIDTH = CARD_WIDTH - MARGIN_LEFT - MARGIN_RIGHT
    INNER_HEIGHT = CARD_HEIGHT - MARGIN_TOP - MARGIN_BOTTOM
    NAME_Y = mm_to_px(40)
    VALUES_Y = mm_to_px(50)
    IMAGE_SIZE = mm_to_px(30), mm_to_px(30)
    VALUE_MARGIN = mm_to_px(0)

    COLS, ROWS = 2, 3
    CONFIG_FILE = "./player_cards.yaml"

    def generate(self, config: hash, show_border: bool, show_count: bool) -> list:
        for card_config in config:
            yield self._card(show_border=show_border, **card_config)

    def _card(self, show_border: bool, name: str, image: str, initial: hash, income: hash, flavour: str):
        card = Image.new("RGBA", (self.CARD_WIDTH, self.CARD_HEIGHT), self.BACKGROUND_COLOR)
        draw = ImageDraw.Draw(card)

        # Image
        sized_image = self._images[image].resize(self.IMAGE_SIZE, Image.Resampling.LANCZOS)
        card.paste(sized_image, ((self.CARD_WIDTH - self.IMAGE_SIZE[0]) // 2, self.MARGIN_TOP), mask=sized_image)

        # Initial prosperity
        self._value(card, draw, (self.MARGIN_LEFT, self.MARGIN_TOP),
                              f"{initial['prosperity']}$",
                    size=self.FONT_HEIGHT_COST)

        # Initial pollution
        self._value(card, draw,
                    (self.CARD_WIDTH - self.MARGIN_RIGHT, self.MARGIN_TOP),
                              f"{initial['pollution']}P",
                    size=self.FONT_HEIGHT_COST, right_justify=True)

        # Name
        self._font.text(draw, (self.CARD_WIDTH // 2, self.NAME_Y), name, color=self.INK_COLOR,
                        size=self.FONT_HEIGHT_TITLE, anchor="ma")

        # Production: Productivity and Pollution
        self._value(card, draw,
                    (self.MARGIN_LEFT + self.VALUE_MARGIN, self.VALUES_Y),
                              f"+{income['prosperity']}$",
                    size=self.FONT_HEIGHT_VALUE)

        self._value(card, draw,
                    (self.CARD_WIDTH - self.MARGIN_RIGHT - self.VALUE_MARGIN, self.VALUES_Y),
                              f"+{income['pollution']}P",
                    size=self.FONT_HEIGHT_VALUE,
                    right_justify=True)

        if flavour:
            self._font.text(draw, (self.MARGIN_LEFT, self.CARD_HEIGHT - self.MARGIN_BOTTOM), flavour,
                            color=self.INK_COLOR, size=self.FONT_HEIGHT_FLAVOUR, wrap_width=32, anchor="ld")

        if show_border:
            draw.rectangle((0, 0, self.CARD_WIDTH - 1, self.CARD_HEIGHT - 1), outline=(210, 210, 210, 255))

        return card
