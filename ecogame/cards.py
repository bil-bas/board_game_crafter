from .base_cards import BaseCards
from .card import Card


class Cards(BaseCards):
    CARD_CLASS = Card
    CONFIG_FILE = "./config/cards.yaml"
