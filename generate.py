#!/usr/bin/env python3.12

import argparse
import os
import glob

from ecogame.cards import Cards
from ecogame.player_cards import PlayerCards
from ecogame.disaster_cards import DisasterCards


def create_parser():
    parser = argparse.ArgumentParser(description="Layout generator for Ishara Press Regen-D game")

    parser.add_argument("--show-border", action='store_true')
    parser.add_argument("--show-count", action='store_true')

    return parser


def parse(parser):
    args = parser.parse_args()

    for folder in ("output", ):
        os.makedirs(folder, exist_ok=True)

    for filename in glob.glob(f"./output/*.png"):
        os.remove(filename)

    for cards in [Cards, PlayerCards, DisasterCards]:
        cards.create_cards(args.show_border, args.show_count)


if __name__ == "__main__":
    parse(create_parser())


