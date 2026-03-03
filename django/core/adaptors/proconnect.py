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
        return int(response.json()[0]["Somme de Distinct values of Sub Fi"])


class LaSuiteAdaptor(ProConnectAdaptor):
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

            if product_name == "Messagerie de la Suite Numérique":
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
        url = "https://stats.moncomptepro.beta.gouv.fr/public/question/777dec23-cd88-47df-a576-57f4b954d59d.json"
        response = requests.get(url)
        response.raise_for_status()
        return [
            {entry["Fournisseur Service"]: entry["Somme de Distinct values of Sub Fi"]}
            for entry in response.json()
        ]
