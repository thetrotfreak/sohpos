from flet import (
    Divider,
    Icons,
    PopupMenuButton,
    PopupMenuItem,
    PopupMenuPosition,
    Ref,
    ThemeMode,
)

from .about import SohposAboutDialog
from .account import SohposAccountDialog
from .material import SohposThemeAlertDialog
from .theme import SohposThemeModeAlertDialog


class SohposMenuButton(PopupMenuButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dialog = Ref[SohposThemeAlertDialog]()
        self.ref_theme_mode = Ref[PopupMenuItem]()

    def _theme_mode_icon(self):
        match self.page.theme_mode:
            case ThemeMode.LIGHT:
                return Icons.LIGHT_MODE
            case ThemeMode.DARK:
                return Icons.DARK_MODE
            case _:
                return Icons.CONTRAST

    def before_update(self):
        self.ref_theme_mode.current.icon = self._theme_mode_icon()

    def build(self):
        self.menu_position = PopupMenuPosition.UNDER
        self.icon = Icons.ACCOUNT_CIRCLE
        self.items = [
            PopupMenuItem(
                icon=Icons.SCHOOL,
                text="Account".title(),
                on_click=lambda _: self.page.open(control=SohposAccountDialog()),
            ),
            Divider(),
            PopupMenuItem(
                icon=Icons.PALETTE,
                text="Color".title(),
                on_click=lambda _: self.page.open(control=SohposThemeAlertDialog()),
            ),
            PopupMenuItem(
                ref=self.ref_theme_mode,
                icon=self._theme_mode_icon(),
                text="theme".title(),
                on_click=lambda _: self.page.open(control=SohposThemeModeAlertDialog()),
            ),
            Divider(),
            PopupMenuItem(
                icon=Icons.INFO,
                text="about".title(),
                on_click=lambda _: self.page.open(control=SohposAboutDialog()),
            ),
            Divider(),
            PopupMenuItem(
                icon=Icons.EXIT_TO_APP,
                text="exit".capitalize(),
                on_click=lambda _: self.page.window.close(),
            ),
        ]
