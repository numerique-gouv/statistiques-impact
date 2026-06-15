"""
Unit tests for the records/ endpoint
"""

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from core import models, factories

pytestmark = pytest.mark.django_db


# DELETE
def test_api_records_delete__anonymous_cannot_delete():
    """Anonymous users should not be allowed to delete records."""
    record = factories.RecordFactory()

    response = APIClient().delete(
        f"/api/products/{record.productid.slug}/records/{record.slug}/",
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert models.Record.objects.exists()


def test_api_records_delete__invalid_api_key_cannot_delete():
    """Calls bearing an invalid API key should not be able to delete records."""
    record = factories.RecordFactory()
    api_key, key = models.ProductAPIKey.objects.create_key(
        name="valid_key", product=record.productid
    )

    response = APIClient().delete(
        f"/api/products/{record.productid.slug}/records/{record.slug}/",
        headers={"x-api-key": key + "ko"},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert models.Record.objects.exists()


def test_api_records_delete__valid_api_key_can_delete():
    """Calls bearing a valid API key for this product can delete record for product."""
    record = factories.RecordFactory()
    api_key, key = models.ProductAPIKey.objects.create_key(
        name="valid_key", product=record.productid
    )

    response = APIClient().delete(
        f"/api/products/{record.productid.slug}/records/{record.slug}/",
        headers={"x-api-key": key},
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not models.Record.objects.exists()
