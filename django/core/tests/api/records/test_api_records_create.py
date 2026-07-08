"""
Tests for the records endpoint
"""

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from core import models, factories

pytestmark = pytest.mark.django_db


def test_api_records_create__anonymous_cannot_create():
    """Anonymous users should not be allowed to create records."""
    indicator = factories.IndicatorFactory()

    response = APIClient().post(
        f"/api/products/{indicator.productid.slug}/indicators/{indicator.slug}/records/",
        json={
            "indicator": str(indicator.id),
            "value": 3,
            "end_date": "2025-06-30",
            "start_date": "2025-04-01",
            "is_auto_added": "false",
        },
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert not models.Record.objects.exists()


def test_api_records_create__invalid_api_key_cannot_create():
    """Calls bearing an invalid api key should not be able to create records."""
    indicator = factories.IndicatorFactory()

    response = APIClient().post(
        f"/api/products/{indicator.productid.slug}/indicators/{indicator.slug}/records/",
        json={
            "indicator": str(indicator.id),
            "value": 3,
            "end_date": "2025-06-30",
            "start_date": "2025-04-01",
            "is_auto_added": "false",
        },
        headers={"x-api-key": "invalid-key"},
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert not models.Record.objects.exists()


def test_api_records_create__valid_api_key_can_create():
    """Calls bearing a working API key for this product can create indicator for product."""
    indicator = factories.IndicatorFactory()
    _, valid_key = models.ProductAPIKey.objects.create_key(
        name="valid_key", product=indicator.productid
    )

    payload = {
        "value": 3,
        "end_date": "2025-06-30",
        "start_date": "2025-04-01",
        "is_auto_added": "false",
    }

    response = APIClient().post(
        f"/api/products/{indicator.productid.slug}/indicators/{indicator.slug}/records/",
        data=payload,
        headers={"x-api-key": valid_key},
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_201_CREATED
    record = models.Record.objects.get()
    # check response
    assert response.json()["indicator"] == {
        "productid": indicator.productid.slug,
        "slug": indicator.slug,
    }

    record.indicator = indicator
    record.valeur = payload["value"]


def test_api_records_create__admin_can_create(admin_key):
    """Calls bearing the ADMIN API KEY can create records on every products."""
    indicators = factories.IndicatorFactory.create_batch(2)

    for indicator in indicators:
        response = APIClient().post(
            f"/api/products/{indicator.productid.slug}/indicators/{indicator.slug}/records/",
            data={
                "value": 3,
                "end_date": "2025-06-30",
                "start_date": "2025-04-01",
                "is_auto_added": "false",
            },
            headers={"x-api-key": "admin_key"},
        )
        assert response.status_code == status.HTTP_201_CREATED
    assert models.Record.objects.count() == 2


@pytest.mark.skip(reason="broken until unique constraints is added on record model")
def test_api_records_create__cannot_create_duplicate(admin_key):
    """Should not be able to create duplicate."""
    record = factories.RecordFactory()

    response = APIClient().post(
        f"/api/products/{record.indicator.productid.slug}/indicators/{record.indicator.slug}/records/",
        data={
            "value": record.value,
            "end_date": str(record.end_date),
            "is_auto_added": record.is_auto_added,
        },
        headers={"x-api-key": "admin_key"},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "non_field_errors": [
            "Les champs indicator, date doivent former un ensemble unique."
        ]
    }
    assert len(models.Record.objects.all()) == 1
