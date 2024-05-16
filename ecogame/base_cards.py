import glob
import yaml
from itertools import batched

import img2pdf

from .layout_page import layout_page

GAME_NAME = "Ecogame for E2M"


class BaseCards:
    CONFIG_FILE = None
    CARD_CLASS = None

    def __init__(self, config):
        self._cards = []
        self._add_cards(config)

    def _add_cards(self, config):
        for conf in config:
            self._cards.append(self.CARD_CLASS(**conf))

    def __iter__(self):
        for card in self._cards:
            yield card

    @classmethod
    def create_cards(cls, show_border: bool, show_count: bool, show_margin: bool):
        with open(cls.CONFIG_FILE) as f:
            config = yaml.load(f, Loader=yaml.SafeLoader)

        cards = cls(config)

        c = []
        for card in cards:
            for _ in range(card.count):
                c.append(card)

        for i, cards_on_page in enumerate(batched(c, cls.CARD_CLASS.COLS * cls.CARD_CLASS.ROWS), 1):
            doc = layout_page(cards_on_page, show_border=show_border, show_margin=show_margin)
            doc.save_png(f"./output/{cls.__name__}_{i:02}.png")

        with open(f"./output/{GAME_NAME} - {cls.__name__}.pdf", "wb") as f:
            f.write(img2pdf.convert(sorted(glob.glob(f"./output/{cls.__name__}_*.png"))))

        print(f"Generated {len(c)} {cls.__name__}.")



