# CLAUDE.md — QA Lab: Pytest + Python + Playwright + Allure

> **This file is the authoritative specification for Claude Code.**
> Read it completely before writing any test, any conftest, any fixture.
> Every architectural decision documented here has a rationale — don't override without explicit instruction.
> When in doubt — ask. Do not invent test cases. Do not mix assertion logic into page objects.

**Author:** Evgenii Subbotin
**Project:** QA Lab Cross-Stack Series — Stack 2: Pytest + Python
**Target:** https://subbotin.es/QA-Lab/qa-lab.html
**Stack:** pytest · Playwright-Python · pytest-allure · pytest-xdist · GitHub Actions · GitHub Pages
**Version:** 1.0 | April 2026

---

## 1. What This Project Does

Isolated Pytest + Python test framework targeting the QA Lab live environment.
Demonstrates Python-ecosystem automation practices: pytest fixtures with yield, conftest hierarchy, parametrize, xdist parallel execution, and Allure reports published to GitHub Pages.

**This is portfolio artefact #2 in the Cross-Stack Series:**
```
Same target (qa-lab.html) → different stacks → comparative analysis
Stack 1: Playwright + TS
Stack 2: Pytest + Python    ← this project
Stack 3: Selenium + Java + TestNG
Stack 4: Cypress + JS
Stack 5: Playwright + C# + NUnit
```

**Key differentiator from Stack 1 (Playwright TS):**
Python fixtures with `yield` vs TypeScript `base.extend` — different idiom, same principle.
`@pytest.mark.parametrize` for data-driven tests — idiomatic Python, not available in raw Playwright TS.
`pytest-xdist` parallel execution via `-n auto` — Python-native parallelism.

**Test coverage scope:**
```
Buttons          → click states, disabled state assertion
Forms            → validation, field interaction, submit
Input Fields     → text, number, date, search, URL types
Checkboxes       → check/uncheck, disabled state
Radio Buttons    → selection, mutual exclusivity
Dropdowns        → single select, multi-select
Tables           → cell content, row count, edit action
Alerts/Modals    → open, confirm, cancel, dismiss
Dynamic Visibility → checkbox-triggered panel reveal
Async Buttons    → loading → success/error state transitions
IFrames          → context switching, inner element interaction
Drag & Drop      → item reorder, drop zone validation
Slider           → value change assertion
```

---

## 2. Absolute Rules — Read Before Every Task

```
NEVER use time.sleep() — use Playwright's expect() auto-wait
NEVER hardcode URLs — always use BASE_URL from conftest.py or pytest.ini
NEVER write assertions inside Page Object methods — they return values, tests assert
NEVER use implicit waits — all waits are explicit expect() calls
NEVER commit .env files — .env.example is the template
NEVER use bare except: — always catch specific exceptions
ALWAYS run mypy --strict before pushing (or pyright) — zero type errors
ALWAYS use type hints on all function signatures
ALWAYS use conftest.py for shared fixtures — never duplicate setup in test files
ALWAYS use @allure.step on all Page Object methods
ALWAYS use pytest.mark for tagging — smoke, regression, flaky
ALWAYS use yield fixtures — not setup/teardown class methods
KEEP conftest.py files scoped — root conftest for browser, section-level for page objects
```

---

## 3. Tech Stack

| Layer | Technology | Version | Why |
|---|---|---|---|
| Test runner | pytest | 8.x | Industry standard, fixture system, plugin ecosystem |
| Browser automation | playwright-python | 1.44+ | Same Playwright engine as Stack 1 — fair comparison |
| Reporting | allure-pytest | 2.13+ | Rich HTML reports, steps, screenshots, parametrize support |
| Parallelism | pytest-xdist | 3.x | `-n auto` parallel workers, free |
| Type checking | mypy | 1.x | Strict mode — demonstrates Python type discipline |
| Linting | ruff | 0.4+ | Fast, replaces flake8 + isort + black |
| CI/CD | GitHub Actions | current | Free 2000 min/month |
| Report hosting | GitHub Pages | current | Free, automatic from Actions |

**No Selenium. No Robot Framework. No unittest.**
Budget target: $0/month (all free tiers).

---

## 4. Repository Structure

```
qa-lab-pytest-python/
├── tests/
│   ├── conftest.py                  # Root: browser, page, base_url fixtures
│   ├── test_buttons.py
│   ├── test_forms.py
│   ├── test_inputs.py
│   ├── test_checkboxes.py
│   ├── test_dropdowns.py
│   ├── test_tables.py
│   ├── test_modals.py
│   ├── test_dynamic_visibility.py
│   ├── test_async_buttons.py
│   ├── test_iframes.py
│   ├── test_drag_and_drop.py
│   └── test_slider.py
├── pages/
│   ├── __init__.py
│   ├── qa_lab_page.py              # Base page — navigation, shared locators
│   ├── buttons_section.py
│   ├── forms_section.py
│   ├── inputs_section.py
│   ├── checkboxes_section.py
│   ├── dropdowns_section.py
│   ├── tables_section.py
│   ├── modals_section.py
│   ├── dynamic_visibility_section.py
│   ├── async_buttons_section.py
│   ├── iframe_section.py
│   └── drag_drop_section.py
├── data/
│   └── form_data.py                # Test data as Python dataclasses
├── helpers/
│   └── allure_helpers.py           # @allure.step wrappers, screenshot helper
├── .github/
│   └── workflows/
│       └── ci.yml
├── pytest.ini
├── pyproject.toml                  # ruff + mypy config
├── requirements.txt
├── requirements-dev.txt
├── .env.example
└── README.md
```

---

## 5. Python Types — Define in data/form_data.py First

```python
# data/form_data.py
from dataclasses import dataclass
from typing import Literal


@dataclass
class RegistrationFormData:
    full_name: str
    email: str
    age: int
    phone: str


@dataclass
class TableRow:
    row_id: str
    name: str
    email: str
    status: Literal["Active", "Inactive"]


@dataclass
class DragItem:
    label: str
    index: int


AsyncButtonState = Literal["default", "loading", "success", "error"]
```

---

## 6. pytest.ini + pyproject.toml — Exact Configuration

```ini
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    --alluredir=allure-results
    --clean-alluredir
    -v
    --tb=short
markers =
    smoke: Core happy-path tests — run on every push
    regression: Full regression suite
    iframe: Tests requiring iframe context switching
    flaky: Known intermittent tests — always retried
```

```toml
# pyproject.toml
[tool.ruff]
line-length = 100
select = ["E", "F", "I", "N", "UP", "ANN"]
ignore = ["ANN101", "ANN102"]

[tool.mypy]
strict = true
python_version = "3.12"
ignore_missing_imports = false
```

---

## 7. conftest.py — Root Fixture File

```python
# tests/conftest.py
import os
import pytest
import allure
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright
from pages.qa_lab_page import QALabPage


BASE_URL = os.environ.get("BASE_URL", "https://subbotin.es")
QA_LAB_PATH = "/QA-Lab/qa-lab.html"


@pytest.fixture(scope="session")
def playwright_instance() -> Playwright:
    pw = sync_playwright().start()
    yield pw
    pw.stop()


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright) -> Browser:
    browser = playwright_instance.chromium.launch(headless=True)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser: Browser) -> BrowserContext:
    ctx = browser.new_context(base_url=BASE_URL)
    yield ctx
    ctx.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Page:
    p = context.new_page()
    yield p
    # Attach screenshot on failure — handled in pytest_runtest_makereport hook


@pytest.fixture(scope="function")
def qa_lab(page: Page) -> QALabPage:
    lab = QALabPage(page)
    lab.goto()
    return lab


# Screenshot on failure
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo) -> None:  # type: ignore
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        page_fixture = item.funcargs.get("page")
        if page_fixture:
            allure.attach(
                page_fixture.screenshot(),
                name="failure_screenshot",
                attachment_type=allure.attachment_type.PNG,
            )
```

---

## 8. Page Object Pattern — Exact Standard

```python
# pages/forms_section.py
from __future__ import annotations
from playwright.sync_api import Page, Locator, expect
import allure
from data.form_data import RegistrationFormData


class FormsSection:
    def __init__(self, page: Page) -> None:
        self._page = page
        self.full_name_input: Locator = page.locator('input[placeholder="Full Name"]')
        self.email_input: Locator = page.locator('input[type="email"]').first
        self.age_input: Locator = page.locator('input[type="number"]').first
        self.phone_input: Locator = page.locator('input[type="tel"]')
        self.register_button: Locator = page.get_by_role("button", name="Register")

    @allure.step("Fill registration form with: {data}")
    def fill_form(self, data: RegistrationFormData) -> None:
        self.full_name_input.fill(data.full_name)
        self.email_input.fill(data.email)
        self.age_input.fill(str(data.age))
        self.phone_input.fill(data.phone)

    @allure.step("Submit registration form")
    def submit(self) -> None:
        self.register_button.click()

    # NO assertions in page objects — return Locators, let tests assert
```

---

## 9. Test File Pattern — With Allure Annotations

```python
# tests/test_forms.py
import pytest
import allure
from playwright.sync_api import Page, expect
from pages.forms_section import FormsSection
from data.form_data import RegistrationFormData


@allure.feature("Forms")
class TestForms:

    @allure.story("Registration")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_valid_form_submit(self, qa_lab: "QALabPage", page: Page) -> None:  # noqa: F821
        forms = FormsSection(page)
        data = RegistrationFormData(
            full_name="John Doe",
            email="john@example.com",
            age=30,
            phone="+1234567890",
        )
        forms.fill_form(data)
        forms.submit()
        expect(forms.register_button).to_be_visible()

    @allure.story("Validation")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.parametrize("field,value", [
        ("full_name", ""),
        ("email", "not-an-email"),
        ("age", "-1"),
    ])
    def test_form_validation(self, page: Page, field: str, value: str) -> None:
        forms = FormsSection(page)
        # parametrize demonstrates Python-idiomatic data-driven testing
        ...
```

---

## 10. IFrame Handling

```python
# pages/iframe_section.py
from __future__ import annotations
from playwright.sync_api import Page, FrameLocator, Locator
import allure


class IFrameSection:
    def __init__(self, page: Page) -> None:
        self._page = page
        # Playwright-Python uses frame_locator() — same API as TS
        self._frame: FrameLocator = page.frame_locator("#iframes iframe")
        self.inner_heading: Locator = self._frame.locator("h1, h2, h3").first

    @allure.step("Get iframe heading text")
    def get_inner_text(self) -> str:
        return self.inner_heading.inner_text()
```

---

## 11. Parallel Execution with pytest-xdist

```bash
# Run tests in parallel — auto-detects CPU count
pytest -n auto

# Fixed worker count for CI
pytest -n 4

# Note: xdist requires function-scoped fixtures (not session-scoped browser)
# Session-scoped browser with xdist needs --dist=loadfile
pytest -n 4 --dist=loadfile
```

In CI, use `--dist=loadfile` to keep test files on the same worker — prevents browser context conflicts.

---

## 12. CI/CD Pipeline

```yaml
# .github/workflows/ci.yml
name: QA Lab — Pytest + Python + Allure

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 9 * * 1'   # Monday 09:00 UTC

jobs:
  test:
    name: Run Pytest Tests
    runs-on: ubuntu-latest
    timeout-minutes: 30

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Install Playwright browsers
        run: playwright install --with-deps chromium

      - name: Type check
        run: mypy tests/ pages/ data/ --ignore-missing-imports

      - name: Lint
        run: ruff check .

      - name: Run smoke tests
        run: pytest -m smoke -n 4 --dist=loadfile
        env:
          BASE_URL: https://subbotin.es

      - name: Run full regression
        if: github.ref == 'refs/heads/main'
        run: pytest -n 4 --dist=loadfile
        env:
          BASE_URL: https://subbotin.es

      - name: Generate Allure Report
        if: always()
        run: |
          npm install -g allure-commandline --save-dev
          allure generate allure-results --clean -o allure-report

      - name: Upload Allure artifact
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: allure-report-python
          path: allure-report/
          retention-days: 30

      - name: Deploy to GitHub Pages
        if: github.ref == 'refs/heads/main' && always()
        uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./allure-report
          destination_dir: allure
```

---

## 13. Infrastructure Setup — Step by Step

### Step 1: Python Prerequisites

```powershell
# Python 3.12 (required — install from https://python.org or via winget)
winget install Python.Python.3.12

# Verify
python --version   # 3.12.x
pip --version
```

### Step 2: Create Virtual Environment

```powershell
mkdir qa-lab-pytest-python
cd qa-lab-pytest-python

python -m venv .venv
.venv\Scripts\Activate.ps1        # PowerShell
# .venv\Scripts\activate.bat      # cmd.exe

# Verify
where python   # should point to .venv\Scripts\python.exe
```

> **Note:** If PowerShell blocks script execution, run once:
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### Step 3: requirements.txt

```
# requirements.txt — production dependencies
pytest==8.2.0
playwright==1.44.0
allure-pytest==2.13.5
pytest-xdist==3.5.0

# requirements-dev.txt — dev only
mypy==1.10.0
ruff==0.4.4
```

```powershell
pip install -r requirements.txt
pip install -r requirements-dev.txt
playwright install chromium firefox webkit
```

### Step 4: Register Accounts

**GitHub** (existing):
- Repo: `qa-lab-pytest-python` — create at https://github.com/new
- Enable GitHub Pages: Settings → Pages → Branch: `gh-pages`

No other accounts needed.

### Step 5: GitHub Repository Setup

```powershell
git init

# Create .gitignore
@"
.venv/
__pycache__/
*.pyc
.pytest_cache/
allure-results/
allure-report/
.env
.DS_Store
.mypy_cache/
.ruff_cache/
"@ | Out-File -FilePath .gitignore -Encoding utf8

git add .
git commit -m "chore: initial setup — pytest + python + allure"
git remote add origin https://github.com/YOUR_USERNAME/qa-lab-pytest-python.git
git push -u origin main
```

### Step 6: Verify Local Run

```powershell
# Smoke test against live QA Lab
pytest -m smoke -v

# Type check
mypy tests/ pages/ data/

# Lint
ruff check .

# Generate and open report (requires npm)
npm install -g allure-commandline
allure generate allure-results --clean -o allure-report
allure open allure-report
```

---

## 14. Python vs TypeScript — Key Differences (Portfolio Talking Point)

Document these in README to demonstrate stack-agnostic thinking:

| Aspect | Playwright TS (Stack 1) | Pytest Python (Stack 2) |
|---|---|---|
| Fixture system | `test.extend<Fixtures>({})` | `conftest.py` with `yield` |
| Parallelism | `fullyParallel: true` in config | `pytest-xdist -n auto` |
| Data-driven tests | Manual loop or test.each | `@pytest.mark.parametrize` |
| Type safety | Compile-time via tsc | Runtime via mypy |
| Async | Native async/await | Sync API (simpler) |
| Package manager | npm/package.json | pip/requirements.txt |
| CI install speed | `npm ci` (~30s) | `pip install` (~45s) |

---

## 15. Known Limitations & Trade-offs

| Topic | Decision | Rationale |
|---|---|---|
| Drag & Drop | Mouse event simulation | Playwright-Python drag_and_drop() handles most cases |
| IFrame cross-origin | Skipped with pytest.mark.skip | Document reason in test |
| Async browser in pytest | Using sync_api | Simpler for portfolio; async_api exists if needed |
| xdist + session scope | Using loadfile dist | Prevents fixture conflicts across workers |

---

## 16. Definition of Done — Per Task

```
□ mypy --strict passes — zero errors
□ ruff check . passes — zero warnings
□ Test has @allure.feature, @allure.story, @allure.severity
□ Test has at minimum one expect() assertion
□ Page Object method has @allure.step decorator
□ No time.sleep() anywhere in diff
□ Smoke tests pass locally before push
□ Commit message: test(section-name): describe what is tested
```

---

## 17. Day-by-Day Prompts for Claude Code

### DAY 1 PROMPT — Infrastructure

```
Read CLAUDE.md Sections 13, 6, 7 completely before starting.

Goal: Project scaffolded, zero test code.

Tasks in order:
1. Verify python --version (3.12 required)
2. Create qa-lab-pytest-python directory, create venv
3. Create requirements.txt and requirements-dev.txt (Section 13 Step 3)
4. pip install -r requirements.txt && pip install -r requirements-dev.txt
5. playwright install chromium
6. Create pytest.ini and pyproject.toml (Section 6)
7. Create directory structure: tests/ pages/ data/ helpers/
8. Create data/form_data.py (Section 5)
9. Create tests/conftest.py skeleton (Section 7)
10. Create .gitignore, initial commit, push to GitHub

After completing:
- pytest --collect-only → shows 0 tests (no test files yet, OK)
- mypy tests/ → shows no errors
- python --version → 3.12.x

Do NOT write any test files today.
```

---

### DAY 2 PROMPT — Page Objects

```
Read CLAUDE.md Sections 8, 10, 14 before starting.

Goal: All Page Objects written with type hints and allure.step.

Implement in order:
1. pages/__init__.py (empty)
2. pages/qa_lab_page.py — goto(), scroll_to_section()
3. pages/buttons_section.py
4. pages/forms_section.py — exact pattern from Section 8
5. pages/inputs_section.py
6. pages/checkboxes_section.py
7. pages/dropdowns_section.py
8. pages/tables_section.py — get_row(), get_cell_text()
9. pages/modals_section.py
10. pages/dynamic_visibility_section.py
11. pages/async_buttons_section.py
12. pages/iframe_section.py — exact pattern from Section 10
13. pages/drag_drop_section.py

After each file: mypy pages/that_file.py — fix all errors before continuing.
```

---

### DAY 3 PROMPT — Test Files

```
Read CLAUDE.md Sections 9, 15, 16 before starting.

Goal: All test files written, smoke tests pass locally.

Write tests in order:
1. tests/test_buttons.py
2. tests/test_forms.py — include @parametrize example (Section 9)
3. tests/test_inputs.py
4. tests/test_checkboxes.py
5. tests/test_dropdowns.py
6. tests/test_tables.py
7. tests/test_modals.py
8. tests/test_dynamic_visibility.py
9. tests/test_async_buttons.py
10. tests/test_iframes.py
11. tests/test_drag_and_drop.py
12. tests/test_slider.py

Run after each: pytest tests/test_that_file.py -v
All smoke tests at end: pytest -m smoke -v
```

---

### DAY 4 PROMPT — CI + README

```
Goal: CI green, Allure published, README portfolio-ready.

Tasks:
1. Create .github/workflows/ci.yml (Section 12)
2. Push, verify Actions run
3. Check Allure at GitHub Pages URL
4. Write README.md:
   - What this demonstrates
   - Live Allure Report link
   - Stack table
   - Run locally (4 commands)
   - Python vs TS comparison table (Section 14)
   - Known limitations (Section 15)
   - Cross-Stack Series links

Final checklist:
□ CI badge green
□ Allure report live
□ mypy zero errors in CI
□ ruff zero warnings in CI
```

---

## 18. Common Errors and How to Fix Them

**`ModuleNotFoundError: No module named 'playwright'`**
→ Virtual environment not activated. Run `.venv\Scripts\Activate.ps1` (PowerShell) or `.venv\Scripts\activate.bat` (cmd.exe).

**`playwright._impl._errors.TimeoutError`**
→ Element not found in time. Check locator selector against live QA Lab HTML. Increase `timeout` if page is slow.

**`mypy error: Missing return statement`**
→ Add explicit return type to function. All methods must have return annotations.

**`pytest-xdist worker crashed`**
→ Browser session conflict. Switch to `--dist=loadfile` instead of `--dist=load`.

**`allure-results is empty`**
→ `--alluredir=allure-results` must be in pytest.ini `addopts` or passed explicitly.

**`ruff: ANN001 Missing type annotation for function argument`**
→ Add type hints to all function parameters. This is enforced — do not ignore.

**`FrameLocator not found`**
→ IFrame might not be loaded. Add `page.wait_for_selector("iframe")` before `frame_locator()`.

**`time.sleep() in diff`**
→ Blocked by rule. Replace with `expect(locator).to_be_visible()` or `to_have_text()`.

**`cannot be loaded because running scripts is disabled`** (PowerShell)
→ Run once: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

---

## 19. Branching Strategy

```
main      → production (triggers CI + Allure deploy)
feat/     → new test sections
fix/      → broken test fixes
chore/    → config, dependency updates
```

Commit message format: `type(scope): description`
Examples:
- `test(forms): add parametrized validation cases`
- `fix(iframe): update frame_locator after QA Lab DOM change`
- `chore(deps): bump playwright to 1.45`

---

*End of CLAUDE.md*
*Version: 1.0 | Author: Evgenii Subbotin | Project: QA Lab Cross-Stack Series — Stack 2*
*April 2026*
