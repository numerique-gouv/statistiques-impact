"""Test every clients."""

import pytest
from rest_framework import status
from rest_framework.test import APIClient
import responses
from core import models, factories
from freezegun import freeze_time
import re

pytestmark = pytest.mark.django_db


# PROCONNECT
@responses.activate
def test_proconnect_active_users():
    adaptor = factories.AdaptorFactory.create(
        product=factories.ProductFactory(nom_service_public_numerique="proconnect"),
        indicator="monthly active users",
        client="MetabaseClient",
        source_url="https://stats.moncomptepro.beta.gouv.fr/public/question/single-product-question.json",
    )

    # Mock successful response
    responses.get(
        re.compile(r".*/*.json"),
        json=[{"Time: Mois": "2026-02-01", "Valeurs distinctes de Sub Fi": 343349}],
        status=status.HTTP_200_OK,
        content_type="application/json",
    )
    assert adaptor.get_data() == 343349


@responses.activate
def test_suite_active_users(metabase_lasuite_MAU):
    """Test a question with multiple products is handled as expected."""
    adaptor = factories.AdaptorFactory.create(
        product=factories.ProductFactory(nom_service_public_numerique="proconnect"),
        indicator="monthly active users",
        client="MetabaseMultipleProductsClient",
        source_url="https://stats.moncomptepro.beta.gouv.fr/public/question/multiple-products-question.json",
    )

    # Response mocked in fixture
    value = adaptor.get_data()
    assert len(value) == 8
    assert value == [
        {"product": "Tchap", "value": 27654},
        {"product": "Resana", "value": 23323},
        {"product": "Grist", "value": 16094},
        {"product": "Docs", "value": 11515},
        {"product": "Visio", "value": 8184},
        {"product": "Fichiers", "value": 1771},
        {"product": "Messagerie de la Suite Numérique", "value": 1155},
        {"product": "Hors suj", "value": 13},
    ]


# FRANCE TRANSFERT
@freeze_time("2025-10-02")
def test_france_transfert_indicators():
    """Monthly retrieval should fetch csv files from data.gouv.fr and compute expected indicators."""
    adaptor = factories.AdaptorFactory(
        product=factories.ProductFactory(
            nom_service_public_numerique="france-transfert",
            dataset_id="68b86764fd43cc1591faa6a5",  # démo dataset = 68b86764fd43cc1591faa6a5
        ),
        client="FranceTransfertClient",
    )

    assert adaptor.get_data() == [
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
def test_api_submissions__files_sent_to_datagouv(datagouv_file_sent):
    """When a file is submitted, it's succesfully sent to data.gouv.fr."""
    product = factories.ProductFactory(
        nom_service_public_numerique="france-transfert-tests",
        dataset_id="68b86764fd43cc1591faa6a5",
    )
    _, key = models.ProductAPIKey.objects.create_key(name="valid_key", product=product)
    filepath = "core/tests/api/examples/ip-127-0-0-1_FranceTransfert_2025-05-11_download_stats.csv"
    filename = filepath.split("/")[-1]

    # Mock successfull response from data.gouv.fr
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

    # no response expected
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
def test_messagerie_active_users(datagouv_messagerie_data):
    """Checks that DataGouvClient retrieves data.gouv data as expected."""
    adaptor = factories.AdaptorFactory.create(
        product=factories.ProductFactory(
            nom_service_public_numerique="messagerie",
            dataset_id="68650cd6130c82da6ba44a92",
        ),
        indicator="monthly active users",
        client="MessagerieClient",
    )

    # Responses mocked in fixtures
    assert adaptor.get_data() == 580


## TCHAP
@responses.activate
def test_tchap_indicators():
    """Tchap client should retrieve expected data."""
    adaptor = factories.AdaptorFactory.create(
        product=factories.ProductFactory(
            nom_service_public_numerique="tchap",
        ),
        source_url="https://metabase.tchap.net/public/question/last_MAU.json",
        indicator="monthly active users",
        client="TchapClient",
    )

    # Mock data.gouv.fr API response
    responses.get(
        re.compile(r"https://metabase.tchap.net/public/question/last_MAU.json"),
        json=[{"Visit Date": "sept., 2025", "Nombre de lignes": "367 146"}],
        status=status.HTTP_200_OK,
        content_type="application/json",
    )

    assert adaptor.get_data() == 367146

    # Message échangés
    # responses.get(
    #     re.compile(r"https://stats.tchap.incubateur.net/public/question/84a9b0bc-*"),
    #     json=[
    #         {"Hour": "août, 2025", "Somme de Events": "5 404 085"},
    #         {"Hour": "sept., 2025", "Somme de Events": "10 877 632"},
    #     ],
    #     status=status.HTTP_200_OK,
    #     content_type="application/json",
    # )
