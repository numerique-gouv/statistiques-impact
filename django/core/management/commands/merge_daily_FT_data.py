"""Command to merge France Transfert csv"""

from django.conf import settings
from django.core.management.base import BaseCommand
from core.utils.datagouv_client import DataGouvClient
from core.adaptors import FranceTransfertAdaptor
from datetime import date


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
        adaptor = FranceTransfertAdaptor()
        dataset_id = adaptor.product.dataset_id
        client = DataGouvClient()

        if dataset_id == "68b86764fd43cc1591faa6a5":
            client.api_key = settings.DATAGOUV_DEMO_API_KEY
            client.env = "demo"
            client.api_url = "https://demo.data.gouv.fr/api/1"

        self.stdout.write(
            f'Starting merge job for month {month} on dataset "{dataset_id}".'
        )
        dataset = client.get_dataset(dataset_id)
        client.merge_monthly_stats(dataset, month)
