"""
Unit tests for the product API
"""

import re
import pytest
from core import factories, models
import responses
from rest_framework import status
from django.core.management import call_command
from freezegun import freeze_time


pytestmark = pytest.mark.django_db


# FETCH_NEW_DATA
@freeze_time("2025-10-02")
@responses.activate
def test_commands_fetch_new_data_ok(
    settings,
    proconnect_MAU,
    proconnect_lasuite_MAU,
    datagouv_messagerie_data,
    tchap_MAU,
    tchap_monthly_messages,
    posthog_visio_MAU,
):
    settings.DEBUG = True
    products = [
        "ProConnect",
        "Messagerie",
        "Tchap",
        "Visio",
        "Resana",
        "Grist",
        "Docs",
        "Fichiers",
    ]
    for product in products:
        factories.AdaptorFactory(
            product=factories.ProductFactory(nom_service_public_numerique=product)
        )

    factories.AdaptorFactory(
        product=factories.ProductFactory(
            nom_service_public_numerique="france-transfert",
            dataset_id="68b86764fd43cc1591faa6a5",
        ),
        method="FranceTransfertAdaptor",
    )

    # Responses mocked in fixtures
    call_command("fetch_new_data")

    indicators = models.Indicator.objects.filter(date="2025-09-30")
    assert indicators.count() == 21
    assert indicators.filter(productid__slug="proconnect").count() == 1
    assert indicators.filter(productid__slug="messagerie").count() == 1
    assert indicators.filter(productid__slug="france-transfert").count() == 10
    assert indicators.filter(productid__slug="tchap").count() == 3
    assert indicators.filter(productid__slug="visio").count() == 2
    assert indicators.filter(productid__slug="resana").count() == 1
    assert indicators.filter(productid__slug="grist").count() == 1
    assert indicators.filter(productid__slug="docs").count() == 1
    assert indicators.filter(productid__slug="fichiers").count() == 1
    assert not models.Indicator.objects.exclude(date="2025-09-30").exists()


@freeze_time("2025-10-02")
@responses.activate
def test_commands_fetch_new_data_continues_when_adaptor_exception(
    settings,
    proconnect_MAU,
    proconnect_lasuite_MAU,
    datagouv_messagerie_data,
    tchap_MAU,
    tchap_monthly_messages,
):
    """Data retrieval should not stop if an adaptor raises an exception."""
    settings.DEBUG = True
    products = [
        "ProConnect",
        "Messagerie",
        "Tchap",
        "Visio",
        "Resana",
        "Grist",
        "Docs",
        "Fichiers",
    ]
    for product in products:
        factories.ProductFactory(nom_service_public_numerique=product)
    factories.ProductFactory(
        nom_service_public_numerique="france-transfert",
        dataset_id="68b86764fd43cc1591faa6a5",
    )

    # Successful responses mocked in fixtures
    responses.get(
        re.compile(r"https://eu.posthog.com*"),
        json={"result": [{"data": [], "days": []}]},
        status=status.HTTP_200_OK,
        content_type="application/json",
    )
    call_command("fetch_new_data")

    indicators = models.Indicator.objects.all()
    # failing adaptor created no indicator
    assert not (
        indicators.filter(
            productid__slug="visio", indicateur="utilisateurs actifs"
        ).exists()
    )

    # other adaptors worked fine
    assert indicators.filter(productid__slug="proconnect").exists()
    assert indicators.filter(productid__slug="messagerie").exists()
    assert indicators.filter(productid__slug="france-transfert").exists()
    assert indicators.filter(productid__slug="tchap").exists()
    assert indicators.filter(productid__slug="resana").exists()
