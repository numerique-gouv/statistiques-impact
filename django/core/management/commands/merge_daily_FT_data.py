"""Command to merge France Transfert csv"""

from django.conf import settings
from django.core.management.base import BaseCommand
from core.utils import utils
from core.utils.datagouv_client import DataGouvClient
from core.adaptors import FranceTransfertAdaptor


class Command(BaseCommand):
    """
    Management command to merge all France Transfert's very small csv into a
    single csv per type of data per month. This could also be made upon
    receiving file but this would multiply the download / upload
    """

    def handle(self, *args, **options):
        """Call all adaptors to create indicators."""
        adaptor = FranceTransfertAdaptor()
        dataset_id = adaptor.product.dataset_id
        client = DataGouvClient()

        if dataset_id == "68b86764fd43cc1591faa6a5":
            client.api_key = settings.DATAGOUV_DEMO_API_KEY
            client.env = "demo"
            client.api_url = "https://demo.data.gouv.fr/api/1"

        month = str(utils.get_last_month_limits()[0])[0:-3]
        dataset = client.get_dataset(dataset_id)
        client.merge_monthly_stats(dataset, month)
