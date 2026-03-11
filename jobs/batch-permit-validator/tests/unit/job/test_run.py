import logging
import sys
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest


@pytest.mark.parametrize(
    "cli_args, expected_log, should_call_process",
    [
        (["job.py", "valid_file.csv"], "Processing file valid_file.csv", True),
        (["job.py"], "Empty file name.", False),
        (["job.py", ""], "Empty file name.", False),
    ],
)
def test_run_cli_scenarios(app, log_capture, cli_args, expected_log, should_call_process):
    """
    Tests the run() entry point using the structlog log_capture fixture.
    """
    process_path = "batch_permit_validator.job._process_file"

    with (
        patch.object(sys, "argv", cli_args),
        patch("batch_permit_validator.job.create_app", return_value=app),
        patch(process_path) as mock_process,
    ):

        from batch_permit_validator.job import run

        run()

        log_messages = [log.get("event") for log in log_capture]

        assert any(
            expected_log in msg for msg in log_messages if msg
        ), f"Expected '{expected_log}' to be in logs: {log_messages}"

        if should_call_process:
            mock_process.assert_called_once_with(file_name=cli_args[1])
        else:
            mock_process.assert_not_called()


def test_run_unexpected_error(app, log_capture):
    """Test that structlog and capture are working."""
    test_args = ["job.py", "some_file.csv"]

    with patch.object(sys, "argv", test_args):
        # Force create_app to explode
        with patch("batch_permit_validator.job.create_app", side_effect=Exception("DB Boom")):
            from batch_permit_validator.job import run

            run()

    assert any(
        log.get("event") == "Unexpected error occurred during job execution"
        for log in log_capture
        if log.get("log_level") == "error"
    )

    error_log = next(log for log in log_capture if log.get("log_level") == "error")
    assert error_log.get("error") == "DB Boom"

    log_summary = [(l.get("log_level"), l.get("event")) for l in log_capture]
    assert ("error", "Unexpected error occurred during job execution") in log_summary
