from __future__ import annotations

from helpers.allure_helpers import allure_step
from playwright.sync_api import Locator, Page


class DragDropSection:
    def __init__(self, page: Page) -> None:
        self._page = page
        self.draggable_item: Locator = page.locator(".drag-item").first
        self.drop_zone: Locator = page.locator("#drag-target")

    @allure_step("Drag item to drop zone")
    def drag_to_drop_zone(self) -> None:
        self.draggable_item.drag_to(self.drop_zone)
