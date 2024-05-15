from .base_cards import BaseCards
from .player_card import PlayerCard


class PlayerCards(BaseCards):
    CONFIG_FILE = "./config/player_cards.yaml"
    CARD_CLASS = PlayerCard

