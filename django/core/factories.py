"""
Test application factories
"""

import factory.fuzzy
from faker import Faker
import random

from core import models

fake = Faker()


class ProductFactory(factory.django.DjangoModelFactory):
    """Factory for the Product model."""

    class Meta:
        model = models.Product

    nom_service_public_numerique = factory.Faker("company", locale="fr_FR")


class IndicatorFactory(factory.django.DjangoModelFactory):
    """Factory for the Indicator model."""

    class Meta:
        model = models.Indicator

    productid = factory.SubFactory(ProductFactory)
    indicateur = "utilisateurs actifs"
    valeur = random.randint(1, 300000)
    unite_mesure = "unite"
    frequence_monitoring = "mensuelle"
    date = f"2025-{format(random.randint(1, 12), '02d')}-30"
    est_periode = True
    est_automatise = random.choice([True, False])
    date_debut = ""
