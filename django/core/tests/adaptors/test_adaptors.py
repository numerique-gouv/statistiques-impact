"""Test every adaptors."""

import pytest
from rest_framework import status
from rest_framework.test import APIClient
import responses
from core import models, factories
import json
from freezegun import freeze_time
from core import adaptors
import re
from core.tests import fixtures

pytestmark = pytest.mark.django_db


# PROCONNECT


@responses.activate
def test_proconnect_active_users():
    factories.ProductFactory(nom_service_public_numerique="proconnect")
    adaptor = adaptors.ProConnectAdaptor()

    # Mock successful response
    responses.get(
        re.compile(r".*/*.json"),
        b'[{"Time: Mois": "2024-02-01", "Valeurs distinctes de Sub Fi": "200000"}]',
        status=status.HTTP_200_OK,
        content_type="application/json",
    )
    assert adaptor.get_last_month_data()[0]["value"] == 200000


# FRANCE TRANSFERT


@freeze_time("2025-10-02")
def test_france_transfert_indicators():
    """Monthly retrieval should fetch csv files from data.gouv.fr and compute expected indicators."""
    factories.ProductFactory(
        nom_service_public_numerique="france-transfert",
        dataset_id="68b86764fd43cc1591faa6a5",
    )  # démo dataset = 68b86764fd43cc1591faa6a5

    ft_client = adaptors.FranceTransfertAdaptor()
    result = ft_client.get_last_month_data()
    assert result == [
        {"name": "utilisateurs actifs (téléchargement)", "value": 1},
        {"name": "utilisateurs actifs (envoi)", "value": 2},
        {"name": "utilisateurs actifs", "value": 3},
        {"name": "téléchargements", "value": 4},
        {"name": "plis émis", "value": 30},
        {"name": "Go émis", "value": 10.38},
        {"name": "Go téléchargés", "value": 0.36},
        {"name": "Taille pli moyen (Mo)", "value": 345.89},
        {
            "name": "top 5 domaines expéditeurs",
            "value": "actongroup.com, mail.numerique.gouv.fr",
        },
        {"name": "avis émis", "value": 1},
        {"name": "pourcentage satisfaction", "value": 100},
    ]


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
        f"/api/products/{product.slug}/submission/",
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


# MESSAGERIE


@freeze_time("2025-07-02")
@responses.activate
def test_messagerie_active_users():
    factories.ProductFactory(nom_service_public_numerique="messagerie")
    adaptor = adaptors.MessagerieAdaptor()

    # Mock data.gouv.fr API response
    responses.get(
        re.compile(adaptor.indicators[0]["url"]),
        body=fixtures.datagouv_messagerie_data,
        status=status.HTTP_200_OK,
        content_type="application/json",
    )

    assert adaptor.get_monthly_active_users() == 580
