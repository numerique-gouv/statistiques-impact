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
        },
        {
            "name": "messages échangés",
            "frequency": "mensuelle",
            "method": "get_last_month_messages_count",
        },
    ]

    def get_last_month_data(self):
        """Grab latest values for all indicators."""
        for indicator in self.indicators:
            indicator["value"] = getattr(self, indicator["method"])()
        return self.indicators

    def get_last_month_active_users(self):
        """Fetch last month active users count from dedicated url."""
        url = "https://stats.tchap.incubateur.net/public/question/ae34205d-9010-4a00-b1bf-5d6a7c5901fb.json"
        response = requests.get(url)
        return int(response.json()[0]["Nombre de lignes"].replace(" ", ""))

    def get_last_month_messages_count(self):
        """Fetch last month exchanged messages count from dedicated url."""
        url = "https://stats.tchap.incubateur.net/public/question/84a9b0bc-c5a3-4aaa-b156-fc39791f23a5.json"
        response = requests.get(url)
        return int(response.json()[-1]["Somme de Events"].replace(" ", ""))
