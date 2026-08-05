"""Management command to fill database with some demo objects."""

from core import models, utils, factories
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


User = get_user_model()
services = ["liberte connect", "mon france egalité", "adelphie.gouv.fr"]


class Command(BaseCommand):
    """
    Management command populate local database and ease development
    """

    def handle(self, *args, **options):
        user = User.objects.filter(username="admin")
        if not user.exists():
            User.objects.create_superuser(
                username="admin",
                email="",
                password="admin",
                is_staff=True,
                is_active=True,
            )
        else:
            user[0].is_superuser = True
            user[0].save()

        for service in services:
            product, _ = models.Product.objects.get_or_create(name=service)
            for i in range(0, 5):
                indicator = factories.IndicatorFactory(productid=product)

                for month in range(1, 13):
                    factories.RecordFactory(
                        indicator=indicator,
                        end_date=utils.utils.get_last_day_of_month(
                            f"2026-{format(month, '02d')}-01"
                        ),
                    )

        print("Demo objects created.")
