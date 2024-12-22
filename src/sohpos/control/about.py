import flet as ft

from ..strings import SohposStrings


class SohposAboutDialog(ft.AlertDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def build(self):
        self.title = ft.Text(
            value=self.page.title,  # type: ignore
            text_align=ft.TextAlign.CENTER,
        )
        self.content = ft.Column(
            controls=[
                ft.Column(
                    [
                        ft.Text(
                            value=SohposStrings.SOHPOS_APP_DESCRIPTION,
                            theme_style=ft.TextThemeStyle.TITLE_LARGE,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Text(
                            value=SohposStrings.SOHPOS_COPYRIGHT,
                            theme_style=ft.TextThemeStyle.BODY_SMALL,
                        ),
                        ft.Text(
                            value=SohposStrings.SOHPOS_LICENSE,
                            theme_style=ft.TextThemeStyle.BODY_SMALL,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                ),
                ft.Divider(),
                ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.CODE,
                            url=SohposStrings.SOHPOS_URI_PROJECT,
                            tooltip=SohposStrings.SOHPOS_URI_PROJECT_TOOLTIP,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.COPYRIGHT,
                            url=SohposStrings.SOHPOS_URI_LICENSE,
                            tooltip=SohposStrings.SOHPOS_URI_LICENSE_TOOLTIP,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.BUG_REPORT,
                            url=SohposStrings.SOHPOS_URI_ISSUES,
                            tooltip=SohposStrings.SOHPOS_URI_ISSUES_TOOLTIP,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.HELP,
                            url=SohposStrings.SOHPOS_URI_WIKI,
                            tooltip=SohposStrings.SOHPOS_URI_WIKI_TOOLTIP,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            tight=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
