#!/usr/bin/env python3.12

import argparse
import os
import yaml
import glob
from itertools import batched

import img2pdf

from ecogame.cards import Cards
from ecogame.layout_page import layout_page, COLS, ROWS


def create_parser():
    parser = argparse.ArgumentParser(description="Layout generator for Ishara Press Regen-D game")

    return parser


def parse(parser):
    args = parser.parse_args()

    for folder in ("output", ):
        os.makedirs(folder, exist_ok=True)

    with open(f"./cards.yaml") as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)

    cards = Cards().generate(config)
    for i, cards_on_page in enumerate(batched(cards, COLS * ROWS), 1):
        layout_page(cards_on_page).save(f"./output/page_{i}.png")

    with open(f"./output/cards.pdf", "wb") as f:
        f.write(img2pdf.convert(glob.glob(f"./output/page_*.png")))


if __name__ == "__main__":
    parse(create_parser())


