# QA Lab — Pytest + Python + Playwright + Allure

> **Portfolio artefact #2 — Cross-Stack QA Series**
> Same target app, different stacks — comparative analysis across automation ecosystems.

[![CI](https://github.com/subbotin-es/qa-lab-pytest-python/actions/workflows/ci.yml/badge.svg)](https://github.com/subbotin-es/qa-lab-pytest-python/actions/workflows/ci.yml)

---

## What This Demonstrates

An isolated Pytest + Python automation framework targeting the [QA Lab live environment](https://subbotin.es/QA-Lab/qa-lab.html).

**Python-ecosystem practices on display:**
- `conftest.py` with `yield` fixtures — scoped browser, context, page, and page-object fixtures
- `@pytest.mark.parametrize` — data-driven tests without boilerplate loops
- `pytest-xdist` with `--dist=loadfile` — parallel execution without fixture conflicts
- `allure-pytest` — rich HTML reports with steps, screenshots on failure, severity levels
- `mypy --strict` + `ruff` — type-safe, lint-clean Python throughout
- Page Object Model — locators and actions in page classes, assertions only in tests

**Test coverage (13 sections):**

| Section | Scenarios |
|---|---|
| Buttons | Click states, disabled state assertion |
| Forms | Valid submit, parametrized validation (3 field/value combos) |
| Input Fields | Text, number, date, search, URL types |
| Checkboxes | Check, uncheck, disabled state |
| Radio Buttons | Selection, mutual exclusivity |
| Dropdowns | Single select, multi-select |
| Tables | Row count, cell content, edit action |
| Alerts & Modals | Open, confirm, cancel |
| Dynamic Visibility | Checkbox-triggered panel reveal and hide |
| Async Button States | Loading → success transition, loading → error transition |
| IFrames | Context switching, inner element interaction |
| Drag & Drop | Item drag to target zone |
| Slider | Value change assertion |

---

## Live Allure Report

[https://subbotin-es.github.io/qa-lab-pytest-python/allure](https://subbotin-es.github.io/qa-lab-pytest-python/allure)

---

## Run Locally

```bash
# 1. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1        # Windows PowerShell
# source .venv/bin/activate        # macOS/Linux

# 2. Install dependencies + browsers
pip install -r requirements.txt -r requirements-dev.txt
playwright install chromium

# 3. Run smoke tests
pytest -m smoke -v

# 4. Run full suite in parallel
pytest -n auto --dist=loadfile
```

Generate Allure report (requires `allure` CLI):

```bash
allure generate allure-results --clean -o allure-report
allure open allure-report
```

---

## Tech Stack

| Layer | Technology | Version |
|---|---|---|
| Test runner | pytest | 8.x |
| Browser automation | playwright-python | 1.44+ |
| Reporting | allure-pytest | 2.13+ |
| Parallelism | pytest-xdist | 3.x |
| Type checking | mypy | 1.x |
| Linting | ruff | 0.4+ |
| CI/CD | GitHub Actions | — |
| Report hosting | GitHub Pages | — |

---

## Python vs TypeScript — Key Differences

This project is intentionally comparable to [Stack 1 (Playwright + TypeScript)](https://github.com/subbotin-es/qa-lab-playwright-ts). Same target, different paradigm:

| Aspect | Playwright TS (Stack 1) | Pytest Python (Stack 2) |
|---|---|---|
| Fixture system | `test.extend<Fixtures>({})` | `conftest.py` with `yield` |
| Parallelism | `fullyParallel: true` in config | `pytest-xdist -n auto` |
| Data-driven tests | Manual loop or `test.each` | `@pytest.mark.parametrize` |
| Type safety | Compile-time via `tsc` | Runtime via `mypy` |
| Async model | Native `async/await` | Sync API (simpler) |
| Package manager | npm / `package.json` | pip / `requirements.txt` |
| CI install speed | `npm ci` (~30 s) | `pip install` (~45 s) |

---

## Known Limitations

| Topic | Decision | Rationale |
|---|---|---|
| Drag & Drop | Mouse event simulation via `drag_to()` | Playwright-Python handles HTML5 drag in most cases |
| IFrame cross-origin | Skipped with `pytest.mark.skip` if cross-origin | Document reason in test |
| Async model | Using `sync_api` throughout | Simpler for portfolio; `async_api` exists if needed |
| xdist + session scope | `--dist=loadfile` | Keeps test files on same worker, preventing browser context conflicts |

---

## Cross-Stack Series

| # | Stack | Repo |
|---|---|---|
| 1 | Playwright + TypeScript | [qa-lab-playwright](https://github.com/subbotin-es/qa-lab-playwright) |
| 2 | **Pytest + Python + Allure** <-This repo | [qa-lab-pytest-python](https://github.com/subbotin-es/qa-lab-pytest-python) |
| 3 | Selenium + Java + TestNG  | [qa-lab-selenium-java](https://github.com/subbotin-es/qa-lab-selenium-java) |
| 4 | Cypress + JavaScript | [qa-lab-cypress](https://github.com/subbotin-es/qa-lab-cypress) |
| 5 | Playwright + C# + NUnit | [qa-lab-playwright-csharp](https://github.com/subbotin-es/qa-lab-playwright-csharp)  |

**Target app:** [https://subbotin.es/QA-Lab/qa-lab.html](https://subbotin.es/QA-Lab/qa-lab.html)

---

*Author: Evgenii Subbotin · April 2026*
