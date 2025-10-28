import requests
from core.adaptors.base_adaptor import BaseAdaptor


class TchapAdaptor(BaseAdaptor):
    """Adaptor to fetch and send Tchap's indicators."""

    slug = "tchap"
    indicators = [
        {
            "name": "utilisateurs actifs",
            "frequency": "mensuelle",
            "method": "get_last_month_active_users",
        }
    ]

    def get_last_month_data(self):
        """Grab and push all indicators."""
        for indicator in self.indicators:
            indicator["value"] = getattr(self, indicator["method"])()
        return self.indicators

    def get_last_month_active_users(self):
        """Fetch last month active users count from designated url."""
        url = "https://stats.tchap.incubateur.net/public/question/ae34205d-9010-4a00-b1bf-5d6a7c5901fb.json"
        response = requests.get(url)
        return int(response.json()[0]["Nombre de lignes"].replace(" ", ""))
