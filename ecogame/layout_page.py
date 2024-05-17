import drawsvg as svg
from ecogame.utils import A4_WIDTH, A4_HEIGHT, mm_to_px


MARGIN = mm_to_px(13)
SPACING = mm_to_px(3.5)
REG_MARGIN = mm_to_px(10)
REG_LEFT, REG_TOP = REG_MARGIN, REG_MARGIN
REG_LEN, REG_WIDTH = mm_to_px(5), 4
REG_RIGHT = A4_WIDTH - REG_MARGIN

COLOR_BORDER = "grey"
COLOR_REG = "red"
COLOR_MARGIN = "lightgrey"


def layout_page(cards, show_border, show_margin):
    draw = svg.Drawing(A4_WIDTH, A4_HEIGHT, origin="top-left")

    if cards[0].ROTATE:
        width, height = cards[0].height, cards[0].width
        rotation = f", translate(0, {height}) rotate({-90})"
    else:
        width, height = cards[0].width, cards[0].height
        rotation = ""

    cols, rows = cards[0].COLS, cards[0].ROWS

    base = render_cards(cards, cols, draw, height, rotation, rows, show_border, show_margin, width)

    draw.extend(reg_mark(REG_LEFT, REG_TOP))
    draw.extend(reg_mark(REG_RIGHT, REG_TOP))
    draw.extend(reg_mark(REG_LEFT, base))
    draw.extend(reg_mark(REG_RIGHT, base))

    return draw


def render_cards(cards, cols, draw, height, rotation, rows, show_border, show_margin, width):
    top = None

    for row in range(rows):
        for col in range(cols):
            index = row * cols + col
            left = MARGIN + col * (width + SPACING)
            top = MARGIN + row * (height + SPACING)

            try:
                card = cards[index]
            except IndexError:
                return top

            group = svg.Group(transform=f"translate({left}, {top}) {rotation}")

            group.extend(card.render())

            if show_border:
                group.append(svg.Rectangle(0, 0, card.width, card.height, stroke=COLOR_BORDER, fill="none"))

            if show_margin:
                group.append(svg.Rectangle(card.MARGIN_LEFT, card.MARGIN_TOP, card.INNER_WIDTH, card.INNER_HEIGHT,
                                           stroke=COLOR_MARGIN, fill="none"))

            draw.append(group)

    return top + height + SPACING


def reg_mark(x, y):
    yield svg.Line(x - REG_LEN, y, x + REG_LEN, y, stroke=COLOR_REG)
    yield svg.Line(x, y - REG_LEN, x, y + REG_LEN, stroke=COLOR_REG)
