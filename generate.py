#!/usr/bin/env python3.12

import argparse
import os
import glob
import pathlib
import zipfile
from itertools import batched
import subprocess
from io import BytesIO

import img2pdf
from PIL import Image

from ecogame.layout_page import layout_page
from ecogame.buy_card import BuyCards
from ecogame.player_card import PlayerCards
from ecogame.event_card import EventCards
from ecogame.starting_card import StartingCards
from ecogame.disaster_card import DisasterCards
from ecogame.disaster_die import DisasterDice
from ecogame.cloud_api import DriveAPI
from ecogame.card_cut_template import CardCutTemplates
from ecogame.die_cut_template import DieCutTemplates
from ecogame.utils import DEFAULT_DPI

GAME_NAME = "Ecogame for E2M"
ALL_CARD_TYPES = [PlayerCards, DisasterCards, EventCards, StartingCards, BuyCards]


def create_parser():
    parser = argparse.ArgumentParser(description="Layout generator for Ishara Press Regen-D game")

    parser.add_argument("--show-border", action='store_true', help="Draw border around cards")
    parser.add_argument("--show-margin", action='store_true', help="Draw margin inside cards")
    parser.add_argument("--dpi", type=int, default=DEFAULT_DPI, choices=[DEFAULT_DPI, 150, 300],
                        help=f"DPI of rendered images in PDFs")
    parser.add_argument("--upload", action='store_true', help="Upload to Google Drive")

    return parser


def parse(parser) -> None:
    args = parser.parse_args()

    for folder in ("output/download", ):
        os.makedirs(folder, exist_ok=True)

    for filename in glob.glob(f"./output/*.*"):
        os.remove(filename)

    create_cards(ALL_CARD_TYPES, "cards - fronts", show_border=args.show_border, show_margin=args.show_margin,
                 dpi=args.dpi)
    create_cards(ALL_CARD_TYPES, "cards - backs", show_border=args.show_border, show_margin=args.show_margin,
                 render_backs=True,
                 dpi=args.dpi)
    create_cards([DisasterDice], "disaster dice", show_border=args.show_border, show_margin=False,
                 dpi=args.dpi)
    create_cards([CardCutTemplates], "card cut templates", show_border=False, show_margin=False,
                 save_as_svg=True)
    create_cards([DieCutTemplates], "die cut templates", show_border=False, show_margin=False,
                 save_as_svg=True)

    merge_fronts_and_backs()

    if args.upload:
        upload()


def merge_fronts_and_backs() -> None:
    subprocess.check_call([
        f"pdftk",
        f"A=./output/{GAME_NAME} - cards - fronts.pdf",
        f"B=./output/{GAME_NAME} - cards - backs.pdf",
        "shuffle",
        "A",
        "B",
        "output",
        f"./output/{GAME_NAME} - cards - double-sided.pdf"
    ])


def upload() -> None:
    google_api = DriveAPI()

    for name in glob.glob("output/*.pdf"):
        google_api.upload(name)

    for name in glob.glob("output/*.svg"):
        google_api.upload(name)

    google_api.download_doc_as_pdf(f"./output/download/{GAME_NAME} - Rules.pdf")
    p_and_p_file = f"./output/{GAME_NAME} - print-and-play.zip"
    create_p_and_p(p_and_p_file)
    google_api.upload(p_and_p_file)


def create_cards(card_types: list, name, show_border: bool, show_margin: bool, save_as_svg: bool = False,
                 render_backs: bool = False, dpi: int = DEFAULT_DPI) -> None:
    num_cards_on_page = card_types[0].cols * card_types[0].rows

    cards = []
    for card_type in card_types:
        cards.extend(card_type.create_cards())

    for i, cards_on_page in enumerate(batched(cards, num_cards_on_page), 1):
        doc = layout_page(cards_on_page, show_border=show_border, show_margin=show_margin, render_backs=render_backs,
                          dpi=dpi)
        if save_as_svg:
            size_mm = getattr(cards_on_page[0], "size_mm", 0)
            doc.save_svg(f"./output/{GAME_NAME} - {name}{f' {size_mm}mm' if size_mm else ''}.svg")
        else:
            data = BytesIO()
            doc.save_png(data)
            image = Image.open(data)
            image.save(f"./output/{name}_{i:02}.png", dpi=(dpi, dpi))

    if not save_as_svg:
        output_file = f"./output/{GAME_NAME} - {name}.pdf"
        with open(output_file, "wb") as f:
            f.write(img2pdf.convert(sorted(glob.glob(f"./output/{name}_*.png"))))
        print(f"Written {len(cards)} cards to {output_file}")


def create_p_and_p(p_and_p_file: str) -> None:
    pathlib.Path(p_and_p_file).unlink(missing_ok=True)
    with zipfile.ZipFile(p_and_p_file, "x", compresslevel=zipfile.ZIP_LZMA) as z_file:
        for name in glob.glob("./output/download/*"):
            z_file.write(name, os.path.basename(name))

        for name in glob.glob("./output/*.svg"):
            z_file.write(name, f"templates/{os.path.basename(name)}")

        for name in glob.glob("./output/*.pdf"):
            z_file.write(name, f"print/{os.path.basename(name)}")


if __name__ == "__main__":
    parse(create_parser())


