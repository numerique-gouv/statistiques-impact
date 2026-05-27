"""
Tests for the records endpoint
"""

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from core import factories

pytestmark = pytest.mark.django_db


def test_api_records_retrieve__anonymous_ok():
    """Anonymous users should be allowed to retrieve records."""
    record = factories.RecordFactory()
    indicator = record.indicator
    factories.RecordFactory(indicator=indicator)

    response = APIClient().get(
        f"/api/products/{indicator.productid.slug}/indicators/{indicator.slug}/records/{record.id}/",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": str(record.id),
        "indicator": {
            "productid": indicator.productid.slug,
            "slug": indicator.slug,
        },
        "valeur": float(record.valeur),
        "date": str(record.date),
        "date_debut": str(record.date_debut),
        "est_automatise": record.est_automatise,
        "created_at": record.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "updated_at": record.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
    }
