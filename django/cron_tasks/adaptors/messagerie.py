import requests
from cron_tasks import utils
from cron_tasks.adaptors.base_adaptor import BaseAdaptor
from datetime import date as dtdate, timedelta
from core import models


class MessagerieAdaptor(BaseAdaptor):
    """Adaptor to fetch and send ProConnect's indicators."""

    slug = "messagerie"
    indicators = [
        {
            "name": "utilisateurs actifs 30 derniers jours",
            "frequency": "mensuelle",
            "url": "https://tabular-api.data.gouv.fr/api/resources/f5d3d162-d485-4bed-94bc-96679d299747/data/",
        }
    ]
    # https://tabular-api.data.gouv.fr/api/resources/f5d3d162-d485-4bed-94bc-96679d299747/data/?yyyy-mm-dd__exact=%222025-07-01%22

    def fetch_latest_data(self):
        """Grab and push all indicators. From data.gouv dataset, we use every 30 days value
        from all first days of month."""
        for indicator in self.indicators:
            response = requests.get(indicator["url"])

            last_indicator = models.Indicator.objects.filter(indicateur=indicator)
            if last_indicator.exists():
                stop_date = utils.get_first_day_of_month(last_indicator[-1].date)
            else:
                # we'll try to add all possible dates from response
                stop_date = utils.get_first_day_of_month(
                    response.json()[0]["yyyy-mm-dd"]
                )

            created_indicators = []
            date = utils.get_first_day_of_month(dtdate.today())
            while date != stop_date:
                entry = [d for d in response.json() if d["yyyy-mm-dd"] == str(date)]
                if entry != []:
                    new_indicator = self.create_indicator(
                        indicator,
                        date - timedelta(days=1),
                        entry[0][" sur les 30 derniers jours"],
                    )
                    created_indicators.append(new_indicator)
                date = utils.get_first_day_of_month(date - timedelta(days=1))
            return created_indicators
