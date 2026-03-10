"""Management command to fetch data from."""

from django.core.management.base import BaseCommand
from core.utils.utils import get_last_month_limits
from core import models


class Command(BaseCommand):
    """
    Management command to call all adaptators and create related indicators.
    """

    def handle(self, *args, **options):
        """Call all adaptors to create indicators."""
        date_debut, date_fin = get_last_month_limits()
        self.stdout.write(
            f"Fetching indicators for last month ({date_debut} to {date_fin})"
        )

        for adaptor in models.Adaptor.objects.all():
            self.stdout.write(f"{str(adaptor.product)} - {str(adaptor.indicator)}")
            try:
                adaptor.save_last_month_indicator()
            except Exception as exc:
                self.stdout.write(
                    f'Failed to fetch new data for indicator "{adaptor.indicator}" on {adaptor.product}: {exc} '
                )
