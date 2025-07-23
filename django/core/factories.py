"""
Test application factories
"""

import factory.fuzzy
from faker import Faker

from core import models

fake = Faker()


class ProductFactory(factory.django.DjangoModelFactory):
    """A factory to create mail domain. Please not this is a factory to create mail domain with
    default values. So the status is pending and no mailbox can be created from it,
    until the mail domain is enabled."""

    class Meta:
        model = models.Product

    nom_service_public_numerique = factory.Faker("company", locale="fr_FR")
