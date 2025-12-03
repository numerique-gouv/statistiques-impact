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


@responses.activate
def test_suite_active_users():
    adaptor = adaptors.LaSuiteAdaptor()

    # Mock successful response
    responses.get(
        re.compile(r"https://stats.moncomptepro.beta.gouv.fr/*"),
        json=[
            {"Fournisseur Service": "Tchap", "Valeurs distinctes de Sub Fi": 27654},
            {
                "Fournisseur Service": "DINUM - RESANA",
                "Valeurs distinctes de Sub Fi": 23323,
            },
            {"Fournisseur Service": "Grist", "Valeurs distinctes de Sub Fi": 16094},
            {"Fournisseur Service": "Docs", "Valeurs distinctes de Sub Fi": 11515},
            {"Fournisseur Service": "Visio", "Valeurs distinctes de Sub Fi": 8184},
            {"Fournisseur Service": "Fichiers", "Valeurs distinctes de Sub Fi": 1771},
            {
                "Fournisseur Service": "Messagerie de la Suite Numérique",
                "Valeurs distinctes de Sub Fi": 1155,
            },
        ],
        status=status.HTTP_200_OK,
        content_type="application/json",
    )
    MAU = adaptor.get_last_month_data()
    assert len(MAU) == 7
    assert MAU[0]["product"] == "Tchap"
    assert MAU[0]["value"] == 27654


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
        {"name": "utilisateurs actifs (téléchargement)", "value": 4},
        {"name": "utilisateurs actifs (envoi)", "value": 1},
        {"name": "utilisateurs actifs", "value": 5},
        {"name": "téléchargements", "value": 4},
        {"name": "plis émis", "value": 3},
        {"name": "Go émis", "value": 4.91},
        {"name": "Go téléchargés", "value": 0.64},
        {"name": "Taille pli moyen (Mo)", "value": 1636.67},
        {
            "name": "top 5 domaines expéditeurs",
            "value": "actongroup.com, diplomatie.gouv.fr, gmail.com, justice.fr",
        },
        {"name": "avis émis", "value": 148},
        {"name": "pourcentage satisfaction", "value": 86},
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
        re.compile(r"https://www.data.gouv.fr/*"),
        body=fixtures.datagouv_messagerie_data,
        status=status.HTTP_200_OK,
        content_type="application/json",
    )

    assert adaptor.get_last_month_active_users() == 580


## TCHAP
@responses.activate
def test_tchap_indicators():
    """Tchap adaptor should retrieve expected data."""
    factories.ProductFactory(nom_service_public_numerique="tchap")
    adaptor = adaptors.TchapAdaptor()

    # Mock data.gouv.fr API response
    responses.get(
        re.compile(r"https://stats.tchap.incubateur.net/public/question/ae34205d-*"),
        json=[{"Visit Date": "sept., 2025", "Nombre de lignes": "367 146"}],
        status=status.HTTP_200_OK,
        content_type="application/json",
    )
    responses.get(
        re.compile(r"https://stats.tchap.incubateur.net/public/question/84a9b0bc-*"),
        json=[
            {"Hour": "août, 2025", "Somme de Events": "5 404 085"},
            {"Hour": "sept., 2025", "Somme de Events": "10 877 632"},
        ],
        status=status.HTTP_200_OK,
        content_type="application/json",
    )

    assert adaptor.get_last_month_data() == [
        {
            "frequency": "mensuelle",
            "name": "utilisateurs actifs",
            "method": "get_last_month_active_users",
            "value": 367146,
        },
        {
            "frequency": "mensuelle",
            "name": "messages échangés",
            "method": "get_last_month_messages_count",
            "value": 10877632,
        },
    ]
