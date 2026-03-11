from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from strr_api.models import BulkValidation
from strr_api.services import gcp_queue_publisher as real_pub


def test_process_records_in_parallel_full_flow(app, log_capture):
    """
    Verifies the orchestration logic:
    1. Chunks data correctly.
    2. Aggregates results from process_chunk.
    3. Saves response via _save_response.
    4. Publishes correct payload to the GCP Queue using a real QueueMessage object.
    """
    # Setup
    mock_request_json = {
        "control": {"callBackUrl": "https://callback.com/api/v1"},
        "data": [{"id": i} for i in range(6)],
    }
    request_key = "req_999"
    mock_presigned_url = "https://gcp.com/presigned/123"

    job_path = "batch_permit_validator.job"

    with app.app_context():
        with (
            patch(f"{job_path}.process_chunk") as mock_chunk,
            patch(f"{job_path}._save_response") as mock_save,
            patch(f"{job_path}.gcp_queue_publisher") as mock_pub,
            patch(f"{job_path}.ValidationCache") as mock_cache_class,
        ):

            mock_pub.QueueMessage = real_pub.QueueMessage

            mock_chunk.side_effect = lambda chunk, cache: [{"processed": r["id"]} for r in chunk]
            mock_save.return_value = mock_presigned_url

            from batch_permit_validator.job import process_records_in_parallel

            process_records_in_parallel(mock_request_json, request_key, chunk_size=2)

            assert mock_chunk.call_count == 3

            expected_response_json = {
                "control": mock_request_json["control"],
                "data": [{"processed": i} for i in range(6)],
            }
            mock_save.assert_called_once_with(
                response_json=expected_response_json, request_file_key=request_key
            )

            # Assertions
            mock_pub.publish_to_queue.assert_called_once()

            sent_message = mock_pub.publish_to_queue.call_args[0][0]

            assert sent_message.payload["preSignedUrl"] == mock_presigned_url
            assert sent_message.payload["callBackUrl"] == "https://callback.com/api/v1"
            assert sent_message.topic == app.config.get("BULK_VALIDATION_RESPONSE_TOPIC")
            assert sent_message.source == "batch-permit-validator"


def test_process_records_in_parallel_error_handling(app, session):
    """Verifies that if processing fails, the DB record is marked as ERROR."""
    request_key = "req_fail_123"

    rec = BulkValidation(request_file_id=request_key, status=BulkValidation.Status.PROCESSING)
    rec.save()
    session.commit()

    with app.app_context():
        # Force a crash during chunking
        with patch(
            "batch_permit_validator.job.process_chunk",
            side_effect=RuntimeError("Heavy Metal Crash"),
        ):
            from batch_permit_validator.job import process_records_in_parallel

            # This catches the exception internally and updates the DB
            process_records_in_parallel({"data": [{"id": 1}]}, request_key)
            session.commit()

    # Verify DB state in the Postgres container
    updated_rec = BulkValidation.get_record_by_request_file_id(request_key)
    assert updated_rec is not None
    assert updated_rec.status == BulkValidation.Status.ERROR
