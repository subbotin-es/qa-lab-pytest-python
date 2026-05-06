from __future__ import annotations

from helpers.allure_helpers import allure_step
from playwright.sync_api import Locator, Page


class CheckboxesSection:
    def __init__(self, page: Page) -> None:
        self._page = page
        self.agree_checkbox: Locator = page.get_by_role("checkbox", name="Agree to terms")
        self.notifications_checkbox: Locator = page.get_by_role("checkbox", name="Enable notifications")
        self.disabled_checkbox: Locator = page.get_by_role("checkbox", name="Disabled option")

    @allure_step("Check agree checkbox")
    def check_agree(self) -> None:
        self.agree_checkbox.check()

    @allure_step("Uncheck agree checkbox")
    def uncheck_agree(self) -> None:
        self.agree_checkbox.uncheck()

    @allure_step("Toggle notifications checkbox")
    def toggle_notifications(self) -> None:
        self.notifications_checkbox.click()
