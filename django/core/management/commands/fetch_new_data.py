"""Management command to fetch data from."""

from django.core.management.base import BaseCommand
from core.utils.utils import get_last_month_limits, create_indicator
from core import models


class Command(BaseCommand):
    """
    Management command to call all adaptators and create related indicators.
    """

    def handle(self, *args, **options):
        """Call all adaptors to create indicators."""
        date_fin = get_last_month_limits()[1]
        self.stdout.write("Fetching last month's indicators")

        for adaptor in models.Adaptor.objects.all():
            import pdb

            pdb.set_trace()
            adaptor_method = getattr(APIClient(), "get_last_month_data")
            # adaptor.method
            self.stdout.write(f"{str(adaptor.product)}")
            import pdb

            pdb.set_trace()
            for indicator in adaptor_method.get_last_month_data():
                self.stdout.write(f"\t{indicator['name']}")
                if "frequency" not in indicator:
                    indicator["frequency"] = "mensuelle"

                if "product" in indicator:
                    product = indicator["product"]
                else:
                    product = adaptor_method.product
            try:
                create_indicator(
                    product=product,
                    name=indicator["name"],
                    date=date_fin,
                    value=indicator["value"],
                    frequency=indicator["frequency"],
                )
            except ValueError:
                self.stdout.write(
                    f"ValueError occured when trying to create indicator {indicator['name']}"
                )
                pass
