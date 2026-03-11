"""
Unit tests for views
"""

import pytest
from core import factories
from django.urls import reverse
from django.test import Client


pytestmark = pytest.mark.django_db


def test_last_indicators_empty_ok():
    """Last indicators view should return even if no indicators to show."""
    client = Client()
    response = client.get(reverse("last_indicators"))
    assert response.status_code == 200


def test_last_indicators_indicators_ok():
    """Last indicators should be successfully returned."""
    indicators = factories.IndicatorFactory.create_batch(3)

    client = Client()
    response = client.get(reverse("last_indicators"))
    assert response.status_code == 200
    for indicator in indicators:
        assert str(indicator.indicateur) in response.content.decode("utf-8")
