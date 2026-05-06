import pytest
import allure
from playwright.sync_api import Page, expect

from pages.checkboxes_section import CheckboxesSection
from pages.qa_lab_page import QALabPage


@allure.feature("Checkboxes")  # type: ignore[misc]
class TestCheckboxes:

    @allure.story("Agree Checkbox")  # type: ignore[misc]
    @allure.severity(allure.severity_level.CRITICAL)  # type: ignore[misc]
    @pytest.mark.smoke
    def test_agree_checkbox_check(self, qa_lab: QALabPage, page: Page) -> None:
        checkboxes = CheckboxesSection(page)
        if checkboxes.agree_checkbox.count() > 0:
            checkboxes.check_agree()
            expect(checkboxes.agree_checkbox).to_be_checked()
        else:
            pytest.skip("No agree checkbox found on page")

    @allure.story("Agree Checkbox")  # type: ignore[misc]
    @allure.severity(allure.severity_level.NORMAL)  # type: ignore[misc]
    @pytest.mark.regression
    def test_agree_checkbox_uncheck(self, qa_lab: QALabPage, page: Page) -> None:
        checkboxes = CheckboxesSection(page)
        if checkboxes.agree_checkbox.count() > 0:
            checkboxes.check_agree()
            checkboxes.uncheck_agree()
            expect(checkboxes.agree_checkbox).not_to_be_checked()
        else:
            pytest.skip("No agree checkbox found on page")

    @allure.story("Notifications Checkbox")  # type: ignore[misc]
    @allure.severity(allure.severity_level.NORMAL)  # type: ignore[misc]
    @pytest.mark.regression
    def test_notifications_checkbox_toggle(self, qa_lab: QALabPage, page: Page) -> None:
        checkboxes = CheckboxesSection(page)
        if checkboxes.notifications_checkbox.count() > 0:
            checkboxes.toggle_notifications()
            expect(checkboxes.notifications_checkbox).to_be_checked()
        else:
            pytest.skip("No notifications checkbox found on page")

    @allure.story("Disabled Checkbox")  # type: ignore[misc]
    @allure.severity(allure.severity_level.NORMAL)  # type: ignore[misc]
    @pytest.mark.regression
    def test_disabled_checkbox_state(self, qa_lab: QALabPage, page: Page) -> None:
        checkboxes = CheckboxesSection(page)
        if checkboxes.disabled_checkbox.count() > 0:
            expect(checkboxes.disabled_checkbox).to_be_disabled()
        else:
            pytest.skip("No disabled checkbox found on page")
