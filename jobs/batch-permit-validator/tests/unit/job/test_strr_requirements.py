import json
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest


@pytest.mark.parametrize(
    "unit_address, expected_address_key",
    [
        (
            {
                "unitNumber": "101",
                "streetNumber": "525",
                "streetName": "Superior St",
                "city": "Victoria",
                "province": "BC",
            },
            "101-525 Superior St, Victoria, BC",
        ),
        (
            {
                "unitNumber": None,
                "streetNumber": "123",
                "streetName": "Main St",
                "city": "Vancouver",
                "province": "BC",
            },
            "123 Main St, Vancouver, BC",
        ),
    ],
)
def test_get_strr_requirements_caching(redis_client, unit_address, expected_address_key):
    """
    Comprehensive test for caching logic:
    1. Verify address string construction.
    2. Verify cache MISS (calls ApprovalService).
    3. Verify cache HIT (returns from Redis without calling Service).
    """

    # Setup mocks and wrapper
    mock_wrapper = MagicMock()
    mock_wrapper.cache = redis_client

    mock_api_data = {"isStraaExempt": True, "other_field": "data"}
    service_path = "batch_permit_validator.job.ApprovalService"

    with patch(service_path) as mock_service:
        # --- CACHE MISS ---
        mock_service.getSTRDataForAddress.return_value = mock_api_data

        from batch_permit_validator.job import get_strr_requirements

        # Initial Call
        result = get_strr_requirements(unit_address, mock_wrapper)

        # Assertions for MISS
        assert result == {"isStraaExempt": True}
        mock_service.getSTRDataForAddress.assert_called_once_with(address=expected_address_key)

        cached_value = redis_client.get(expected_address_key)
        assert cached_value is not None
        assert json.loads(cached_value) == mock_api_data

        # --- CACHE HIT ---
        mock_service.reset_mock()

        # Second Call with same address
        result_two = get_strr_requirements(unit_address, mock_wrapper)

        # Assertions for HIT
        assert result_two == {"isStraaExempt": True}
        mock_service.getSTRDataForAddress.assert_not_called()  # Crucial: hit the cache instead!


def test_get_strr_requirements_error_handling(redis_client):
    """Tests the error path when the API returns no data."""
    unit_address = {"streetNumber": "0", "streetName": "Void", "city": "N/A", "province": "BC"}
    mock_wrapper = MagicMock(cache=redis_client)

    with patch("batch_permit_validator.job.ApprovalService") as mock_service:
        mock_service.getSTRDataForAddress.return_value = None

        from batch_permit_validator.job import get_strr_requirements

        result = get_strr_requirements(unit_address, mock_wrapper)

        # Verify error structure matches your Enum-based return
        assert "code" in result
        assert "message" in result
        # Ensure nothing was saved to Redis on failure
        assert redis_client.dbsize() == 0
