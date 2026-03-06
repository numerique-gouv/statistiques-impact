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
def test_fetch_new_data_single_adaptor_ok(
    settings,
    proconnect_MAU,
):
    settings.DEBUG = True

    factories.AdaptorFactory.create(
        product=factories.ProductFactory(nom_service_public_numerique="proconnect"),
        indicator="monthly active users",
        client="MetabaseClient",
        source_url="https://stats.moncomptepro.beta.gouv.fr/public/question/single-product-question.json",
        frequence_monitoring="monthly",
    )

    # Response in fixtures
    call_command("fetch_new_data")

    assert models.Indicator.objects.count() == 1
    indicator = models.Indicator.objects.get()
    assert str(indicator.date) == "2025-09-30"
    assert str(indicator.productid) == "proconnect"


@freeze_time("2025-10-02")
@responses.activate
def test_fetch_new_data_many_products_adaptor_ok(metabase_lasuite_MAU):
    """Test adaptors can add indicators on multiple products."""

    models.Product.objects.get(slug="visio").delete()
    factories.AdaptorFactory.create(
        product=None,
        indicator="monthly active users via ProConnect",
        client="MetabaseClient",
        source_url="https://stats.moncomptepro.beta.gouv.fr/public/question/multiple-products-question.json",
        frequence_monitoring="monthly",
    )

    # Responses mocked in fixtures
    call_command("fetch_new_data")

    assert models.Indicator.objects.count() == 6
    assert not models.Indicator.objects.exclude(date="2025-09-30").exists()


@freeze_time("2025-10-02")
@responses.activate
def test_fetch_new_data_continues_when_adaptor_fails(
    settings,
    metabase_lasuite_MAU,
):
    """Data retrieval should not stop if an adaptor raises an exception."""
    settings.DEBUG = True

    # Failing adaptor and response
    factories.AdaptorFactory.create(
        product=factories.ProductFactory(nom_service_public_numerique="ProConnect"),
        indicator="monthly active users",
        client="MetabaseClient",
        source_url="https://stats.moncomptepro.beta.gouv.fr/public/question/single-product-question.json",
        frequence_monitoring="monthly",
    )
    responses.get(
        re.compile(
            r"https://stats.moncomptepro.beta.gouv.fr/public/question/single-product-question.json"
        ),
        json={},
        status=status.HTTP_504_GATEWAY_TIMEOUT,
        content_type="application/json",
    )

    # Functional adaptor. Product and responses in fixture
    factories.AdaptorFactory.create(
        product=None,
        indicator="monthly active users via ProConnect",
        client="MetabaseClient",
        source_url="https://stats.moncomptepro.beta.gouv.fr/public/question/multiple-products-question.json",
        frequence_monitoring="monthly",
    )

    call_command("fetch_new_data")

    indicators = models.Indicator.objects.all()
    visio_indicator = indicators.filter(
        productid__slug="proconnect", indicateur="monthly active users"
    )
    assert not visio_indicator.exists()  # failing adaptor created no indicator
    assert indicators.count() == 7  # other adaptors worked fine
