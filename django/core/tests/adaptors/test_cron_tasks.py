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
from core.tests import fixtures

pytestmark = pytest.mark.django_db


@freeze_time("2025-10-02")
@responses.activate
def test_commands_fetch_new_data(settings):
    settings.DEBUG = True
    products = ["proconnect", "messagerie"]
    for product in products:
        factories.ProductFactory(nom_service_public_numerique=product)
    factories.ProductFactory(
        nom_service_public_numerique="france-transfert",
        dataset_id="68b86764fd43cc1591faa6a5",
    )

    # Mock expected response
    responses.get(
        re.compile(r".*/*.json"),
        b'[{"Time: Mois": "2025-09-01", "Valeurs distinctes de Sub Fi": "200000"}]',
        status=status.HTTP_200_OK,
        content_type="application/json",
    )
    responses.get(
        re.compile(r"https://www.data.gouv.fr/*"),
        body=fixtures.datagouv_messagerie_data.replace("2025-07", "2025-10"),
        status=status.HTTP_200_OK,
        content_type="application/json",
    )
    call_command("fetch_new_data")

    assert (
        models.Indicator.objects.filter(
            productid__slug="proconnect", date="2025-09-30"
        ).count()
        == 1
    )
    assert (
        models.Indicator.objects.filter(
            productid__slug="messagerie", date="2025-09-30"
        ).count()
        == 1
    )
    assert (
        models.Indicator.objects.filter(
            productid__slug="france-transfert", date="2025-09-30"
        ).count()
        == 10
    )
