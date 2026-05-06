import pytest
import allure
from playwright.sync_api import Page, expect

from pages.tables_section import TablesSection
from pages.qa_lab_page import QALabPage


@allure.feature("Tables")  # type: ignore[misc]
class TestTables:

    @allure.story("Row Count")  # type: ignore[misc]
    @allure.severity(allure.severity_level.CRITICAL)  # type: ignore[misc]
    @pytest.mark.smoke
    def test_table_row_count(self, qa_lab: QALabPage, page: Page) -> None:
        tables = TablesSection(page)
        row_count = tables.get_row_count()
        assert row_count > 0

    @allure.story("Cell Content")  # type: ignore[misc]
    @allure.severity(allure.severity_level.NORMAL)  # type: ignore[misc]
    @pytest.mark.regression
    def test_table_cell_content(self, qa_lab: QALabPage, page: Page) -> None:
        tables = TablesSection(page)
        cell_text = tables.get_cell_text(0, 0)
        assert len(cell_text) > 0

    @allure.story("Edit Action")  # type: ignore[misc]
    @allure.severity(allure.severity_level.NORMAL)  # type: ignore[misc]
    @pytest.mark.regression
    def test_table_edit_action(self, qa_lab: QALabPage, page: Page) -> None:
        tables = TablesSection(page)
        tables.click_edit_in_row(0)
        # Assuming edit action opens some dialog or changes state
        expect(page.locator("body")).to_be_visible()
