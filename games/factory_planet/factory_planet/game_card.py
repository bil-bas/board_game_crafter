import drawsvg as svg

from board_game_crafter.base_card import BaseCard, PortraitCardMixin
from board_game_crafter.utils import mm_to_px, image_path


class GameCard(PortraitCardMixin, BaseCard):
    TEXT_ICON_SPACING = 2

    FONT_HEIGHT_TITLE = 24
    FONT_HEIGHT_VALUE = 30
    FONT_HEIGHT_TEXT = 20
    FONT_HEIGHT_KEYWORDS = 12
    FONT_HEIGHT_FLAVOUR = 12
    FONT_HEIGHT_COST = 28

    BACK_BORDER_COLOR = "#555555"  # Dark grey
    BACK_BACKGROUND_COLOR = "#F2EBE3"  # Ivory
    BACK_BORDER_WIDTH = mm_to_px(10)
    BACK_FONT_HEIGHT_TITLE = 32
    BACK_FONT_HEIGHT_TYPE = 20

    WRAP_WIDTH = 18

    BACK_IMAGE = None
    BACK_IMAGE_SIZE = mm_to_px(40)
    BACK_LABEL = None
    BACK_LABEL_FONT_SIZE = 24
    BACK_LABEL_Y = mm_to_px(75)

    COLS, ROWS = 3, 3
    ROTATE = False

    def _render_back(self, image: str = "", **config):
        yield svg.Rectangle(-self.BLEED_MARGIN, -self.BLEED_MARGIN, self.bleed_width, self.bleed_height,
                            fill=self.BACK_BORDER_COLOR, stroke="none")

        yield svg.Rectangle(self.margin_left, self.margin_top, self.inner_width, self.inner_height,
                            stroke="none", fill=self.BACK_BACKGROUND_COLOR)

        yield self._image((self.width - self.BACK_IMAGE_SIZE) / 2, (self.height - self.BACK_IMAGE_SIZE) / 2,
                          self.BACK_IMAGE_SIZE, f"card_backs/{self.BACK_IMAGE}")

        yield svg.Text(self.BACK_LABEL, self.BACK_LABEL_FONT_SIZE, self.width / 2, self.BACK_LABEL_Y,
                       font=self.FONT_FAMILY_BODY, center=True)

    def _value(self, value: str, size: int, x: float, y: float, font_family: str = None):
        if font_family is None:
            font_family = self.FONT_FAMILY_BODY

        if value.endswith("E"):
            icon = "energy"
            value = value[:-1]
        elif value.endswith("$"):
            icon = "money"
            value = value[:-1]
        elif value.endswith("T"):
            icon = "seed"
            value = value[:-1]
        else:
            icon = None

        text_anchor = "start"
        icon_x = x + len(value) * size * 0.6 + self.TEXT_ICON_SPACING

        yield svg.Text(value, size, x, y + size, text_anchor=text_anchor, font_weight="bold",
                       font_family=font_family)

        if icon:
            yield self._image(icon_x, y + size * 0.2, size * 0.8, icon)

    @staticmethod
    def _image(x: float, y: float, size: float, name: str) -> svg.Image:
        return svg.Image(x, y, size, size, path=image_path(f"{name}.png"), embed=True)
