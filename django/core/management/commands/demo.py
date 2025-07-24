"""Management command to fill database with some demo objects."""

import random
from core import models

services = ["service connect", "mon france pro"]

for service in services:
    product = models.Product.objects.get_or_create(nom_service_public_numerique=service)
    for i in range(0, 5):
        models.Indicator.objects.create(
            productid=product[0],
            indicateur=random.choice(
                ["utilisateurs actifs", "indicateur2", "autre_indicateur"]
            ),
            valeur=random.randint(1, 300000),
            unite_mesure="unite",
            frequence_monitoring="mensuelle",
            date=f"2025-{format(random.randint(1, 12), '02d')}-30",
            est_periode=True,
            est_automatise=random.choice([True, False]),
            date_debut="",
        )
