from __future__ import annotations

from helpers.allure_helpers import allure_step
from playwright.sync_api import Locator, Page


class DynamicVisibilitySection:
    def __init__(self, page: Page) -> None:
        self._page = page
        self.toggle_checkbox: Locator = page.get_by_role("checkbox", name="Show details")
        self.dynamic_panel: Locator = page.locator("#dynamic-panel")

    @allure_step("Toggle dynamic visibility checkbox")
    def toggle_panel(self) -> None:
        self.toggle_checkbox.click()

    @allure_step("Check whether dynamic panel is visible")
    def is_panel_visible(self) -> bool:
        return self.dynamic_panel.is_visible()
