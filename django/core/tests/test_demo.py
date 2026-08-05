import pytest
from core import models
from django.core.management import call_command
from django.contrib.auth import get_user_model

User = get_user_model()
pytestmark = pytest.mark.django_db


def test_demo():
    call_command("demo")

    assert User.objects.filter(is_staff=True).count() == 1
    assert models.Product.objects.count() == 3
    assert models.Indicator.objects.count() == 15
    assert models.Record.objects.count() == 180
