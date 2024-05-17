import drawsvg as svg

from .utils import A4_WIDTH, A4_HEIGHT, mm_to_px, DEFAULT_DPI

MARGIN = mm_to_px(13)
SPACING = mm_to_px(4)
REG_MARGIN = mm_to_px(10)
REG_LEFT, REG_TOP = REG_MARGIN, REG_MARGIN
REG_LEN, REG_WIDTH = mm_to_px(5), 4
REG_RIGHT = A4_WIDTH - REG_MARGIN

COLOR_BORDER = "grey"
COLOR_REG = "red"
COLOR_MARGIN = "lightgrey"


def layout_page(cards: list, show_border: bool, show_margin: bool, render_backs: bool, dpi: int = DEFAULT_DPI):
    scale = dpi / DEFAULT_DPI
    draw = svg.Drawing(A4_WIDTH * scale, A4_HEIGHT * scale, origin="top-left")

    if cards[0].ROTATE:
        width, height = cards[0].height, cards[0].width
        rotation = f", translate(0, {height}) rotate({-90})"
    else:
        width, height = cards[0].width, cards[0].height
        rotation = ""

    cols, rows = cards[0].COLS, cards[0].ROWS

    page = svg.Group(transform=f"scale({scale})")

    base = render_cards(cards=cards, cols=cols, draw=page, height=height, rotation=rotation, rows=rows,
                        show_border=show_border, show_margin=show_margin, width=width, render_backs=render_backs)

    page.extend(reg_mark(REG_LEFT, REG_TOP, left=True, top=True))
    page.extend(reg_mark(REG_RIGHT, REG_TOP, left=False, top=True))
    page.extend(reg_mark(REG_LEFT, base, left=True, top=False))
    page.extend(reg_mark(REG_RIGHT, base, left=False, top=False))

    draw.append(page)

    return draw


def render_cards(cards: list, cols: int, draw, height: int, rotation: str, rows: int, show_border: bool,
                 show_margin: bool, width: int, render_backs: bool):
    top = None

    for row in range(rows):
        for col in range(cols):
            index = row * cols + col

            if render_backs:
                left = MARGIN + (cols - 1 - col) * (width + SPACING)
            else:
                left = MARGIN + col * (width + SPACING)

            top = MARGIN + row * (height + SPACING)

            try:
                card = cards[index]
            except IndexError:
                return top

            group = svg.Group(transform=f"translate({left}, {top}) {rotation}")

            group.extend(card.render_back() if render_backs else card.render_front())

            if show_border:
                group.append(svg.Rectangle(0, 0, card.width, card.height, stroke=COLOR_BORDER, fill="none"))

            if show_margin:
                group.append(svg.Rectangle(card.MARGIN_LEFT, card.MARGIN_TOP, card.INNER_WIDTH, card.INNER_HEIGHT,
                                           stroke=COLOR_MARGIN, fill="none"))

            draw.append(group)

    return top + height + SPACING


def reg_mark(x: float, y: float, left: bool, top: bool):
    yield svg.Line(x, y, x + REG_LEN * (1 if left else -1), y, stroke=COLOR_REG)
    yield svg.Line(x, y, x, y + REG_LEN * (1 if top else -1), stroke=COLOR_REG)
