"""
Unit tests for the product API
"""

import re
import pytest
from core import factories, models
from cron_tasks.adaptors import proconnect
from cron_tasks.adaptors.france_transfert import FranceTransfertAdaptor
import responses
from rest_framework import status
from django.core.management import call_command
from freezegun import freeze_time


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


@freeze_time("2025-10-02")
@responses.activate
def test_commands_fetch_new_data(settings):
    settings.DEBUG = True
    product = factories.ProductFactory(nom_service_public_numerique="agent-connect")
    factories.ProductFactory(
        nom_service_public_numerique="france-transfert",
        dataset_id="68b86764fd43cc1591faa6a5",
    )

    # Mock expected response
    responses.get(
        re.compile(r".*/*.json"),
        b'[{"Time: Mois": "2024-09-01", "Valeurs distinctes de Sub Fi": "200000"}]',
        status=status.HTTP_200_OK,
        content_type="application/json",
    )
    call_command("fetch_new_data")

    assert models.Indicator.objects.filter(productid__slug="france-transfert").count()

    assert models.Indicator.objects.filter(
        productid=product, date="2024-09-30"
    ).exists()


@freeze_time("2025-10-02")
def test_france_transfert_active_users():
    """Monthly retrieval should fetch csv files from data.gouv.fr and compute expected indicators."""
    factories.ProductFactory(
        nom_service_public_numerique="france-transfert",
        dataset_id="68b86764fd43cc1591faa6a5",
    )  # démo dataset = 68b86764fd43cc1591faa6a5

    ft_client = FranceTransfertAdaptor()
    result = ft_client.get_last_month_data()
    assert result == [
        {"name": "utilisateurs actifs (téléchargement)", "value": 1},
        {"name": "utilisateurs actifs (émission)", "value": 2},
        {"name": "utilisateurs actifs", "value": 3},
        {"name": "téléchargements", "value": 4},
        {"name": "plis émis", "value": 30},
    ]
