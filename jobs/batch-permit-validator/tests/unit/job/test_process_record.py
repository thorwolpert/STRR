from unittest.mock import MagicMock
from unittest.mock import patch

import pytest


@pytest.mark.parametrize(
    "record, validate_return, registration_return, str_return, expected_keys",
    [
        ({"id": 1}, [False, ["Invalid Schema"]], None, None, ["id", "errors"]),
        (
            {"id": 2, "identifier": "REG123"},
            [True, []],
            {"reg_id": "found"},
            None,
            ["id", "identifier", "validated_details"],
        ),
        (
            {"id": 3, "identifier": "MISSING"},
            [True, []],
            None,
            None,
            ["id", "identifier", "errors"],
        ),
        (
            {"id": 4, "address": {"city": "Victoria"}},
            [True, []],
            None,
            {"isStraaExempt": True},
            ["id", "address", "isStraaExempt"],
        ),
    ],
)
def test_process_record_branches(
    app, redis_client, record, validate_return, registration_return, str_return, expected_keys
):
    """Verifies all logical branches of individual record processing."""

    # Setup
    mock_cache = MagicMock(cache=redis_client)
    job_path = "batch_permit_validator.job"

    with (
        patch(f"{job_path}._validate_record", return_value=validate_return),
        patch(
            f"{job_path}.RegistrationService.find_by_registration_number",
            return_value=registration_return,
        ),
        patch(f"{job_path}.ValidationService.check_permit_details") as mock_val_svc,
        patch(f"{job_path}.get_strr_requirements", return_value=str_return),
    ):

        # Registration found case
        if registration_return:
            mock_val_svc.return_value = ({**record, "validated_details": True}, None)

        from batch_permit_validator.job import process_record

        # Test
        result = process_record(record, mock_cache, app)

        # Check
        for key in expected_keys:
            assert key in result

        if record.get("id") == 3:
            assert result["errors"][0]["code"] == "PERMIT_NOT_FOUND"
