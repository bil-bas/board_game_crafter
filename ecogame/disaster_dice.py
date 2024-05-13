from PIL import Image, ImageDraw

from ecogame.utils import mm_to_px
from ecogame.base_cards import BaseCards


class DisasterDice(BaseCards):
    WIDTH, HEIGHT = mm_to_px(30), mm_to_px(30)
    ROWS, COLS = 6, 6

    CONFIG_FILE = "./config/disaster_dice.yaml"

    def generate(self, config: hash, show_border: bool, show_count: bool) -> list:
        for size in [25, 19, 16, 12]:  # in mm.
            for dice_config in config:
                count = dice_config.get("count", 1)
                dice = self._card(show_border=show_border, size=mm_to_px(size), **dice_config)
                for _ in range(count):
                    yield dice

    def _card(self, show_border: bool, pips: int, size: int, count: int = 1):
        dice = Image.new("RGBA", (size, size), self.BACKGROUND_COLOR)
        draw = ImageDraw.Draw(dice)

        sized_image = self._image(f"dice-{pips}", (size, size))
        dice.paste(sized_image, (0, 0), mask=sized_image)

        if show_border:
            draw.rectangle((0, 0, size - 1, size - 1), outline=(210, 210, 210, 255))

        dice.cols, dice.rows = self.COLS, self.ROWS

        return dice
