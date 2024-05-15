from ecogame.utils import mm_to_px
from ecogame.base_cards import BaseCards
from ecogame.disaster_die import DisasterDie


class DisasterDice(BaseCards):
    CONFIG_FILE = "./config/disaster_dice.yaml"
    CARD_CLASS = DisasterDie

    def _add_cards(self, config):
        for size in self.CARD_CLASS.SIZES:
            for dice_config in config:
                self._cards.append(self.CARD_CLASS(size=mm_to_px(size), **dice_config))
