"""
Unit tests for admin actions
"""

from django.urls import reverse

import pytest

from core import factories, models
from rest_framework import status
import responses
import re

pytestmark = pytest.mark.django_db


@responses.activate
def test_admin_fetch_adds_indicators(client, metabase_lasuite_MAU):
    """Test admin action to check health of some domains"""
    adaptor = factories.AdaptorFactory.create(
        product=factories.ProductFactory(nom_service_public_numerique="proconnect"),
        indicator="monthly active users",
        client="MetabaseClient",
        source_url="https://stats.moncomptepro.beta.gouv.fr/public/question/single-product-question.json",
    )

    # Mock successful response
    responses.get(
        re.compile(r".*/*.json"),
        json=[{"Time: Mois": "2026-02-01", "Valeurs distinctes de Sub Fi": 343349}],
        status=status.HTTP_200_OK,
        content_type="application/json",
    )

    admin = factories.UserFactory(is_staff=True)
    client.force_login(admin)

    data = {
        "action": "fetch_newest_data",
        "_selected_action": [
            adaptor.id,
        ],
    }
    url = reverse("admin:core_adaptor_changelist")
    response = client.post(url, data, follow=True)
    assert response.status_code == status.HTTP_200_OK

    adaptor.refresh_from_db()
    assert models.Indicator.objects.count() == 6
