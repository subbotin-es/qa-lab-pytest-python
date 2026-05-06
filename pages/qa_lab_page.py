from __future__ import annotations
from playwright.sync_api import Page


class QALabPage:
    def __init__(self, page: Page) -> None:
        self._page = page

    def goto(self) -> None:
        self._page.goto("https://subbotin.es/QA-Lab/qa-lab.html")

    def scroll_to_section(self, section_title: str) -> None:
        section_heading = self._page.get_by_role("heading", name=section_title)
        section_heading.scroll_into_view_if_needed()
