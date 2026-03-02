import json
import os
import re

import pytest
import responses

from interactions_update.job import run


@pytest.mark.load
@pytest.mark.benchmark(group="worker-performance")
@responses.activate
@pytest.mark.parametrize("setup_bulk_interactions", [{"records": 100}], indirect=True)
def test_benchmark_job_performance(
    benchmark, db_session, setup_bulk_interactions, monkeypatch
):
    """Benchmark Sequential (1 worker) vs Parallel (10 workers)."""

    # Setup Mocks
    # 1. Setup Environment Mocks
    notify_url = "http://my-notify-mock"
    notify_ver = "/api/v1"
    auth_url = "http://my-auth-url"
    strr_sa_id = "strr-sa-client-id"
    strr_sa_secret = "strr-sa-secret"
    monkeypatch.setenv("NOTIFY_API_URL", notify_url)
    monkeypatch.setenv("NOTIFY_API_VERSION", notify_ver)
    monkeypatch.setenv("NOTIFY_SVC_URL", notify_url + notify_ver)
    monkeypatch.setenv("KEYCLOAK_AUTH_TOKEN_URL", auth_url)
    monkeypatch.setenv("NOTIFY_API_TIMEOUT", "30")
    monkeypatch.setenv("AUTH_SVC_TIMEOUT", "30")
    monkeypatch.setenv("STRR_SERVICE_ACCOUNT_CLIENT_ID", strr_sa_id)
    monkeypatch.setenv("STRR_SERVICE_ACCOUNT_SECRET", strr_sa_secret)
    responses.add(
        responses.POST,
        os.getenv("KEYCLOAK_AUTH_TOKEN_URL"),
        json={"access_token": "123"},
    )

    # Mock Notify with a slight artificial delay to simulate network latency
    def delayed_callback(request):
        import time

        time.sleep(0.2)  # 10ms latency
        return (200, {}, json.dumps({"notifyStatus": "DELIVERED", "id": "123"}))

    responses.add_callback(
        responses.GET,
        url=re.compile(f"{notify_url}/notify/.*"),
        callback=delayed_callback,
        content_type="application/json",
    )

    # Parametrize the benchmark to run both 1 and 10 workers
    # You can run this test twice or use the benchmark fixture inside a loop
    @benchmark
    def result():
        # Change this to 1 to test sequential, then 10 to test parallel
        run(max_workers=10)
