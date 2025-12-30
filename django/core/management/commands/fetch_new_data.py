"""Management command to fetch data from."""

from django.core.management.base import BaseCommand
from core.utils.utils import get_last_month_limits, create_indicator
from core.adaptors import all_adaptors


class Command(BaseCommand):
    """
    Management command to call all adaptators and create related indicators.
    """

    def handle(self, *args, **options):
        """Call all adaptors to create indicators."""
        date_fin = get_last_month_limits()[1]
        self.stdout.write("Fetching last month's indicators")

        for adaptor in all_adaptors:
            adaptor = adaptor()
            self.stdout.write(f"{str(adaptor)}")
            try:
                # to catch ValueError possibly raised in adaptors
                for indicator in adaptor.get_last_month_data():
                    self.stdout.write(f"\t{indicator['name']}")
                    if "frequency" not in indicator:
                        indicator["frequency"] = "mensuelle"

                    if "product" in indicator:
                        product = indicator["product"]
                    else:
                        product = adaptor.product

                    create_indicator(
                        product=product,
                        name=indicator["name"],
                        date=date_fin,
                        value=indicator["value"],
                        frequency=indicator["frequency"],
                    )
            except ValueError:
                self.stdout.write("ValueError occurred.")
                pass
