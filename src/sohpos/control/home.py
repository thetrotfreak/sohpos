import flet as ft

from ..preferences import SohposPreferences
from ..sohpos import SohposMode
from ..strings import SohposStrings
from ..topics import SohposTopics
from .account import SohposAccountDialog


class SohposStatusControl(ft.Column):
    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.ref_switch = ft.Ref[ft.Switch]()
        self.ref_text = ft.Ref[ft.Text]()

    def text_value(self) -> str:
        mode = self.page.session.get(SohposPreferences.SOHPOS_MRU_MODE.value)
        return (
            SohposStrings.SOHPOS_LOGIN_STATUS
            if mode == SohposMode.LOGIN.value
            else SohposStrings.SOHPOS_LOGOUT_STATUS
        )

    def text_color(self) -> ft.Colors:
        mode = self.page.session.get(SohposPreferences.SOHPOS_MRU_MODE.value)

        return (
            ft.Colors.PRIMARY
            if mode == SohposMode.LOGIN.value
            else ft.Colors.ON_SURFACE
        )

    def switch_value(self) -> bool:
        mode = self.page.session.get(SohposPreferences.SOHPOS_MRU_MODE.value)

        return True if mode == SohposMode.LOGIN.value else False

    async def __on_change(self, event: ft.ControlEvent):
        if not all(
            (
                self.page.session.get(SohposPreferences.SOHPOS_USERNAME.value),
                self.page.session.get(SohposPreferences.SOHPOS_PASSWORD.value),
            )
        ):
            self.page.open(SohposAccountDialog(modal=True))
        else:
            match event.control.value:
                case True | False as key:
                    self.page.pubsub.send_all_on_topic(
                        SohposTopics.SOHPOS_TOPIC_MODE_CHANGED.value,
                        event.control.data.get(key),
                    )

                    self.ref_text.current.value = self.text_value()
                    self.ref_text.current.color = self.text_color()
                    self.ref_text.current.update()
                case _:
                    pass

    def before_update(self):
        self.ref_text.current.value = self.text_value()
        self.ref_text.current.color = self.text_color()

    def build(self):
        self.expand = True
        self.expand_loose = True
        self.alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.controls = [
            ft.Row(
                controls=[
                    ft.Switch(
                        ref=self.ref_switch,
                        data={
                            True: SohposMode.LOGIN,
                            False: SohposMode.LOGOUT,
                        },
                        on_change=self.__on_change,
                        scale=2,
                        value=self.switch_value(),
                    )
                ],
                expand=1,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                controls=[
                    ft.Text(
                        ref=self.ref_text,
                        value=self.text_value(),
                        theme_style=ft.TextThemeStyle.HEADLINE_LARGE,
                        text_align=ft.TextAlign.CENTER,
                        color=self.text_color(),
                    )
                ],
                expand=1,
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
        ]
