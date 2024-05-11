import os
import glob

from PIL import Image, ImageDraw

from ecogame.utils import mm_to_px, Font

FONT_HEIGHT_TITLE = 28
FONT_HEIGHT_VALUE = 40
FONT_HEIGHT_TEXT = 20
FONT_HEIGHT_KEYWORDS = 12
FONT_HEIGHT_FLAVOUR = 12
FONT_HEIGHT_COST = 20
FONT_HEIGHT_COUNT = 12

CARD_WIDTH, CARD_HEIGHT = mm_to_px(88.9), mm_to_px(63.5)
BACKGROUND_COLOR = (255, 255, 255, 255)
INK_COLOR = (0, 0, 0, 255)
CENTER_ICON_SIZE = 32, 32
IMAGE_SIZE = 60, 60
MARGIN_LEFT, MARGIN_RIGHT = mm_to_px(7), mm_to_px(7)
MARGIN_TOP, MARGIN_BOTTOM = mm_to_px(5), mm_to_px(5)
INNER_WIDTH = CARD_WIDTH - MARGIN_LEFT - MARGIN_RIGHT
INNER_HEIGHT = CARD_HEIGHT - MARGIN_TOP - MARGIN_BOTTOM
VALUE_MARGIN = mm_to_px(10)
TITLE_Y = mm_to_px(20)
VALUES_Y = mm_to_px(30)
CENTER_ICON_Y = VALUES_Y + 8
FLAVOUR_Y = mm_to_px(45)


class Cards:
    def __init__(self):
        self._font = Font("Arimo-Bold")
        self._images = {os.path.basename(im)[:-4]: Image.open(im) for im in glob.glob("./images/*.png")}

    def generate(self, config: hash, show_border: bool) -> list:
        for card_config in config:
            count = card_config.get("count", 1)
            card = self._card(show_border=show_border, **card_config)
            for _ in range(count):
                yield card

    def _card(self, title: str, cost: str, image: str = "", text: str = "", left_value: str = "", center_icon: str = "",
              right_value: str = "", flavour: str = "", keywords: list = None, count: int = 1,
              show_border: bool = False):
        card = Image.new("RGBA", (CARD_WIDTH, CARD_HEIGHT), BACKGROUND_COLOR)
        draw = ImageDraw.Draw(card)

        self._font.text(draw, (MARGIN_LEFT, MARGIN_TOP), cost, color=INK_COLOR, size=FONT_HEIGHT_COST)

        if image:
            sized_image = self._images[image].resize(IMAGE_SIZE, Image.Resampling.LANCZOS)
            card.paste(sized_image, ((CARD_WIDTH - IMAGE_SIZE[0]) // 2, MARGIN_TOP), mask=sized_image)

        if keywords:
            self._font.text(draw, (CARD_WIDTH - MARGIN_RIGHT, MARGIN_TOP), "\n".join(keywords),
                            anchor="ra", color=INK_COLOR, size=FONT_HEIGHT_KEYWORDS)

        self._font.text(draw, (CARD_WIDTH // 2, TITLE_Y), title, color=INK_COLOR, size=FONT_HEIGHT_TITLE,
                        anchor="ma")

        if text:
            self._font.text(draw, (MARGIN_LEFT, VALUES_Y), text, color=INK_COLOR, size=FONT_HEIGHT_TEXT)

        if left_value:
            self._font.text(draw, (MARGIN_LEFT + VALUE_MARGIN, VALUES_Y), left_value, color=INK_COLOR,
                            size=FONT_HEIGHT_VALUE)

        if center_icon:
            sized_image = self._images[center_icon].resize(CENTER_ICON_SIZE, Image.Resampling.LANCZOS)
            card.paste(sized_image, box=((CARD_WIDTH - CENTER_ICON_SIZE[0]) // 2, CENTER_ICON_Y), mask=sized_image)

        if right_value:
            self._font.text(draw, (CARD_WIDTH - MARGIN_RIGHT - VALUE_MARGIN, VALUES_Y), right_value, color=INK_COLOR,
                            size=FONT_HEIGHT_VALUE, anchor="ra")

        if flavour:
            self._font.text(draw, (MARGIN_LEFT, CARD_HEIGHT - MARGIN_BOTTOM), flavour, color=INK_COLOR,
                            size=FONT_HEIGHT_FLAVOUR, wrap_width=44, anchor="ld")

        if count != 1:
            self._font.text(draw, (CARD_WIDTH - MARGIN_RIGHT, CARD_HEIGHT - MARGIN_BOTTOM), str(count),
                            color=INK_COLOR, size=FONT_HEIGHT_COUNT, anchor="rd")

        if show_border:
            draw.rectangle((0, 0, CARD_WIDTH - 1, CARD_HEIGHT - 1), outline=(230, 230, 230, 255))

        return card
