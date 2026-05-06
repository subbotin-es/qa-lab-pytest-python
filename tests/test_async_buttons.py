import pytest
import allure
from playwright.sync_api import Page, expect

from pages.async_buttons_section import AsyncButtonsSection
from pages.qa_lab_page import QALabPage


@allure.feature("Async Buttons")  # type: ignore[misc]
class TestAsyncButtons:

    @allure.story("Load Button")  # type: ignore[misc]
    @allure.severity(allure.severity_level.CRITICAL)  # type: ignore[misc]
    @pytest.mark.smoke
    def test_async_load_success(self, qa_lab: QALabPage, page: Page) -> None:
        async_buttons = AsyncButtonsSection(page)
        async_buttons.click_load()
        expect(async_buttons.status).to_contain_text("Success")

    @allure.story("Error Button")  # type: ignore[misc]
    @allure.severity(allure.severity_level.NORMAL)  # type: ignore[misc]
    @pytest.mark.regression
    def test_async_load_error(self, qa_lab: QALabPage, page: Page) -> None:
        async_buttons = AsyncButtonsSection(page)
        async_buttons.click_error()
        expect(async_buttons.status).to_contain_text("Error")
