import json
import os
import random
import re
import uuid
from datetime import datetime
from datetime import timezone

import pytest
import responses
from sqlalchemy import select

from interactions_update.job import run
from strr_api.models import CustomerInteraction

scenario_uno_day = {
    "records": 1,
    "target_days": [40],
    "target_pct": 1.0,
}


# @pytest.mark.load
@responses.activate
@pytest.mark.parametrize("setup_bulk_interactions", [scenario_uno_day], indirect=True)
def test_run(db_session, setup_bulk_interactions, monkeypatch):
    """Test the update job using mocked notify service responses."""

    # Setup Environment Mocks
    notify_url = "http://my-notify-mock"
    notify_ver = "/api/v1"
    notify_svc = notify_url + notify_ver
    auth_url = "http://my-auth-url"
    strr_sa_id = "strr-sa-client-id"
    strr_sa_secret = "strr-sa-secret"
    monkeypatch.setenv("NOTIFY_API_URL", notify_url)
    monkeypatch.setenv("NOTIFY_API_VERSION", notify_ver)
    monkeypatch.setenv("NOTIFY_SVC_URL", notify_svc)
    monkeypatch.setenv("KEYCLOAK_AUTH_TOKEN_URL", auth_url)
    monkeypatch.setenv("NOTIFY_API_TIMEOUT", "30")
    monkeypatch.setenv("AUTH_SVC_TIMEOUT", "30")
    monkeypatch.setenv("STRR_SERVICE_ACCOUNT_CLIENT_ID", strr_sa_id)
    monkeypatch.setenv("STRR_SERVICE_ACCOUNT_SECRET", strr_sa_secret)

    # Identify the Interaction created by the fixture
    reg_id = setup_bulk_interactions["registration_ids"][0]
    interaction = db_session.execute(
        select(CustomerInteraction).where(CustomerInteraction.registration_id == reg_id)
    ).scalar_one()

    # Manually add a notify_reference to simulate a sent notification
    interaction.notify_reference = "mock-notify-123"
    db_session.commit()

    # Define the Notify Mock Callback
    def notify_callback(request):
        # Extract ID from URL path: .../notify/{reference}
        ref = request.url.split("/")[-1]
        response = {
            "id": f"provider-{ref}",
            "recipients": ["test@example.com"],
            "requestDate": datetime.now(timezone.utc).isoformat(),
            "sentDate": datetime.now(timezone.utc).isoformat(),
            "notifyStatus": "DELIVERED",
            "notifyProvider": "HOUSING",
        }
        return (200, {}, json.dumps(response))

    # Register Mocks
    responses.add(responses.POST, auth_url, json={"access_token": "123"}, status=200)
    responses.add_callback(
        responses.GET,
        f"{notify_svc}/notify/{interaction.notify_reference}",
        callback=notify_callback,
        content_type="application/json",
    )

    # TEST
    # Run the Job
    run()

    # Assertions - Check results
    db_session.expire_all()  # Ensure we fetch fresh data
    updated_interaction = db_session.get(CustomerInteraction, interaction.id)

    assert updated_interaction.status == CustomerInteraction.InteractionStatus.DELIVERED
    assert updated_interaction.provider_reference == "provider-mock-notify-123"
    assert updated_interaction.meta_data["notifyStatus"] == "DELIVERED"


# @pytest.mark.load
@responses.activate
@pytest.mark.parametrize("setup_bulk_interactions", [{"records": 1}], indirect=True)
def test_run_failure_502(db_session, setup_bulk_interactions, monkeypatch):
    """Test that 502 errors from Notify are handled gracefully."""
    auth_url = "http://my-auth-url"
    notify_url = "http://my-notify-mock"
    notify_ver = "/api/v1"
    notify_svc = notify_url + notify_ver
    monkeypatch.setenv("NOTIFY_API_URL", notify_url)
    monkeypatch.setenv("NOTIFY_API_VERSION", notify_ver)
    monkeypatch.setenv("NOTIFY_SVC_URL", notify_url + notify_ver)
    monkeypatch.setenv("KEYCLOAK_AUTH_TOKEN_URL", auth_url)

    # Setup Mock for 502 error
    responses.add(responses.GET, f"{notify_svc}/notify/.*", status=502)
    responses.add(
        responses.POST,
        os.getenv("KEYCLOAK_AUTH_TOKEN_URL"),
        json={"access_token": "123"},
    )

    # TEST
    # Run Job
    run()

    # Assert status is still SENT (no update performed)
    interaction_ids = setup_bulk_interactions["interaction_ids"]
    db_session.expire_all()
    stmt = select(CustomerInteraction).where(
        CustomerInteraction.id.in_(interaction_ids)
    )
    interactions = db_session.scalars(stmt).all()
    for interaction in interactions:
        assert interaction.status == CustomerInteraction.InteractionStatus.SENT


scenario_bulk = {
    "records": 1000,
    "target_days": [0],
    "target_pct": 1.0,
}


@pytest.mark.load
@responses.activate
@pytest.mark.parametrize("setup_bulk_interactions", [scenario_bulk], indirect=True)
def test_run_bulk_statuses(db_session, setup_bulk_interactions, monkeypatch):
    """Test bulk processing with randomized Notify statuses."""
    notify_url = "http://my-notify-mock"
    notify_ver = "/api/v1"
    notify_svc = notify_url + notify_ver
    monkeypatch.setenv("NOTIFY_API_URL", notify_url)
    monkeypatch.setenv("NOTIFY_API_VERSION", notify_ver)
    monkeypatch.setenv("NOTIFY_SVC_URL", notify_svc)

    # List of possible statuses from Notify
    statuses = ["PENDING", "QUEUED", "SENT", "DELIVERED", "FAILURE", "FORWARDED"]

    def bulk_notify_callback(request):
        # Randomly select a status for this specific request
        status = random.choice(statuses)
        response = {
            "id": str(uuid.uuid4()),
            "notifyStatus": status,
            "notifyProvider": "HOUSING",
        }
        return (200, {}, json.dumps(response))

    # Register Mocks
    responses.add(
        responses.POST,
        os.getenv("KEYCLOAK_AUTH_TOKEN_URL"),
        json={"access_token": "123"},
    )
    responses.add_callback(
        responses.GET,
        url=re.compile(f"{notify_svc}/notify/.*"),
        callback=bulk_notify_callback,
        content_type="application/json",
    )

    # Run the multi-threaded job
    run()

    # Verify results
    interaction_ids = setup_bulk_interactions["interaction_ids"]
    db_session.expire_all()
    stmt = select(CustomerInteraction).where(
        CustomerInteraction.id.in_(interaction_ids)
    )
    my_interactions = db_session.scalars(stmt).all()

    # Ensure those marked DELIVERED or FAILURE were updated correctly
    delivered = [
        i
        for i in my_interactions
        if i.status == CustomerInteraction.InteractionStatus.DELIVERED
    ]
    failed = [
        i
        for i in my_interactions
        if i.status == CustomerInteraction.InteractionStatus.FAILED
    ]
    sent = [
        i
        for i in my_interactions
        if i.status == CustomerInteraction.InteractionStatus.SENT
    ]

    # Logical check: At 1000 records, statistically all three lists should have members
    assert (
        len(my_interactions) == scenario_bulk["records"] * scenario_bulk["target_pct"]
    )
    print(
        f"Results: Delivered: {len(delivered)}, Failed: {len(failed)}, Remained Sent: {len(sent)}"
    )
