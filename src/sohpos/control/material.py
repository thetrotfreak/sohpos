from flet import (
    AlertDialog,
    BoxShape,
    Colors,
    Container,
    ControlEvent,
    Icon,
    Icons,
    Ref,
    ResponsiveRow,
    Text,
    TextAlign,
    Theme,
)

from ..preferences import SohposColors, SohposPreferences
from ..strings import SohposStrings


class SohposThemeAlertDialog(AlertDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._palette = Ref[ResponsiveRow]()
        self._color = Ref[Container]()

    def __on_click__(self, event: ControlEvent):
        # remove icon from current accent
        self._color.current.content = None

        # iterate over all color containers
        # updating only the clicked color container
        for index, container in enumerate(self._palette.current.controls):
            if container.key == event.control.key:
                self._palette.current.controls[index] = Container(
                    ref=self._color,
                    key=event.control.key,
                    content=Icon(
                        name=Icons.DONE,
                        color=Colors.ON_PRIMARY,
                    ),
                    bgcolor=event.control.bgcolor,
                    width=24 * 2,
                    height=24 * 2,
                    col=2,
                    shape=BoxShape.CIRCLE,
                    on_click=lambda e: self.__on_click__(event=e),
                    expand=False,
                    shadow=None,
                    ink=False,
                    tooltip=event.control.bgcolor.title(),
                )
                break
        self.page.session.set(SohposPreferences.SOHPOS_THEME, event.control.bgcolor)
        self.page.theme = Theme(
            color_scheme_seed=event.control.bgcolor, use_material3=True
        )
        self.page.dark_theme = Theme(
            color_scheme_seed=event.control.bgcolor, use_material3=True
        )
        self.page.update()

    def __generate_color_container(self, accent: str) -> Container:
        return Container(
            key=accent,
            ref=(
                self._color
                if self.page.theme.color_scheme_seed.casefold() == accent.casefold()
                else None
            ),
            content=(
                Icon(
                    name=Icons.DONE,
                    color=Colors.ON_PRIMARY,
                )
                if self.page.theme.color_scheme_seed.casefold() == accent.casefold()
                else None
            ),
            bgcolor=accent,
            width=24 * 2,
            height=24 * 2,
            col=2,
            shape=BoxShape.CIRCLE,
            on_click=lambda event: self.__on_click__(event=event),
            expand=False,
            shadow=None,
            ink=False,
            tooltip=accent.title(),
        )

    def build(self):
        self.title = Text(
            value=SohposStrings.SOHPOS_DIALOG_THEME.value.title(),
            text_align=TextAlign.CENTER,
        )
        self.content = ResponsiveRow(
            ref=self._palette,
            controls=[
                *map(lambda color: self.__generate_color_container(color), SohposColors)
            ],
        )
