import drawsvg as svg

from board_game_crafter.utils import mm_to_px
from board_game_crafter.base_components import BaseComponents
from .game_card import GameCard


class BuyCard(GameCard):
    MARGIN_LEFT = MARGIN_RIGHT = MARGIN_TOP = MARGIN_BOTTOM = GameCard.MARGIN
    IMAGE_SIZE = mm_to_px(45), mm_to_px(45)
    TITLE_Y = mm_to_px(28)
    TEXT_Y = mm_to_px(60)
    VALUE_WIDTH = mm_to_px(18)

    def _render_front(self, cost: str = "Start", value: str = "", title: str = "", text: str = "", image: str = "",
                      instant: bool = False):
        # Cost
        yield svg.Text(str(cost), self.FONT_HEIGHT_COST, self.margin_left, self.margin_top,
                       font_family=self.FONT_FAMILY_TITLE, dominant_baseline="hanging", font_weight="bold")

        if instant:
            yield svg.Text("Instant", self.FONT_HEIGHT_COST, self.width - self.margin_right, self.margin_top,
                           text_anchor="end",
                           font_family=self.FONT_FAMILY_TITLE, dominant_baseline="hanging", font_weight="bold")

        # image
        yield self._image((self.width - self.IMAGE_SIZE[0]) // 2, self.margin_top + mm_to_px(5),
                          self.IMAGE_SIZE[0], image)

        # Title
        yield svg.Text(title, self.FONT_HEIGHT_TITLE, self.WIDTH // 2, self.TITLE_Y, font_weight="bold",
                       text_anchor="middle", font_family=self.FONT_FAMILY_TITLE)

        # text
        if text:
            yield self._wrap(text, self.FONT_HEIGHT_TEXT, self.MARGIN_LEFT, self.TEXT_Y,
                             font_family=self.FONT_FAMILY_BODY, width=self.WRAP_WIDTH)

        # value
        if value:
            yield self._add_value(value)

    def _add_value(self, value):
        values = value.split(" ")

        group = svg.Group(transform=f"translate({(self.width - self.VALUE_WIDTH * len(values)) / 2})")

        for i, val in enumerate(values):
            group.extend(self._value(val, self.FONT_HEIGHT_VALUE, i * self.VALUE_WIDTH,
                         self.HEIGHT - self.MARGIN_BOTTOM - self.FONT_HEIGHT_VALUE, font_family=self.FONT_FAMILY_TITLE))

        return group


class BuyCards(BaseComponents):
    CARD_CLASS = BuyCard
    CONFIG_FILE = "local_cards.yaml"
