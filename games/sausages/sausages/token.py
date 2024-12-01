import textwrap

import drawsvg as svg

from board_game_crafter.utils import mm_to_px
from board_game_crafter.base_components import BaseComponents
from board_game_crafter.base_component import BaseComponent


class Token(BaseComponent):
    WIDTH = HEIGHT = mm_to_px(16)
    IMAGE_SIZE = mm_to_px(12), mm_to_px(12)
    FONT_SIZE = 10
    FONT_FAMILY = "Albertus"
    COLS, ROWS = 5, 7
    TEMPLATE_RADIUS = 4
    SPACING = mm_to_px(2)

    def _render_front(self, title: str = "", image: str = "", shape: str = "square"):
        # image
        if image:
            yield self._image((self.width - self.IMAGE_SIZE[0]) // 2, (self.height - self.IMAGE_SIZE[0]) // 2,
                              self.IMAGE_SIZE[0], image)

        # Title
        if title:
            lines = textwrap.wrap(title, 12)
            height = (self.FONT_SIZE + 2) * (len(lines) - 1)

            yield svg.Text("\n".join(lines), self.FONT_SIZE, self.WIDTH / 2, self.height / 2 -height // 2 ,
                           font_family=self.FONT_FAMILY,
                           text_anchor="middle", dominant_baseline="middle",)

    def _render_template(self, title: str = "", image: str = "", shape: str = "square") -> None:
        yield from super()._render_template()

class Tokens(BaseComponents):
    CARD_CLASS = Token
    CONFIG_FILE = "tokens.yaml"
