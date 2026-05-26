"""
Unit tests for the records/ endpoint
"""

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from core import models, factories
from django.conf import settings
from django.test import override_settings

pytestmark = pytest.mark.django_db


# CREATE
def test_api_records_create__anonymous_cannot_create():
    """Anonymous users should not be allowed to create records."""
    product = factories.ProductFactory()

    response = APIClient().post(
        f"/api/products/{product.slug}/records/",
        body="{'nom_service_public_numerique': 'product'}",
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {
        "detail": "Informations d'authentification non fournies."
    }
    assert not models.Record.objects.exists()


def test_api_records_create__invalid_api_key_cannot_create():
    """Calls bearing an invalid api key should not be able to create records."""
    product = factories.ProductFactory()
    api_key, key = models.ProductAPIKey.objects.create_key(
        name="valid_key", product=product
    )

    response = APIClient().post(
        f"/api/products/{product.slug}/records/",
        {
            "indicateur": "participants",
            "valeur": 3,
            "unite_mesure": "unite",
            "frequence_monitoring": "mensuelle",
            "date": "2025-06-30",
            "date_debut": "2025-04-01",
            "est_periode": "true",
            "est_automatise": "false",
        },
        headers={"x-api-key": key + "ko"},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "Invalid API Key"}
    assert not models.Record.objects.exists()


def test_api_records_create__other_product_api_key_cannot_create():
    """Calls bearing another product's api key should not be able to create records."""
    product = factories.ProductFactory()
    _, valid_key = models.ProductAPIKey.objects.create_key(
        name="valid_key", product=product
    )

    # other product and its valid API key
    _, other_key = models.ProductAPIKey.objects.create_key(
        name="other_key", product=factories.ProductFactory()
    )

    response = APIClient().post(
        f"/api/products/{product.slug}/records/",
        {
            "indicateur": "participants",
            "valeur": 3,
            "unite_mesure": "unite",
            "frequence_monitoring": "mensuelle",
            "date": "2025-06-30",
            "date_debut": "2025-04-01",
            "est_periode": "true",
            "est_automatise": "false",
        },
        headers={"x-api-key": other_key},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "Wrong API Key"}
    assert not models.Record.objects.exists()


def test_api_records_create__valid_api_key_can_create():
    """Calls bearing a working API key for this product can create record for product."""
    product = factories.ProductFactory()
    api_key, key = models.ProductAPIKey.objects.create_key(
        name="valid_key", product=product
    )

    response = APIClient().post(
        f"/api/products/{product.slug}/records/",
        {
            "indicateur": "participants",
            "valeur": 3,
            "unite_mesure": "unite",
            "frequence_monitoring": "mensuelle",
            "date": "2025-06-30",
            "date_debut": "2025-04-01",
            "est_periode": "true",
            "est_automatise": "false",
        },
        headers={"x-api-key": key},
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert models.Record.objects.exists()


@override_settings(ADMIN_API_KEY="admin_key")
def test_api_records_create__admin_can_create():
    """Calls bearing the ADMIN API KEY can create record on any product."""
    products = factories.ProductFactory.create_batch(2)

    for product in products:
        response = APIClient().post(
            f"/api/products/{product.slug}/records/",
            {
                "indicateur": "participants",
                "valeur": 3,
                "unite_mesure": "unite",
                "frequence_monitoring": "mensuelle",
                "date": "2025-06-30",
                "date_debut": "2025-04-01",
                "est_periode": "true",
                "est_automatise": "false",
            },
            headers={"x-api-key": settings.ADMIN_API_KEY},
        )
        assert response.status_code == status.HTTP_201_CREATED
    assert models.Record.objects.count() == 2


def test_api_records_create__cannot_create_duplicate():
    """Should not be able to create duplicate records."""
    product = factories.ProductFactory()
    api_key, key = models.ProductAPIKey.objects.create_key(
        name="valid_key", product=product
    )
    data = {
        "indicateur": "participants",
        "valeur": 3,
        "unite_mesure": "unite",
        "frequence_monitoring": "mensuelle",
        "date": "2025-06-30",
        "date_debut": "2025-04-01",
        "est_periode": True,
        "est_automatise": False,
    }

    models.Record.objects.create(productid=product, **data)
    response = APIClient().post(
        f"/api/products/{product.slug}/records/",
        data,
        headers={"x-api-key": key},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == [
        "{'__all__': ['Un objet Record avec ces champs Productid, Indicateur, Frequence monitoring et Date existe déjà.']}"
    ]
    assert len(models.Record.objects.all()) == 1
