from __future__ import annotations

from playwright.sync_api import Locator, Page

from helpers.allure_helpers import allure_step


class InputsSection:
    def __init__(self, page: Page) -> None:
        self._page = page
        self.text_input: Locator = page.locator('input[placeholder="Enter text"]')
        self.number_input: Locator = page.locator('input[type="number"]').nth(1)
        self.date_input: Locator = page.locator('input[type="date"]')
        self.search_input: Locator = page.locator('input[type="search"]')
        self.url_input: Locator = page.locator('input[type="url"]')

    @allure_step("Fill text input with: {value}")
    def fill_text(self, value: str) -> None:
        self.text_input.fill(value)

    @allure_step("Fill number input with: {value}")
    def fill_number(self, value: str) -> None:
        self.number_input.fill(value)

    @allure_step("Fill date input with: {value}")
    def fill_date(self, value: str) -> None:
        self.date_input.fill(value)

    @allure_step("Fill search input with: {value}")
    def fill_search(self, value: str) -> None:
        self.search_input.fill(value)

    @allure_step("Fill URL input with: {value}")
    def fill_url(self, value: str) -> None:
        self.url_input.fill(value)

    @allure_step("Get text input value")
    def get_text_value(self) -> str:
        return self.text_input.input_value()
