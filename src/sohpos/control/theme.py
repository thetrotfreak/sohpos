from flet import (
    AlertDialog,
    Column,
    ControlEvent,
    Radio,
    RadioGroup,
    Ref,
    Text,
    TextAlign,
    ThemeMode,
)

from ..preferences import SohposPreferences
from ..strings import SohposStrings


class SohposThemeModeAlertDialog(AlertDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ref_radio_group = Ref[RadioGroup]()

    async def __on_change(self, event: ControlEvent):
        self.page.theme_mode = ThemeMode(event.control.value)
        self.page.session.set(
            SohposPreferences.SOHPOS_THEME_MODE.value, self.page.theme_mode.value
        )
        self.page.update()

    def __value(self):
        match self.page.theme_mode:
            case ThemeMode.LIGHT | ThemeMode.DARK as e:
                return e.value
            case _:
                return ThemeMode.SYSTEM.value

    def build(self):
        self.title = Text(
            value=SohposStrings.SOHPOS_DIALOG_THEME_MODE.value.title(),
            text_align=TextAlign.CENTER,
        )
        self.content = RadioGroup(
            ref=self.ref_radio_group,
            content=Column(
                controls=[
                    Radio(
                        value=ThemeMode.SYSTEM.value,
                        label=ThemeMode.SYSTEM.value.capitalize(),
                    ),
                    Radio(
                        value=ThemeMode.LIGHT.value,
                        label=ThemeMode.LIGHT.value.capitalize(),
                    ),
                    Radio(
                        value=ThemeMode.DARK.value,
                        label=ThemeMode.DARK.value.capitalize(),
                    ),
                ],
                tight=True,
            ),
            value=self.__value(),
            on_change=self.__on_change,
        )
