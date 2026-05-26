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
        "last_records": [],
    }


def test_api_products_retrieve__last_records_ok():
    """Last records should be returned when retrieving Product's details."""
    product = factories.ProductFactory()
    factories.RecordFactory(productid=product, date="2025-06-30")
    most_recent_records = factories.RecordFactory.create_batch(
        2, productid=product, date="2025-07-30"
    )

    response = APIClient().get(f"/api/products/{product.slug}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "nom_service_public_numerique": product.nom_service_public_numerique,
        "slug": product.slug,
        "last_records": [
            {
                "id": str(record.id),
                "indicateur": record.indicateur,
                "slug": record.slug,
                "valeur": float(record.valeur),
                "unite_mesure": record.unite_mesure,
                "frequence_monitoring": record.frequence_monitoring,
                "date": str(record.date),
                "date_debut": str(record.date_debut),
                "est_periode": record.est_periode,
                "est_automatise": record.est_automatise,
                "productid": str(record.productid.id),
                "created_at": record.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "updated_at": record.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            }
            for record in most_recent_records
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
