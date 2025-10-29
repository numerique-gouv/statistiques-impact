from core import models
from django.core import exceptions
from datetime import date as dtdate


class BaseAdaptor:
    """Base adaptor to fetch product's data and create indicators."""

    slug = "product_slug"
    # example indicator
    # indicators = [
    #     {
    #         "name": "indicator_name",
    #         "frequency": "frequency",
    #         "method": "custom_method_name" # to get last month's data
    #     }
    # ]

    def __init__(self):
        self.product = models.Product.objects.get(slug=self.slug)

    def create_indicator(self, name, date, value, frequency, automatic_call=True):
        if type(date) is str:
            date = dtdate.fromisoformat(date)

        try:
            new_entry = models.Indicator.objects.create(
                productid=self.product,
                indicateur=name,
                valeur=value,
                unite_mesure="unite",
                frequence_monitoring=frequency,
                date=date,
                date_debut=date.replace(day=1)
                if frequency == "mensuelle"
                else date
                if frequency == "quotidienne"
                else "",
                est_automatise=automatic_call,
                est_periode=True,
            )
        except exceptions.ValidationError as e:
            return e
        else:
            return new_entry
