import requests
from core.adaptors.base_adaptor import BaseAdaptor
from core.utils import utils
from django.conf import settings


class PostHogAdaptor(BaseAdaptor):
    """Adaptor to fetch and send PostHog insights indicators."""

    POSTHOG_API_URL = settings.POSTHOG_API_URL
    POSTHOG_API_KEY = settings.POSTHOG_API_KEY

    slug = None
    indicators = []
    # Example structure:
    # indicators = [
    #     {
    #         "name": "utilisateurs actifs mensuels",
    #         "frequency": "mensuelle",``
    #         "project_id": "xxxxx",
    #         "insight_id": "xxxxx",
    #     }
    # ]

    def get_last_month_data(self):
        """Grab and push all indicators."""
        for indicator in self.indicators:
            indicator["value"] = self._get_last_month_insight(
                indicator["project_id"], indicator["insight_id"]
            )
        return self.indicators

    def _get_last_month_insight(self, project_id, insight_id):
        """Fetch data from PostHog API for a specific insight."""
        url = f"{self.POSTHOG_API_URL}/api/projects/{project_id}/insights/{insight_id}"
        headers = {"Authorization": f"Bearer {self.POSTHOG_API_KEY}"}

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        try:
            results = response.json()["result"][0]
        except TypeError:
            raise ValueError(
                f"Failed to get value from Posthog insight {url}. Please manually refresh insight."
            )

        if not results["data"]:
            raise ValueError(f"No data available for insight {insight_id}")

        # Find last month in "days" list and return corresponding data
        last_month = str(utils.get_last_month_limits()[0])
        try:
            index = results["days"].index(last_month)
        except ValueError:
            raise ValueError("Last month data not found in insight.")
        else:
            return results["data"][index]
