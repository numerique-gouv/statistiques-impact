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
    assert response.json() == [
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
    ]


def test_api_indicators_create__anonymous_cannot_create():
    """Anonymous users should not be allowed to create indicators."""
    product = factories.ProductFactory()

    response = APIClient().post(
        f"/api/products/{product.slug}/indicators/",
        body="{'nom_service_public_numerique': 'product'}",
    )
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    assert len(models.Product.objects.all()) == 1
