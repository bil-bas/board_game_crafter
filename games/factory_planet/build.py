import os
import glob
import pathlib
import zipfile

from board_game_crafter.cloud_api import DriveAPI
from board_game_crafter.utils import output_path, merge_pdf_fronts_and_backs
from board_game_crafter.base_component import Face
from board_game_crafter.create_components import create_components
from .factory_planet.starting_card import StartingCards
from .factory_planet.local_card import LocalCards
from .factory_planet.far_card import FarCards
from .factory_planet.near_card import NearCards
from .factory_planet.disapproval_card import DisapprovalCards

GAME_NAME = "Factory Planet"
GDRIVE_FOLDER_ID = '1ky7NfJ80ipeGiUhbnb7_8CjM9jL_NVlQ'
GDRIVE_CARDS_FOLDER_ID = '1iSucmrGoQeKJj-vF_pLy4s2xIUXGcIWP'


ALL_CARD_TYPES = [StartingCards, LocalCards, NearCards, FarCards, DisapprovalCards]


def build(show_border: bool, show_margin: bool):
    make_cards(show_border, show_margin)


def make_cards(show_border: bool, show_margin: bool):
    create_components(ALL_CARD_TYPES, f"{GAME_NAME} - cards - fronts", show_border=show_border,
                      show_margin=show_margin)
    create_components(ALL_CARD_TYPES, f"{GAME_NAME} - cards - backs", show_border=show_border,
                      show_margin=show_margin, face=Face.BACK)
    create_components(ALL_CARD_TYPES, f"{GAME_NAME} - cards - templates", keep_as_svg=True,
                      face=Face.TEMPLATE)

    merge_pdf_fronts_and_backs(fronts=f'{GAME_NAME} - cards - fronts.pdf',
                               backs=f'{GAME_NAME} - cards - backs.pdf',
                               output=f'{GAME_NAME} - cards - double-sided.pdf')


def upload() -> None:
    google_api = DriveAPI()

    for name in sorted(glob.glob(output_path("*cards*.*"))):
        google_api.upload(name, GDRIVE_CARDS_FOLDER_ID)

    google_api.download_doc_as_pdf(output_path(f"download/{GAME_NAME} - Rules.pdf"), GDRIVE_FOLDER_ID)
    p_and_p_file = output_path(f"{GAME_NAME} - print-and-play.zip")
    _create_p_and_p(p_and_p_file)
    google_api.upload(p_and_p_file, GDRIVE_FOLDER_ID)


def _create_p_and_p(p_and_p_file: str) -> None:
    pathlib.Path(p_and_p_file).unlink(missing_ok=True)
    with zipfile.ZipFile(p_and_p_file, "x", compresslevel=zipfile.ZIP_LZMA) as z_file:
        for name in glob.glob(output_path("download/*")):
            z_file.write(name, os.path.basename(name))

        for name in glob.glob(output_path("*card*.*")):
            z_file.write(name, f"cards/{os.path.basename(name)}")
