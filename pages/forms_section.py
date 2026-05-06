from __future__ import annotations

from playwright.sync_api import Locator, Page

from data.form_data import RegistrationFormData
from helpers.allure_helpers import allure_step


class FormsSection:
    def __init__(self, page: Page) -> None:
        self._page = page
        self.full_name_input: Locator = page.locator('input[placeholder="Full Name"]')
        self.email_input: Locator = page.locator('input[type="email"]').first
        self.age_input: Locator = page.locator('input[type="number"]').first
        self.phone_input: Locator = page.locator('input[type="tel"]')
        self.register_button: Locator = page.get_by_role("button", name="Register")

    @allure_step("Fill registration form with: {data}")
    def fill_form(self, data: RegistrationFormData) -> None:
        self.full_name_input.fill(data.full_name)
        self.email_input.fill(data.email)
        self.age_input.fill(str(data.age))
        self.phone_input.fill(data.phone)

    @allure_step("Submit registration form")
    def submit(self) -> None:
        self.register_button.click()

    @allure_step("Get registration button text")
    def get_submit_button_text(self) -> str:
        return self.register_button.inner_text()
