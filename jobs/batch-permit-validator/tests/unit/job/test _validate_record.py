from unittest.mock import patch

import pytest


# Table: (record_input, expected_schema, mock_return, expected_result)
@pytest.mark.parametrize(
    "record, expected_schema, mock_return, expected_valid",
    [
        ({"identifier": "123", "data": "abc"}, "real_time_validation", [True, []], True),
        ({"address": "123 Main St"}, "rental_unit_address", [True, []], True),
        ({"identifier": "456"}, "real_time_validation", [False, ["Invalid format"]], False),
    ],
)
def test_validate_record_logic(record, expected_schema, mock_return, expected_valid):
    """Verifies that the correct schema is selected based on record content."""

    # Patch the 'validate' function where it is imported in your job module
    validate_path = "batch_permit_validator.job.validate"

    with patch(validate_path, return_value=mock_return) as mock_validate:
        from batch_permit_validator.job import _validate_record

        # Test
        valid, errors = _validate_record(record)

        # Assert the correct schema was passed to the validator
        mock_validate.assert_called_once_with(record, expected_schema)

        # Assert the function returned exactly what the validator produced
        assert valid == expected_valid
        assert errors == mock_return[1]
