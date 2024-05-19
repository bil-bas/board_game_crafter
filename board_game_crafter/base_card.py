from .utils import mm_to_px
from .base_component import BaseComponent


class BaseCard(BaseComponent):
    pass


class PortraitCardMixin:
    WIDTH, HEIGHT = mm_to_px(63.5), mm_to_px(88.9)
    MARGIN_LEFT, MARGIN_RIGHT = mm_to_px(5), mm_to_px(5)
    MARGIN_TOP, MARGIN_BOTTOM = mm_to_px(5), mm_to_px(5)
    COLS, ROWS = 2, 4
    ROTATE = True


class LandscapeCardMixin:
    WIDTH, HEIGHT = mm_to_px(88.9), mm_to_px(63.5)
    MARGIN_LEFT, MARGIN_RIGHT = mm_to_px(5), mm_to_px(5)
    MARGIN_TOP, MARGIN_BOTTOM = mm_to_px(5), mm_to_px(5)
    COLS, ROWS = 2, 4
