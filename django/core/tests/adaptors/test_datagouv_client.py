"""Test every clients."""

import pytest
import responses
from freezegun import freeze_time

from core import factories

pytestmark = pytest.mark.django_db


# MESSAGERIE
@freeze_time("2025-07-02")
@responses.activate
def test_messagerie_active_users(datagouv_messagerie_data):
    """Checks that DataGouvClient retrieves data.gouv data as expected."""
    adaptor = factories.AdaptorFactory.create(
        product=factories.ProductFactory(
            name="messagerie",
            dataset_id="68650cd6130c82da6ba44a92",
        ),
        indicator="monthly active users",
        client="MessagerieClient",
    )

    # Responses mocked in fixtures
    assert adaptor.get_data() == [
        {
            "product": adaptor.product.name,
            "indicator": adaptor.indicator,
            "value": 580,
        }
    ]
