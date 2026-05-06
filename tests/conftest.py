import os
from typing import Any, Generator

import allure
import pytest
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright

from pages.qa_lab_page import QALabPage

BASE_URL = os.environ.get("BASE_URL", "https://subbotin.es")
QA_LAB_PATH = "/QA-Lab/qa-lab.html"


@pytest.fixture(scope="session")
def playwright_instance() -> Generator[Playwright, None, None]:
    pw = sync_playwright().start()
    yield pw
    pw.stop()


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright) -> Generator[Browser, None, None]:
    browser = playwright_instance.chromium.launch(headless=True)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser: Browser) -> Generator[BrowserContext, None, None]:
    ctx = browser.new_context(base_url=BASE_URL)
    yield ctx
    ctx.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Generator[Page, None, None]:
    p = context.new_page()
    yield p


@pytest.fixture(scope="function")
def qa_lab(page: Page) -> QALabPage:
    lab = QALabPage(page)
    lab.goto()
    return lab


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(
    item: pytest.Item, call: pytest.CallInfo[Any]
) -> Generator[None, None, None]:
    outcome: Any = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        page_fixture = getattr(item, "funcargs", {}).get("page")
        if page_fixture:
            allure.attach(
                page_fixture.screenshot(),
                name="failure_screenshot",
                attachment_type=allure.attachment_type.PNG,
            )
