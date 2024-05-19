#!/usr/bin/env python3.12

import argparse
import os
import glob

import time
import importlib

from board_game_crafter.utils import output_path, set_game_name


def create_parser():
    parser = argparse.ArgumentParser(description="Component layout generator for board, card and dice games")

    parser.add_argument("game", help="Mame of the game", choices=["ecogame"])
    parser.add_argument("--show-border", action='store_true', help="Draw border around components")
    parser.add_argument("--show-margin", action='store_true', help="Draw margin inside components")
    parser.add_argument("--upload", action='store_true', help="Upload to Google Drive")

    return parser


def parse(parser) -> None:
    args = parser.parse_args()

    set_game_name(args.game)
    build = importlib.import_module(f"games.{args.game}.build")

    os.makedirs(output_path("download"), exist_ok=True)

    for filename in glob.glob(output_path("*.*")):
        os.remove(filename)

    start = time.perf_counter()
    build.build(show_border=args.show_border, show_margin=args.show_margin)

    if args.upload:
        build.upload()

    print(f"Completed in {time.perf_counter() - start:.1f}s")


if __name__ == "__main__":
    parse(create_parser())


