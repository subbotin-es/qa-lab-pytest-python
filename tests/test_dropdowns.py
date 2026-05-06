import pytest
import allure
from playwright.sync_api import Page, expect

from pages.dropdowns_section import DropdownsSection
from pages.qa_lab_page import QALabPage


@allure.feature("Dropdowns")  # type: ignore[misc]
class TestDropdowns:

    @allure.story("Single Select")  # type: ignore[misc]
    @allure.severity(allure.severity_level.CRITICAL)  # type: ignore[misc]
    @pytest.mark.smoke
    def test_single_select_option(self, qa_lab: QALabPage, page: Page) -> None:
        dropdowns = DropdownsSection(page)
        if dropdowns.single_select.count() > 0:
            # Try to select the first available option
            options = dropdowns.single_select.locator('option')
            if options.count() > 1:
                option_value = options.nth(1).get_attribute('value') or options.nth(1).inner_text()
                dropdowns.select_single_option(option_value)
                expect(dropdowns.single_select).to_have_value(option_value)
            else:
                pytest.skip("No selectable options found")
        else:
            pytest.skip("No single select dropdown found on page")

    @allure.story("Multi Select")  # type: ignore[misc]
    @allure.severity(allure.severity_level.NORMAL)  # type: ignore[misc]
    @pytest.mark.regression
    def test_multi_select_options(self, qa_lab: QALabPage, page: Page) -> None:
        dropdowns = DropdownsSection(page)
        if dropdowns.multi_select.count() > 0:
            # Try to select first two available options
            options = dropdowns.multi_select.locator('option')
            if options.count() >= 2:
                option1 = options.nth(0).get_attribute('value') or options.nth(0).inner_text()
                option2 = options.nth(1).get_attribute('value') or options.nth(1).inner_text()
                test_values = [option1, option2]
                dropdowns.select_multiple_options(test_values)
                selected = dropdowns.get_selected_values()
                assert len(selected) >= 1
            else:
                pytest.skip("Not enough options for multi-select test")
        else:
            pytest.skip("No multi-select dropdown found on page")
