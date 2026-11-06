"""
Test application factories
"""

import datetime
import random

import factory.fuzzy
from faker import Faker

from core import models

fake = Faker()


class ProductFactory(factory.django.DjangoModelFactory):
    """Factory for the Product model."""

    class Meta:
        model = models.Product

    name = factory.Faker("company", locale="fr_FR")


class IndicatorFactory(factory.django.DjangoModelFactory):
    """Factory for the Indicator model."""

    class Meta:
        model = models.Indicator

    productid = factory.SubFactory(ProductFactory)
    indicateur = factory.Faker("text", max_nb_chars=30)
    unite_mesure = "unite"
    frequence_monitoring = "mensuelle"
    est_periode = True
    est_automatise = random.choice([True, False])


class AdaptorFactory(factory.django.DjangoModelFactory):
    """Factory for the Adaptor model."""

    class Meta:
        model = models.Adaptor

    product = factory.SubFactory(ProductFactory)
    indicator = factory.Faker("text", max_nb_chars=30)


class RecordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Record

    indicator = factory.SubFactory(IndicatorFactory)
    value = random.randint(1, 300000)
    end_date = factory.fuzzy.FuzzyDate(datetime.date(2025, 1, 1))
    start_date = None
    is_auto_added = random.choice([True, False])


class FTUsageLogsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.FTUsageLogs

    date = factory.fuzzy.FuzzyDate(datetime.date(2025, 1, 1))
    domaine_expediteur = factory.Faker("domain_name")
    domaine_destinataire = factory.Faker("domain_name")
    taille = factory.fuzzy.FuzzyInteger(0, 999999999)
    hash_expe = factory.Faker("uuid4")
    type_action = random.choice(["download", "upload"])
    is_demo = False


class FTSatisfactionLogsFactory(factory.django.DjangoModelFactory):
    """
    Save satisfaction logs submitted by Acton on francetransfert/submission endpoint.
    """

    class Meta:
        model = models.FTSatisfactionLogs

    date = factory.fuzzy.FuzzyDate(datetime.date(2025, 1, 1))
    commentaire = factory.Faker("sentence")
    note = random.choice([1, 2, 3])
    type_satisfaction = random.choice(["download", "upload"])
    domaine = factory.Faker("domain_name")
    is_demo = False
