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
    assert adaptor.get_data() == [
        {
            "product": "proconnect",
            "indicator": "monthly active users",
            "value": 343349,
        }
    ]


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
    assert adaptor.get_data() == [
        {
            "product": "Tchap",
            "indicator": "monthly active users",
            "value": 27654,
        },
        {
            "product": "Resana",
            "indicator": "monthly active users",
            "value": 23323,
        },
        {
            "product": "Grist",
            "indicator": "monthly active users",
            "value": 16094,
        },
        {
            "product": "Docs",
            "indicator": "monthly active users",
            "value": 11515,
        },
        {
            "product": "Visio",
            "indicator": "monthly active users",
            "value": 8184,
        },
        {
            "product": "Fichiers",
            "indicator": "monthly active users",
            "value": 1771,
        },
        {
            "product": "Messagerie de la Suite Numérique",
            "indicator": "monthly active users",
            "value": 1155,
        },
        {
            "product": "Hors suj",
            "indicator": "monthly active users",
            "value": 13,
        },
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

    assert adaptor.get_data() == [
        {"product": "tchap", "indicator": "monthly active users", "value": 367146}
    ]
