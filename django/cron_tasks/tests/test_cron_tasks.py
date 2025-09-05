"""
Unit tests for the product API
"""

import re
import pytest
from core import factories, models
from cron_tasks.adaptors import proconnect, messagerie
import responses
from rest_framework import status
from django.core.management import call_command
from cron_tasks.tests import fixtures
import json

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

    new_entry = adaptor.fetch_latest_data()
    assert models.Indicator.objects.exists()
    assert new_entry.date == "2024-02-29"
    assert new_entry.date_debut == "2024-02-01"
    assert new_entry.valeur == 200000.0


@responses.activate
def test_commands_fetch_new_data():
    products = ["agent-connect", "messagerie"]
    for product in products:
        factories.ProductFactory(nom_service_public_numerique=product)

    # Mock expected response
    responses.get(
        re.compile(r".*/*.json"),
        b'[{"Time: Mois": "2024-04-02", "Valeurs distinctes de Sub Fi": "200000"}]',
        status=status.HTTP_200_OK,
        content_type="application/json",
    )
    responses.get(
        re.compile(r".*/*/data/"),
        body=json.dumps(fixtures.messagerie_response),
        status=status.HTTP_200_OK,
        content_type="application/json",
    )
    call_command("fetch_new_data")

    assert models.Indicator.objects.filter(
        productid__slug="agent-connect", date="2024-04-30"
    ).exists()
    assert models.Indicator.objects.filter(
        productid__slug="messagerie", date="2025-06-30"
    ).exists()


@responses.activate
def test_messagerie_active_users():
    factories.ProductFactory(nom_service_public_numerique="messagerie")
    adaptor = messagerie.MessagerieAdaptor()

    # Mock data.gouv.fr API response
    responses.get(
        re.compile(adaptor.indicators[0]["url"]),
        body=json.dumps(fixtures.messagerie_response),
        status=status.HTTP_200_OK,
        content_type="application/json",
    )

    new_entry = adaptor.fetch_latest_data()
    assert models.Indicator.objects.exists()
    assert new_entry[0].date == "2025-06-30"
    assert new_entry[0].date_debut == "2025-06-01"
    assert new_entry[0].valeur == 580.0
