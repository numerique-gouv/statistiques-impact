import requests
from cron_tasks import utils
from cron_tasks.adaptors.base_adaptor import BaseAdaptor


class ProConnectAdaptor(BaseAdaptor):
    """Adaptor to fetch and send ProConnect's indicators."""

    slug = "agent-connect"
    indicators = [
        {
            "name": "utilisateurs actifs",
            "frequency": "mensuelle",
            "url": "https://stats.moncomptepro.beta.gouv.fr/public/question/cd934f6d-fb60-413b-a955-581859451141.json",
        }
    ]

    def fetch_latest_data(self):
        """Grab and push all indicators."""
        for indicator in self.indicators:
            date, value = self._get_data(indicator["url"])
            return self.create_indicator(
                indicator["name"], date, value, indicator["frequency"]
            )

    def _get_data(self, url):
        """Fetch data from url."""
        response = requests.get(url)
        indicator_date = utils.get_last_day_of_month(response.json()[0]["Time: Mois"])
        value = response.json()[0]["Valeurs distinctes de Sub Fi"]
        return indicator_date, value
