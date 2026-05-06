import pytest
import allure
from playwright.sync_api import Page, expect

from pages.dynamic_visibility_section import DynamicVisibilitySection
from pages.qa_lab_page import QALabPage


@allure.feature("Dynamic Visibility")  # type: ignore[misc]
class TestDynamicVisibility:

    @allure.story("Panel Toggle")  # type: ignore[misc]
    @allure.severity(allure.severity_level.CRITICAL)  # type: ignore[misc]
    @pytest.mark.smoke
    def test_panel_toggle_show(self, qa_lab: QALabPage, page: Page) -> None:
        dynamic = DynamicVisibilitySection(page)
        if dynamic.toggle_checkbox.count() > 0 and dynamic.dynamic_panel.count() > 0:
            dynamic.toggle_panel()
            expect(dynamic.dynamic_panel).to_be_visible()
        else:
            pytest.skip("Dynamic visibility elements not found on page")

    @allure.story("Panel Toggle")  # type: ignore[misc]
    @allure.severity(allure.severity_level.NORMAL)  # type: ignore[misc]
    @pytest.mark.regression
    def test_panel_toggle_hide(self, qa_lab: QALabPage, page: Page) -> None:
        dynamic = DynamicVisibilitySection(page)
        if dynamic.toggle_checkbox.count() > 0 and dynamic.dynamic_panel.count() > 0:
            dynamic.toggle_panel()
            dynamic.toggle_panel()
            expect(dynamic.dynamic_panel).not_to_be_visible()
        else:
            pytest.skip("Dynamic visibility elements not found on page")
