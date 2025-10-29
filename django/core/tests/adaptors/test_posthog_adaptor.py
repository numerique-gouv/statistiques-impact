"""
Unit tests for the PostHog adaptor
"""

import pytest
from core.adaptors import posthog
from core import factories
import responses
from rest_framework import status
from freezegun import freeze_time

pytestmark = pytest.mark.django_db


@responses.activate
@freeze_time("2025-10-19")
def test_posthog_monthly_active_users(settings):
    """Test fetching monthly active users from PostHog."""

    factories.ProductFactory(nom_service_public_numerique="visio")

    # Create a test adaptor with project_id
    class TestVisioAdaptor(posthog.PostHogAdaptor):
        slug = "visio"
        indicators = [
            {
                "name": "utilisateurs actifs mensuels",
                "frequency": "mensuelle",
                "project_id": "44954",
                "insight_id": "65340",
            }
        ]

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

    adaptor = TestVisioAdaptor()
    results = adaptor.get_last_month_data()

    # Verify the latest data point was returned
    assert len(results) == 1
    assert results[0]["name"] == "utilisateurs actifs mensuels"
    assert results[0]["frequency"] == "mensuelle"
    assert results[0]["value"] == 7533


@responses.activate
def test_posthog_multiple_indicators(settings):
    """Test fetching multiple indicators from PostHog."""
    factories.ProductFactory(nom_service_public_numerique="test-product")


    # Create a custom adaptor with multiple indicators
    class TestMultipleAdaptor(posthog.PostHogAdaptor):
        slug = "test-product"
        indicators = [
            {
                "name": "utilisateurs actifs",
                "frequency": "mensuelle",
                "project_id": "44954",
                "insight_id": "111",
            },
            {
                "name": "pages vues",
                "frequency": "mensuelle",
                "project_id": "44954",
                "insight_id": "222",
            },
        ]

    # Mock responses for both insights
    mock_response_1 = {
        "result": [
            {
                "data": [100, 200],
                "days": ["2025-09-01", "2025-10-01"],
            }
        ]
    }
    mock_response_2 = {
        "result": [
            {
                "data": [1000, 2000],
                "days": ["2025-09-01", "2025-10-01"],
            }
        ]
    }

    responses.get(
        "https://eu.posthog.com/api/projects/44954/insights/111",
        json=mock_response_1,
        status=status.HTTP_200_OK,
    )
    responses.get(
        "https://eu.posthog.com/api/projects/44954/insights/222",
        json=mock_response_2,
        status=status.HTTP_200_OK,
    )

    adaptor = TestMultipleAdaptor()
    results = adaptor.get_last_month_data()

    # Verify two indicators were returned with values
    assert len(results) == 2
    
    # Verify values
    assert results[0]["name"] == "utilisateurs actifs"
    assert results[0]["value"] == 200
    
    assert results[1]["name"] == "pages vues"
    assert results[1]["value"] == 2000


@responses.activate
def test_posthog_no_data_error(settings):
    """Test error handling when PostHog returns no data."""

    factories.ProductFactory(nom_service_public_numerique="test-product")

    # Create a test adaptor
    class TestEmptyAdaptor(posthog.PostHogAdaptor):
        slug = "test-product"
        indicators = [
            {
                "name": "utilisateurs actifs",
                "frequency": "mensuelle",
                "project_id": "44954",
                "insight_id": "65340",
            }
        ]

    # Mock empty response
    mock_response = {"result": [{"data": [], "days": []}]}

    responses.get(
        "https://eu.posthog.com/api/projects/44954/insights/65340",
        json=mock_response,
        status=status.HTTP_200_OK,
    )

    adaptor = TestEmptyAdaptor()

    # Should raise ValueError when no data is available
    with pytest.raises(ValueError, match="No data available"):
        adaptor.get_last_month_data()


