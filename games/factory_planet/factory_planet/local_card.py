from board_game_crafter.base_components import BaseComponents
from .buy_card import BuyCard


class LocalCard(BuyCard):
    BACK_IMAGE = "local"
    BACK_LABEL = "Local"


class LocalCards(BaseComponents):
    CARD_CLASS = LocalCard
    CONFIG_FILE = "local_cards.yaml"

