import drawsvg as svg

from .utils import mm_to_px
from .base_component import Face

MARGIN = mm_to_px(10)
SPACING = mm_to_px(4)
REG_MARGIN = mm_to_px(5)
REG_LEFT, REG_TOP = REG_MARGIN, REG_MARGIN
REG_LEN, REG_WIDTH = mm_to_px(5), 4

COLOR_BORDER = "grey"
COLOR_REG = "red"
COLOR_MARGIN = "lightgrey"


def layout_page(components: list, show_border: bool, show_margin: bool, face: str,
                page_width: int, page_height: int):
    assert face in Face.ALL

    draw = svg.Drawing(page_width, page_height, origin="top-left")

    cols, rows = components[0].COLS, components[0].ROWS

    if components[0].ROTATE:
        width, height = components[0].height, components[0].width
        rotation = f"translate(0, {height}) rotate({-90})"
    else:
        width, height = components[0].width, components[0].height
        rotation = ""

    # Ensure we center any components.
    render_width = cols * width + (cols - 1) * SPACING
    render_offset_y = (page_width - render_width) / 2

    page = svg.Group()

    render_area = svg.Group(transform=f"translate({render_offset_y}, {MARGIN})")
    reg_bottom = render_components(components=components, cols=cols, draw=render_area, height=height, rotation=rotation,
                                   rows=rows, show_border=show_border, show_margin=show_margin, width=width, face=face)
    page.append(render_area)

    reg_bottom += MARGIN * 2 - REG_MARGIN
    reg_right = page_width - REG_MARGIN

    page.extend(reg_mark(REG_LEFT, REG_TOP, left=True, top=True))
    page.extend(reg_mark(reg_right, REG_TOP, left=False, top=True))
    page.extend(reg_mark(REG_LEFT, reg_bottom, left=True, top=False))
    page.extend(reg_mark(reg_right, reg_bottom, left=False, top=False))

    draw.append(page)

    return draw


def render_components(components: list, cols: int, draw, height: int, rotation: str, rows: int, show_border: bool,
                      show_margin: bool, width: int, face: str):
    assert face in Face.ALL

    top = None

    for row in range(rows):
        for col in range(cols):
            index = row * cols + col

            # Flip backs the other way around, so they line up with the fronts when printed double-sided.
            if face == Face.BACK:
                left = (cols - 1 - col) * (width + SPACING)
            else:
                left = col * (width + SPACING)

            top = row * (height + SPACING)

            try:
                component = components[index]
            except IndexError:
                return top - SPACING if col == 0 else top + height

            group = svg.Group(transform=f"translate({left}, {top}) {rotation}")

            group.extend(component.render(face))

            if show_border:
                group.extend(component.render(Face.TEMPLATE))

            if show_margin:
                group.append(svg.Rectangle(component.margin_left, component.margin_top,
                                           component.inner_width, component.inner_height,
                                           stroke=COLOR_MARGIN, fill="none"))

            draw.append(group)

    return top + height


def reg_mark(x: float, y: float, left: bool, top: bool):
    yield svg.Line(x, y, x + REG_LEN * (1 if left else -1), y, stroke=COLOR_REG)
    yield svg.Line(x, y, x, y + REG_LEN * (1 if top else -1), stroke=COLOR_REG)
