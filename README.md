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

## Performance Testing (Locust)

SLO compliance tests run automatically after every pytest suite pass in CI.
Target: `https://subbotin.es` — static site served by S3 + CloudFront.

**Smoke baseline results (5 VU · 30 s · local run):**

| Metric | Result | SLO | Status |
|---|---|---|---|
| p50 | 24 ms | — | — |
| p95 | 38 ms | ≤ 500 ms | ✅ |
| p99 | 650 ms | ≤ 1000 ms | ✅ |
| Error rate | 0 % | ≤ 1 % | ✅ |

p99 spike is a CloudFront cold edge miss — warm cache requests stay consistently ≤ 40 ms.
See [Findings.md](Findings.md) for full analysis, assumptions, and limitations.

**Run performance tests locally:**

```powershell
# Smoke (headless, 5 VU, 30 s)
locust -f performance/locust/locustfiles/slo_smoke.py `
  --headless -u 5 -r 1 -t 30s --host https://subbotin.es

# Baseline (headless, 10 VU, 60 s)
locust -f performance/locust/locustfiles/slo_baseline.py `
  --headless -u 10 -r 2 -t 60s --host https://subbotin.es

# Interactive Web UI at http://localhost:8089
locust -f performance/locust/locustfiles/slo_smoke.py --host https://subbotin.es
```

**Links:**
- [Locust locustfiles](performance/locust/locustfiles/) — smoke, baseline, CDN cold/warm
- [Performance Findings](Findings.md) — approach, results, assumptions, limitations
- CI artifact: `locust-reports` — HTML reports, 14-day retention (Actions tab → run → Artifacts)

---

## Tech Stack

| Layer | Technology | Version |
|---|---|---|
| Test runner | pytest | 8.x |
| Browser automation | playwright-python | 1.44+ |
| Reporting | allure-pytest | 2.13+ |
| Parallelism | pytest-xdist | 3.x |
| Performance testing | Locust | 2.28+ |
| Type checking | mypy | 1.x |
| Linting | ruff | 0.4+ |
| CI/CD | GitHub Actions | — |
| Report hosting | GitHub Pages | — |

---

## Python vs TypeScript — Key Differences

This project is intentionally comparable to [Stack 1 (Playwright + TypeScript)](https://github.com/subbotin-es/qa-lab-playwright). Same target, different paradigm:

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
