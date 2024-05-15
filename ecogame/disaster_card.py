import drawsvg as svg
from ecogame.utils import mm_to_px
from ecogame.base_card import PortraitCard


class DisasterCard(PortraitCard):
    TABLE_Y = mm_to_px(35)
    TABLE_ROW_HEIGHT = mm_to_px(12)
    TABLE_COL_WIDTH = mm_to_px(25)
    FONT_HEIGHT_TABLE = 18
    FONT_HEIGHT_PLAYERS = 24
    PLAYERS_Y = mm_to_px(22)

    def _render(self, number_of_players: int):
        # Title and number of players
        yield svg.Text("Disasters", self.FONT_HEIGHT_TITLE, self.CARD_WIDTH // 2,
                       self.MARGIN_TOP + self.FONT_HEIGHT_TITLE,
                       font_weight="bold", text_anchor="middle")

        yield svg.Text(f"{number_of_players} players", self.FONT_HEIGHT_PLAYERS, self.CARD_WIDTH // 2,
                       self.PLAYERS_Y, text_anchor="middle")

        yield from self.effects_table(number_of_players)

    def effects_table(self, number_of_players):
        # Effects table.
        center = self.MARGIN_LEFT + self.TABLE_COL_WIDTH
        size = self.FONT_HEIGHT_TABLE
        for add, multiplier in enumerate(range(8, 20, 4)):
            y_offset = self.TABLE_Y + self.TABLE_ROW_HEIGHT * add
            label = f"{multiplier * number_of_players}-{(multiplier + 2) * number_of_players - 1}P"
            yield from self._value(label, self.FONT_HEIGHT_TABLE, center - size - 2, y_offset, right_justify=True)

            yield self._image(center - size, y_offset, size, "then")
            yield self._image(center + 8, y_offset, size, "dice")

            if add:
                add_value = f" + {add}$"
            else:
                add_value = " $"

            yield from self._value(add_value, self.FONT_HEIGHT_TABLE, center + size + 12, y_offset)

            yield from self._end_of_civilisation(center, number_of_players, size)

    def _end_of_civilisation(self, center, number_of_players, size):
        # End of civilisation!
        yield from self._value(f"{20 * number_of_players}+P", self.FONT_HEIGHT_TABLE,
                               center - 20, self.TABLE_Y + self.TABLE_ROW_HEIGHT * 3,
                               right_justify=True)
        yield self._image(center - size, self.TABLE_Y + self.TABLE_ROW_HEIGHT * 3, size, "then")
        yield svg.Text("END", self.FONT_HEIGHT_TABLE,
                       center + 10, self.TABLE_Y + self.FONT_HEIGHT_TABLE + self.TABLE_ROW_HEIGHT * 3,
                       font_weight="bold")
