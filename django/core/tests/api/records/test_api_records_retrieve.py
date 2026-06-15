"""
Unit tests for the records/ endpoint
"""

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from core import factories

pytestmark = pytest.mark.django_db


# RETRIEVE
def test_api_records_retrieve__anonymous_ok():
    """Anonymous users should be allowed to retrieve a specific records."""
    record = factories.RecordFactory()

    # same product, other record : should not appear
    factories.RecordFactory(productid=record.productid)
    # other product, same name record : should not appear
    factories.RecordFactory.create_batch(2, indicateur=record.indicateur)

    response = APIClient().get(
        f"/api/products/{record.productid.slug}/records/{record.slug}/",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
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
