"""
Unit tests for the indicators/ endpoint
"""

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from core import models, factories

pytestmark = pytest.mark.django_db


# LIST
def test_api_indicators_list__anonymous_ok():
    """Anonymous users should not be allowed to list indicators."""
    product = factories.ProductFactory()
    indicators = factories.IndicatorFactory.create_batch(2, productid=product)

    # indicator for another product. should not be listed
    factories.IndicatorFactory()

    response = APIClient().get(f"/api/products/{product.slug}/indicators/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2
    assert response.json() == sorted(
        [
            {
                "id": str(indicator.id),
                "indicateur": indicator.indicateur,
                "valeur": indicator.valeur,
                "unite_mesure": indicator.unite_mesure,
                "frequence_monitoring": indicator.frequence_monitoring,
                "date": str(indicator.date),
                "date_debut": str(indicator.date_debut),
                "est_periode": indicator.est_periode,
                "est_automatise": indicator.est_automatise,
                "productid": str(indicator.productid.id),
            }
            for indicator in indicators
        ],
        key=lambda x: x["date"],
        reverse=True,
    )


# CREATE
def test_api_indicators_create__anonymous_cannot_create():
    """Anonymous users should not be allowed to create indicators."""
    product = factories.ProductFactory()

    response = APIClient().post(
        f"/api/products/{product.slug}/indicators/",
        body="{'nom_service_public_numerique': 'product'}",
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert not models.Indicator.objects.exists()


def test_api_indicators_create__invalid_api_key_cannot_create():
    """Calls bearing an invalid api key should not be able to create indicators."""
    product = factories.ProductFactory()
    api_key, key = models.ProductAPIKey.objects.create_key(
        name="valid_key", product=product
    )

    response = APIClient().post(
        f"/api/products/{product.slug}/indicators/",
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
    assert not models.Indicator.objects.exists()


def test_api_indicators_create__valid_api_key_can_create():
    """Calls bearing a working API key for this product can create indicator for product."""
    product = factories.ProductFactory()
    api_key, key = models.ProductAPIKey.objects.create_key(
        name="valid_key", product=product
    )

    response = APIClient().post(
        f"/api/products/{product.slug}/indicators/",
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
    assert models.Indicator.objects.exists()


def test_api_indicators_create__cannot_create_duplicate():
    """Should not be able to create duplicate."""
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

    models.Indicator.objects.create(productid=product, **data)
    response = APIClient().post(
        f"/api/products/{product.slug}/indicators/",
        data,
        headers={"x-api-key": key},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == [
        "{'__all__': ['Un objet Indicator avec ces champs Productid, Indicateur, Frequence monitoring et Date existe déjà.']}"
    ]
    assert len(models.Indicator.objects.all()) == 1


# RETRIEVE
def test_api_indicators_retrieve__anonymous_ok():
    """Anonymous users should be allowed to delete indicators."""
    indicator = factories.IndicatorFactory()

    response = APIClient().get(
        f"/api/products/{indicator.productid.slug}/indicators/{indicator.id}/",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": str(indicator.id),
        "indicateur": indicator.indicateur,
        "valeur": indicator.valeur,
        "unite_mesure": indicator.unite_mesure,
        "frequence_monitoring": indicator.frequence_monitoring,
        "date": str(indicator.date),
        "date_debut": str(indicator.date_debut),
        "est_periode": indicator.est_periode,
        "est_automatise": indicator.est_automatise,
        "productid": str(indicator.productid.id),
    }


# DELETE
def test_api_indicators_delete__anonymous_cannot_delete():
    """Anonymous users should not be allowed to delete indicators."""
    indicator = factories.IndicatorFactory()

    response = APIClient().delete(
        f"/api/products/{indicator.productid.slug}/indicators/{indicator.id}/",
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert models.Indicator.objects.exists()


def test_api_indicators_delete__invalid_api_key_cannot_delete():
    """Calls bearing an invalid API key should not be able to delete indicators."""
    indicator = factories.IndicatorFactory()
    api_key, key = models.ProductAPIKey.objects.create_key(
        name="valid_key", product=indicator.productid
    )

    response = APIClient().delete(
        f"/api/products/{indicator.productid.slug}/indicators/{indicator.id}/",
        headers={"x-api-key": key + "ko"},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert models.Indicator.objects.exists()


def test_api_indicators_delete__valid_api_key_can_delete():
    """Calls bearing a valid API key for this product can delete indicator for product."""
    indicator = factories.IndicatorFactory()
    api_key, key = models.ProductAPIKey.objects.create_key(
        name="valid_key", product=indicator.productid
    )

    response = APIClient().delete(
        f"/api/products/{indicator.productid.slug}/indicators/{indicator.id}/",
        headers={"x-api-key": key},
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not models.Indicator.objects.exists()
