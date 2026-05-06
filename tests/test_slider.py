import pytest
import allure
from playwright.sync_api import Page, expect

from pages.slider_section import SliderSection
from pages.qa_lab_page import QALabPage


@allure.feature("Slider")  # type: ignore[misc]
class TestSlider:

    @allure.story("Value Change")  # type: ignore[misc]
    @allure.severity(allure.severity_level.CRITICAL)  # type: ignore[misc]
    @pytest.mark.smoke
    def test_slider_value_change(self, qa_lab: QALabPage, page: Page) -> None:
        slider = SliderSection(page)
        test_value = "75"
        slider.set_slider_value(test_value)
        expect(slider.slider).to_have_value(test_value)
