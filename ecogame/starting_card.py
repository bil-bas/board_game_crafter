from .base_cards import BaseCards
from .buy_card import BuyCard


class StartingCard(BuyCard):
    BACK_LABEL = "Starting"
    BACK_BACKGROUND_COLOR = "yellow"


class StartingCards(BaseCards):
    CONFIG_FILE = "./config/starting_cards.yaml"
    CARD_CLASS = StartingCard
