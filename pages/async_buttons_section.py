from __future__ import annotations

from playwright.sync_api import Locator, Page

from helpers.allure_helpers import allure_step


class AsyncButtonsSection:
    def __init__(self, page: Page) -> None:
        self._page = page
        self.load_button: Locator = page.locator("#btn-async-success")
        self.error_button: Locator = page.locator("#btn-async-error")
        self.reset_button: Locator = page.locator("#btn-async-reset")
        self.status: Locator = page.locator("#async-status")

    @allure_step("Click async load button")
    def click_load(self) -> None:
        self.load_button.click()

    @allure_step("Click async error button")
    def click_error(self) -> None:
        self.error_button.click()

    @allure_step("Reset async button states")
    def click_reset(self) -> None:
        self.reset_button.click()

    @allure_step("Get async status text")
    def get_status_text(self) -> str:
        return self.status.inner_text()
