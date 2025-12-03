from core import models


class BaseAdaptor:
    """Base adaptor to fetch product's data and create indicators."""

    slug = "product_slug"
    # example indicator
    # indicators = [
    #     {
    #         "name": "utilisateurs actifs",
    #         "frequency": "mensuelle",
    #         "method": "get_last_month_active_users"
    #     }
    # ]

    def __init__(self):
        self.product = models.Product.objects.get(slug=self.slug)

    def get_last_month_data(self):
        """Get latest values for all indicators."""
        for indicator in self.indicators:
            indicator["value"] = getattr(self, indicator["method"])()
        return self.indicators
