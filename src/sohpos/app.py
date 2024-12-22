import logging

import flet as ft
from pydantic import ValidationError

from .control import SohposAppBar, SohposStatusControl
from .preferences import (
    SohposColors,
    SohposDefaultTheme,
    SohposPreferences,
    SohposPreferencesWindow,
)
from .sohpos import (
    SohposBaseModel,
    SohposConnectionError,
    SohposError,
    SohposMode,
    SohposParseError,
    sohpos_form_action,
    sohpos_parse,
)
from .strings import SohposStrings
from .topics import SohposTopics

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SohposApplication:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = SohposStrings.SOHPOS_APP_NAME.value
        self.page.window.width = SohposPreferencesWindow.SOHPOS_WINDOW_WIDTH.value
        self.page.window.height = SohposPreferencesWindow.SOHPOS_WINDOW_HEIGHT.value
        self.page.window.title_bar_hidden = True
        self.page.window.resizable = False
        self.page.appbar = SohposAppBar()
        self.page.window.center()
        self.page.on_app_lifecycle_state_change = self.lifecycle
        self.page.pubsub.subscribe_topic(
            SohposTopics.SOHPOS_TOPIC_MODE_CHANGED.value, self.channel
        )
        self.page.pubsub.subscribe_topic(
            SohposTopics.SOHPOS_TOPIC_AUTHENTICATED.value, self.channel
        )
        self.page.update()

    async def channel(self, topic, message):
        logger.info(f"{topic=}, {message=}")
        if topic == SohposTopics.SOHPOS_TOPIC_AUTHENTICATED.value and isinstance(
            message, SohposBaseModel
        ):
            try:
                match message.mode:
                    case SohposMode.LOGIN:
                        if await self.login(message):
                            self.page.session.set(
                                SohposPreferences.SOHPOS_USERNAME.value,
                                message.username,
                            )
                            self.page.session.set(
                                SohposPreferences.SOHPOS_PASSWORD.value,
                                message.password,
                            )
                            self.page.session.set(
                                SohposPreferences.SOHPOS_MRU_MODE.value,
                                message.mode.value,
                            )
                    case SohposMode.LOGOUT:
                        if await self.logout(message):
                            # NOTE
                            # If we remove these keys,
                            # Then in lifecycle, we will not be able to
                            # delete it off the client storage
                            # cause, guess what? we will not have the keys!
                            # Let's set them to None, instead :)
                            self.page.session.set(
                                SohposPreferences.SOHPOS_USERNAME.value, None
                            )
                            self.page.session.set(
                                SohposPreferences.SOHPOS_PASSWORD.value, None
                            )
                            self.page.session.set(
                                SohposPreferences.SOHPOS_MRU_MODE.value, None
                            )
                    case _:
                        pass
            except ValidationError:
                self.dialog(SohposStrings.SOHPOS_GENERIC_VALIDATION_ERROR.value)
            except SohposError:
                self.dialog(SohposStrings.SOHPOS_GENERIC_BASE_ERROR.value)
            else:
                pass
            finally:
                self.ref_status.current.update()
        elif topic == SohposTopics.SOHPOS_TOPIC_MODE_CHANGED.value and isinstance(
            message, SohposMode
        ):
            try:
                model = SohposBaseModel(
                    username=self.page.session.get(
                        SohposPreferences.SOHPOS_USERNAME.value
                    ),
                    password=self.page.session.get(
                        SohposPreferences.SOHPOS_PASSWORD.value
                    ),
                )
                match message:
                    case SohposMode.LOGIN as mode:
                        model.mode = mode
                        if await self.login(model):
                            self.page.session.set(
                                SohposPreferences.SOHPOS_MRU_MODE.value, mode.value
                            )
                            self.ref_status.current.update()
                    case SohposMode.LOGOUT as mode:
                        if await self.logout(model):
                            self.page.session.set(
                                SohposPreferences.SOHPOS_MRU_MODE.value, mode.value
                            )
                            self.ref_status.current.update()
                    case _:
                        pass
            except ValidationError:
                self.dialog(SohposStrings.SOHPOS_GENERIC_VALIDATION_ERROR.value)
            except SohposError:
                self.dialog(SohposStrings.SOHPOS_GENERIC_BASE_ERROR.value)
            else:
                pass
            finally:
                pass
        else:
            pass

    async def lifecycle(
        self,
        e: ft.AppLifecycleStateChangeEvent,
    ):
        logger.info(e.state)
        match e.state:
            case ft.AppLifecycleState.DETACH:
                pass
            case ft.AppLifecycleState.HIDE:
                logger.info(f"{e.state} {self.page.session.get_keys()}")
                for key in self.page.session.get_keys():
                    if self.page.session.get(key) is not None:
                        logger.info(f"\tSetting key: {key}")
                        await self.page.client_storage.set_async(
                            key, self.page.session.get(key)
                        )
                    else:
                        logger.info(f"\tRemoving key: {key}")
                        await self.page.client_storage.remove_async(key)
            case ft.AppLifecycleState.INACTIVE:
                pass
            case ft.AppLifecycleState.PAUSE:
                pass
            case ft.AppLifecycleState.RESTART:
                pass
            case ft.AppLifecycleState.RESUME:
                pass
            case ft.AppLifecycleState.SHOW:
                pass
            case _:
                pass

    async def __call__(self, *args, **kwds):
        self.ref_dialog = ft.Ref[ft.AlertDialog]()
        self.ref_status = ft.Ref[SohposStatusControl]()
        logger.info(self.page.session.get_keys())
        # FIXME
        # Would using a Pydantic model make sense?
        # since, any one can put really large values for
        # the preferences in the client storage
        # any one can change the client storage
        # validaton is required
        # we need to read them once during startup
        # and make changes to the same but in session storage
        # with the flet shutdown event
        # we can flush session into client storage

        username = await self.page.client_storage.get_async(
            SohposPreferences.SOHPOS_USERNAME
        )
        password = await self.page.client_storage.get_async(
            SohposPreferences.SOHPOS_PASSWORD
        )
        mode = await self.page.client_storage.get_async(
            SohposPreferences.SOHPOS_MRU_MODE
        )
        theme = await self.page.client_storage.get_async(SohposPreferences.SOHPOS_THEME)
        theme_mode = await self.page.client_storage.get_async(
            SohposPreferences.SOHPOS_THEME_MODE
        )

        if username is not None and password is not None:
            self.page.session.set(SohposPreferences.SOHPOS_USERNAME.value, username)
            self.page.session.set(SohposPreferences.SOHPOS_PASSWORD.value, password)

        if mode in SohposMode:
            self.page.session.set(SohposPreferences.SOHPOS_MRU_MODE.value, mode)

        if theme is None:
            # NOTE
            # This is a must to be set
            # otherwise, the app will break for the
            # custom control for accent picker
            self.page.theme = SohposDefaultTheme
            self.page.dark_theme = SohposDefaultTheme
        elif theme in SohposColors:
            self.page.theme = ft.Theme(color_scheme_seed=theme)
            self.page.dark_theme = ft.Theme(color_scheme_seed=theme)
        else:
            pass

        if theme_mode is None:
            self.page.theme_mode = ft.ThemeMode.SYSTEM
        elif theme_mode in ft.ThemeMode:
            self.page.theme_mode = ft.ThemeMode(theme_mode)
            self.page.update()
        else:
            pass

        await self.build()

    def dialog(self, content: ft.Control | str):
        """
        Pop up a dialog with the given content.

        This is not a control that we need to add to :attr:`page`
        :class:`ft.Page` when :meth:`__call__()` invokes :meth:`build()`.

        Remember, :attr:`self` class is a normal class abstraction
        to act as a unified place for state management and not a
        :class:`ft.Control` itself.
        """
        ft.AlertDialog(
            ref=self.ref_dialog,
            title=ft.Text(
                value=self.page.title,
                text_align=ft.TextAlign.CENTER,
            ),
            content=ft.Text(value=content) if isinstance(content, str) else content,
            scrollable=True,
        )
        self.page.open(self.ref_dialog.current)

    async def login(self, form_model: SohposBaseModel):
        try:
            result = await sohpos_form_action(form_model)
            _ = sohpos_parse(
                result,
                username=form_model.username,
            )
        except (SohposConnectionError, SohposParseError) as e:
            raise e
        else:
            return True

    async def logout(self, form_model: SohposBaseModel):
        try:
            result = await sohpos_form_action(form_model)
            _ = sohpos_parse(result)
        except (SohposConnectionError, SohposParseError) as e:
            raise e
        else:
            return True

    async def build(self):
        self.page.add(SohposStatusControl(ref=self.ref_status))
