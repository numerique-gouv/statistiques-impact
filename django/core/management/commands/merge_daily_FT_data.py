"""Command to merge France Transfert csv"""

from django.core.management.base import BaseCommand
from datetime import date
from core.models import Adaptor


class Command(BaseCommand):
    """
    Management command to merge all France Transfert's very small csv into a
    single csv per type of data per month. This could also be made upon
    receiving file but this would multiply the download / upload
    """

    help = "Merge all daily files into monthly on France-transfert dataset"

    def add_arguments(self, parser):
        parser.add_argument(
            "month",
            nargs="?",
            type=str,
            default=str(date.today())[0:-3],
            help="Month you want to merge files of. Default is current month.",
        )

    def handle(self, *args, **options):
        """Call all adaptors to create indicators."""
        # self.stdout.write(self.style.SUCCESS("..."))
        month = options["month"]
        adaptor = Adaptor.objects.get(client="FranceTransfertClient")
        client = adaptor.get_client()

        dataset = client.get_dataset()
        client.merge_monthly_stats(dataset, month)
