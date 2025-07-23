"""
Unit tests for the product API
"""

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from core import models, factories

pytestmark = pytest.mark.django_db


def test_api_products__list_anonymous():
    """Anonymous users should not be allowed to list mailboxes."""
    product = factories.ProductFactory()

    response = APIClient().get("/api/products/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "id": str(product.id),
            "nom_service_public_numerique": product.nom_service_public_numerique,
        }
    ]


@pytest.mark.parametrize("verb", ["post", "put", "patch", "delete"])
def test_api_products_anonymous_forbidden(verb):
    """Anonymous users should not be allowed to create products."""
    response = getattr(APIClient(), verb)(
        "/api/products/", body="{'nom_service_public_numerique': 'product'}"
    )
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    assert not models.Product.objects.exists()
