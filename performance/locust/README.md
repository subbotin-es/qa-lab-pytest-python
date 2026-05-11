# Locust Performance Tests — QA Lab

**Parent project:** qa-lab-pytest-python (Stack 2 — Cross-Stack Series)
**Target:** https://subbotin.es/QA-Lab/qa-lab.html (S3 + CloudFront)
**Tool:** Locust 2.28+

---

## What This Tests

SLO compliance for a CDN-served static site. Not capacity testing.

```
✅ p95 / p99 response time via Locust stats
✅ HTTP 200 status verification
✅ Page content presence check ("QA Lab")
✅ Cold vs warm CDN cache hit comparison
✅ HTML report as CI artifact
❌ Capacity testing — CDN does not degrade under these loads
❌ Degradation curves — not applicable to this target
```

---

## Locustfiles

| File | VUs | Duration | Purpose |
|---|---|---|---|
| `slo_smoke.py` | 5 | 30s | Is the site up under minimal load? |
| `slo_baseline.py` | 10 | 60s | p95/p99 baseline measurement |
| `cdn_cold_warm.py` | 1 | manual | Cold vs warm CloudFront cache comparison |

---

## Run Locally

```powershell
# Activate venv
.venv\Scripts\Activate.ps1

# Interactive Web UI at http://localhost:8089
locust -f performance/locust/locustfiles/slo_smoke.py --host https://subbotin.es

# Headless smoke test
locust -f performance/locust/locustfiles/slo_smoke.py `
  --headless -u 5 -r 1 -t 30s `
  --host https://subbotin.es

# Headless baseline
locust -f performance/locust/locustfiles/slo_baseline.py `
  --headless -u 10 -r 2 -t 60s `
  --host https://subbotin.es

# CDN cold/warm comparison
locust -f performance/locust/locustfiles/cdn_cold_warm.py `
  --headless -u 1 -r 1 -t 30s `
  --host https://subbotin.es
```

---

## SLO Thresholds

Defined in `config.py`:

| Metric | Threshold |
|---|---|
| p95 response time | ≤ 500 ms |
| p99 response time | ≤ 1000 ms |
| Error rate | ≤ 1% |

---

## CI Integration

The `performance` job runs after `test` passes (see `.github/workflows/ci.yml`).
- Smoke test runs on every push
- Baseline runs on `main` only
- HTML reports uploaded as `locust-reports` artifact (14-day retention)

---

## Honest Scope Note

This target is a static site served by S3 + CloudFront. The CDN absorbs all load at
these user counts — p95/p99 will be consistently low (often < 100ms from CI runners).
The value here is **SLO compliance verification**, not capacity discovery.
Distributed load testing with `--master`/`--worker` Locust flags would be the path
to genuine capacity testing if the target were a dynamic origin server.
