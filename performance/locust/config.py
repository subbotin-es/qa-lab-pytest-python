from __future__ import annotations

import os

BASE_URL: str = os.environ.get("BASE_URL", "https://subbotin.es")
QA_LAB_PATH: str = "/QA-Lab/qa-lab.html"

# SLO thresholds (milliseconds)
P95_THRESHOLD_MS: float = 500.0
P99_THRESHOLD_MS: float = 1000.0
ERROR_RATE_THRESHOLD: float = 0.01   # 1%
