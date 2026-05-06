from __future__ import annotations

from playwright.sync_api import Locator, Page

from helpers.allure_helpers import allure_step


class ButtonsSection:
    def __init__(self, page: Page) -> None:
        self._page = page
        self.primary_button: Locator = page.get_by_role("button", name="Primary")
        self.secondary_button: Locator = page.get_by_role("button", name="Secondary")
        self.disabled_button: Locator = page.get_by_role("button", name="Disabled")

    @allure_step("Click primary button")
    def click_primary(self) -> None:
        self.primary_button.click()

    @allure_step("Click secondary button")
    def click_secondary(self) -> None:
        self.secondary_button.click()

    @allure_step("Attempt to click disabled button")
    def click_disabled(self) -> None:
        self.disabled_button.click()
