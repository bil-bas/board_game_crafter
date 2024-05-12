import os
import glob
import yaml
from itertools import batched

from PIL import Image
import img2pdf

from ecogame.layout_page import layout_page
from ecogame.utils import Font

GAME_NAME = "Ecogame for E2M"


class BaseCards:
    FONT_HEIGHT_TITLE = 28
    FONT_HEIGHT_VALUE = 40
    FONT_HEIGHT_TEXT = 20
    FONT_HEIGHT_KEYWORDS = 12
    FONT_HEIGHT_FLAVOUR = 12
    FONT_HEIGHT_COST = 20
    FONT_HEIGHT_COUNT = 12

    BACKGROUND_COLOR = (255, 255, 255, 255)
    INK_COLOR = (0, 0, 0, 255)

    UNIT_SIZE = FONT_HEIGHT_VALUE, FONT_HEIGHT_VALUE

    CONFIG_FILE = None
    COLS, ROWS = None, None

    TEXT_ICON_SPACING = 2

    def __init__(self):
        self._font = Font("Arimo-Bold")
        self._images = {os.path.basename(im)[:-4]: Image.open(im) for im in glob.glob("./images/*.png")}

    def generate(self, config: hash, show_border: bool, show_count: bool) -> list:
        raise NotImplementedError

    def _value(self, card, draw, position: tuple, value: str, size: int, right_justify: bool = False):
        if value.endswith("P"):
            icon = "pollution"
            value = value[:-1]
        elif value.endswith("$"):
            icon = "prosperity"
            value = value[:-1]
        else:
            icon = None

        text_width = self._font.width(value, size)

        x, y = position
        if right_justify:
            text_x = x - text_width - size - self.TEXT_ICON_SPACING
            icon_x = x - size
        else:
            text_x = x
            icon_x = x + text_width + self.TEXT_ICON_SPACING

        self._font.text(draw, (text_x, y), value, color=self.INK_COLOR, size=size)

        if icon:
            sized_image = self._images[icon].resize((size, size), Image.Resampling.LANCZOS)
            card.paste(sized_image, (icon_x, y), mask=sized_image)

    @classmethod
    def create_cards(cls, show_border, show_count):
        with open(cls.CONFIG_FILE) as f:
            config = yaml.load(f, Loader=yaml.SafeLoader)

        instance = cls()

        cards = list(instance.generate(config, show_border=show_border, show_count=show_count))

        for i, cards_on_page in enumerate(batched(cards, cls.COLS * cls.ROWS), 1):
            layout_page(cards_on_page).save(f"./output/{cls.__name__}_{i:02}.png")

        with open(f"./output/{GAME_NAME} - {cls.__name__}.pdf", "wb") as f:
            f.write(img2pdf.convert(sorted(glob.glob(f"./output/{cls.__name__}_*.png"))))

        print(f"Generated {len(cards)} {cls.__name__}.")
