from __future__ import annotations

from helpers.allure_helpers import allure_step
from playwright.sync_api import Locator, Page


class TablesSection:
    def __init__(self, page: Page) -> None:
        self._page = page
        self.rows: Locator = page.locator("table tbody tr")

    @allure_step("Get row count")
    def get_row_count(self) -> int:
        return self.rows.count()

    @allure_step("Get cell text at row {row_index}, column {column_index}")
    def get_cell_text(self, row_index: int, column_index: int) -> str:
        return self.rows.nth(row_index).locator("td").nth(column_index).inner_text()

    @allure_step("Click edit button in row {row_index}")
    def click_edit_in_row(self, row_index: int) -> None:
        self.rows.nth(row_index).get_by_role("button", name="Edit").click()
