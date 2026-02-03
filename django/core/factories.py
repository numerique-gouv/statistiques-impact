"""
Test application factories
"""

import datetime
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
    indicateur = factory.Faker("text", max_nb_chars=30)
    valeur = random.randint(1, 300000)
    unite_mesure = "unite"
    frequence_monitoring = "mensuelle"
    date = factory.fuzzy.FuzzyDate(datetime.date(2025, 1, 1))
    est_periode = True
    est_automatise = random.choice([True, False])
    date_debut = ""


class AdaptorFactory(factory.django.DjangoModelFactory):
    """Factory for the Adaptor model."""

    class Meta:
        model = models.Adaptor

    product = factory.SubFactory(ProductFactory)
    indicator = factory.Faker("text", max_nb_chars=30)
    last_successful_run = factory.fuzzy.FuzzyDate(datetime.date(2025, 1, 1))
