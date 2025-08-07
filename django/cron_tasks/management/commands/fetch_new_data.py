"""Management command to fetch data from."""

from django.core.management.base import BaseCommand
from cron_tasks.adaptors.proconnect import ProConnectAdaptor


class Command(BaseCommand):
    """
    Management command to call all adaptators and create related indicators.
    """

    def handle(self, *args, **options):
        pc_adaptor = ProConnectAdaptor()
        pc_adaptor.fetch_latest_data()
