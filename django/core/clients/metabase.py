import requests
from core.clients.client_base import ClientBase
from rest_framework import status, exceptions


class MetabaseClient(ClientBase):
    """Adaptor to extract data of interest from Metabase responses."""

    def get_data(self):
        """Extract data from response content."""
        response = self.get_response()
        content = response.json()

        if len(content) == 1:
            return [
                {
                    "product": str(self.adaptor.product),
                    "indicator": self.adaptor.indicator,
                    "value": int(content[0]["Valeurs distinctes de Sub Fi"]),
                }
            ]
        else:
            return [
                {
                    "product": entry["Fournisseur Service"],
                    "indicator": self.adaptor.indicator,
                    "value": entry["Somme de Distinct values of Sub Fi"],
                }
                for entry in content
            ]


class TchapClient(MetabaseClient):
    """Adaptor to fetch and send Tchap's indicators."""

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
                "product": str(self.adaptor.product),
                "indicator": self.adaptor.indicator,
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
    """Adaptor to fetch LaSuite's basic indicators."""

    def get_data(self):
        """Get latest values for all indicators."""
        response = self.get_response()
        content = response.json()

        return [
            {
                "product": product["Fournisseur Service"],
                "indicator": self.adaptor.indicator,
                "value": product["Somme de Distinct values of Sub Fi"],
            }
            for product in content
        ]
