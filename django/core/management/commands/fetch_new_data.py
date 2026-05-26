"""Management command to fetch data from."""

from django.core.management.base import BaseCommand
from core.utils.utils import get_last_month_limits
from core import models


class Command(BaseCommand):
    """
    Management command to call all adaptators and create related records.
    """

    def handle(self, *args, **options):
        """Call all adaptors to create records."""
        date_debut, date_fin = get_last_month_limits()
        self.stdout.write(
            f"Fetching records for last month ({date_debut} to {date_fin})"
        )

        for adaptor in models.Adaptor.objects.all():
            self.stdout.write(f"{str(adaptor.product)} - {str(adaptor.record)}")
            try:
                adaptor.save_last_month_record()
            except Exception as exc:
                self.stdout.write(
                    f'Failed to fetch new data for record "{adaptor.record}" on {adaptor.product}: {exc} '
                )
