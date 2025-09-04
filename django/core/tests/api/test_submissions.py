"""
Unit tests for the product API
"""

import pytest
from rest_framework import status
from rest_framework.test import APIClient
import responses
from core import models, factories
import json

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
    """Cannot submit files on any product on specifically on France Transfert."""
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
    assert response.json()["detail"] == "Soumission non autorisée pour ce produit."


# FRANCE TRANSFERT
@responses.activate
def test_api_submissions__files_sent_to_datagouv():
    """When a file is submitted, it's succesfully sent to data.gouv.fr."""
    product = factories.ProductFactory(
        nom_service_public_numerique="france-transfert-tests",
        dataset_id="68b86764fd43cc1591faa6a5",
    )
    _, key = models.ProductAPIKey.objects.create_key(name="valid_key", product=product)
    filepath = "core/tests/api/examples/ip-127-0-0-1_FranceTransfert_2025-05-11_download_stats.csv"
    filename = filepath.split("/")[-1]

    # Mock successfull response from data.gouv.fr
    responses.post(
        f"https://demo.data.gouv.fr/api/1/datasets/{product.dataset_id}/upload/",
        json.dumps(
            {
                "checksum": {
                    "type": "sha1",
                    "value": "47cc980e80adf717d00d8a64c25fcd1395962b56",
                },
                "created_at": "2025-09-04T16:29:00.353226+00:00",
                "description": None,
                "extras": {},
                "filesize": 1545,
                "filetype": "file",
                "format": "csv",
                "harvest": None,
                "id": "d0280651-e268-44de-a7a7-ed515e2bb565",
                "internal": {
                    "created_at_internal": "2025-09-04T16:29:00.353226+00:00",
                    "last_modified_internal": "2025-09-04T18:29:00.299496+00:00",
                },
                "last_modified": "2025-09-04T18:29:00.299496+00:00",
                "latest": "https://demo.data.gouv.fr/api/1/datasets/r/d0280651-e268-44de-a7a7-ed515e2bb565",
                "metrics": {},
                "mime": "text/csv",
                "preview_url": None,
                "schema": None,
                "success": True,
                "title": f"{filename}",
                "type": "main",
                "url": f"https://demo-static.data.gouv.fr/resources/test-envoi-fichiers-france-transfert/20250904-162900/{filename}",
            }
        ),
        status=status.HTTP_201_CREATED,
        content_type="application/json",
    )
    response = APIClient().post(
        f"/api/products/{product}/submission/",
        data={
            "upload_file": open(
                filepath,
                "r",
            )
        },
        headers={
            "x-api-key": key,
            "Content-Type": "text/csv",
            "Content-Disposition": f"attachment; filename={filename}",
        },
    )
    assert response.json() == {"file": filename, "success": True}
    assert response.status_code == status.HTTP_201_CREATED


def test_api_submissions__no_dataset_id_fails():
    """API returns a clear error if product has no dataset_id."""
    product = factories.ProductFactory(
        nom_service_public_numerique="france-transfert-tests"
    )
    _, key = models.ProductAPIKey.objects.create_key(name="valid_key", product=product)
    filepath = "core/tests/api/examples/ip-127-0-0-1_FranceTransfert_2025-05-11_download_stats.csv"
    filename = filepath.split("/")[-1]

    response = APIClient().post(
        f"/api/products/{product}/submission/",
        data={
            "upload_file": open(
                filepath,
                "r",
            )
        },
        headers={
            "x-api-key": key,
            "Content-Type": "text/csv",
            "Content-Disposition": f"attachment; filename={filename}",
        },
    )
    assert response.json() == {"detail": "Please provide a data.gouv.fr dataset"}
