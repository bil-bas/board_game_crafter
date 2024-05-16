#!/usr/bin/env python3.12

import argparse
import os
import glob
import pathlib
import zipfile

from ecogame.cards import Cards
from ecogame.player_cards import PlayerCards
from ecogame.disaster_cards import DisasterCards
from ecogame.disaster_dice import DisasterDice
from ecogame.cloud_api import DriveAPI
from ecogame.base_cards import GAME_NAME


def create_parser():
    parser = argparse.ArgumentParser(description="Layout generator for Ishara Press Regen-D game")

    parser.add_argument("--show-border", action='store_true')
    parser.add_argument("--show-count", action='store_true')
    parser.add_argument("--show-margin", action='store_true')
    parser.add_argument("--upload", action='store_true')

    return parser


def parse(parser):
    args = parser.parse_args()

    for folder in ("output/download", ):
        os.makedirs(folder, exist_ok=True)

    for filename in glob.glob(f"./output/*.png"):
        os.remove(filename)

    for cards in [DisasterDice, DisasterCards, PlayerCards, Cards]:
        cards.create_cards(args.show_border, args.show_count, args.show_margin)

    if args.upload:
        google_api = DriveAPI()
        for name in glob.glob("./output/*.pdf"):
            google_api.upload(name)

        google_api.download_doc_as_pdf(f"./output/download/{GAME_NAME} - Rules.pdf")

        p_and_p_file = f"./output/{GAME_NAME} - print-and-play.zip"
        create_p_and_p(p_and_p_file)
        google_api.upload(p_and_p_file)


def create_p_and_p(p_and_p_file):
    pathlib.Path(p_and_p_file).unlink(missing_ok=True)
    with zipfile.ZipFile(p_and_p_file, "x", compresslevel=zipfile.ZIP_LZMA) as z_file:
        for name in glob.glob("./output/download/*"):
            z_file.write(name, os.path.basename(name))

        for name in glob.glob("./output/*.pdf"):
            z_file.write(name, os.path.basename(name))


if __name__ == "__main__":
    parse(create_parser())


