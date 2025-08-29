"""
Tests for the messagerie adaptor
"""

import re
import pytest
from core import factories
from core.adaptors import messagerie
import responses
from rest_framework import status
from freezegun import freeze_time
from core.tests.adaptors import fixtures

pytestmark = pytest.mark.django_db


@freeze_time("2025-07-02")
@responses.activate
def test_messagerie_active_users():
    factories.ProductFactory(nom_service_public_numerique="messagerie")
    adaptor = messagerie.MessagerieAdaptor()

    # Mock data.gouv.fr API response
    responses.get(
        re.compile(adaptor.indicators[0]["url"]),
        body=fixtures.datagouv_messagerie_data,
        status=status.HTTP_200_OK,
        content_type="application/json",
    )

    assert adaptor.get_monthly_active_users() == 580
