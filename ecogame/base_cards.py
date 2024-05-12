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

    def __init__(self):
        self._font = Font("Arimo-Bold")
        self._images = {os.path.basename(im)[:-4]: Image.open(im) for im in glob.glob("./images/*.png")}

    def generate(self, config: hash, show_border: bool, show_count: bool) -> list:
        raise NotImplementedError

    def unit_icon(self, card, value: str, position: tuple):
        if value.endswith("P"):
            icon = "pollution"
        elif value.endswith("$"):
            icon = "prosperity"
        else:
            icon = None

        if icon:
            value = value[:-1] + "    "
            sized_image = self._images[icon].resize(self.UNIT_SIZE, Image.Resampling.LANCZOS)
            card.paste(sized_image, position, mask=sized_image)

        return value

    @classmethod
    def create_cards(cls, show_border, show_count):
        with open(cls.CONFIG_FILE) as f:
            config = yaml.load(f, Loader=yaml.SafeLoader)

        instance = cls()

        cards = list(instance.generate(config, show_border=show_border, show_count=show_count))

        for i, cards_on_page in enumerate(batched(cards, cls.COLS * cls.ROWS), 1):
            layout_page(cards_on_page).save(f"./output/{cls.__name__}_{i}.png")

        with open(f"./output/{GAME_NAME} - {cls.__name__}.pdf", "wb") as f:
            f.write(img2pdf.convert(sorted(glob.glob(f"./output/{cls.__name__}_*.png"))))

        print(f"Generated {len(cards)} cards.")