import allure
import pytest
from playwright.sync_api import Page, expect

from pages.buttons_section import ButtonsSection
from pages.qa_lab_page import QALabPage


@allure.feature("Buttons")
class TestButtons:

    @allure.story("Primary Button")  # type: ignore[misc]
    @allure.severity(allure.severity_level.CRITICAL)  # type: ignore[misc]
    @pytest.mark.smoke
    def test_primary_button_click(self, qa_lab: QALabPage, page: Page) -> None:
        buttons = ButtonsSection(page)
        buttons.click_primary()
        expect(buttons.primary_button).to_be_visible()

    @allure.story("Secondary Button")  # type: ignore[misc]
    @allure.severity(allure.severity_level.NORMAL)  # type: ignore[misc]
    @pytest.mark.regression
    def test_secondary_button_click(self, qa_lab: QALabPage, page: Page) -> None:
        buttons = ButtonsSection(page)
        buttons.click_secondary()
        expect(buttons.secondary_button).to_be_visible()

    @allure.story("Disabled Button")  # type: ignore[misc]
    @allure.severity(allure.severity_level.NORMAL)  # type: ignore[misc]
    @pytest.mark.regression
    def test_disabled_button_state(self, qa_lab: QALabPage, page: Page) -> None:
        buttons = ButtonsSection(page)
        expect(buttons.disabled_button).to_be_disabled()
