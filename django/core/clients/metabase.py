import requests
from core.clients.client_base import ClientBase


class MetabaseClient(ClientBase):
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


class TchapClient(ClientBase):
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


class MetabaseMultipleProductsClient(MetabaseClient):
    """Adaptor to fetch LaSuite's basic indicators."""

    indicators_types = [
        {
            "name": "utilisateurs actifs",
            "frequency": "mensuelle",
        }
    ]
    indicators = []

    def __init__(self):
        self.name = "LaSuite"

    def get_last_month_data(self):
        """Get latest values for all indicators."""
        values = self.get_last_month_active_users()

        for product in values:
            this_indicator = {}
            product_name, value = product.popitem()

            if product_name == "DINUM - RESANA":
                product_name = "Resana"
            elif product_name == "Messagerie de la Suite Numérique":
                product_name = "Messagerie"
            else:
                pass

            this_indicator = {
                key: value for key, value in self.indicators_types[0].items()
            }
            if product_name in [
                "Resana",
                "France transfert",
                "Visio",
                "Messagerie",
                "Tchap",
            ]:
                this_indicator["name"] = f"{this_indicator['name']} via ProConnect"

            this_indicator["product"] = product_name
            this_indicator["value"] = value
            self.indicators.append(this_indicator)

        return self.indicators

    def get_last_month_active_users(self):
        """Fetch data from url."""
        url = "https://stats.moncomptepro.beta.gouv.fr/public/question/0e3cee98-df38-4d57-8c37-d38c5a2d3231.json"
        response = requests.get(url)
        return [
            {entry["Fournisseur Service"]: entry["Valeurs distinctes de Sub Fi"]}
            for entry in response.json()
        ]
