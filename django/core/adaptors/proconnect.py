import requests
from core.adaptors.base_adaptor import BaseAdaptor


class ProConnectAdaptor(BaseAdaptor):
    """Adaptor to fetch and send ProConnect's indicators."""

    slug = "proconnect"
    indicators = [
        {
            "name": "utilisateurs actifs",
            "frequency": "mensuelle",
            "method": "get_last_month_active_users",
        }
    ]

    def get_last_month_active_users(self):
        """Fetch data from url."""
        url = "https://stats.moncomptepro.beta.gouv.fr/public/question/cd934f6d-fb60-413b-a955-581859451141.json"
        response = requests.get(url)
        return int(response.json()[0]["Valeurs distinctes de Sub Fi"])
