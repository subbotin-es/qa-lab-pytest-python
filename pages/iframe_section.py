from __future__ import annotations

from helpers.allure_helpers import allure_step
from playwright.sync_api import FrameLocator, Locator, Page


class IFrameSection:
    def __init__(self, page: Page) -> None:
        self._page = page
        self._frame: FrameLocator = page.frame_locator("iframe")
        self.inner_heading: Locator = self._frame.locator("h1, h2, h3").first

    @allure_step("Get iframe inner heading text")
    def get_inner_text(self) -> str:
        return self.inner_heading.inner_text()
