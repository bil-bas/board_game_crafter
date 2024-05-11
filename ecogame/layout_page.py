from PIL import Image, ImageDraw

from ecogame.utils import A4_WIDTH, A4_HEIGHT, mm_to_px
from ecogame.cards import CARD_WIDTH, CARD_HEIGHT

COLS, ROWS = 3, 3
MARGIN_LEFT, MARGIN_TOP = mm_to_px(14), mm_to_px(9)
SPACING = mm_to_px(1)
REG_MARGIN = mm_to_px(8)
REG_LEFT, REG_TOP = REG_MARGIN, REG_MARGIN
REG_LEN = mm_to_px(5)
REG_RIGHT, REG_BOTTOM = A4_HEIGHT - REG_MARGIN, A4_WIDTH - REG_MARGIN


def layout_page(cards):
    page = Image.new("RGBA", (A4_HEIGHT, A4_WIDTH), (255, 255, 255, 255))
    draw = ImageDraw.Draw(page)

    for row in range(ROWS):
        for col in range(COLS):
            try:
                index = row * COLS + col
                page.paste(cards[index], (MARGIN_LEFT + col * (CARD_WIDTH + SPACING),
                                          MARGIN_TOP + row * (CARD_HEIGHT + SPACING)))
            except IndexError:
                break

    # Top left.
    reg_mark(draw, REG_LEFT, REG_TOP)
    reg_mark(draw, REG_RIGHT, REG_TOP)
    reg_mark(draw, REG_LEFT, REG_BOTTOM)
    reg_mark(draw, REG_RIGHT, REG_BOTTOM)

    return page


def reg_mark(draw, x, y):
    draw.line(((x - REG_LEN, y), (x + REG_LEN, y)), fill=(0, 0, 0, 0), width=1)
    draw.line(((x, y - REG_LEN), (x, y + REG_LEN)), fill=(0, 0, 0, 0), width=1)
