import requests


class ClientBase:
    """A basic client to fetch product's data and create indicators."""

    def __init__(self, adaptor):
        self.adaptor = adaptor
        self.product = adaptor.product

    def get_response(self, headers={}):
        """Returns response from data source server."""
        response = requests.get(url=self.adaptor.source_url, headers=headers)
        response.raise_for_status()
        return response

    def get_last_month_data(self):
        """Get latest values for all indicators."""
        for indicator in self.indicators:
            indicator["value"] = getattr(self, indicator["method"])()
        return self.indicators
