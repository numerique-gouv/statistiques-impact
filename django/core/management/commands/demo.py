"""Management command to fill database with some demo objects."""

import random
from core import models
from django.core.management.base import BaseCommand


services = ["service connect", "mon france pro"]


class Command(BaseCommand):
    """
    Management command populate local database and ease development
    """

    def handle(self, *args, **options):
        for service in services:
            product, is_created = models.Product.objects.get_or_create(
                nom_service_public_numerique=service
            )
            for i in range(1, 13):
                models.Indicator.objects.create(
                    productid=product,
                    indicateur=random.choice(
                        ["utilisateurs actifs", "indicateur2", "autre_indicateur"]
                    ),
                    valeur=random.randint(1, 300000),
                    unite_mesure="unite",
                    frequence_monitoring="mensuelle",
                    date=f"2024-{format(i, '02d')}-30",
                    est_periode=True,
                    est_automatise=random.choice([True, False]),
                    date_debut="",
                )
