from PIL import Image, ImageDraw

from ecogame.utils import mm_to_px
from ecogame.base_cards import BaseCards, PortraitCards


class DisasterCards(PortraitCards, BaseCards):
    TABLE_Y = mm_to_px(35)
    TABLE_ROW_HEIGHT = mm_to_px(12)
    TABLE_COL_WIDTH = mm_to_px(25)
    FONT_HEIGHT_TABLE = 20
    FONT_HEIGHT_PLAYERS = 24
    PLAYERS_Y = mm_to_px(18)

    CONFIG_FILE = "./config/disaster_cards.yaml"

    def generate(self, config: hash, show_border: bool, show_count: bool) -> list:
        for card_config in config:
            yield self._card(show_border=show_border, **card_config)

    def _card(self, show_border: bool, number_of_players: int):
        card = Image.new("RGBA", (self.CARD_WIDTH, self.CARD_HEIGHT), self.BACKGROUND_COLOR)
        draw = ImageDraw.Draw(card)

        # Title & number of players.
        self._font.text(draw, (self.CARD_WIDTH // 2, self.MARGIN_TOP), "Disaster Effect",
                        color=self.INK_COLOR, size=self.FONT_HEIGHT_TITLE, anchor="ma")

        self._font.text(draw, (self.CARD_WIDTH // 2, self.PLAYERS_Y), f"{number_of_players} players",
                        color=self.INK_COLOR, size=self.FONT_HEIGHT_PLAYERS, anchor="ma")

        # Effects table.
        center = self.MARGIN_LEFT + self.TABLE_COL_WIDTH
        sized_image = self._image("dice", (self.FONT_HEIGHT_TABLE, self.FONT_HEIGHT_TABLE))

        for add, multiplier in enumerate(range(8, 20, 4)):
            y = self.TABLE_Y + self.TABLE_ROW_HEIGHT * add
            self._font.text(draw, (center, y),
                            f"{multiplier * number_of_players}-{(multiplier + 2) * number_of_players - 1}: ",
                            color=self.INK_COLOR, size=self.FONT_HEIGHT_TABLE, anchor="ra")

            card.paste(sized_image, (center, y), mask=sized_image)
            if add:
                add = f" + {add}$"
            else:
                add = "$"
            self._value(card, draw, (center + sized_image.width, y), add, size=self.FONT_HEIGHT_TABLE)

        # End of civilisation!
        self._font.text(draw, (center, self.TABLE_Y + self.TABLE_ROW_HEIGHT * 3),
                        f"{20 * number_of_players}+: ",
                        color=self.INK_COLOR, size=self.FONT_HEIGHT_TABLE, anchor="ra")

        self._font.text(draw, (center, self.TABLE_Y + self.TABLE_ROW_HEIGHT * 3),
                        "END", color=self.INK_COLOR, size=self.FONT_HEIGHT_TABLE)

        if show_border:
            draw.rectangle((0, 0, self.CARD_WIDTH - 1, self.CARD_HEIGHT - 1), outline=(210, 210, 210, 255))

        return card
