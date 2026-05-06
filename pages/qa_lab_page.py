from __future__ import annotations
from playwright.sync_api import Page


class QALabPage:
    def __init__(self, page: Page) -> None:
        self._page = page

    def goto(self) -> None:
        self._page.goto("https://subbotin.es/QA-Lab/qa-lab.html")
