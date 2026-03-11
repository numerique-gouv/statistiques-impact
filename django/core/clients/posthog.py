from core.clients.client_base import ClientBase
from core.utils import utils
from django.conf import settings


class PostHogClient(ClientBase):
    """Adaptor to fetch and send PostHog insights indicators."""

    POSTHOG_API_URL = settings.POSTHOG_API_URL
    POSTHOG_API_KEY = settings.POSTHOG_API_KEY

    def get_data(self):
        response = self.get_response(
            headers={"Authorization": f"Bearer {self.POSTHOG_API_KEY}"}
        )
        content = response.json()
        return self._get_last_month_insight(result=content["result"])

    def _get_last_month_insight(self, result):
        """Extract value from response's content results."""

        try:
            result = result[0]
        except TypeError:
            raise ValueError(
                f"Failed to get value from Posthog insight {self.adaptor.source_url}. Please manually refresh insight."
            )

        if not result["data"]:
            raise KeyError("This insight has no data.")

        return result["data"][-2]  # [-1] is the last month = current unfinished month

    def check_expected_data(self, result):
        # Find last month in "days" list and return corresponding data
        last_month = str(utils.get_last_month_limits()[0])
        try:
            index = result["days"].index(last_month)
        except ValueError:
            raise ValueError("Last month data not found in insight.")
        else:
            return result["data"][index]
