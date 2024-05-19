from .utils import mm_to_px
from .base_component import BaseComponent


class BaseCard(BaseComponent):
    pass


class PortraitCardMixin:
    WIDTH, HEIGHT = mm_to_px(63.5), mm_to_px(88.9)
    MARGIN_LEFT, MARGIN_RIGHT = mm_to_px(5), mm_to_px(5)
    MARGIN_TOP, MARGIN_BOTTOM = mm_to_px(5), mm_to_px(5)
    INNER_WIDTH = WIDTH - MARGIN_LEFT - MARGIN_RIGHT
    INNER_HEIGHT = HEIGHT - MARGIN_TOP - MARGIN_BOTTOM
    BLEED_WIDTH = WIDTH + BaseCard.BLEED_MARGIN * 2
    BLEED_HEIGHT = HEIGHT + BaseCard.BLEED_MARGIN * 2
    ROTATE = True
    COLS, ROWS = 2, 4


class LandscapeCardMixin:
    WIDTH, HEIGHT = mm_to_px(88.9), mm_to_px(63.5)
    MARGIN_LEFT, MARGIN_RIGHT = mm_to_px(5), mm_to_px(5)
    MARGIN_TOP, MARGIN_BOTTOM = mm_to_px(5), mm_to_px(5)
    INNER_WIDTH = WIDTH - MARGIN_LEFT - MARGIN_RIGHT
    INNER_HEIGHT = HEIGHT - MARGIN_TOP - MARGIN_BOTTOM
    BLEED_WIDTH = WIDTH + BaseCard.BLEED_MARGIN * 2
    BLEED_HEIGHT = HEIGHT + BaseCard.BLEED_MARGIN * 2
    COLS, ROWS = 2, 4