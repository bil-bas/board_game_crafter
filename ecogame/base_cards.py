import yaml


class BaseCardsMeta(type):
    CARD_CLASS = None

    @property
    def rows(cls) -> int:
        return cls.CARD_CLASS.ROWS

    @property
    def cols(cls) -> int:
        return cls.CARD_CLASS.COLS


class BaseCards(metaclass=BaseCardsMeta):
    CONFIG_FILE = None
    CARD_CLASS = None

    def __init__(self, config: dict):
        self._cards = []
        self._add_cards(config)

    def _add_cards(self, config: dict) -> None:
        for conf in config:
            self._cards.append(self.CARD_CLASS(**conf))

    def __iter__(self):
        for card in self._cards:
            yield card

    @property
    def total(self) -> int:
        return sum(c.count for c in self)

    @classmethod
    def create_cards(cls) -> None:
        with open(cls.CONFIG_FILE) as f:
            config = yaml.load(f, Loader=yaml.SafeLoader)

        cards = cls(config)

        for card in cards:
            for _ in range(card.count):
                yield card

        print(f"Generated {cards.total} {cls.__name__}.")
