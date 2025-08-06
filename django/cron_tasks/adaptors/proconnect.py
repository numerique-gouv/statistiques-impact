import requests
from core import models
from django.core import exceptions
from cron_tasks import utils


class ProConnectAdaptor:
    """Adaptor to fetch and send ProConnect's indicators."""

    slug = "agent-connect"
    indicators = [
        {
            "name": "utilisateurs actifs",
            "frequency": "mensuelle",
            "url": "https://stats.moncomptepro.beta.gouv.fr/public/question/cd934f6d-fb60-413b-a955-581859451141.json",
        }
    ]

    def _fetch_data(self, url):
        """Fetch data from url."""
        response = requests.get(url)

        indicator_date = utils.get_last_day_of_month(response.json()[0]["Time: Mois"])
        value = response.json()[0]["Valeurs distinctes de Sub Fi"]
        return indicator_date, value

    def create_indicator(self, indicator, automatic_call=True):
        date, value = self._fetch_data(indicator["url"])
        product = models.Product.objects.get(slug=self.slug)
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
                else "",
                est_automatise=automatic_call,
                est_periode=True,
            )
        except exceptions.ValidationError:
            print(
                product,
                indicator["name"],
                date,
                indicator["frequency"],
                "already exists",
            )
            return None
        else:
            print(
                product,
                indicator["name"],
                date,
                indicator["frequency"],
                "added",
            )
            return new_entry
