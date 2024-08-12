from board_game_crafter.base_components import BaseComponents
from .buy_card import BuyCard


class StartingCard(BuyCard):
    BACK_IMAGE = "starting"
    BACK_LABEL = "Starting"


class StartingCards(BaseComponents):
    CONFIG_FILE = "starting_cards.yaml"
    CARD_CLASS = StartingCard
