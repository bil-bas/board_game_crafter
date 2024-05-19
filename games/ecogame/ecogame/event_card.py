from board_game_crafter.base_components import BaseComponents
from .buy_card import BuyCard


class EventCard(BuyCard):
    BACK_LABEL = "Event"
    BACK_BACKGROUND_COLOR = "lightblue"


class EventCards(BaseComponents):
    CONFIG_FILE = "event_cards.yaml"
    CARD_CLASS = EventCard
