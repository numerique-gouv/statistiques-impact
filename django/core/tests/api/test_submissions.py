"""
Unit tests for the product API
"""

import pytest
from rest_framework import status
from rest_framework.test import APIClient
from core import models, factories

pytestmark = pytest.mark.django_db


def test_api_submissions__anonymous_cannot_submit():
    """Anonymous should not be able to send files."""
    product = factories.ProductFactory(nom_service_public_numerique="france-transfert")
    filename = "core/tests/api/examples/ip-127-0-0-1_FranceTransfert_2025-07-23_upload_stats.csv"

    response = APIClient().post(
        f"/api/products/{product}/submission/",
        data={
            "upload_file": open(
                filename,
                "r",
            )
        },
        headers={
            "Content-Type": "text/csv",
            "Content-Disposition": f"attachment; filename={filename}",
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert not models.Indicator.objects.exists()


def test_api_submissions__unauthorized_cannot_submit():
    """Anonymous should not be able to send files."""
    product = factories.ProductFactory(nom_service_public_numerique="france-transfert")
    filename = "core/tests/api/examples/ip-127-0-0-1_FranceTransfert_2025-07-23_upload_stats.csv"
    another_product = factories.ProductFactory(
        nom_service_public_numerique="autre-produit"
    )
    _, someone_else_key = models.ProductAPIKey.objects.create_key(
        name="valid_key", product=another_product
    )

    response = APIClient().post(
        f"/api/products/{product}/submission/",
        data={
            "upload_file": open(
                filename,
                "rb",
            )
        },
        headers={
            "x-api-key": someone_else_key,
            "Content-Type": "text/csv",
            "Content-Disposition": f"attachment; filename={filename}",
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert not models.Indicator.objects.exists()


def test_api_submissions__cannot_submit_on_any_product():
    """Cannot submit files on a product not expecting file processing."""
    product = factories.ProductFactory()
    _, key = models.ProductAPIKey.objects.create_key(name="valid_key", product=product)
    filename = "core/tests/api/examples/ip-127-0-0-1_FranceTransfert_2025-07-23_upload_stats.csv"
    response = APIClient().post(
        f"/api/products/{product.slug}/submission/",
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
    assert (
        response.json()["detail"] == "File submission not authorized for this product."
    )
