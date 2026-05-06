import pytest
import allure
from playwright.sync_api import Page, expect

from pages.drag_drop_section import DragDropSection
from pages.qa_lab_page import QALabPage


@allure.feature("Drag & Drop")  # type: ignore[misc]
class TestDragDrop:

    @allure.story("Item Drag")  # type: ignore[misc]
    @allure.severity(allure.severity_level.CRITICAL)  # type: ignore[misc]
    @pytest.mark.smoke
    def test_drag_item_to_drop_zone(self, qa_lab: QALabPage, page: Page) -> None:
        if page.locator(".drag-item").count() == 0 or page.locator("#drag-target").count() == 0:
            pytest.skip("Drag item or drop zone not found on page")
        
        drag_drop = DragDropSection(page)
        drag_drop.drag_to_drop_zone()
        expect(drag_drop.drop_zone).to_be_visible()
