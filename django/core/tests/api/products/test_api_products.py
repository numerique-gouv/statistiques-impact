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
            "id": str(product.id),
            "nom_service_public_numerique": product.nom_service_public_numerique,
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

    response = APIClient().get(f"/api/products/{product.id}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": str(product.id),
        "nom_service_public_numerique": product.nom_service_public_numerique,
    }


@pytest.mark.parametrize("verb", ["put", "patch", "delete"])
def test_api_products_retrieve__anonymous_read_only(verb):
    """Anonymous users should not be allowed to update or delete products."""
    product = factories.ProductFactory()

    response = getattr(APIClient(), verb)(
        f"/api/products/{product.id}/",
        body="{'nom_service_public_numerique': 'product'}",
    )
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
