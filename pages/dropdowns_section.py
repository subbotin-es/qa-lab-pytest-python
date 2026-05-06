from __future__ import annotations

from typing import cast

from helpers.allure_helpers import allure_step
from playwright.sync_api import Locator, Page


class DropdownsSection:
    def __init__(self, page: Page) -> None:
        self._page = page
        self.single_select: Locator = page.locator('select').first
        self.multi_select: Locator = page.locator('select[multiple]')

    @allure_step("Select single option: {value}")
    def select_single_option(self, value: str) -> None:
        self.single_select.select_option(value)

    @allure_step("Select multiple options: {values}")
    def select_multiple_options(self, values: list[str]) -> None:
        self.multi_select.select_option(values)

    @allure_step("Get selected values from multi-select")
    def get_selected_values(self) -> list[str]:
        return cast(
            list[str],
            self.multi_select.evaluate(
                "el => Array.from(el.selectedOptions).map(option => option.value)"
            ),
        )
