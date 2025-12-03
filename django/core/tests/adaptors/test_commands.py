"""
Unit tests for the product API
"""

import re
import json
import pytest
from core import factories, models
import responses
from rest_framework import status
from django.core.management import call_command
from freezegun import freeze_time
from core.tests import fixtures

pytestmark = pytest.mark.django_db


# FETCH_NEW_DATA
@freeze_time("2025-10-02")
@responses.activate
def test_commands_fetch_new_data_ok(settings):
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

    # Mock expected response
    responses.get(
        re.compile(
            r"https://stats.moncomptepro.beta.gouv.fr/public/question/cd934f6d-*"
        ),
        b'[{"Time: Mois": "2025-09-01", "Valeurs distinctes de Sub Fi": "200000"}]',
        status=status.HTTP_200_OK,
        content_type="application/json",
    )
    responses.get(
        re.compile(
            r"https://stats.moncomptepro.beta.gouv.fr/public/question/0e3cee98-*"
        ),
        json=[
            {"Fournisseur Service": "Tchap", "Valeurs distinctes de Sub Fi": 27654},
            {
                "Fournisseur Service": "DINUM - RESANA",
                "Valeurs distinctes de Sub Fi": 23323,
            },
            {"Fournisseur Service": "Grist", "Valeurs distinctes de Sub Fi": 16094},
            {"Fournisseur Service": "Docs", "Valeurs distinctes de Sub Fi": 11515},
            {"Fournisseur Service": "Visio", "Valeurs distinctes de Sub Fi": 8184},
            {"Fournisseur Service": "Fichiers", "Valeurs distinctes de Sub Fi": 1771},
            {
                "Fournisseur Service": "Messagerie de la Suite Numérique",
                "Valeurs distinctes de Sub Fi": 1155,
            },
        ],
        status=status.HTTP_200_OK,
        content_type="application/json",
    )
    responses.get(
        re.compile(r"https://www.data.gouv.fr/*"),
        body=fixtures.datagouv_messagerie_data.replace("2025-07", "2025-10"),
        status=status.HTTP_200_OK,
        content_type="application/json",
    )
    responses.get(
        re.compile(r"https://stats.tchap.incubateur.net/public/question/ae34205d-*"),
        json=[{"Visit Date": "sept., 2025", "Nombre de lignes": "367 146"}],
        status=status.HTTP_200_OK,
        content_type="application/json",
    )
    responses.get(
        re.compile(r"https://stats.tchap.incubateur.net/public/question/84a9b0bc-*"),
        json=[
            {"Hour": "août, 2025", "Somme de Events": "5 404 085"},
            {"Hour": "sept., 2025", "Somme de Events": "10 877 632"},
        ],
        status=status.HTTP_200_OK,
        content_type="application/json",
    )
    responses.get(
        re.compile(r"https://eu.posthog.com*"),
        json={
            "id": 65340,
            "name": "Monthly Active Users",
            "result": [
                {
                    "data": [5728, 3985, 8458, 7533],
                    "days": ["2025-07-01", "2025-08-01", "2025-09-01", "2025-10-01"],
                }
            ],
        },
        status=status.HTTP_200_OK,
        content_type="application/json",
    )
    call_command("fetch_new_data")

    indicators = models.Indicator.objects.filter(date="2025-09-30")
    assert indicators.filter(productid__slug="proconnect").count() == 1
    assert indicators.filter(productid__slug="messagerie").count() == 2
    assert indicators.filter(productid__slug="france-transfert").count() == 10
    assert indicators.filter(productid__slug="tchap").count() == 2
    assert indicators.filter(productid__slug="visio").count() == 2
    assert indicators.filter(productid__slug="resana").count() == 1
    assert indicators.filter(productid__slug="grist").count() == 1
    assert indicators.filter(productid__slug="docs").count() == 1
    assert indicators.filter(productid__slug="fichiers").count() == 1
    assert not models.Indicator.objects.exclude(date="2025-09-30").exists()


@freeze_time("2025-10-02")
@responses.activate
def test_commands_fetch_new_data_continues_when_adaptor_exception(settings):
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

    # Mock expected response
    responses.get(
        re.compile(
            r"https://stats.moncomptepro.beta.gouv.fr/public/question/cd934f6d-*"
        ),
        b'[{"Time: Mois": "2025-09-01", "Valeurs distinctes de Sub Fi": "200000"}]',
        status=status.HTTP_200_OK,
        content_type="application/json",
    )
    responses.get(
        re.compile(
            r"https://stats.moncomptepro.beta.gouv.fr/public/question/0e3cee98-*"
        ),
        json=[
            {"Fournisseur Service": "Tchap", "Valeurs distinctes de Sub Fi": 27654},
            {
                "Fournisseur Service": "DINUM - RESANA",
                "Valeurs distinctes de Sub Fi": 23323,
            },
            {"Fournisseur Service": "Grist", "Valeurs distinctes de Sub Fi": 16094},
            {"Fournisseur Service": "Docs", "Valeurs distinctes de Sub Fi": 11515},
            {"Fournisseur Service": "Visio", "Valeurs distinctes de Sub Fi": 8184},
            {"Fournisseur Service": "Fichiers", "Valeurs distinctes de Sub Fi": 1771},
            {
                "Fournisseur Service": "Messagerie de la Suite Numérique",
                "Valeurs distinctes de Sub Fi": 1155,
            },
        ],
        status=status.HTTP_200_OK,
        content_type="application/json",
    )
    responses.get(
        re.compile(r"https://www.data.gouv.fr/*"),
        body=fixtures.datagouv_messagerie_data.replace("2025-07", "2025-10"),
        status=status.HTTP_200_OK,
        content_type="application/json",
    )
    responses.get(
        re.compile(r"https://stats.tchap.incubateur.net/public/question/ae34205d-*"),
        body=json.dumps([{"Visit Date": "sept., 2025", "Nombre de lignes": "367 146"}]),
        status=status.HTTP_200_OK,
        content_type="application/json",
    )
    responses.get(
        re.compile(r"https://stats.tchap.incubateur.net/public/question/84a9b0bc-*"),
        json=[
            {"Hour": "août, 2025", "Somme de Events": "5 404 085"},
            {"Hour": "sept., 2025", "Somme de Events": "10 877 632"},
        ],
        status=status.HTTP_200_OK,
        content_type="application/json",
    )
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
