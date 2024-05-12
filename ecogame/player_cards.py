
from PIL import Image, ImageDraw

from ecogame.utils import mm_to_px
from ecogame.base_cards import BaseCards


class PlayerCards(BaseCards):
    CARD_WIDTH, CARD_HEIGHT = mm_to_px(70), mm_to_px(120)
    MARGIN_LEFT, MARGIN_RIGHT = mm_to_px(14), mm_to_px(14)
    MARGIN_TOP, MARGIN_BOTTOM = mm_to_px(10), mm_to_px(10)
    INNER_WIDTH = CARD_WIDTH - MARGIN_LEFT - MARGIN_RIGHT
    INNER_HEIGHT = CARD_HEIGHT - MARGIN_TOP - MARGIN_BOTTOM
    TITLE_Y = mm_to_px(60)
    VALUES_Y = mm_to_px(100)
    IMAGE_SIZE = INNER_WIDTH, INNER_WIDTH
    COST_ICON_SIZE = 22, 22

    COLS, ROWS = 2, 2
    CONFIG_FILE = "./player_cards.yaml"

    def generate(self, config: hash, show_border: bool, show_count: bool) -> list:
        for card_config in config:
            yield self._card(show_border=show_border, **card_config)

    def _card(self, show_border: bool, name: str, image: str,
              initial: hash, income: hash, flavour: str, products: str, pollutions: str):

        card = Image.new("RGBA", (self.CARD_WIDTH, self.CARD_HEIGHT), self.BACKGROUND_COLOR)
        draw = ImageDraw.Draw(card)

        # Image
        sized_image = self._images[image].resize(self.IMAGE_SIZE, Image.Resampling.LANCZOS)
        card.paste(sized_image, ((self.CARD_WIDTH - self.IMAGE_SIZE[0]) // 2, self.MARGIN_TOP), mask=sized_image)

        # Initial prosperity and pollution
        prosperity_icon = self._images["prosperity"].resize(self.COST_ICON_SIZE, Image.Resampling.LANCZOS)
        card.paste(prosperity_icon, (self.MARGIN_LEFT + 15, self.MARGIN_TOP), mask=prosperity_icon)
        pollution_icon = self._images["pollution"].resize(self.COST_ICON_SIZE, Image.Resampling.LANCZOS)
        card.paste(pollution_icon, (self.MARGIN_LEFT + 15, self.MARGIN_TOP), mask=pollution_icon)

        self._font.text(draw, (self.MARGIN_LEFT, self.MARGIN_TOP), str(initial["prosperity"]), color=self.INK_COLOR,
                        size=self.FONT_HEIGHT_COST)
        self._font.text(draw, (self.MARGIN_LEFT, self.MARGIN_TOP), str(initial["pollution"]), color=self.INK_COLOR,
                        size=self.FONT_HEIGHT_COST)

        # Name
        self._font.text(draw, (self.CARD_WIDTH // 2, self.TITLE_Y), name, color=self.INK_COLOR, size=self.FONT_HEIGHT_TITLE,
                        anchor="ma")

        # Production and Pollution
        self._font.text(draw, (self.MARGIN_LEFT, self.VALUES_Y), str(income["prosperity"]), color=self.INK_COLOR,
                        size=self.FONT_HEIGHT_TEXT)
        self._font.text(draw, (self.MARGIN_LEFT, self.VALUES_Y), str(income["pollution"]), color=self.INK_COLOR,
                        size=self.FONT_HEIGHT_TEXT)

        if flavour:
            self._font.text(draw, (self.MARGIN_LEFT, self.CARD_HEIGHT - self.MARGIN_BOTTOM), flavour, color=INK_COLOR,
                            size=self.FONT_HEIGHT_FLAVOUR, wrap_width=44, anchor="ld")

        if show_border:
            draw.rectangle((0, 0, self.CARD_WIDTH - 1, self.CARD_HEIGHT - 1), outline=(210, 210, 210, 255))

        return card
