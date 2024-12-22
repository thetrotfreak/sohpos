import flet as ft
from pydantic import ValidationError

from ..preferences import SohposPreferences
from ..sohpos import SohposBaseModel, SohposMode
from ..strings import SohposStrings
from ..topics import SohposTopics


class SohposAccountDialog(ft.AlertDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.isolated = True
        self.username = ft.Ref[ft.TextField]()
        self.password = ft.Ref[ft.TextField]()
        self.button = ft.Ref[ft.FilledButton]()

    async def on_click_sign_in(self, e: ft.ControlEvent):
        try:
            self.data = SohposBaseModel.model_validate(
                dict(
                    username=self.username.current.value,
                    password=self.password.current.value,
                    mode=SohposMode.LOGIN,
                )
            )
        except (ValueError, ValidationError):
            self.username.current.counter_text = (
                SohposStrings.SOHPOS_VALIDATION_USERNAME
            )
            self.password.current.counter_text = (
                SohposStrings.SOHPOS_VALIDATION_PASSWORD
            )
        else:
            if self.modal:
                self.modal = False
                self.open = False

            self.page.pubsub.send_all_on_topic(
                SohposTopics.SOHPOS_TOPIC_AUTHENTICATED.value,
                self.data,
            )
            self.username.current.disabled = True
            self.password.current.disabled = True
            self.button.current.text = SohposStrings.SOHPOS_SIGN_OUT.title()
            self.button.current.on_click = self.on_click_sign_out
        finally:
            self.username.current.update()
            self.password.current.update()
            self.button.current.update()
            self.update()

    async def on_click_sign_out(self, e: ft.ControlEvent):
        if all(
            (
                self.page.session.get(SohposPreferences.SOHPOS_USERNAME.value),
                self.page.session.get(SohposPreferences.SOHPOS_PASSWORD.value),
            )
        ):
            self.page.pubsub.send_all_on_topic(
                SohposTopics.SOHPOS_TOPIC_AUTHENTICATED.value,
                SohposBaseModel(
                    username=self.username.current.value,
                    password=self.password.current.value,
                    mode=SohposMode.LOGOUT,
                ),
            )

            self.username.current.value = None
            self.password.current.value = None

            self.username.current.disabled = False
            self.password.current.disabled = False

            self.button.current.text = SohposStrings.SOHPOS_SIGN_IN.title()
            self.button.current.on_click = self.on_click_sign_in

            self.username.current.update()
            self.password.current.update()
            self.button.current.update()

    def __on_change__counter_text_reset(self, e: ft.ControlEvent):
        self.username.current.counter_text = None
        self.password.current.counter_text = None
        self.username.current.update()
        self.password.current.update()

    def before_update(self):
        if all(
            (
                self.page.session.get(SohposPreferences.SOHPOS_USERNAME.value),
                self.page.session.get(SohposPreferences.SOHPOS_PASSWORD.value),
            )
        ):
            self.button.current.text = SohposStrings.SOHPOS_SIGN_OUT.title()
            self.button.current.on_click = self.on_click_sign_out
        else:
            self.button.current.text = SohposStrings.SOHPOS_SIGN_IN.title()
            self.button.current.on_click = self.on_click_sign_in

    def build(self):
        self.actions = [ft.FilledButton(ref=self.button)]
        self.title = ft.Text(
            SohposStrings.SOHPOS_APP_NAME, text_align=ft.TextAlign.CENTER
        )
        self.content = ft.Column(
            tight=True,
            controls=[
                ft.TextField(
                    ref=self.username,
                    label=ft.Icon(ft.Icons.ACCOUNT_CIRCLE),
                    autofocus=True,
                    border=ft.InputBorder.UNDERLINE,
                    value=self.page.session.get(
                        SohposPreferences.SOHPOS_USERNAME.value
                    ),
                    on_change=self.__on_change__counter_text_reset,
                    disabled=(
                        True
                        if self.page.session.get(
                            SohposPreferences.SOHPOS_USERNAME.value
                        )
                        else False
                    ),
                ),
                ft.TextField(
                    ref=self.password,
                    label=ft.Icon(ft.Icons.PASSWORD),
                    password=True,
                    can_reveal_password=True,
                    border=ft.InputBorder.UNDERLINE,
                    value=self.page.session.get(
                        SohposPreferences.SOHPOS_PASSWORD.value
                    ),
                    on_change=self.__on_change__counter_text_reset,
                    disabled=(
                        True
                        if self.page.session.get(
                            SohposPreferences.SOHPOS_PASSWORD.value
                        )
                        else False
                    ),
                ),
            ],
        )
