import pytest
import allure
from playwright.sync_api import Page, expect

from pages.inputs_section import InputsSection
from pages.qa_lab_page import QALabPage


@allure.feature("Inputs")  # type: ignore[misc]
class TestInputs:

    @allure.story("Text Input")  # type: ignore[misc]
    @allure.severity(allure.severity_level.CRITICAL)  # type: ignore[misc]
    @pytest.mark.smoke
    def test_text_input_fill(self, qa_lab: QALabPage, page: Page) -> None:
        inputs = InputsSection(page)
        test_value = "Hello World"
        inputs.fill_text(test_value)
        expect(inputs.text_input).to_have_value(test_value)

    @allure.story("Number Input")  # type: ignore[misc]
    @allure.severity(allure.severity_level.NORMAL)  # type: ignore[misc]
    @pytest.mark.regression
    def test_number_input_fill(self, qa_lab: QALabPage, page: Page) -> None:
        inputs = InputsSection(page)
        test_value = "42"
        inputs.fill_number(test_value)
        expect(inputs.number_input).to_have_value(test_value)

    @allure.story("Date Input")  # type: ignore[misc]
    @allure.severity(allure.severity_level.NORMAL)  # type: ignore[misc]
    @pytest.mark.regression
    def test_date_input_fill(self, qa_lab: QALabPage, page: Page) -> None:
        inputs = InputsSection(page)
        test_value = "2024-01-01"
        inputs.fill_date(test_value)
        expect(inputs.date_input).to_have_value(test_value)

    @allure.story("Search Input")  # type: ignore[misc]
    @allure.severity(allure.severity_level.NORMAL)  # type: ignore[misc]
    @pytest.mark.regression
    def test_search_input_fill(self, qa_lab: QALabPage, page: Page) -> None:
        inputs = InputsSection(page)
        test_value = "search query"
        inputs.fill_search(test_value)
        expect(inputs.search_input).to_have_value(test_value)

    @allure.story("URL Input")  # type: ignore[misc]
    @allure.severity(allure.severity_level.NORMAL)  # type: ignore[misc]
    @pytest.mark.regression
    def test_url_input_fill(self, qa_lab: QALabPage, page: Page) -> None:
        inputs = InputsSection(page)
        test_value = "https://example.com"
        inputs.fill_url(test_value)
        expect(inputs.url_input).to_have_value(test_value)
