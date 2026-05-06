from __future__ import annotations

from playwright.sync_api import Locator, Page

from helpers.allure_helpers import allure_step


class CheckboxesSection:
    def __init__(self, page: Page) -> None:
        self._page = page
        # Look for checkboxes in main content, not navigation
        all_checkboxes = page.locator('input[type="checkbox"]:not(#nav-toggle)')
        self.agree_checkbox: Locator = all_checkboxes.first
        self.notifications_checkbox: Locator = (
            all_checkboxes.nth(1) if all_checkboxes.count() > 1
            else page.locator('input[type="checkbox"][disabled]')
        )
        self.disabled_checkbox: Locator = page.locator('input[type="checkbox"][disabled]')

    @allure_step("Check agree checkbox")
    def check_agree(self) -> None:
        self.agree_checkbox.check()

    @allure_step("Uncheck agree checkbox")
    def uncheck_agree(self) -> None:
        self.agree_checkbox.uncheck()

    @allure_step("Toggle notifications checkbox")
    def toggle_notifications(self) -> None:
        self.notifications_checkbox.click()
