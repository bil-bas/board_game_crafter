import yaml

from .utils import config_path


class BaseComponentsMeta(type):
    CARD_CLASS = None

    @property
    def rows(cls) -> int:
        return cls.CARD_CLASS.ROWS

    @property
    def cols(cls) -> int:
        return cls.CARD_CLASS.COLS


class BaseComponents(metaclass=BaseComponentsMeta):
    CONFIG_FILE = None
    CARD_CLASS = None

    def __init__(self, config: dict, extra_config: dict):
        self._components = []
        self._add_components(config, extra_config)

    def _add_components(self, config: dict, extra_config: dict) -> None:
        for conf in config:
            if extra_config is not None:
                conf.update(extra_config)
            self._components.append(self.CARD_CLASS(**conf))

    def __iter__(self):
        for component in self._components:
            yield component

    @property
    def total(self) -> int:
        return sum(c.count for c in self)

    @classmethod
    def create_components(cls, extra_config: dict) -> None:
        with open(config_path(cls.CONFIG_FILE)) as f:
            config = yaml.load(f, Loader=yaml.SafeLoader)

        components = cls(config, extra_config)

        for component in components:
            for _ in range(component.count):
                yield component

        print(f"Generated {components.total} {cls.__name__}.")
