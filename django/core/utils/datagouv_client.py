import requests
from django.conf import settings
from rest_framework import exceptions, status
from datagouv import Client, Dataset
import pandas
import os


class DataGouvClient:
    API_URL = settings.DATAGOUV_API_URL

    def get_headers(self, env="prod"):
        """Simple headers to provide auth, but key depends on env."""
        return {
            "x-api-key": settings.DATAGOUV_DEMO_API_KEY
            if env == "demo"
            else settings.DATAGOUV_API_KEY,
        }

    def upload_file(self, file, product, env="prod"):
        """Upload a file to a dataset."""
        if not product.dataset_id:
            raise exceptions.APIException(
                detail="Please provide a data.gouv.fr dataset",
                code=status.HTTP_400_BAD_REQUEST,
            )

        API_URL = "https://demo.data.gouv.fr/api/1" if env == "demo" else self.API_URL
        # Upload directly to API because package upload method expects a path
        response = requests.post(
            url=f"{API_URL}/datasets/{product.dataset_id}/upload/",
            files={"file": (file.name, file.file.getvalue(), "text/csv")},
            headers=self.get_headers(env),
        )
        response.raise_for_status()
        return response

    def aggregate_monthly_stats(self, dataset_id, month):
        """Aggregate daily files into 2 dataframes : stats and satisfaction."""
        if dataset_id == "68b86764fd43cc1591faa6a5":
            dataset = Dataset(
                dataset_id,
                _client=Client(
                    environment="demo", api_key=settings.DATAGOUV_DEMO_API_KEY
                ),
            )
        else:
            dataset = Dataset(
                dataset_id, _client=Client(api_key=settings.DATAGOUV_API_KEY)
            )

        df_stats = pandas.DataFrame()
        df_satisfaction = pandas.DataFrame()
        for resource in dataset.resources:
            if month in resource.title:
                resource_type = resource.title.split("-")[-1]
                resource.download(f"tmp/{resource.title}")

                try:
                    df = pandas.read_csv(f"tmp/{resource.title}", delimiter=",")
                except UnicodeDecodeError:
                    df = pandas.read_csv(
                        f"tmp/{resource.title}", delimiter=",", compression="gzip"
                    )

                match resource_type:
                    case "stats.csv":
                        df_stats = pandas.concat([df_stats, df])
                    case "satisfaction.csv":
                        df_satisfaction = pandas.concat([df_satisfaction, df])
                    case _:
                        print(f"Unexpected type for {resource.title}")

                os.remove(f"tmp/{resource.title}")

        return df_stats, df_satisfaction
