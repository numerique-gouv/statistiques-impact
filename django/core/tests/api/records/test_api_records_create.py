"""
Tests for the records endpoint
"""

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from core import models, factories
from django.test import override_settings
from core.api import serializers

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
    import pdb

    pdb.set_trace()
    # check object
    record.indicator = indicator
    record.valeur = payload["value"]
    # assert response.json()['indicator'] == {}
    #     "id": str(record.id),
    #     "indicator": {
    #         "productid": indicator.productid.slug,
    #         "slug": indicator.slug,
    #     },
    #     "valeur": payload.valeur,
    #     "date": str(payload.date),
    #     "date_debut": str(payload.date_debut),
    #     "est_automatise": payload.est_automatise,
    #     "created_at": payload.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
    #     "updated_at": payload.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
    # }


@override_settings(ADMIN_API_KEY="admin_key")
def test_api_records_create__admin_can_create():
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
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_201_CREATED
    assert models.Record.objects.count() == 2


def test_api_records_create__cannot_create_duplicate():
    """Should not be able to create duplicate."""
    record = factories.RecordFactory()
    api_key, key = models.ProductAPIKey.objects.create_key(
        name="valid_key", product=record.indicator.productid
    )

    response = APIClient().post(
        f"/api/products/{record.indicator.productid.slug}/indicators/{record.indicator.slug}/records/",
        json=serializers.RecordSerializer(record).data,
        headers={"x-api-key": key},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "non_field_errors": [
            "Les champs indicator, date doivent former un ensemble unique."
        ]
    }
    assert len(models.Record.objects.all()) == 1
