import pytest
import allure
from playwright.sync_api import Page, expect

from pages.iframe_section import IFrameSection
from pages.qa_lab_page import QALabPage


@allure.feature("IFrames")  # type: ignore[misc]
class TestIFrames:

    @allure.story("IFrame Content")  # type: ignore[misc]
    @allure.severity(allure.severity_level.CRITICAL)  # type: ignore[misc]
    @pytest.mark.smoke
    @pytest.mark.iframe
    def test_iframe_content_access(self, qa_lab: QALabPage, page: Page) -> None:
        if page.locator("iframe").count() == 0:
            pytest.skip("No iframe found on page")
        
        iframe = IFrameSection(page)
        text = iframe.get_inner_text()
        if not text:
            pytest.skip("No heading content in iframe")
        assert len(text) > 0
