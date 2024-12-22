from enum import IntEnum, StrEnum

from flet import Colors, Theme


class SohposPreferences(StrEnum):
    SOHPOS_THEME_MODE = "sohpos.theme_mode"
    SOHPOS_THEME = "sohpos.theme"
    SOHPOS_USERNAME = "sohpos.username"
    SOHPOS_PASSWORD = "sohpos.password"
    SOHPOS_MRU_MODE = "sohpos.mode"


class SohposPreferencesWindow(IntEnum):
    SOHPOS_WINDOW_WIDTH = 450
    SOHPOS_WINDOW_HEIGHT = 550


SohposColors = (
    Colors.AMBER,
    Colors.BLUE,
    Colors.BROWN,
    Colors.CYAN,
    Colors.GREEN,
    Colors.INDIGO,
    Colors.LIME,
    Colors.ORANGE,
    Colors.PINK,
    Colors.PURPLE,
    Colors.RED,
    Colors.TEAL,
    Colors.YELLOW,
)

SohposDefaultTheme = Theme(color_scheme_seed=Colors.BLUE)
