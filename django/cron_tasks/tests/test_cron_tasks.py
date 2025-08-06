"""
Unit tests for the product API
"""

import re
import pytest
from core import factories, models
from cron_tasks.adaptors import proconnect
import responses
from rest_framework import status
from django.core.management import call_command

pytestmark = pytest.mark.django_db


@responses.activate
def test_proconnect_active_users():
    factories.ProductFactory(nom_service_public_numerique="agent-connect")
    adaptor = proconnect.ProConnectAdaptor()

    # Mock successful response
    responses.get(
        re.compile(r".*/*.json"),
        b'[{"Time: Mois": "2024-02-01", "Valeurs distinctes de Sub Fi": "200000"}]',
        status=status.HTTP_200_OK,
        content_type="application/json",
    )

    new_entry = adaptor.create_indicator(adaptor.indicators[0])
    assert models.Indicator.objects.exists()
    assert new_entry.date == "2024-02-29"
    assert new_entry.date_debut == "2024-02-01"
    assert new_entry.valeur == 200000.0


@responses.activate
def test_commands_fetch_new_data(settings):
    settings.DEBUG = True
    product = factories.ProductFactory(nom_service_public_numerique="agent-connect")

    # Mock expected response
    responses.get(
        re.compile(r".*/*.json"),
        b'[{"Time: Mois": "2024-04-02", "Valeurs distinctes de Sub Fi": "200000"}]',
        status=status.HTTP_200_OK,
        content_type="application/json",
    )
    call_command("fetch_new_data")

    assert models.Indicator.objects.filter(
        productid=product, date="2024-04-30"
    ).exists()
