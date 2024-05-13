from PIL import Image, ImageDraw

from ecogame.utils import mm_to_px
from ecogame.base_cards import BaseCards, PortraitCards


class DisasterDice(BaseCards):
    CARD_WIDTH, CARD_HEIGHT = 20, 20
    ROWS, COLS = 6, 6

    CONFIG_FILE = "./config/disaster_dice.yaml"

    def generate(self, config: hash, show_border: bool, show_count: bool) -> list:
        for dice_config in config:
            count = dice_config.get("count", 1)
            dice = self._card(show_border=show_border, **dice_config)
            for _ in range(count):
                yield dice

    def _card(self, show_border: bool, pips: int, count: int = 1):
        card = Image.new("RGBA", (self.CARD_WIDTH, self.CARD_HEIGHT), self.BACKGROUND_COLOR)
        draw = ImageDraw.Draw(card)

        sized_image = self._image(f"dice-{pips}", (self.CARD_WIDTH, self.CARD_HEIGHT))
        card.paste(sized_image, (0, 0), mask=sized_image)

        if show_border:
            draw.rectangle((0, 0, self.CARD_WIDTH - 1, self.CARD_HEIGHT - 1), outline=(210, 210, 210, 255))

        return card
