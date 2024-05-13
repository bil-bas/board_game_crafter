#!/usr/bin/env python3.12

import argparse
import os
import glob

from ecogame.cards import Cards
from ecogame.player_cards import PlayerCards
from ecogame.disaster_cards import DisasterCards
from ecogame.disaster_dice import DisasterDice
from ecogame.cloud_api import DriveAPI


def create_parser():
    parser = argparse.ArgumentParser(description="Layout generator for Ishara Press Regen-D game")

    parser.add_argument("--show-border", action='store_true')
    parser.add_argument("--show-count", action='store_true')
    parser.add_argument("--upload", action='store_true')

    return parser


def parse(parser):
    args = parser.parse_args()

    for folder in ("output/print-and-play", ):
        os.makedirs(folder, exist_ok=True)

    for filename in glob.glob(f"./output/*.png"):
        os.remove(filename)

    for cards in [Cards, PlayerCards, DisasterCards, DisasterDice]:
        cards.create_cards(args.show_border, args.show_count)

    if args.upload:
        google_api = DriveAPI()
        for name in glob.glob("./output/*.pdf"):
            google_api.upload(name)

        google_api.download_doc_as_pdf("./output/print-and-play/Ecogame for E2M - Rules.pdf")


if __name__ == "__main__":
    parse(create_parser())


