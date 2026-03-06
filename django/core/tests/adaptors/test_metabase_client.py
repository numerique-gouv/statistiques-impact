"""Test every clients."""

import pytest
from rest_framework import status
import responses
from core import factories
import re

pytestmark = pytest.mark.django_db


# METABASE
@responses.activate
def test_metabase_single_indicator():
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
def test_metabase_multiple_products(metabase_lasuite_MAU):
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
