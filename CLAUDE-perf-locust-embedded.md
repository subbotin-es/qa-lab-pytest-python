# CLAUDE.md — Performance / Locust (Embedded)
# File location: qa-lab-pytest-python/performance/CLAUDE.md

> **This file is the authoritative specification for Claude Code.**
> Read it completely before writing any locustfile, any config, any CI step.
> This is an augmentation of the existing Pytest + Python framework — not a standalone project.
> When in doubt — ask. Do not invent scenarios. Do not add pip packages outside this spec.

**Author:** Evgenii Subbotin
**Parent project:** qa-lab-pytest-python (Stack 2 — Cross-Stack Series)
**Performance tool:** Locust
**Target:** https://subbotin.es/QA-Lab/qa-lab.html (S3 + CloudFront)
**Language:** Python — natively consistent with the pytest ecosystem of this repo
**Version:** 1.0 | May 2026

---

## 1. What This Augmentation Does

Adds SLO compliance performance testing to the existing Pytest + Python framework.
Locust is the natural performance companion to this stack: pure Python, same venv,
same CI, same language discipline (type hints, ruff, mypy).

**Narrative for portfolio / interviews:**
> "Locust lives in the Python repo because the team that owns pytest owns Locust.
> Same language, same venv, same CI pipeline. No context switch, no extra toolchain.
> Going from portfolio-scale to production distributed load means adding
> `--master` and `--worker` flags — not migrating tools."

**Honest scope (same CDN target as k6):**
```
✅ p95 / p99 response time assertions via custom event hooks
✅ Error rate monitoring
✅ HTTP status code checks
✅ Locust HTML report as CI artifact
✅ Locust Web UI for interactive runs (local only)
❌ Capacity testing — CDN target does not degrade
❌ Degradation curves — not applicable
```

---

## 2. Absolute Rules

```
NEVER import pytest fixtures inside locustfiles — Locust and pytest are separate runtimes
NEVER use time.sleep() — use Locust's built-in wait_time
NEVER exceed 30 users in CI — respect free runner resources
NEVER add packages outside the approved list in Section 3
ALWAYS define wait_time on every User class
ALWAYS use @task decorator — never call tasks directly
ALWAYS use response.raise_for_status() inside catch block — never silently swallow errors
ALWAYS keep locustfiles in performance/locust/ — never mix with pytest tests
ALWAYS run mypy on locustfiles — same type discipline as rest of repo
ALWAYS document CDN limitation in README — no fake capacity claims
```

---

## 3. Tech Stack

| Layer | Technology | Version | Why |
|---|---|---|---|
| Load tool | Locust | 2.28+ | Pure Python, distributed, Web UI, same venv |
| Language | Python | 3.12 | Same as parent project |
| Report | Locust HTML report | built-in | `--html` flag, zero extra packages |
| CI | GitHub Actions | current | Existing pipeline — add one job |
| Type checking | mypy | same as parent | Same discipline, same config |
| Lint | ruff | same as parent | Same config |

**Add to requirements-dev.txt in parent repo:**
```
locust==2.28.0
```

No other additions.

---

## 4. Directory Structure

```
qa-lab-pytest-python/       ← existing repo root
└── performance/
    └── locust/
        ├── locustfiles/
        │   ├── slo_smoke.py        # 5 users, 30s — is the site up?
        │   ├── slo_baseline.py     # 10 users, 60s — baseline measurement
        │   └── cdn_cold_warm.py    # sequential cold/warm comparison
        ├── config.py               # shared constants, thresholds
        └── README.md
```

---

## 5. config.py — Shared Constants

```python
# performance/locust/config.py
from __future__ import annotations
import os

BASE_URL: str = os.environ.get("BASE_URL", "https://subbotin.es")
QA_LAB_PATH: str = "/QA-Lab/qa-lab.html"

# SLO thresholds (milliseconds)
P95_THRESHOLD_MS: float = 500.0
P99_THRESHOLD_MS: float = 1000.0
ERROR_RATE_THRESHOLD: float = 0.01   # 1%
```

---

## 6. Locustfiles — Exact Implementation

### slo_smoke.py
```python
# performance/locust/locustfiles/slo_smoke.py
from __future__ import annotations
from locust import HttpUser, task, constant
from performance.locust.config import QA_LAB_PATH


class QALabSmokeUser(HttpUser):
    """
    Smoke load: 5 VU, 30 seconds.
    Verifies site is responding under minimal concurrent load.
    Target: S3 + CloudFront — SLO compliance, not capacity.
    """
    wait_time = constant(1)
    host = "https://subbotin.es"

    @task
    def visit_qa_lab(self) -> None:
        with self.client.get(
            QA_LAB_PATH,
            catch_response=True,
            name="QA Lab page",
        ) as response:
            if response.status_code != 200:
                response.failure(f"Expected 200, got {response.status_code}")
            elif "QA Lab" not in response.text:
                response.failure("Page content missing 'QA Lab'")
            else:
                response.success()
```

### slo_baseline.py
```python
# performance/locust/locustfiles/slo_baseline.py
from __future__ import annotations
import random
from locust import HttpUser, task, between


PAGES: list[str] = [
    "/QA-Lab/qa-lab.html",
    "/QA-Lab/index.html",
]


class QALabBaselineUser(HttpUser):
    """
    Baseline load: 10 VU, 60 seconds with ramp.
    Establishes p95/p99 baseline for CDN-served pages.
    Run headlessly in CI: locust --headless -u 10 -r 2 -t 60s
    """
    wait_time = between(1, 2)
    host = "https://subbotin.es"

    @task
    def visit_random_page(self) -> None:
        path = random.choice(PAGES)
        with self.client.get(
            path,
            catch_response=True,
            name=path,
        ) as response:
            if response.status_code != 200:
                response.failure(f"Expected 200, got {response.status_code}")
            else:
                response.success()
```

### cdn_cold_warm.py
```python
# performance/locust/locustfiles/cdn_cold_warm.py
from __future__ import annotations
from locust import HttpUser, task, constant


class CDNColdWarmUser(HttpUser):
    """
    Sequential cold vs warm CDN hit comparison.
    Single user, no sleep between requests — measures cache behaviour.
    First request: potentially cold (CloudFront edge miss).
    Second request: warm (CloudFront edge hit).
    """
    wait_time = constant(0)
    host = "https://subbotin.es"

    @task
    def cold_then_warm(self) -> None:
        # Request 1 — cold hit label
        with self.client.get(
            "/QA-Lab/qa-lab.html",
            catch_response=True,
            name="cold_hit",
        ) as r:
            if r.status_code == 200:
                r.success()
            else:
                r.failure(f"cold hit {r.status_code}")

        # Request 2 — warm hit label
        with self.client.get(
            "/QA-Lab/qa-lab.html",
            catch_response=True,
            name="warm_hit",
        ) as r:
            if r.status_code == 200:
                r.success()
            else:
                r.failure(f"warm hit {r.status_code}")
```

---

## 7. CI Integration — Add to Existing Pipeline

Add a new job to `.github/workflows/ci.yml` in the parent repo.
Do NOT modify existing pytest jobs.

```yaml
  performance:
    name: Locust SLO Check
    runs-on: ubuntu-latest
    needs: test          # run after pytest passes
    timeout-minutes: 10

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

      - name: Run Locust smoke test (headless)
        run: |
          locust \
            -f performance/locust/locustfiles/slo_smoke.py \
            --headless \
            -u 5 -r 1 \
            -t 30s \
            --html performance/locust/smoke-report.html \
            --host https://subbotin.es \
            --exit-code-on-error 1
        env:
          BASE_URL: https://subbotin.es

      - name: Run Locust baseline test (main only)
        if: github.ref == 'refs/heads/main'
        run: |
          locust \
            -f performance/locust/locustfiles/slo_baseline.py \
            --headless \
            -u 10 -r 2 \
            -t 60s \
            --html performance/locust/baseline-report.html \
            --host https://subbotin.es \
            --exit-code-on-error 1

      - name: Upload Locust HTML reports
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: locust-reports
          path: performance/locust/*.html
          retention-days: 14
```

**Note:** `--exit-code-on-error 1` makes CI fail if any request fails — this is the quality gate.

---

## 8. Infrastructure Setup — Step by Step

### Step 1: Add Locust to requirements-dev.txt

```
# Add to requirements-dev.txt in repo root
locust==2.28.0
```

### Step 2: Install locally

```bash
# Activate existing venv
source .venv/bin/activate

pip install -r requirements-dev.txt
locust --version   # 2.28+
```

### Step 3: Create directory structure

```bash
mkdir -p performance/locust/locustfiles
```

### Step 4: Create files per Section 6

### Step 5: Type check locustfiles

```bash
# Same mypy config as rest of repo
mypy performance/locust/ --ignore-missing-imports
```

### Step 6: Run locally (interactive Web UI)

```bash
# Start Locust Web UI at http://localhost:8089
locust -f performance/locust/locustfiles/slo_smoke.py \
  --host https://subbotin.es

# Or headless
locust -f performance/locust/locustfiles/slo_smoke.py \
  --headless -u 5 -r 1 -t 30s \
  --host https://subbotin.es
```

---

## 9. Definition of Done

```
□ locust --version passes (2.28+)
□ locust==2.28.0 added to requirements-dev.txt
□ All 3 locustfiles pass mypy and ruff
□ Smoke test runs headlessly locally — exit code 0
□ performance/locust/README.md written with honest scope
□ CI job added — does not break existing pytest jobs
□ HTML report uploaded as artifact in CI
□ Commit message: perf(locust): add SLO compliance tests for QA Lab CDN
```

---

*End of CLAUDE.md*
*Version: 1.0 | Author: Evgenii Subbotin | Augmentation: Locust → qa-lab-pytest-python*
*May 2026*
