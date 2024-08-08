from board_game_crafter.base_components import BaseComponents
from .buy_card import BuyCard


class FarCard(BuyCard):
    BACK_IMAGE = "far"
    BACK_LABEL = "International"
    BACK_BACKGROUND_COLOR = "#ff3333"


class FarCards(BaseComponents):
    CARD_CLASS = FarCard
    CONFIG_FILE = "far_cards.yaml"

