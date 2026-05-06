from __future__ import annotations

from helpers.allure_helpers import allure_step
from playwright.sync_api import Locator, Page


class SliderSection:
    def __init__(self, page: Page) -> None:
        self._page = page
        self.slider: Locator = page.locator('input[type="range"]')

    @allure_step("Set slider value to {value}")
    def set_slider_value(self, value: str) -> None:
        self.slider.fill(value)

    @allure_step("Get current slider value")
    def get_slider_value(self) -> str:
        return self.slider.input_value()
