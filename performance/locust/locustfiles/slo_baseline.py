from __future__ import annotations

import random

from locust import HttpUser, between, task

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
