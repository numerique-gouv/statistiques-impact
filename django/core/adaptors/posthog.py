import os
import requests
from core.adaptors.base_adaptor import BaseAdaptor
from core.utils import date_utils
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
            indicator["value"] = self._get_data(indicator["project_id"], indicator["insight_id"])
        return self.indicators

    def _get_data(self, project_id, insight_id):
        """Fetch data from PostHog API for a specific insight."""
        url = f"{self.POSTHOG_API_URL}/api/projects/{project_id}/insights/{insight_id}"
        headers = {"Authorization": f"Bearer {self.POSTHOG_API_KEY}"}

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()

        result = data["result"][0]
        values = result["data"]

        if not values:
            raise ValueError(f"No data available for insight {insight_id}")

        # Get the previous month data point
        latest_value = values[-2]

        return latest_value