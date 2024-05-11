import os
import glob

from PIL import ImageFont, Image, ImageDraw

from ecogame.utils import (FONT_HEIGHT_KEYWORDS, FONT_HEIGHT_VALUE, FONT_HEIGHT_TITLE, FONT_HEIGHT_FLAVOUR,
                           FONT_HEIGHT_TEXT, mm_to_px, draw_text)

CARD_WIDTH, CARD_HEIGHT = mm_to_px(88.9), mm_to_px(63.5)
BACKGROUND_COLOR = (255, 255, 255, 255)
INK_COLOR = (0, 0, 0, 255)
CENTER_ICON_SIZE = 32, 32
IMAGE_SIZE = 60, 60
MARGIN_LEFT, MARGIN_RIGHT = mm_to_px(5), mm_to_px(5)
MARGIN_TOP, MARGIN_BOTTOM = mm_to_px(3), mm_to_px(1)
INNER_WIDTH = CARD_WIDTH - MARGIN_LEFT - MARGIN_RIGHT
INNER_HEIGHT = CARD_HEIGHT - MARGIN_TOP - MARGIN_BOTTOM
VALUE_MARGIN = mm_to_px(10)
TITLE_Y = mm_to_px(20)
VALUES_Y = mm_to_px(30)
CENTER_ICON_Y = VALUES_Y + 8
FLAVOUR_Y = mm_to_px(45)
LINE_SPACING_KEYWORDS = FONT_HEIGHT_KEYWORDS + 2


class Cards:
    def __init__(self):
        font_file = "Arimo-Bold"
        self._font_title = ImageFont.truetype(f"./fonts/{font_file}.ttf", FONT_HEIGHT_TITLE)
        self._font_text = ImageFont.truetype(f"./fonts/{font_file}.ttf", FONT_HEIGHT_TEXT)
        self._font_value = ImageFont.truetype(f"./fonts/{font_file}.ttf", FONT_HEIGHT_VALUE)
        self._font_flavour = ImageFont.truetype(f"./fonts/{font_file}.ttf", FONT_HEIGHT_FLAVOUR)
        self._font_keywords = ImageFont.truetype(f"./fonts/{font_file}.ttf", FONT_HEIGHT_KEYWORDS)

        self._images = {os.path.basename(im)[:-4]: Image.open(im) for im in glob.glob("./images/*.png")}

    def generate(self, config) -> list:
        for card_config in config:
            count = card_config.pop("count", 1)
            card = self._card(**card_config)
            for _ in range(count):
                yield card

    def _card(self, title: str, image: str = "", text: str = "", left_value: str = "", center_icon: str = "",
              right_value: str = "", flavour: str = "", keywords: list = None):
        card = Image.new("RGBA", (CARD_WIDTH, CARD_HEIGHT), BACKGROUND_COLOR)
        draw = ImageDraw.Draw(card)

        if image:
            sized_image = self._images[image].resize(IMAGE_SIZE, Image.Resampling.LANCZOS)
            card.paste(sized_image, ((CARD_WIDTH - IMAGE_SIZE[0]) // 2, MARGIN_TOP), mask=sized_image)

        if keywords:
            for i, keyword in enumerate(keywords):
                draw_text(draw, (CARD_WIDTH - MARGIN_RIGHT, MARGIN_TOP + i * LINE_SPACING_KEYWORDS), keyword,
                          color=INK_COLOR, align="right", font=self._font_keywords)

        draw_text(draw, (MARGIN_LEFT, TITLE_Y), title, color=INK_COLOR, font=self._font_title, align="center",
                  width=INNER_WIDTH)

        if text:
            draw_text(draw, (MARGIN_LEFT, VALUES_Y), text, color=INK_COLOR, font=self._font_text, width=20, align="wrap")

        if left_value:
            draw_text(draw, (MARGIN_LEFT + VALUE_MARGIN, VALUES_Y), left_value, color=INK_COLOR, font=self._font_value)

        if center_icon:
            sized_image = self._images[center_icon].resize(CENTER_ICON_SIZE, Image.Resampling.LANCZOS)
            card.paste(sized_image, box=((CARD_WIDTH - CENTER_ICON_SIZE[0]) // 2, CENTER_ICON_Y), mask=sized_image)

        if right_value:
            draw_text(draw, (CARD_WIDTH - MARGIN_RIGHT - VALUE_MARGIN, VALUES_Y), right_value, color=INK_COLOR,
                      font=self._font_value,
                      align="right")

        if flavour:
            draw_text(draw, (MARGIN_LEFT, FLAVOUR_Y), flavour, color=INK_COLOR, font=self._font_flavour,
                      width=50, align="wrap")

        draw.rectangle((0, 0, CARD_WIDTH - 1, CARD_HEIGHT - 1), outline=(230, 230, 230, 255))

        return card
