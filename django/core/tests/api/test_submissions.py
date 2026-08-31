"""
Unit tests for the product API
"""

import pytest
from rest_framework import status
from rest_framework.test import APIClient
from core import models, factories
import responses

pytestmark = pytest.mark.django_db


def test_api_submissions__anonymous_cannot_submit():
    """Anonymous should not be able to send files."""
    adaptor = factories.AdaptorFactory(
        product=factories.ProductFactory(
            name="france transfert-tests",
            dataset_id="69e8b42855b96c292988a106",
        ),
        client="FranceTransfertClient",
    )
    filename = "core/tests/api/examples/ft-example-francetransfert-2026-08-31-upload-stats.csv"

    response = APIClient().post(
        f"/api/products/{adaptor.product.slug}/submission/",
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
        format="multipart",
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert not models.Indicator.objects.exists()


def test_api_submissions__unauthorized_cannot_submit():
    """Anonymous should not be able to send files."""
    adaptor = factories.AdaptorFactory(
        product=factories.ProductFactory(
            name="france transfert-tests",
            dataset_id="69e8b42855b96c292988a106",
        ),
        client="FranceTransfertClient",
    )
    filename = "core/tests/api/examples/ft-example-francetransfert-2026-08-31-upload-stats.csv"
    another_product = factories.ProductFactory(name="autre-produit")
    _, someone_else_key = models.ProductAPIKey.objects.create_key(
        name="valid_key", product=another_product
    )

    response = APIClient().post(
        f"/api/products/{adaptor.product.slug}/submission/",
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
        format="multipart",
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert not models.Indicator.objects.exists()


def test_api_submissions__cannot_submit_on_random_product():
    """Cannot submit files on a product not expecting file processing."""
    adaptor = factories.AdaptorFactory(
        product=factories.ProductFactory(
            name="unauthorized-product",
        ),
    )
    _, key = models.ProductAPIKey.objects.create_key(
        name="valid_key", product=adaptor.product
    )
    filename = "core/tests/api/examples/ft-example-francetransfert-2026-08-31-upload-stats.csv"
    response = APIClient().post(
        f"/api/products/{adaptor.product.slug}/submission/",
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
        format="multipart",
    )
    assert (
        response.json()["detail"] == "File submission not authorized for this product."
    )


@responses.activate
def test_submission_data_is_saved():
    product = factories.ProductFactory(name="France Transfert")
    _, key = models.ProductAPIKey.objects.create_key(name="valid_key", product=product)

    files = [
        "ft-example-francetransfert-2026-08-31-download-satisfaction.csv",
        "ft-example-francetransfert-2026-08-31-upload-satisfaction.csv",
        "ft-example-francetransfert-2026-08-31-download-stats.csv",
        "ft-example-francetransfert-2026-08-31-upload-stats.csv",
    ]
    for filename in files:
        response = APIClient().post(
            f"/api/products/{product.slug}/submission/",
            data={
                "upload_file": open(
                    f"core/tests/api/examples/{filename}",
                    "r",
                ),
                "format": "multipart",
            },
            format="multipart",
            headers={
                "x-api-key": key,
                "Content-Type": "text/csv",
                "Content-Disposition": f"attachment; filename={f'{filename}'}",
            },
        )
        assert response.status_code == 201

    assert models.FTUsageLogs.objects.count() == 2
    assert models.FTSatisfactionLogs.objects.count() == 2
