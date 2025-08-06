"""Management command to fetch data from."""

from django.core.management.base import BaseCommand
from cron_tasks.adaptors.proconnect import ProConnectAdaptor


class Command(BaseCommand):
    """
    Management command to call all adaptators and create related indicators.
    """

    def handle(self, *args, **options):
        pc_adaptor = ProConnectAdaptor()
        pc_adaptor.create_indicator(pc_adaptor.indicators[0])
