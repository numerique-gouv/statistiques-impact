"""Test every clients."""

import pytest
from rest_framework import status
import responses
from core import factories
import re

pytestmark = pytest.mark.django_db


# METABASE
@responses.activate
def test_metabase_single_record():
    indicator = factories.IndicatorFactory.create(
        product=factories.ProductFactory(nom_service_public_numerique="proconnect"),
        record="monthly active users",
        client="MetabaseClient",
        source_url="https://metabase.gouv.fr/public/question/single-product-question.json",
    )

    # Mock successful response
    responses.get(
        re.compile(r".*/*.json"),
        json=[{"Time: Mois": "2026-02-01", "Valeurs distinctes de Sub Fi": 343349}],
        status=status.HTTP_200_OK,
        content_type="application/json",
    )
    assert indicator.get_data() == [
        {
            "product": "proconnect",
            "record": "monthly active users",
            "value": 343349,
        }
    ]


@responses.activate
def test_metabase_multiple_products(metabase_lasuite_MAU):
    """Test a question with multiple products is handled as expected."""
    indicator = factories.IndicatorFactory.create(
        product=factories.ProductFactory(nom_service_public_numerique="proconnect"),
        record="monthly active users",
        client="MetabaseMultipleProductsClient",
        source_url="https://metabase.gouv.fr/public/question/multiple-products-question.json",
    )

    # Response mocked in fixture
    assert indicator.get_data() == [
        {
            "product": "Tchap",
            "record": "monthly active users",
            "value": 27654,
        },
        {
            "product": "Resana",
            "record": "monthly active users",
            "value": 23323,
        },
        {
            "product": "Grist",
            "record": "monthly active users",
            "value": 16094,
        },
        {
            "product": "Docs",
            "record": "monthly active users",
            "value": 11515,
        },
        {
            "product": "Visio",
            "record": "monthly active users",
            "value": 8184,
        },
        {
            "product": "Fichiers",
            "record": "monthly active users",
            "value": 1771,
        },
        {
            "product": "Messagerie de la Suite Numérique",
            "record": "monthly active users",
            "value": 1155,
        },
        {
            "product": "Hors suj",
            "record": "monthly active users",
            "value": 13,
        },
    ]


## TCHAP
@responses.activate
def test_tchap_records():
    """Tchap client should retrieve expected data."""
    indicator = factories.IndicatorFactory.create(
        product=factories.ProductFactory(
            nom_service_public_numerique="tchap",
        ),
        source_url="https://metabase.tchap.net/public/question/last_MAU.json",
        record="monthly active users",
        client="TchapClient",
    )

    # Mock data.gouv.fr API response
    responses.get(
        re.compile(r"https://metabase.tchap.net/public/question/last_MAU.json"),
        json=[{"Visit Date": "sept., 2025", "Nombre de lignes": "367 146"}],
        status=status.HTTP_200_OK,
        content_type="application/json",
    )

    assert indicator.get_data() == [
        {"product": "tchap", "record": "monthly active users", "value": 367146}
    ]
