from core import models
from django.core import exceptions
from datetime import date as dtdate


class BaseAdaptor:
    """Adaptor to fetch product's data and create indicators."""

    def __init__(self):
        self.product = models.Product.objects.get(slug=self.slug)

    def create_indicator(self, name, date, value, frequency, automatic_call=True):
        product = models.Product.objects.get(slug=self.slug)
        if type(date) is str:
            date = dtdate.fromisoformat(date)

        try:
            new_entry = models.Indicator.objects.create(
                productid=product,
                indicateur=name,
                valeur=float(value),
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
