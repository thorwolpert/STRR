import json
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from strr_api.models import BulkValidation


def test_save_response_and_update_db(app, session):
    """
    Verifies that _save_response:
    1. Uploads the correct JSON to GCP.
    2. Generates a presigned URL.
    3. Updates the BulkValidation record in the real DB.
    """
    # Setup
    request_key = "req_12345"
    initial_record = BulkValidation(
        request_file_id=request_key, status=BulkValidation.Status.PROCESSING
    )
    initial_record.save()
    session.commit()

    response_data = {"results": "all valid"}
    mock_file_key = "resp_98765.json"
    mock_url = "https://storage.googleapis.com/signed-url"

    gcp_service_path = "batch_permit_validator.job.GCPStorageService"

    with app.app_context():
        with patch(gcp_service_path) as mock_gcp:
            # Configure mocks
            mock_gcp.upload_file.return_value = mock_file_key
            mock_gcp.get_presigned_url.return_value = mock_url

            from batch_permit_validator.job import _save_response

            returned_url = _save_response(response_data, request_key)
            session.commit()  # Ensure the _update_bulk_validation_record changes are flushed

            # Assertions
            expected_bucket = app.config.get("BULK_VALIDATION_RESPONSE_BUCKET")
            mock_gcp.upload_file.assert_called_once_with(
                file_type="application/json",
                file_contents=json.dumps(response_data),
                bucket_id=expected_bucket,
            )

            assert returned_url == mock_url

            updated_record = BulkValidation.get_record_by_request_file_id(request_key)
            assert updated_record.status == BulkValidation.Status.COMPLETED
            assert updated_record.response_file_id == mock_file_key
            assert updated_record.response_timestamp is not None
