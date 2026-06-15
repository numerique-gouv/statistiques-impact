import requests
from core.clients.client_base import ClientBase
from rest_framework import status, exceptions


class MetabaseClient(ClientBase):
    """Indicator to extract data of interest from Metabase responses."""

    def get_data(self):
        """Extract data from response content."""
        response = self.get_response()
        content = response.json()

        if len(content) == 1:
            return [
                {
                    "product": str(self.indicator.product),
                    "record": self.indicator.record,
                    "value": int(content[0]["Valeurs distinctes de Sub Fi"]),
                }
            ]
        else:
            return [
                {
                    "product": entry["Fournisseur Service"],
                    "record": self.indicator.record,
                    "value": entry["Somme de Distinct values of Sub Fi"],
                }
                for entry in content
            ]


class TchapClient(MetabaseClient):
    """Indicator to fetch and send Tchap's records."""

    def get_data(self):
        response = self.get_response()
        content = response.json()

        if len(content) > 1:
            raise exceptions.APIException(
                detail="Don't know how to handle these data. Please verify you're using the correct client.",
                code=status.HTTP_400_BAD_REQUEST,
            )

        return [
            {
                "product": str(self.indicator.product),
                "record": self.indicator.record,
                "value": int(content[0]["Nombre de lignes"].replace(" ", "")),
            }
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
    """Indicator to fetch LaSuite's basic records."""

    def get_last_month_data(self):
        """Get latest values for all records."""
        values = self.get_value()

        for product in values:
            this_record = {}
            product_name, value = product.popitem()

            if product_name == "DINUM - RESANA":
                product_name = "Resana"
            elif product_name == "Messagerie de la Suite Numérique":
                product_name = "Messagerie"
            else:
                pass

            this_record = {key: value for key, value in self.records_types[0].items()}
            if product_name in [
                "Resana",
                "France transfert",
                "Visio",
                "Messagerie",
                "Tchap",
            ]:
                this_record["name"] = f"{this_record['name']} via ProConnect"

            this_record["product"] = product_name
            this_record["value"] = value
            self.records.append(this_record)

        return self.records

    def get_value(self):
        """Fetch data from url."""
        url = "https://metabase.gouv.fr/public/question/0e3cee98-df38-4d57-8c37-d38c5a2d3231.json"
        response = requests.get(url)
        return [
            {entry["Fournisseur Service"]: entry["Valeurs distinctes de Sub Fi"]}
            for entry in response.json()
        ]
