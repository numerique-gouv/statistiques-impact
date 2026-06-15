"""
Unit tests for the records/ endpoint
"""

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from core import factories

pytestmark = pytest.mark.django_db


# LIST
def test_api_records_list__anonymous_ok():
    """Anonymous users should not be allowed to list record."""
    product = factories.ProductFactory()
    records = factories.RecordFactory.create_batch(2, productid=product)

    # record for another product. should not be listed
    factories.RecordFactory()

    response = APIClient().get(f"/api/products/{product.slug}/records/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2
    assert response.json() == sorted(
        [
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
            for record in records
        ],
        key=lambda x: x["date"],
        reverse=True,
    )


def test_api_records_list__filter_ok():
    """Can filter by indicateur."""
    product = factories.ProductFactory()
    factories.RecordFactory(indicateur="somethingelse", productid=product)
    record = factories.RecordFactory(
        indicateur="utilisateurs actifs", productid=product
    )

    response = APIClient().get(
        f"/api/products/{product.slug}/records/?indicateur=utilisateurs actifs"
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert response.json() == [
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
    ]
