from board_game_crafter.base_components import BaseComponents
from .buy_card import BuyCard


class RegionalCard(BuyCard):
    BACK_IMAGE = "regional"
    BACK_LABEL = "Regional"


class RegionalCards(BaseComponents):
    CARD_CLASS = RegionalCard
    CONFIG_FILE = "regional_cards.yaml"

