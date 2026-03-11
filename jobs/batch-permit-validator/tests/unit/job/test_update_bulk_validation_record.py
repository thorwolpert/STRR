from datetime import datetime
from datetime import timezone
from unittest.mock import patch

import pytest
from strr_api.models import BulkValidation


def test_update_bulk_validation_record_success(session, app):
    """Verifies that the bulk validation record is updated correctly using Enums."""

    # Setup
    request_key = "test_request_123"
    initial_record = BulkValidation(
        request_file_id=request_key, status=BulkValidation.Status.NOT_PROCESSED
    )
    initial_record.save()
    session.commit()

    # Test
    from batch_permit_validator.job import _update_bulk_validation_record

    new_status = BulkValidation.Status.COMPLETED
    resp_key = "test_response_456"

    with app.app_context():
        _update_bulk_validation_record(
            request_file_key=request_key, status=new_status, response_file_key=resp_key
        )
        session.commit()

    # Assertions
    updated_record = BulkValidation.get_record_by_request_file_id(request_key)

    assert updated_record is not None
    assert updated_record.status == BulkValidation.Status.COMPLETED
    assert updated_record.response_file_id == resp_key
    assert updated_record.response_timestamp is not None


def test_update_bulk_validation_record_not_found(session, app, log_capture):
    """Ensures no error is raised if the record key is missing."""
    from batch_permit_validator.job import _update_bulk_validation_record

    # This should just exit cleanly
    _update_bulk_validation_record("non_existent_key", "COMPLETED")

    # No record was created, no error raised
    assert BulkValidation.get_record_by_request_file_id("non_existent_key") is None
