from __future__ import annotations

from locust import HttpUser, constant, task

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
