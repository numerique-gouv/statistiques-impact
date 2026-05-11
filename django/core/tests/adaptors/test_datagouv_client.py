"""Test every clients."""

import pytest
from rest_framework.test import APIClient
import responses
from core import models, factories
from freezegun import freeze_time

pytestmark = pytest.mark.django_db


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
    assert adaptor.get_data() == [
        {
            "product": adaptor.product.nom_service_public_numerique,
            "indicator": adaptor.indicator,
            "value": 580,
        }
    ]


# FRANCE TRANSFERT
@freeze_time("2026-05-08")
def test_france_transfert_indicators():
    """Monthly retrieval should fetch csv files from data.gouv.fr and compute expected indicators."""
    adaptor = factories.AdaptorFactory(
        product=factories.ProductFactory(
            nom_service_public_numerique="france transfert-tests",
            dataset_id="69e8b42855b96c292988a106",
        ),
        client="FranceTransfertClient",
    )

    assert adaptor.get_data() == [
        {
            "product": "france transfert-tests",
            "indicators": [
                {"name": "utilisateurs actifs (téléchargement)", "value": 68},
                {"name": "utilisateurs actifs (envoi)", "value": 148},
                {"name": "utilisateurs actifs", "value": 211},
                {"name": "téléchargements", "value": 164},
                {"name": "plis émis", "value": 172},
                {"name": "Go émis", "value": 86.29},
                {"name": "Go téléchargés", "value": 207.11},
                {"name": "Taille pli moyen (Mo)", "value": 501.68},
                {
                    "name": "top 5 domaines expéditeurs",
                    "value": "culture.gouv.fr, numerique.gouv.fr, interieur.gouv.fr, gmail.com, diplomatie.gouv.fr",
                },
                {"name": "avis émis", "value": 8},
                {"name": "pourcentage satisfaction", "value": 88},
            ],
        }
    ]
