import pytest
import allure
from playwright.sync_api import Page, expect

from data.form_data import RegistrationFormData
from pages.forms_section import FormsSection
from pages.qa_lab_page import QALabPage


@allure.feature("Forms")  # type: ignore[misc]
class TestForms:

    @allure.story("Registration")  # type: ignore[misc]
    @allure.severity(allure.severity_level.CRITICAL)  # type: ignore[misc]
    @pytest.mark.smoke
    def test_valid_form_submit(self, qa_lab: QALabPage, page: Page) -> None:
        forms = FormsSection(page)
        data = RegistrationFormData(
            full_name="John Doe",
            email="john@example.com",
            age=30,
            phone="+1234567890",
        )
        forms.fill_form(data)
        forms.submit()
        expect(forms.register_button).to_be_visible()

    @allure.story("Validation")  # type: ignore[misc]
    @allure.severity(allure.severity_level.NORMAL)  # type: ignore[misc]
    @pytest.mark.regression
    @pytest.mark.parametrize("field,value", [
        ("full_name", ""),
        ("email", "not-an-email"),
        ("age", "-1"),
    ])
    def test_form_validation(self, qa_lab: QALabPage, page: Page, field: str, value: str) -> None:
        forms = FormsSection(page)
        # parametrize demonstrates Python-idiomatic data-driven testing
        if field == "full_name":
            forms.full_name_input.fill(value)
        elif field == "email":
            forms.email_input.fill(value)
        elif field == "age":
            forms.age_input.fill(value)
        forms.submit()
        expect(forms.register_button).to_be_visible()
