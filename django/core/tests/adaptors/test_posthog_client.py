"""
Unit tests for the PostHog adaptor
"""

import pytest
from core import factories
import responses
from rest_framework import status
from freezegun import freeze_time

pytestmark = pytest.mark.django_db


@responses.activate
@freeze_time("2025-10-19")
def test_posthog_monthly_active_users(settings):
    """Test fetching monthly active users from PostHog."""
    adaptor = factories.AdaptorFactory.create(
        product=factories.ProductFactory(
            nom_service_public_numerique="visio",
        ),
        source_url="https://eu.posthog.com/api/projects/44954/insights/65340",
        indicator="monthly active users",
        client="PostHogClient",
    )

    # # Create a test adaptor with project_id
    # class TestVisioClient(PostHogClient):
    #     slug = "visio"
    #     indicators = [
    #         {
    #             "name": "utilisateurs actifs mensuels",
    #             "frequency": "mensuelle",
    #             "project_id": "44954",
    #             "insight_id": "65340",
    #         }
    #     ]

    # Mock PostHog API response
    mock_response = {
        "id": 65340,
        "name": "Monthly Active Users",
        "result": [
            {
                "data": [5728, 3985, 8458, 7533],
                "days": ["2025-07-01", "2025-08-01", "2025-09-01", "2025-10-01"],
            }
        ],
    }

    responses.get(
        "https://eu.posthog.com/api/projects/44954/insights/65340",
        json=mock_response,
        status=status.HTTP_200_OK,
        content_type="application/json",
    )

    # Verify the latest data point was returned
    assert adaptor.get_data() == 8458


@responses.activate
def test_posthog_no_data_error(settings):
    """Test error handling when PostHog returns no data."""

    adaptor = factories.AdaptorFactory.create(
        product=factories.ProductFactory(
            nom_service_public_numerique="visio",
        ),
        source_url="https://eu.posthog.com/api/projects/0/insights/broken-insight",
        indicator="monthly active users",
        client="PostHogClient",
    )

    # Mock empty response
    mock_response = {"result": [{"data": [], "days": []}]}

    responses.get(
        "https://eu.posthog.com/api/projects/0/insights/broken-insight",
        json=mock_response,
        status=status.HTTP_200_OK,
    )

    # Should raise ValueError when no data is available
    with pytest.raises(KeyError, match="This insight has no data."):
        adaptor.get_data()
