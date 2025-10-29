import requests
from core.adaptors.base_adaptor import BaseAdaptor
import io
from pandas import read_csv
from datetime import date


class MessagerieAdaptor(BaseAdaptor):
    """Adaptor to fetch and send ProConnect's indicators."""

    slug = "messagerie"
    indicators = [
        {
            "name": "utilisateurs actifs 30 derniers jours",
            "frequency": "mensuelle",
            "method": "get_last_month_active_users",
        }
    ]

    def get_last_month_active_users(self):
        """Get a specific date's active users from messagerie's dataset on data.gouv.fr."""
        url = "https://www.data.gouv.fr/api/1/datasets/r/f5d3d162-d485-4bed-94bc-96679d299747"
        response = requests.get(url)
        as_csv = read_csv(
            io.StringIO(response.content.decode("utf-8")), skipinitialspace=True
        )

        entry = as_csv[as_csv["yyyy-mm-dd"] == str(date.today().replace(day=1))]
        if len(entry) == 1:
            return int(entry["sur les 30 derniers jours"])
        else:
            return None
