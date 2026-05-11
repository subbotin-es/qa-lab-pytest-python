# Performance Testing Findings — QA Lab (Locust)

**Project:** qa-lab-pytest-python — Cross-Stack Series, Stack 2
**Target:** https://subbotin.es/QA-Lab/qa-lab.html
**Infrastructure:** AWS S3 (origin) + CloudFront (CDN)
**Tool:** Locust 2.28 (embedded in the pytest repo, same venv)
**Date:** May 2026

---

## Why Locust in This Repo

Locust is Python-native. It lives in the same virtual environment as pytest and shares
the same language discipline — type hints, ruff, mypy. No extra toolchain, no context
switch. The team that owns the functional tests owns the performance tests.

This is the meaningful difference from k6 (JavaScript DSL) or JMeter (XML config +
Java runtime): with Locust, the performance suite is just more Python code that follows
the same review and quality gates as everything else.

---

## What Was Tested

Three scenarios, each targeting a different question:

| Locustfile | VUs | Duration | Question |
|---|---|---|---|
| `slo_smoke.py` | 5 | 30 s | Is the site up and responding correctly under minimal concurrent load? |
| `slo_baseline.py` | 10 | 60 s | What are the p95/p99 latency baselines across multiple CDN-served pages? |
| `cdn_cold_warm.py` | 1 | manual | What is the latency delta between a cold CDN edge miss and a warm cache hit? |

`slo_smoke.py` also validates page content — it asserts `"QA Lab"` appears in the
response body, not just that HTTP 200 was returned. This catches a silent failure mode
where the CDN returns a stale error page with a 200 status.

---

## Results

### Smoke Run (5 VU · 30 s · local)

```
Requests:    120
Failures:    0 (0.00%)
Req/s:       4.5

Response time percentiles:
  p50   24 ms
  p75   26 ms
  p90   36 ms
  p95   38 ms
  p98   640 ms
  p99   650 ms
  max   880 ms
```

### SLO Assessment

| SLO | Threshold | Result | Status |
|---|---|---|---|
| p95 response time | ≤ 500 ms | 38 ms | ✅ Pass — 13× headroom |
| p99 response time | ≤ 1000 ms | 650 ms | ✅ Pass |
| Error rate | ≤ 1 % | 0 % | ✅ Pass |

### p99 Spike Explained

p99 = 650 ms against a background p95 of 38 ms is not noise — it is a cold CloudFront
edge miss. The first request to an edge node that has not cached the asset must fetch
from the S3 origin in a different region. Subsequent requests to the same edge node
(cache hits) return in 20–40 ms. The `cdn_cold_warm.py` scenario isolates this:
two sequential requests to the same path, labelled `cold_hit` and `warm_hit`, produce
a visible latency gap in the Locust HTML report.

---

## Approach

### Embedded, Not Standalone

Locust runs as a job in the existing GitHub Actions pipeline (`needs: test`), using
the same `requirements-dev.txt` and the same `pip install` step. There is no separate
performance repo, no separate Docker image, no separate CI project.

### Headless CI, Interactive Locally

In CI: `--headless` with fixed VU counts and a time limit. Exit code 1 on any
request failure — this is the quality gate.

Locally: the same locustfiles can be run with the Web UI (`locust -f ... --host ...`)
for interactive exploration, real-time graphs, and manual ramp control without any
code changes.

### Content Validation, Not Just Status Codes

`slo_smoke.py` uses `catch_response=True` and checks both HTTP status and response
body. A CDN misconfiguration that serves a cached error page with HTTP 200 would pass
a status-code-only check but fail here. This is a deliberate design choice.

### CI Scope Limit

Maximum 30 VUs in CI (per project rules) to respect shared runner resources. This is
not a capacity constraint — the CDN can serve far more — it is a resource hygiene rule.

---

## Assumptions

1. **CloudFront absorbs all load at these user counts.** 5–10 concurrent users is
   negligible for a CDN. Response times at 10 VU will be statistically identical to
   response times at 1 VU. We are not observing the origin server under any meaningful
   load.

2. **Geographic proximity matters.** Results depend on which CloudFront edge node the
   runner (or local machine) resolves to. A GitHub Actions runner in US-East will hit a
   different edge than a developer in Europe. Numbers are representative, not universal.

3. **The p99 spike is structural, not intermittent.** It appears consistently in every
   run because the CDN cold-miss pattern is deterministic: the first request in any new
   session to an edge that has not recently served the asset will be a miss. At 5 VU
   the spike affects ~1–2 requests out of 120, landing in the p99 band.

4. **HTTP response ≠ browser render time.** Locust measures raw HTTP response time for
   the HTML document. It does not measure time-to-interactive, JavaScript execution, or
   asset loading. For a static HTML page this is acceptable; for a JS-heavy SPA it
   would not be.

5. **No authentication, no session state.** All requests are anonymous GETs. Any
   authenticated or stateful paths are out of scope.

---

## Limitations

### Not Capacity Testing

The CDN does not degrade at 5–10 VU. You cannot derive a saturation point, a breaking
point, or a throughput ceiling from these results. To find those numbers you would
need to target the S3 origin directly (bypassing CloudFront), which requires AWS-level
access. That is out of scope for this portfolio target.

### No SLO Assertion in Code

Locust 2.28 does not have a built-in threshold assertion that fails the process when
p95 exceeds a threshold (unlike k6's `thresholds`). The current quality gate is binary:
any failed request → exit code 1. A p95 regression from 38 ms to 490 ms would pass CI
silently as long as no request returns a non-200 status. Fixing this would require
a Locust `test_stop` event hook that reads `self.environment.stats` and calls
`self.environment.process_exit_code = 1` on threshold breach.

### Greenlet Version Conflict

Locust 2.28 requires `greenlet ≥ 3.5`; playwright 1.44 requires `greenlet == 3.0.3`.
Both are installed in the same venv, with locust's version winning. In practice this
does not cause failures because pytest and locust are invoked as separate processes in
separate CI jobs, but it is a latent risk if they are ever called from the same Python
process.

### No Distributed Load

`--master` / `--worker` Locust mode is not configured. All load originates from a
single process on a single machine. For the current CDN target this is sufficient.
For a dynamic origin that requires real concurrency at scale, distributed mode would
be the next step.

### HTML Report Only

The Locust HTML report is uploaded as a CI artifact (14-day retention). There is no
trend tracking, no historical comparison, and no alert on regression. A proper
performance monitoring setup would push stats to a time-series database (InfluxDB,
Prometheus) and alert on percentile regressions over time.

---

## What Real Capacity Testing Would Require

For this target (static CDN), real capacity testing is not meaningful without bypassing
the cache. For a different origin type, here is what would change:

| Concern | Current Setup | Production-Ready |
|---|---|---|
| Scale | 10 VU, single process | 100–10,000 VU, `--master` + `--workers` |
| Threshold assertion | Binary (any failure) | p95/p99 checked in `test_stop` hook |
| Trend tracking | None | InfluxDB + Grafana or Locust Cloud |
| Target | CDN-cached static files | Dynamic origin, authenticated flows |
| Duration | 30–60 s | 10–60 min soak tests |
| Ramp strategy | Linear `-r` flag | Custom shapes via `LoadTestShape` |

---

## Useful Links

| Resource | URL |
|---|---|
| Live target | https://subbotin.es/QA-Lab/qa-lab.html |
| CI pipeline | https://github.com/subbotin-es/qa-lab-pytest-python/actions |
| Locust docs | https://docs.locust.io/en/stable/ |
| Locust `catch_response` | https://docs.locust.io/en/stable/api.html#locust.clients.HttpSession.get |
| CloudFront cache behaviour | https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/HowCloudFrontWorks.html |
| Locust distributed mode | https://docs.locust.io/en/stable/running-distributed.html |
| Locust event hooks (for threshold assertions) | https://docs.locust.io/en/stable/extending-locust.html |

---

*Author: Evgenii Subbotin · May 2026*
