"""
Unit tests for the product API
"""

import pytest
from rest_framework import status
from rest_framework.test import APIClient
from datetime import date, timedelta
from core import models, factories

pytestmark = pytest.mark.django_db


# LIST
def test_api_products_list__anonymous_ok():
    """Anonymous users should be allowed to list products."""
    product = factories.ProductFactory()

    response = APIClient().get("/api/products/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "nom_service_public_numerique": product.nom_service_public_numerique,
            "slug": product.slug,
        }
    ]


def test_api_products_list__anonymous_cant_create():
    """Anonymous users should not be allowed to create products."""
    response = APIClient().post(
        "/api/products/", body="{'nom_service_public_numerique': 'product'}"
    )

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    assert not models.Product.objects.exists()


# RETRIEVE
def test_api_products_retrieve__anonymous_ok():
    """Anonymous users should be allowed to retrieve info on a given product."""
    indicator = factories.IndicatorFactory()
    response = APIClient().get(f"/api/products/{indicator.productid.slug}/")
    assert response.status_code == status.HTTP_200_OK


def test_api_products_retrieve__last_indicators_ok():
    """Last indicators should be returned when retrieving Product's details."""
    indicator = factories.IndicatorFactory.create_batch(3)[0]
    product = indicator.productid

    # previous records of indicators should not be retrieve with product
    factories.IndicatorFactory(
        productid=product, date=date.fromisoformat(indicator.date) - timedelta(days=30)
    )

    response = APIClient().get(f"/api/products/{product.slug}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "last_indicators": [
            {
                "created_at": indicator.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "date": indicator.date,
                "date_debut": indicator.date_debut,
                "est_automatise": indicator.est_automatise,
                "est_periode": indicator.est_periode,
                "frequence_monitoring": indicator.frequence_monitoring,
                "id": str(indicator.id),
                "indicateur": indicator.indicateur,
                "productid": product.slug,
                "slug": indicator.slug,
                "unite_mesure": indicator.unite_mesure,
                "updated_at": indicator.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "valeur": int(indicator.valeur),
            }
            for indicator in product.last_indicators
        ],
        "nom_service_public_numerique": product.nom_service_public_numerique,
        "slug": product.slug,
    }


@pytest.mark.parametrize("verb", ["put", "patch", "delete"])
def test_api_products_retrieve__anonymous_read_only(verb):
    """Anonymous users should not be allowed to update or delete products."""
    product = factories.ProductFactory()

    response = getattr(APIClient(), verb)(
        f"/api/products/{product.slug}/",
        body="{'nom_service_public_numerique': 'product'}",
    )
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
