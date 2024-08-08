from board_game_crafter.base_components import BaseComponents
from .buy_card import BuyCard


class NearCard(BuyCard):
    BACK_IMAGE = "near"
    BACK_LABEL = "National"
    BACK_BACKGROUND_COLOR = "yellow"


class NearCards(BaseComponents):
    CARD_CLASS = NearCard
    CONFIG_FILE = "near_cards.yaml"

