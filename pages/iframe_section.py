from __future__ import annotations

from playwright.sync_api import FrameLocator, Locator, Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from helpers.allure_helpers import allure_step


class IFrameSection:
    def __init__(self, page: Page) -> None:
        self._page = page
        self._frame: FrameLocator = page.frame_locator("iframe")
        self.inner_heading: Locator = self._frame.locator("h1, h2, h3, h4").first

    @allure_step("Get iframe inner heading text")
    def get_inner_text(self) -> str:
        try:
            return self.inner_heading.inner_text(timeout=5000)
        except PlaywrightTimeoutError:
            return ""
