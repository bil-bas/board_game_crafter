from .base_cards import BaseCards
from .buy_card import BuyCard


class EventCard(BuyCard):
    pass


class EventCards(BaseCards):
    CONFIG_FILE = "./config/event_cards.yaml"
    CARD_CLASS = EventCard
    ROWS, COLS = 4, 2
