from functools import partial
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest


def test_process_chunk_parallelism(app, redis_client):
    """
    Verifies that process_chunk:
    1. Correctly maps process_record across the chunk.
    2. Passes the real Flask app object (to survive thread switching).
    3. Collects and returns the results.
    """
    # Setup mocks
    chunk = [{"id": 1}, {"id": 2}, {"id": 3}]
    mock_cache = MagicMock(cache=redis_client)

    def mock_return_value(record, **kwargs):
        return {"processed": record["id"]}

    record_path = "batch_permit_validator.job.process_record"

    with app.app_context():
        with patch(record_path, side_effect=mock_return_value) as mock_proc:

            from batch_permit_validator.job import process_chunk

            results = process_chunk(chunk, mock_cache, max_workers=2)

            # Assertions
            # Ensure process_record was called once for every item in the chunk
            assert len(results) == 3
            assert results == [{"processed": 1}, {"processed": 2}, {"processed": 3}]

            # Verify the calls include our mock_cache and the real app object
            assert mock_proc.call_count == 3

            # Check the first call's arguments
            args, kwargs = mock_proc.call_args_list[0]
            assert args[0] == {"id": 1}  # The record
            assert kwargs["validation_cache"] == mock_cache
            assert kwargs["app"] == app  # The unwrapped Flask app
