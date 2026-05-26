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
def test_fetch_new_data_single_indicator_ok(
    settings,
    proconnect_MAU,
):
    settings.DEBUG = True

    factories.IndicatorFactory.create(
        product=factories.ProductFactory(nom_service_public_numerique="proconnect"),
        record="monthly active users",
        client="MetabaseClient",
        source_url="https://metabase.gouv.fr/public/question/single-product-question.json",
        frequence_monitoring="monthly",
    )

    # Response in fixtures
    call_command("fetch_new_data")

    assert models.Record.objects.count() == 1
    record = models.Record.objects.get()
    assert str(record.date) == "2025-09-30"
    assert str(record.productid) == "proconnect"


@freeze_time("2025-10-02")
@responses.activate
def test_fetch_new_data_many_products_indicator_ok(metabase_lasuite_MAU):
    """Test indicators can add records on multiple products."""

    models.Product.objects.get(slug="visio").delete()
    factories.IndicatorFactory.create(
        product=None,
        record="monthly active users via ProConnect",
        client="MetabaseMultipleProductsClient",
        source_url="https://metabase.gouv.fr/public/question/multiple-products-question.json",
        frequence_monitoring="monthly",
    )

    # Responses mocked in fixtures
    call_command("fetch_new_data")

    assert models.Record.objects.count() == 6
    assert not models.Record.objects.exclude(date="2025-09-30").exists()


@freeze_time("2025-10-02")
@responses.activate
def test_fetch_new_data_continues_when_indicator_fails(
    settings,
    metabase_lasuite_MAU,
):
    """Data retrieval should not stop if an indicator raises an exception."""
    settings.DEBUG = True

    # Functional indicator. Product and responses in fixture
    factories.IndicatorFactory.create(
        product=None,
        record="monthly active users via ProConnect",
        client="MetabaseClient",
        source_url="https://metabase.gouv.fr/public/question/multiple-products-question.json",
        frequence_monitoring="monthly",
    )

    # Failing indicator and response
    factories.IndicatorFactory.create(
        product=factories.ProductFactory(nom_service_public_numerique="ProConnect"),
        record="monthly active users",
        client="MetabaseClient",
        source_url="https://source-url.gouv.fr",
        frequence_monitoring="monthly",
    )
    responses.get(
        re.compile(
            r"https://source-url.gouv.fr",
        ),
        json={},
        status=status.HTTP_504_GATEWAY_TIMEOUT,
        content_type="application/json",
    )

    call_command("fetch_new_data")

    records = models.Record.objects.all()
    visio_record = records.filter(
        productid__slug="proconnect", indicateur="monthly active users"
    )
    assert not visio_record.exists()  # failing indicator created no record
    assert records.count() == 7  # other indicators worked fine
