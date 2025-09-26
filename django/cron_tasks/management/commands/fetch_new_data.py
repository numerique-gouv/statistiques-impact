"""Management command to fetch data from."""

from django.core.management.base import BaseCommand
from cron_tasks.adaptors.proconnect import ProConnectAdaptor
from cron_tasks.adaptors.france_transfert import FranceTransfertAdaptor
from cron_tasks import utils


class Command(BaseCommand):
    """
    Management command to call all adaptators and create related indicators.
    """

    def handle(self, *args, **options):
        """Call all adaptors to create indicators."""
        date_fin = utils.get_last_month_limits()[1]
        pc_adaptor = ProConnectAdaptor()
        pc_adaptor.fetch_latest_data()

        ft_adaptor = FranceTransfertAdaptor()
        data = ft_adaptor.get_last_month_data()
        [
            ft_adaptor.create_indicator(
                indicator["name"], date_fin, indicator["value"], "mensuelle"
            )
            for indicator in data
        ]
