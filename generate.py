#!/usr/bin/env python3.12

import argparse
import os
import yaml
import glob
from itertools import batched

import img2pdf
from ecogame.layout_page import layout_page
from ecogame.cards import Cards
from ecogame.player_cards import PlayerCards





def create_parser():
    parser = argparse.ArgumentParser(description="Layout generator for Ishara Press Regen-D game")

    parser.add_argument("--show-border", action='store_true')
    parser.add_argument("--show-count", action='store_true')
    return parser


def parse(parser):
    args = parser.parse_args()

    for folder in ("output", ):
        os.makedirs(folder, exist_ok=True)

    create_cards(show_border=args.show_border, show_count=args.show_count)


def create_cards(show_border, show_count):
    for filename in glob.glob(f"./output/*.png"):
        os.remove(filename)

    Cards.create_cards(show_border, show_count)
    PlayerCards.create_cards(show_border, show_count)


if __name__ == "__main__":
    parse(create_parser())


