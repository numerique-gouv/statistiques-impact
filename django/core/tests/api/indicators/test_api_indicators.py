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
    indicator = factories.IndicatorFactory()

    response = APIClient().get(f"/api/products/{indicator.productid}/indicators/")
    assert response.status_code == status.HTTP_200_OK
    import pdb

    pdb.set_trace()
    assert response.json() == {
        "id": indicator.id,
        "indicateur": indicator.indicator,
        "valeur": indicator.valeur,
        "unite_mesure": indicator.unite,
        "frequence_monitoring": indicator.frequence_monitoring,
        "date": indicator.date,
        "date_debut": indicator.date_debut,
        "est_periode": indicator.est_periode,
        "est_automatise": indicator.est_automatise,
        "productid": indicator.productid,
    }


@pytest.mark.parametrize("verb", ["post"])
def test_api_indicators_list__anonymous_read_only(verb):
    """Anonymous users should not be allowed to create products."""
    response = APIClient().post(
        "/api/products/", body="{'nom_service_public_numerique': 'product'}"
    )
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    assert not models.Product.objects.exists()
