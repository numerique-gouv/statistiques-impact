from core.clients.client_base import ClientBase
from core.utils import utils
import pandas
from rest_framework import status, exceptions
import requests
from datetime import date
from django.conf import settings
from datagouv import Client, Dataset, Resource
import os

# Demo datasets to check France transfert interop
# runs as expected
FT_DEMO_DATASETS = ["68b86764fd43cc1591faa6a5"]


class DataGouvClient(ClientBase):
    """A client for all interactions with datasets at data.gouv.fr."""

    def __init__(self, adaptor, env="www"):
        """Fix to include tests for france-transfert."""
        self.env = "demo" if adaptor.product.dataset_id in FT_DEMO_DATASETS else "www"
        self.dataset_id = adaptor.product.dataset_id
        self.api_url = (
            "https://demo.data.gouv.fr/api/1"
            if adaptor.product.dataset_id in FT_DEMO_DATASETS
            else settings.DATAGOUV_API_URL
        )
        self.api_key = (
            settings.DATAGOUV_DEMO_API_KEY
            if adaptor.product.dataset_id in FT_DEMO_DATASETS
            else settings.DATAGOUV_API_KEY
        )
        super().__init__(adaptor)

    def get_headers(self):
        """Simple headers to provide auth, but key depends on env."""
        return {"x-api-key": self.api_key}

    def get_dataset(self):
        dataset_id = self.adaptor.product.dataset_id

        if not dataset_id:
            raise exceptions.APIException(
                detail=f"Don't know which data.gouv dataset to work with. Please provide a dataset_id for {self.product}.",
                code=status.HTTP_400_BAD_REQUEST,
            )

        return Dataset(
            dataset_id,
            _client=Client(environment=self.env, api_key=self.api_key),
        )

    def upload_new_file(self, file):
        """Upload a file to a dataset."""
        if not self.product.dataset_id:
            raise exceptions.APIException(
                detail="Please provide a data.gouv.fr dataset",
                code=status.HTTP_400_BAD_REQUEST,
            )

        self.get_dataset()

        # Can't use wrapper because it expects a path
        response = requests.post(
            url=f"{self.api_url}/datasets/{self.product.dataset_id}/upload/",
            files={"file": (file.name, file.file.getvalue(), "text/csv")},
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

    def delete_resource(self, dataset, resource_id):
        """delete resource on a given dataset."""
        resource = Resource(id=resource_id, _client=dataset._client)
        print(f"Resource {resource_id} deleted.")
        resource.delete()


class MessagerieClient(DataGouvClient):
    """Adaptor to fetch and send 's indicators."""

    def get_data(self):
        """Get a specific date's active users from messagerie's dataset on data.gouv.fr."""

        dataset = self.get_dataset()
        resource = dataset.resources[0]
        resource.download(f"tmp/{resource.id}.csv")
        as_csv = utils.read_csv(f"tmp/{resource.id}.csv", skipinitialspace=True)
        os.remove(f"tmp/{resource.id}.csv")

        entry = as_csv[as_csv["yyyy-mm-dd"] == str(date.today().replace(day=1))][
            "sur les 30 derniers jours"
        ]

        if len(entry) > 1:
            raise exceptions.APIException(
                detail=f"Multiple value for last month's {self.adaptor.indicator} in data. Please check your dataset.",
                code=status.HTTP_400_BAD_REQUEST,
            )

        return [
            {
                "product": str(self.adaptor.product),
                "indicator": self.adaptor.indicator,
                "value": int(entry.iloc[0]),
            }
        ]


class FranceTransfertClient(DataGouvClient):
    """A client for the special needs of FranceTransfert."""

    def get_data(self):
        """Surchage function to run France-Transfert-specific treatment on data."""
        month = str(utils.get_last_month_limits()[0])[0:-3]
        dataset = self.get_dataset()
        monthly_resources = [
            resource for resource in dataset.resources if month in resource.title
        ]

        if len(monthly_resources) > 2:
            print("Merging files")
            self.merge_monthly_stats(dataset, month)

        df_stats, df_satisfaction = [pandas.DataFrame()] * 2

        for resource in monthly_resources:
            resource.download(f"tmp/{resource.id}")
            if resource.title == f"{month}-stats.csv":
                df_stats = utils.read_csv(f"tmp/{resource.id}")
            elif resource.title == f"{month}-satisfaction.csv":
                df_satisfaction = utils.read_csv(f"tmp/{resource.id}")
            else:
                print(f"Unexpected resource ({resource.title}).")

        return [
            {
                "product": str(self.adaptor.product),
                "indicators": [
                    indicator
                    for indicators_list in [
                        self.calculate_usage_stats(df_stats),
                        self.calculate_satisfaction_stats(df_satisfaction),
                    ]
                    for indicator in indicators_list
                ],
            }
        ]

    def calculate_usage_stats(self, df):
        """Calculate indicators value from stats dataframe."""

        df = df[(df.ID_PLIS != "ID_PLIS")]  # remove possibly remaining headers

        if str(df.dtypes["TAILLE"]) != "int64":
            df["TAILLE2"] = pandas.to_numeric(
                df["TAILLE"].str.replace(r" [GMK]?B", "", regex=True)
            )

            df.loc[df["TAILLE"].str.contains("K", na=False), "TAILLE2"] = (
                df.loc[df["TAILLE"].str.contains("K", na=False), "TAILLE2"] * 1000
            )
            df.loc[df["TAILLE"].str.contains("M", na=False), "TAILLE2"] = df.loc[
                df["TAILLE"].str.contains("M", na=False), "TAILLE2"
            ] * (1000 * 1000)
            df.loc[df["TAILLE"].str.contains("G", na=False), "TAILLE2"] = df.loc[
                df["TAILLE"].str.contains("G", na=False), "TAILLE2"
            ] * (1000 * 1000 * 1000)
            df.TAILLE2 = df.TAILLE2.fillna(df.TAILLE)  # fixes NaN from last command
            df["TAILLE"] = df["TAILLE2"]
            del df["TAILLE2"]

        go_emis = float(
            df[df["TYPE_ACTION"] == "upload"]["TAILLE"].sum() / (1000 * 1000 * 1000)
        )
        plis_emis = df[df["TYPE_ACTION"] == "upload"]["ID_PLIS"].nunique()
        return [
            {
                "name": "utilisateurs actifs (téléchargement)",
                "value": df[df["TYPE_ACTION"] == "download"]["HASH_EXPE"].nunique(),
            },
            {
                "name": "utilisateurs actifs (envoi)",
                "value": df[df["TYPE_ACTION"] == "upload"]["HASH_EXPE"].nunique(),
            },
            {
                "name": "utilisateurs actifs",
                "value": df["HASH_EXPE"].nunique(),
            },
            {
                "name": "téléchargements",
                "value": int(df[df["TYPE_ACTION"] == "download"]["ID_PLIS"].count()),
                # pas "unique" ici. On ne veut pas savoir combien de plis différents
                # ont été téléchargés mais combien de téléchargements ont eu lieu
            },
            {
                "name": "plis émis",
                "value": plis_emis,
            },
            {
                "name": "Go émis",
                "value": round(go_emis, 2),
            },
            {
                "name": "Go téléchargés",
                "value": float(
                    round(
                        df[df["TYPE_ACTION"] == "download"]["TAILLE"].sum()
                        / (1024 * 1024 * 1024),
                        2,
                    )
                ),
            },
            {
                "name": "Taille pli moyen (Mo)",
                "value": round(
                    1000 * go_emis / plis_emis, 2
                ),  # More convenient in Mo than in Go
            },
            {
                "name": "top 5 domaines expéditeurs",
                "value": ", ".join(
                    df["DOMAINE_EXPEDITEUR"].value_counts().index.tolist()[:5]
                ),
            },
        ]

    def calculate_satisfaction_stats(self, dataframe):
        """Calculate indicators value from satisfaction dataframe."""
        if len(dataframe) == 0:
            return []

        return [
            {
                "name": "avis émis",
                "value": int(dataframe["ID_PLIS"].count()),
            },
            {
                "name": "pourcentage satisfaction",
                "value": round(
                    100
                    * (
                        int(dataframe[dataframe["NOTE"] == 3]["ID_PLIS"].count())
                        / int(dataframe["ID_PLIS"].count())
                    )
                ),
            },
        ]

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
