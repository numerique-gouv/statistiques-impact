from core import models
from django.core import exceptions
from datetime import date as dtdate


class BaseAdaptor:
    """Adaptor to create indicators."""

    def create_indicator(self, indicator, date, value, automatic_call=True):
        product = models.Product.objects.get(slug=self.slug)
        if type(date) is str:
            date = dtdate.fromisoformat(date)

        try:
            new_entry = models.Indicator.objects.create(
                productid=product,
                indicateur=indicator["name"],
                valeur=float(value),
                unite_mesure="unite",
                frequence_monitoring=indicator["frequency"],
                date=date,
                date_debut=date.replace(day=1)
                if indicator["frequency"] == "mensuelle"
                else date
                if indicator["frequency"] == "quotidienne"
                else "",
                est_automatise=automatic_call,
                est_periode=True,
            )
        except exceptions.ValidationError as e:
            return e
        else:
            return new_entry
