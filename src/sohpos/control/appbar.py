from flet import AppBar, Colors, IconButton, Icons, Text, WindowDragArea

from ..strings import SohposStrings
from .menu import SohposMenuButton


class SohposAppBar(AppBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def build(self):
        self.bgcolor = Colors.PRIMARY_CONTAINER
        self.title = Text(
            value=self.page.title or SohposStrings.SOHPOS_APP_NAME,
        )
        self.actions = [
            WindowDragArea(
                maximizable=False, content=IconButton(icon=Icons.DRAG_INDICATOR)
            ),
            SohposMenuButton(),
        ]
