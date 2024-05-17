#!/usr/bin/env python3.12

import argparse
import os
import glob
import pathlib
import zipfile
from itertools import batched
import subprocess

from PyPDF2 import PdfMerger
import cairosvg

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

GAME_NAME = "Ecogame for E2M"
ALL_CARD_TYPES = [PlayerCards, DisasterCards, EventCards, StartingCards, BuyCards]


def create_parser():
    parser = argparse.ArgumentParser(description="Layout generator for Ishara Press Regen-D game")

    parser.add_argument("--show-border", action='store_true', help="Draw border around cards")
    parser.add_argument("--show-margin", action='store_true', help="Draw margin inside cards")
    parser.add_argument("--upload", action='store_true', help="Upload to Google Drive")

    return parser


def parse(parser) -> None:
    args = parser.parse_args()

    for folder in ("output/download", ):
        os.makedirs(folder, exist_ok=True)

    for filename in glob.glob(f"./output/*.*"):
        os.remove(filename)

    create_cards(ALL_CARD_TYPES, "cards - fronts", show_border=args.show_border, show_margin=args.show_margin)
    create_cards(ALL_CARD_TYPES, "cards - backs", show_border=args.show_border, show_margin=args.show_margin,
                 render_backs=True)
    create_cards([CardCutTemplates], "card cut templates", show_border=False, show_margin=False,
                 keep_as_svg=True)

    create_cards([DisasterDice], "disaster dice", show_border=args.show_border, show_margin=False,
                 keep_as_svg=True)
    create_cards([DieCutTemplates], "dice cut templates", show_border=False, show_margin=False,
                 keep_as_svg=True)

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


def create_cards(card_types: list, name, show_border: bool, show_margin: bool, keep_as_svg: bool = False,
                 render_backs: bool = False) -> None:
    num_cards_on_page = card_types[0].cols * card_types[0].rows

    cards = []
    for card_type in card_types:
        cards.extend(card_type.create_cards())

    for i, cards_on_page in enumerate(batched(cards, num_cards_on_page), 1):
        doc = layout_page(cards_on_page, show_border=show_border, show_margin=show_margin, render_backs=render_backs)
        if keep_as_svg:
            size_mm = getattr(cards_on_page[0], "size_mm", 0)
            output_file = f"./output/{GAME_NAME} - {name}{f' {size_mm}mm' if size_mm else ''}.svg"
            doc.save_svg(output_file)
            print(f"Written {len(cards)} cards to {output_file}")
        else:
            cairosvg.svg2pdf(doc.as_svg(), write_to=f"./output/{name}_{i:02}.pdf")

    if not keep_as_svg:
        merge_pdfs(cards, name)

        for filename in glob.glob(f"./output/{name}_*.pdf"):
            os.remove(filename)


def merge_pdfs(cards, name):
    output_file = f"./output/{GAME_NAME} - {name}.pdf"

    with PdfMerger() as merger:
        for pdf in sorted(glob.glob(f"./output/{name}_*.pdf")):
            merger.append(pdf)

        merger.write(output_file)

    print(f"Written {len(cards)} cards to {output_file}")


def create_p_and_p(p_and_p_file: str) -> None:
    pathlib.Path(p_and_p_file).unlink(missing_ok=True)
    with zipfile.ZipFile(p_and_p_file, "x", compresslevel=zipfile.ZIP_LZMA) as z_file:
        for name in glob.glob("./output/download/*"):
            z_file.write(name, os.path.basename(name))

        for name in glob.glob("./output/*dice*.svg"):
            z_file.write(name, f"dice/{os.path.basename(name)}")

        for name in glob.glob("./output/*card*.pdf"):
            z_file.write(name, f"cards/{os.path.basename(name)}")


if __name__ == "__main__":
    parse(create_parser())


