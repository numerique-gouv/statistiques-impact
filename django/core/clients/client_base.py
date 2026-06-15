import requests


class ClientBase:
    """A basic client to fetch product's data and create records."""

    def __init__(self, indicator):
        self.indicator = indicator
        self.product = indicator.product

    def get_response(self, headers={}):
        """Returns response from data source server."""
        response = requests.get(url=self.indicator.source_url, headers=headers)
        response.raise_for_status()
        return response

    def get_last_month_data(self):
        """Get latest values for all indicators."""
        for record in self.indicators:
            record["value"] = getattr(self, record["method"])()
        return self.records
