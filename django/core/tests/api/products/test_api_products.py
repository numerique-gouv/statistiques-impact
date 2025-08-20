"""
Unit tests for the product API
"""

import pytest
from rest_framework import status
from rest_framework.test import APIClient

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
    product = factories.ProductFactory()

    response = APIClient().get(f"/api/products/{product.slug}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "nom_service_public_numerique": product.nom_service_public_numerique,
        "slug": product.slug,
        "last_indicators": [],
    }


def test_api_products_retrieve__last_indicators_ok():
    """Last indicators should be returned when retrieving Product's details."""
    product = factories.ProductFactory()
    factories.IndicatorFactory(productid=product, date="2025-06-30")
    most_recent_indicators = factories.IndicatorFactory.create_batch(
        2, productid=product, date="2025-07-30"
    )

    response = APIClient().get(f"/api/products/{product.slug}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "nom_service_public_numerique": product.nom_service_public_numerique,
        "slug": product.slug,
        "last_indicators": [
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
            for indicator in most_recent_indicators
        ],
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
