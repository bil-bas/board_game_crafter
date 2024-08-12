from board_game_crafter.base_components import BaseComponents
from .buy_card import BuyCard


class InternationalCard(BuyCard):
    BACK_IMAGE = "international"
    BACK_LABEL = "International"


class InternationalCards(BaseComponents):
    CARD_CLASS = InternationalCard
    CONFIG_FILE = "international_cards.yaml"

