import textwrap

MM_TO_PX = 3.7795275591
FONT_HEIGHT_TITLE = 32
FONT_HEIGHT_VALUE = 40
FONT_HEIGHT_TEXT = 20
FONT_HEIGHT_KEYWORDS = 14
FONT_HEIGHT_FLAVOUR = 12


def mm_to_px(mm: float) -> int:
    return round(mm * MM_TO_PX)


A4_WIDTH, A4_HEIGHT = mm_to_px(210), mm_to_px(297)
LINE_WIDTH = 2


def draw_text(draw, pos, text: str, color, font, align: str = "left", width: int = None):
    if align == "left":
        pass
    elif align == "right":
        pos = (pos[0] - font.getlength(text), pos[1])
    elif align == "center":
        text_width = font.getlength(text)
        pos = ((pos[0] + (width - text_width) / 2), pos[1])
    elif align == "wrap":
        for i, line in enumerate(textwrap.fill(text, width).split("\n")):
            draw_text(draw, (pos[0], pos[1] + i * 15), line, color=color, font=font)
        return
    else:
        raise f"Unexpected align: {align}"

    draw.text(pos, text, fill=color, font=font)
