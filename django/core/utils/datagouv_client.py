import requests
from django.conf import settings
from rest_framework import exceptions, status


class DataGouvClient:
    API = settings.DATAGOUV_API_URL

    def get_headers(self):
        """Simple headers for API KEY."""
        return {
            "X-API-KEY": settings.DATAGOUV_API_KEY,
        }

    def upload_file(self, file, product):
        """Upload a file to a dataset."""
        if not product.dataset_id:
            raise exceptions.APIException(
                detail="Please provide a data.gouv.fr dataset",
                code=status.HTTP_400_BAD_REQUEST,
            )

        API = self.API
        if product.slug == "france-transfert-tests":
            API = "https://demo.data.gouv.fr/api/1"

        # Upload directly to API because package upload method expects a path
        response = requests.post(
            url=f"{API}/datasets/{product.dataset_id}/upload/",
            files={"file": (file.name, file.file.getvalue(), "text/csv")},
            headers=self.get_headers(),
        )
        response.raise_for_status()
        return response
