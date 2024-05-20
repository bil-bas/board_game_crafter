import os
import glob
import pathlib
import zipfile

from board_game_crafter.cloud_api import DriveAPI
from board_game_crafter.utils import output_path, merge_pdf_fronts_and_backs
from board_game_crafter.base_component import Face
from board_game_crafter.create_components import create_components
from games.ecogame.ecogame.buy_card import BuyCards
from games.ecogame.ecogame.player_card import PlayerCards
from games.ecogame.ecogame.event_card import EventCards
from games.ecogame.ecogame.starting_card import StartingCards
from games.ecogame.ecogame.disaster_card import DisasterCards
from games.ecogame.ecogame.disaster_die import DisasterDice
from games.ecogame.ecogame.token import Tokens
from games.ecogame.ecogame.prosperity_card import ProsperityCards

GAME_NAME = "Ecogame for E2M"
GDRIVE_FOLDER_ID = '1zP7Kwvm6AoIVuCKzXB7zGUuNZbkMDOl6'
GDRIVE_CARDS_FOLDER_ID = '1CMF69VXc3hC_LD_1_ZUsNGXKrlR1ceKS'
GDRIVE_TOKENS_FOLDER_ID = '1o1yQ5lOg1pjg3dvWttKIrMNRkM-b2vOl'
GDRIVE_DICE_FOLDER_ID = '1PueSwam9cZbsIjQpFRgUVulD803AzHZA'


ALL_CARD_TYPES = [PlayerCards, DisasterCards, ProsperityCards, EventCards, StartingCards, BuyCards]


def build(show_border: bool, show_margin: bool):
    make_tokens(show_border)
    make_cards(show_border, show_margin)
    make_dice(show_border)


def make_tokens(show_border: bool):
    create_components([Tokens], f"{GAME_NAME} - tokens - fronts", show_border=show_border)
    create_components([Tokens], f"{GAME_NAME} - tokens - backs", show_border=show_border,
                      face=Face.BACK)
    create_components([Tokens], f"{GAME_NAME} - tokens - templates", show_border=False,
                      face=Face.TEMPLATE)

    merge_pdf_fronts_and_backs(fronts=f'{GAME_NAME} - tokens - fronts.pdf',
                               backs=f'{GAME_NAME} - tokens - backs.pdf',
                               output=f'{GAME_NAME} - tokens - double-sided.pdf')


def make_dice(show_border: bool):
    for size_mm in DisasterDice.SIZES:
        create_components([DisasterDice], f"{GAME_NAME} - dice - {size_mm}mm",
                          show_border=show_border,show_margin=False, keep_as_svg=True,
                          extra_config=dict(size_mm=size_mm))
        create_components([DisasterDice], f"{GAME_NAME} - dice - templates - {size_mm}mm",
                          keep_as_svg=True, face=Face.TEMPLATE, extra_config=dict(size_mm=size_mm))


def make_cards(show_border: bool, show_margin: bool):
    create_components(ALL_CARD_TYPES, f"{GAME_NAME} - cards - fronts", show_border=show_border,
                      show_margin=show_margin)
    create_components(ALL_CARD_TYPES, f"{GAME_NAME} - cards - backs", show_border=show_border,
                      show_margin=show_margin, face=Face.BACK)
    create_components([BuyCards], f"{GAME_NAME} - cards - templates", keep_as_svg=True,
                      face=Face.TEMPLATE)

    merge_pdf_fronts_and_backs(fronts=f'{GAME_NAME} - cards - fronts.pdf',
                               backs=f'{GAME_NAME} - cards - backs.pdf',
                               output=f'{GAME_NAME} - cards - double-sided.pdf')


def upload() -> None:
    google_api = DriveAPI()

    for name in sorted(glob.glob(output_path("*cards*.*"))):
        google_api.upload(name, GDRIVE_CARDS_FOLDER_ID)

    for name in sorted(glob.glob(output_path("*dice*.*"))):
        google_api.upload(name, GDRIVE_DICE_FOLDER_ID)

    for name in sorted(glob.glob(output_path("*tokens*.*"))):
        google_api.upload(name, GDRIVE_TOKENS_FOLDER_ID)

    google_api.download_doc_as_pdf(output_path(f"download/{GAME_NAME} - Rules.pdf"), GDRIVE_FOLDER_ID)
    p_and_p_file = output_path(f"{GAME_NAME} - print-and-play.zip")
    _create_p_and_p(p_and_p_file)
    google_api.upload(p_and_p_file, GDRIVE_FOLDER_ID)


def _create_p_and_p(p_and_p_file: str) -> None:
    pathlib.Path(p_and_p_file).unlink(missing_ok=True)
    with zipfile.ZipFile(p_and_p_file, "x", compresslevel=zipfile.ZIP_LZMA) as z_file:
        for name in glob.glob(output_path("download/*")):
            z_file.write(name, os.path.basename(name))

        for name in glob.glob(output_path("*dice*.*")):
            z_file.write(name, f"dice/{os.path.basename(name)}")

        for name in glob.glob(output_path("*card*.*")):
            z_file.write(name, f"cards/{os.path.basename(name)}")

        for name in glob.glob(output_path("*token*.*")):
            z_file.write(name, f"tokens/{os.path.basename(name)}")
