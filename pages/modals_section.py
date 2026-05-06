from __future__ import annotations

from playwright.sync_api import Locator, Page

from helpers.allure_helpers import allure_step


class ModalsSection:
    def __init__(self, page: Page) -> None:
        self._page = page
        self.open_modal_button: Locator = page.get_by_role("button", name="Open modal")
        self.confirm_button: Locator = page.get_by_role("button", name="Confirm")
        self.cancel_button: Locator = page.get_by_role("button", name="Cancel")

    @allure_step("Open modal dialog")
    def open_modal(self) -> None:
        self.open_modal_button.click()

    @allure_step("Confirm modal dialog")
    def confirm(self) -> None:
        self.confirm_button.click()

    @allure_step("Cancel modal dialog")
    def cancel(self) -> None:
        self.cancel_button.click()
