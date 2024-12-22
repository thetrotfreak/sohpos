import flet as ft

from sohpos import SohposApplication


async def main(page: ft.Page):
    app = SohposApplication(page)
    await app()


ft.app(main)
