import json

import pytest
import responses
from sqlalchemy import select

from interactions_update.database import get_session
from interactions_update.job import run
from strr_api.enums.enum import InteractionStatus
from strr_api.models import CustomerInteraction


# @pytest.mark.load
@responses.activate
@pytest.mark.parametrize("setup_bulk_interactions", [{"records": 20}], indirect=True)
def test_full_job_roundtrip_pooled(db_session, setup_bulk_interactions, monkeypatch):
    """
    End-to-End Integration:
    Pooled DB -> Seeding -> Multi-threaded Job -> Notify Mock -> Assertions.
    """
    # Setup Environment
    notify_url = "http://my-notify-mock"
    notify_ver = "/api/v1"
    notify_svc = notify_url + notify_ver
    auth_url = "http://my-auth-url"
    client_id = "123"
    account_secret = "secret"
    monkeypatch.setenv("STRR_SERVICE_ACCOUNT_CLIENT_ID", client_id)
    monkeypatch.setenv("STRR_SERVICE_ACCOUNT_SECRET", account_secret)
    monkeypatch.setenv("NOTIFY_API_URL", notify_url)
    monkeypatch.setenv("NOTIFY_API_VERSION", notify_ver)
    monkeypatch.setenv("NOTIFY_SVC_URL", notify_svc)
    monkeypatch.setenv("KEYCLOAK_AUTH_TOKEN_URL", auth_url)
    monkeypatch.setenv("MAX_WORKERS", "5")  # Test with a specific pool size

    # Prepare Mock Data
    interaction_ids = setup_bulk_interactions["interaction_ids"]

    # Give all interactions a mock notify reference so the job picks them up
    # We use the db_session from the fixture to perform this setup
    db_session.execute(
        CustomerInteraction.__table__.update()
        .where(CustomerInteraction.id.in_(interaction_ids))
        .values(notify_reference="test-ref-xyz")
    )
    db_session.commit()

    # Setup Mock Responses for Auth and Notify
    responses.add(
        responses.POST, auth_url, json={"access_token": "mock-token"}, status=200
    )

    # Mock Notify to return 'DELIVERED' for all requests
    def notify_callback(request):
        return (
            200,
            {},
            json.dumps(
                {
                    "id": "provider-id-123",
                    "notifyStatus": "DELIVERED",
                    "notifyProvider": "GC_NOTIFY",
                }
            ),
        )

    responses.add_callback(
        responses.GET,
        url=f"{notify_svc}/notify/test-ref-xyz",
        callback=notify_callback,
        content_type="application/json",
    )

    # TEST
    # Run the Job
    run(max_workers=5)

    # Verify Results using a fresh pooled session
    session_gen = get_session()
    verify_session = next(session_gen)

    try:
        stmt = select(CustomerInteraction).where(
            CustomerInteraction.id.in_(interaction_ids)
        )
        updated_records = verify_session.scalars(stmt).all()

        assert len(updated_records) == 20
        for record in updated_records:
            assert record.status == InteractionStatus.DELIVERED
            assert record.provider_reference == "provider-id-123"
            assert record.meta_data["notifyStatus"] == "DELIVERED"

    finally:
        verify_session.close()
