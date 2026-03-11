import json
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest


@pytest.mark.parametrize(
    "mock_json_content",
    [
        ({"records": [{"id": 1, "data": "test"}]}),
        ({"records": []}),
    ],
)
def test_process_file_success(app, log_capture, mock_json_content):
    """Tests _process_file by mocking the GCP Storage bucket and blob."""

    file_name = "test_request.json"

    # Create a mock for the Bucket and the Blob
    mock_blob = MagicMock()
    mock_blob.download_as_text.return_value = json.dumps(mock_json_content)

    mock_bucket = MagicMock()
    mock_bucket.blob.return_value = mock_blob

    # Patch the GCPStorageService and the Parallel Processor
    service_path = "batch_permit_validator.job.GCPStorageService"
    parallel_path = "batch_permit_validator.job.process_records_in_parallel"

    with patch(service_path) as mock_storage, patch(parallel_path) as mock_parallel:

        # Setup the mock service to return our mock bucket
        mock_storage.get_bucket.return_value = mock_bucket

        from batch_permit_validator.job import _process_file

        # Run Test
        with app.app_context():
            _process_file(file_name)

        # Verify it looked for the right bucket from config
        expected_bucket = app.config.get("BULK_VALIDATION_REQUESTS_BUCKET")
        mock_storage.get_bucket.assert_called_once_with(expected_bucket)

        # Verify it downloaded the specific file
        mock_bucket.blob.assert_called_once_with(file_name)

        # Verify parallel processing was triggered with the parsed JSON
        mock_parallel.assert_called_once_with(mock_json_content, file_name)

        # Check logs
        log_events = [log.get("event") for log in log_capture]
        assert mock_json_content in log_events
