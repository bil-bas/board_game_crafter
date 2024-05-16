from .base_cards import BaseCards
from .buy_card import BuyCard


class StartingCard(BuyCard):
    pass


class StartingCards(BaseCards):
    CONFIG_FILE = "./config/starting_cards.yaml"
    CARD_CLASS = StartingCard
    ROWS, COLS = 4, 2
