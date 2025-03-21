from kivy.utils import get_color_from_hex

class AppTheme:
    # Colors
    PRIMARY = '#406D96'
    PRIMARY_DARK = '#2F3A56'
    BACKGROUND = '#F5F5F5'
    ERROR = '#FF4444'
    TEXT = '#333333'
    HINT = '#999999'

    # Fonts
    FONT_SIZE_SMALL = 14
    FONT_SIZE_MEDIUM = 16
    FONT_SIZE_LARGE = 28
    FONT_SIZE_XLARGE = 32

    # Spacing
    PADDING = 20
    SPACING = 15
    BORDER_RADIUS = 10

    @classmethod
    def get_color(cls, color_name):
        return get_color_from_hex(getattr(cls, color_name)) 