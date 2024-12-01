from board_game_crafter.utils import  A4_WIDTH, A4_HEIGHT
from board_game_crafter.base_component import Face
from board_game_crafter.create_components import create_components
from .sausages.token import Tokens

GAME_NAME = "Sausages"
GDRIVE_FOLDER_ID = ''
GDRIVE_CARDS_FOLDER_ID = ''


ALL_CARD_TYPES = [Tokens]


def build(show_border: bool, show_margin: bool):
    make_cards(show_border, show_margin)

def make_cards(show_border: bool, show_margin: bool):
    create_components(ALL_CARD_TYPES, f"{GAME_NAME} - tokens - fronts", show_border=show_border,
                      show_margin=show_margin, page_width=A4_WIDTH / 2, page_height=A4_HEIGHT / 2)
    create_components(ALL_CARD_TYPES, f"{GAME_NAME} - tokens - templates", keep_as_svg=True,
                      page_width=A4_WIDTH / 2, page_height=A4_HEIGHT / 2, face=Face.TEMPLATE)
