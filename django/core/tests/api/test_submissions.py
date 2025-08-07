"""
Unit tests for the product API
"""

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from core import models, factories

pytestmark = pytest.mark.django_db


# FRANCE TRANSFERT
@pytest.mark.skip(
    reason="Test broken because of csv boundaries.\
    Code works as expected when calling with Postman or curl + same file."
)
def test_api_submissions__france_transert():
    """Correctly formatted request should create expected indicators."""
    product = factories.ProductFactory(nom_service_public_numerique="france-transfert")
    api_key, key = models.ProductAPIKey.objects.create_key(
        name="valid_key", product=product
    )
    filename = "core/tests/api/examples/ip-machine1_FranceTransfert_2025-07-23_upload_stats.csv"

    response = APIClient().post(
        "/api/products/france-transfert/submission/",
        data={
            "upload_file": open(
                filename,
                "rb",
            )
        },
        headers={
            "x-api-key": key,
            "Content-Type": "text/csv",
            "Content-Disposition": f"attachment; filename={filename}",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert models.Indicator.objects.filter(
        productid=product, indicateur="Nombre de plis (machine1)"
    ).exists()
