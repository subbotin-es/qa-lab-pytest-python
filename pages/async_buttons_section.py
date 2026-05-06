from __future__ import annotations

from helpers.allure_helpers import allure_step
from playwright.sync_api import Locator, Page


class AsyncButtonsSection:
    def __init__(self, page: Page) -> None:
        self._page = page
        self.load_button: Locator = page.get_by_role("button", name="Load data")
        self.success_message: Locator = page.locator("text=Success")
        self.error_message: Locator = page.locator("text=Error")

    @allure_step("Click async load button")
    def click_load(self) -> None:
        self.load_button.click()

    @allure_step("Get async success text")
    def get_success_text(self) -> str:
        return self.success_message.inner_text()

    @allure_step("Get async error text")
    def get_error_text(self) -> str:
        return self.error_message.inner_text()
