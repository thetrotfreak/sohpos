from random import choice

from flet import ControlEvent, IconButton, Icons, ThemeMode


class SohposThemeModeButton(IconButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __on_click(self, e: ControlEvent):
        if self.page:
            match self.page.theme_mode:
                case ThemeMode.LIGHT:
                    self.page.theme_mode = ThemeMode.DARK
                case ThemeMode.DARK:
                    self.page.theme_mode = ThemeMode.LIGHT
                case ThemeMode.SYSTEM:
                    self.page.theme_mode = choice((ThemeMode.LIGHT, ThemeMode.DARK))
                case _:
                    pass
            # NOTE
            # Since we changed the Page's attributes
            # We need to call update() on the Page
            # This is not an isloated control
            # So, self (our custom control)
            # will be included in the update() digest
            self.page.update()

    def build(self):
        if self.page:
            match self.page.theme_mode:
                case ThemeMode.LIGHT:
                    self.icon = Icons.LIGHT_MODE
                case ThemeMode.DARK:
                    self.icon = Icons.DARK_MODE
                case _:
                    self.icon = Icons.CONTRAST
            self.on_click = self.__on_click

    def before_update(self):
        # NOTE
        # We won't call
        # update() either on the Page, or
        # the self
        if self.page:
            match self.page.theme_mode:
                case ThemeMode.LIGHT:
                    self.icon = Icons.LIGHT_MODE
                case ThemeMode.DARK:
                    self.icon = Icons.DARK_MODE
                case _:
                    self.icon = Icons.CONTRAST
