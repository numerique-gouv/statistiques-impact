"""
Tests for the records endpoint
"""

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from core import factories

pytestmark = pytest.mark.django_db


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
