"""Management command to fetch data from."""

from django.core.management.base import BaseCommand
from core.utils import utils
from core.adaptors import all_adaptors


class Command(BaseCommand):
    """
    Management command to call all adaptators and create related indicators.
    """

    def handle(self, *args, **options):
        """Call all adaptors to create indicators."""
        date_fin = utils.get_last_month_limits()[1]

        for adaptor in all_adaptors:
            adaptor = adaptor()
            try:
                # to catch ValueError possibly raised in adaptors
                for indicator in adaptor.get_last_month_data():
                    if "frequency" not in indicator:
                        indicator["frequency"] = "mensuelle"
                    adaptor.create_indicator(
                        name=indicator["name"],
                        date=date_fin,
                        value=indicator["value"],
                        frequency=indicator["frequency"],
                    )
            except ValueError:
                # should we log errors ?
                pass
