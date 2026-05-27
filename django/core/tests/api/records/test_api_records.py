"""
Unit tests for the indicators/ endpoint
"""

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from core import models, factories
from django.test import override_settings
from core.api import serializers

pytestmark = pytest.mark.django_db


# CREATE
def test_api_records_create__anonymous_cannot_create():
    """Anonymous users should not be allowed to create records."""
    indicator = factories.IndicatorFactory()

    response = APIClient().post(
        f"/api/products/{indicator.productid.slug}/indicators/{indicator.slug}/records/",
        json={
            "indicator": str(indicator.id),
            "valeur": 3,
            "date": "2025-06-30",
            "date_debut": "2025-04-01",
            "est_automatise": "false",
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
            "valeur": 3,
            "date": "2025-06-30",
            "date_debut": "2025-04-01",
            "est_automatise": "false",
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
        "valeur": 3,
        "date": "2025-06-30",
        "date_debut": "2025-04-01",
        "est_automatise": "false",
    }

    response = APIClient().post(
        f"/api/products/{indicator.productid.slug}/indicators/{indicator.slug}/records/",
        data=payload,
        headers={"x-api-key": valid_key},
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_201_CREATED
    import pdb

    pdb.set_trace()
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
    record.valeur = payload["valeur"]
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
                "valeur": 3,
                "date": "2025-06-30",
                "date_debut": "2025-04-01",
                "est_automatise": "false",
            },
            headers={"x-api-key": "admin_key"},
            content_type="application/json",
        )
        import pdb

        pdb.set_trace()
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


# LIST
def test_api_records_list__anonymous_ok():
    """Anonymous users should be allowed to list records."""
    indicator = factories.IndicatorFactory()
    records = factories.RecordFactory.create_batch(2, indicator=indicator)

    # record for another indicator on another product
    factories.RecordFactory(indicator__indicateur=str(indicator.indicateur))
    # record for another indicator on same product
    factories.RecordFactory(indicator__productid=indicator.productid)

    response = APIClient().get(
        f"/api/products/{indicator.productid.slug}/indicators/{indicator.slug}/records/"
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2
    assert sorted(response.json(), key=lambda x: x["id"]) == sorted(
        [
            {
                "id": str(record.id),
                "indicator": {
                    "productid": record.indicator.productid.slug,
                    "slug": record.indicator.slug,
                },
                "valeur": record.valeur,
                "date": str(record.date),
                "date_debut": str(record.date_debut),
                "est_automatise": record.est_automatise,
                "created_at": record.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "updated_at": record.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            }
            for record in records
        ],
        key=lambda x: x["id"],
    )


def test_api_records_list__filtered_ok():
    """Can filter by indicator."""
    record = factories.RecordFactory()
    indicator = record.indicator
    other_product_same_indicator_name = factories.IndicatorFactory(
        indicateur=str(indicator.indicateur)
    )

    # a record on another product but with the same name and same date
    factories.RecordFactory(indicator=other_product_same_indicator_name)
    # filtered record
    factories.RecordFactory(indicator=indicator)

    response = APIClient().get(
        f"/api/products/{indicator.productid.slug}/indicators/{indicator.slug}/records/?date={record.date}",
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert response.json() == [
        {
            "id": str(record.id),
            "indicator": {
                "productid": record.indicator.productid.slug,
                "slug": indicator.slug,
            },
            "valeur": float(record.valeur),
            "date": str(record.date),
            "date_debut": str(record.date_debut),
            "est_automatise": record.est_automatise,
            "created_at": record.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "updated_at": record.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        }
    ]


# RETRIEVE
def test_api_records_retrieve__anonymous_ok():
    """Anonymous users should be allowed to retrieve records."""
    record = factories.RecordFactory()
    indicator = record.indicator
    factories.RecordFactory(indicator=indicator)

    response = APIClient().get(
        f"/api/products/{indicator.productid.slug}/indicators/{indicator.slug}/records/{record.id}/",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": str(record.id),
        "indicator": {
            "productid": indicator.productid.slug,
            "slug": indicator.slug,
        },
        "valeur": float(record.valeur),
        "date": str(record.date),
        "date_debut": str(record.date_debut),
        "est_automatise": record.est_automatise,
        "created_at": record.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "updated_at": record.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
    }


# DELETE
def test_api_records_delete__anonymous_cannot_delete():
    """Anonymous users should not be allowed to delete records."""
    record = factories.RecordFactory()
    indicator = record.indicator

    response = APIClient().delete(
        f"/api/products/{indicator.productid.slug}/indicators/{indicator.slug}/records/{record.id}/",
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert models.Record.objects.exists()


def test_api_records_delete__invalid_api_key_cannot_delete():
    """Calls bearing an invalid API key should not be able to delete records."""
    record = factories.RecordFactory()
    indicator = record.indicator
    api_key, key = models.ProductAPIKey.objects.create_key(
        name="valid_key", product=indicator.productid
    )

    response = APIClient().delete(
        f"/api/products/{indicator.productid.slug}/indicators/{indicator.slug}/records/{record.id}/",
        headers={"x-api-key": key + "ko"},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert models.Indicator.objects.exists()


def test_api_records_delete__valid_api_key_can_delete():
    """Calls bearing a valid API key for a product can delete records on said product."""
    record = factories.RecordFactory()
    indicator = record.indicator
    api_key, key = models.ProductAPIKey.objects.create_key(
        name="valid_key", product=indicator.productid
    )

    # other record from same indicator
    record = factories.RecordFactory(indicator=indicator)

    response = APIClient().delete(
        f"/api/products/{indicator.productid.slug}/indicators/{indicator.slug}/records/{record.id}/",
        headers={"x-api-key": key},
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert models.Record.objects.count() == 1
