import requests
from django.conf import settings
from datagouv import Client, Dataset, Resource
import pandas
import os
from core.utils import utils


class DataGouvClient:
    api_url = settings.DATAGOUV_API_URL
    api_key = settings.DATAGOUV_API_KEY
    env = "www"  # env can be "www", "demo" or "dev"

    def get_headers(self):
        """Simple headers to provide auth, but key depends on env."""
        return {
            "x-api-key": settings.DATAGOUV_DEMO_API_KEY
            if self.env == "demo"
            else settings.DATAGOUV_API_KEY,
        }

    def get_dataset(self, dataset_id):
        if dataset_id == "68b86764fd43cc1591faa6a5":
            self.env = "demo"
            self.api_url = "https://demo.data.gouv.fr/api/1"
            self.api_key = settings.DATAGOUV_DEMO_API_KEY

        return Dataset(
            dataset_id,
            _client=Client(environment=self.env, api_key=self.api_key),
        )

    def upload_new_file(self, dataset_id, data, filename):
        """Upload a file to a dataset."""

        self.get_dataset(dataset_id)  # trick to update env to demo if necessary

        # Can't use wrapper because it expects a path
        response = requests.post(
            url=f"{self.api_url}/datasets/{dataset_id}/upload/",
            files={"file": (filename, data, "text/csv")},
            headers=self.get_headers(),
        )
        response.raise_for_status()
        return response

    def update_resource(self, dataset_id, resource_id, data, filename):
        """Replace a resource by a new file."""
        response = requests.post(
            f"{self.api_url}/datasets/{dataset_id}/resources/{resource_id}/upload",
            headers=self.get_headers(),
            files={"file": (filename, data, "text/csv")},
        )
        response.raise_for_status()
        return response

    def merge_monthly_stats(self, dataset, month):
        """Merge all daily files into 2 monthly files : stats and satisfaction.
        Used daily files are deleted from dataset."""

        type_list = {
            "stats": {
                "dataframe": pandas.DataFrame(),
                "expected_line_count": 0,
            },
            "satisfaction": {
                "dataframe": pandas.DataFrame(),
                "expected_line_count": 0,
            },
        }
        monthly_resources = [
            resource for resource in dataset.resources if month in resource.title
        ]
        titles = [resource.title for resource in monthly_resources]

        print(f"{len(monthly_resources)} resources found for month {month}.")
        if titles == [
            f"{month}-satisfaction.csv",
            f"{month}-stats.csv",
        ]:
            print("Nothing to merge")
            exit()
        for resource in monthly_resources:
            resource.download(f"tmp/{resource.title}")
            df = utils.read_csv(f"tmp/{resource.title}")
            resource_type = resource.title.split("-")[-1][0:-4]

            try:
                type_list[resource_type]["expected_line_count"] += len(df)
                type_list[resource_type]["dataframe"] = pandas.concat(
                    [type_list[resource_type]["dataframe"], df]
                )
            except KeyError:
                print(
                    f'Unexpected format for {resource.title}. Suffix must be "stats" or "satisfaction".'
                )
                exit()

            # data is merged and file ready to be deleted
            os.remove(f"tmp/{resource.title}")

        for itype, data in type_list.items():
            dataframe = data["dataframe"]
            expected_line_count = data["expected_line_count"]
            filename = f"{month}-{itype}.csv"
            titles = [resource.title for resource in monthly_resources]

            print(
                f"For {itype}: expected {expected_line_count} lines, counted {len(dataframe)} lines."
            )
            if expected_line_count == len(dataframe) and len(dataframe) > 0:
                if filename in titles:
                    print(f"Updating file {filename}")
                    resource_id = monthly_resources[titles.index(filename)].id
                    self.update_resource(
                        dataset.id, resource_id, dataframe.to_csv(index=False), filename
                    )

                    # remove this file from deletable resources
                    monthly_resources = [
                        resource
                        for resource in monthly_resources
                        if resource.id != resource_id
                    ]
                else:
                    # create monthly files
                    self.upload_new_file(
                        dataset.id, dataframe.to_csv(index=False), filename
                    )
                    print(f"Uploading new file {filename}")

        # Delete daily files
        print(f"Deleting {len(monthly_resources)} files.")
        for resource in monthly_resources:
            resource.delete()

    def delete_resource(self, dataset, resource_id):
        """delete resource on a given dataset."""
        resource = Resource(id=resource_id, _client=dataset._client)
        print(f"Resource {resource_id} deleted.")
        resource.delete()
