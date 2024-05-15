from ecogame.base_cards import BaseCards
from .disaster_card import DisasterCard


class DisasterCards(BaseCards):
    CARD_CLASS = DisasterCard
    CONFIG_FILE = "./config/disaster_cards.yaml"
