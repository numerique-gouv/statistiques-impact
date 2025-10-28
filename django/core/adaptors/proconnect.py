import requests
from core.adaptors.base_adaptor import BaseAdaptor


class ProConnectAdaptor(BaseAdaptor):
    """Adaptor to fetch and send ProConnect's indicators."""

    slug = "proconnect"
    indicators = [
        {
            "name": "utilisateurs actifs",
            "frequency": "mensuelle",
            "url": "https://stats.moncomptepro.beta.gouv.fr/public/question/cd934f6d-fb60-413b-a955-581859451141.json",
        }
    ]

    def get_last_month_data(self):
        """Grab and push all indicators."""
        self.indicators[0]["value"] = self._get_data(self.indicators[0]["url"])
        return self.indicators

    def _get_data(self, url):
        """Fetch data from url."""
        response = requests.get(url)
        return int(response.json()[0]["Valeurs distinctes de Sub Fi"])
