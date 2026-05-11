from __future__ import annotations

from locust import HttpUser, constant, task


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
