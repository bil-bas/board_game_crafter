import drawsvg as svg

from board_game_crafter.base_card import BaseCard
from board_game_crafter.utils import mm_to_px, image_path


class GameCard(BaseCard):
    TEXT_ICON_SPACING = 2

    FONT_HEIGHT_TITLE = 24
    FONT_HEIGHT_VALUE = 34
    FONT_HEIGHT_TEXT = 20
    FONT_HEIGHT_KEYWORDS = 12
    FONT_HEIGHT_FLAVOUR = 12
    FONT_HEIGHT_COST = 18
    FONT_HEIGHT_COUNT = 12

    BACK_BORDER_COLOR = "#555555"  # Dark grey
    BACK_BACKGROUND_COLOR = "#F2EBE3"  # Ivory
    BACK_BORDER_WIDTH = mm_to_px(10)
    BACK_FONT_HEIGHT_TITLE = 32
    BACK_FONT_HEIGHT_TYPE = 20

    BACK_LABEL = "Card"

    def _render_back(self, **config):
        yield svg.Rectangle(-self.BLEED_MARGIN, -self.BLEED_MARGIN, self.bleed_width, self.bleed_height,
                            fill=self.BACK_BORDER_COLOR, stroke="none")

        yield svg.Rectangle(self.margin_left, self.margin_top, self.inner_width, self.inner_height,
                            stroke="none", fill=self.BACK_BACKGROUND_COLOR)

        yield svg.Text("ECOGAME", self.BACK_FONT_HEIGHT_TITLE, self.width / 2, self.height / 2,
                       center=True, font_family=self.FONT_FAMILY_TITLE)

        yield svg.Text(self.BACK_LABEL, self.BACK_FONT_HEIGHT_TYPE, self.width / 2, self.height / 2 + 40,
                       center=True, font_family=self.FONT_FAMILY_BODY)

    def _value(self, value: str, size: int, x: float, y: float, right_justify: bool = False,
               font_family: str = None):
        if font_family is None:
            font_family = self.FONT_FAMILY_BODY

        if value.endswith("P"):
            icon = "pollution"
            value = value[:-1]
        elif value.endswith("$"):
            icon = "prosperity"
            value = value[:-1]
        else:
            icon = None

        if right_justify:
            text_anchor = "end"
            icon_x = x - size
            text_x = icon_x - self.TEXT_ICON_SPACING
        else:
            text_anchor = "start"
            text_x = x
            icon_x = x + len(value) * size * 0.7 + self.TEXT_ICON_SPACING

        yield svg.Text(value, size, text_x, y + size, text_anchor=text_anchor, font_weight="bold",
                       font_family=font_family)

        if icon:
            yield self._image(icon_x, y + size * 0.2, size * 0.8, icon)

    @staticmethod
    def _image(x: float, y: float, size: float, name: str) -> svg.Image:
        return svg.Image(x, y, size, size, path=image_path(f"{name}.png"), embed=True)