"""
Unit tests for the product API
"""

import pytest
from rest_framework import status
from rest_framework.test import APIClient
from datetime import timedelta
from core import models, factories

pytestmark = pytest.mark.django_db


# LIST
def test_api_products_list__anonymous_ok():
    """Anonymous users should be allowed to list products."""
    product = factories.ProductFactory()

    response = APIClient().get("/api/products/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "name": product.name,
            "slug": product.slug,
        }
    ]


def test_api_products_list__anonymous_cant_create():
    """Anonymous users should not be allowed to create products."""
    response = APIClient().post("/api/products/", body="{'name': 'product'}")

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    assert not models.Product.objects.exists()


# RETRIEVE
def test_api_products_retrieve__anonymous_ok():
    """Anonymous users should be allowed to retrieve info on a given product."""
    indicator = factories.IndicatorFactory()
    response = APIClient().get(f"/api/products/{indicator.productid.slug}/")
    assert response.status_code == status.HTTP_200_OK


def test_api_products_retrieve__last_indicators_ok():
    """Last indicators should be returned when retrieving Product's details."""
    last_record = factories.RecordFactory()
    product = last_record.indicator.productid
    _ = factories.RecordFactory(
        indicator__productid=product, end_date=last_record.end_date
    )  # same date, same product, other indicator = should be listed
    _ = factories.RecordFactory(
        indicator=last_record.indicator,
        end_date=last_record.end_date - timedelta(days=30),
    )  # same indicator, earlier date = should not be listed

    response = APIClient().get(f"/api/products/{product.slug}/")
    assert response.status_code == status.HTTP_200_OK
    last_records = response.json()["last_records"]
    assert len(last_records) == 2
    assert last_records == [
        {
            "created_at": record.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "end_date": str(record.end_date),
            "start_date": record.start_date,
            "is_auto_added": record.is_auto_added,
            "id": str(record.id),
            "indicator": {
                "productid": product.slug,
                "slug": record.indicator.slug,
            },
            "updated_at": record.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "value": record.value,
        }
        for record in last_record.indicator.productid.last_records
    ]


@pytest.mark.parametrize("verb", ["put", "patch", "delete"])
def test_api_products_retrieve__anonymous_read_only(verb):
    """Anonymous users should not be allowed to update or delete products."""
    product = factories.ProductFactory()

    response = getattr(APIClient(), verb)(
        f"/api/products/{product.slug}/",
        body="{'name': 'product'}",
    )
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
