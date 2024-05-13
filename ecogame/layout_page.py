from PIL import Image, ImageDraw

from ecogame.utils import A4_WIDTH, A4_HEIGHT, mm_to_px


MARGIN = mm_to_px(13)
SPACING = mm_to_px(3.5)
REG_MARGIN = mm_to_px(10)
REG_LEFT, REG_TOP = REG_MARGIN, REG_MARGIN
REG_LEN, REG_WIDTH = mm_to_px(5), 4
REG_RIGHT, REG_BOTTOM = A4_WIDTH - REG_MARGIN, A4_HEIGHT - REG_MARGIN


def layout_page(cards):
    page = Image.new("RGBA", (A4_WIDTH, A4_HEIGHT), (255, 255, 255, 255))
    draw = ImageDraw.Draw(page)

    width, height = cards[0].width, cards[0].height
    cols, rows = cards[0].cols, cards[0].rows

    for row in range(rows):
        for col in range(cols):
            try:
                index = row * cols + col
                card = cards[index]
                page.paste(card, (MARGIN + col * (width + SPACING),
                                  MARGIN + row * (height + SPACING)))
            except IndexError:
                break

    # Top left.
    reg_mark(draw, REG_LEFT, REG_TOP)
    reg_mark(draw, REG_RIGHT, REG_TOP)
    reg_mark(draw, REG_LEFT, REG_BOTTOM)
    reg_mark(draw, REG_RIGHT, REG_BOTTOM)

    return page


def reg_mark(draw, x, y):
    draw.line(((x - REG_LEN, y), (x + REG_LEN, y)), fill=(0, 0, 0, 255), width=2)
    draw.line(((x, y - REG_LEN), (x, y + REG_LEN)), fill=(0, 0, 0, 255), width=2)
