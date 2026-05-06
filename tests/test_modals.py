import allure
import pytest
from playwright.sync_api import Page, expect

from pages.modals_section import ModalsSection
from pages.qa_lab_page import QALabPage


@allure.feature("Modals")
class TestModals:

    @allure.story("Open Modal")  # type: ignore[misc]
    @allure.severity(allure.severity_level.CRITICAL)  # type: ignore[misc]
    @pytest.mark.smoke
    def test_open_modal(self, qa_lab: QALabPage, page: Page) -> None:
        modals = ModalsSection(page)
        modals.open_modal()
        expect(modals.confirm_button).to_be_visible()

    @allure.story("Confirm Modal")  # type: ignore[misc]
    @allure.severity(allure.severity_level.NORMAL)  # type: ignore[misc]
    @pytest.mark.regression
    def test_confirm_modal(self, qa_lab: QALabPage, page: Page) -> None:
        modals = ModalsSection(page)
        modals.open_modal()
        modals.confirm()
        # Confirm does not close the modal in this QA Lab — modal remains open
        expect(modals.confirm_button).to_be_visible()

    @allure.story("Cancel Modal")  # type: ignore[misc]
    @allure.severity(allure.severity_level.NORMAL)  # type: ignore[misc]
    @pytest.mark.regression
    def test_cancel_modal(self, qa_lab: QALabPage, page: Page) -> None:
        modals = ModalsSection(page)
        modals.open_modal()
        modals.cancel()
        expect(modals.confirm_button).not_to_be_visible()
