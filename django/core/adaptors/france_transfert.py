from core.adaptors.base_adaptor import BaseAdaptor
from core.utils.datagouv_client import DataGouvClient
from core.utils import utils
import pandas
from rest_framework import status, exceptions


class FranceTransfertAdaptor(BaseAdaptor):
    slug = "france-transfert"

    def __init__(self, is_test=False):
        """Fix to include tests for france-transfert."""
        if is_test:
            self.slug = "france-transfert-tests"
        return super().__init__()

    def get_last_month_data(self):
        """Load last month's csv and return dataframes."""
        month = str(utils.get_last_month_limits()[0])[0:-3]

        client = DataGouvClient()
        dataset = client.get_dataset(self.product.dataset_id)
        monthly_resources = [
            resource for resource in dataset.resources if month in resource.title
        ]

        if len(monthly_resources) > 2:
            print("Merging files")
            client.merge_monthly_stats(dataset, month)

        df_stats, df_satisfaction = [pandas.DataFrame()] * 2

        for resource in monthly_resources:
            resource.download(f"tmp/{resource.id}")
            if resource.title == f"{month}-stats.csv":
                df_stats = utils.read_csv(f"tmp/{resource.id}")
            elif resource.title == f"{month}-satisfaction.csv":
                df_satisfaction = utils.read_csv(f"tmp/{resource.id}")
            else:
                print(f"Unexpected resource ({resource.title}).")

        return self.calculate_usage_stats(df_stats) + self.calculate_satisfaction_stats(
            df_satisfaction
        )

    def calculate_usage_stats(self, df):
        """Calculate indicators value from stats dataframe."""
        if str(df.dtypes["TAILLE"]) != "float64":
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

    def upload_new_file(self, file):
        """Upon reception, send files to data.gouv.fr."""
        if not self.product.dataset_id:
            raise exceptions.APIException(
                detail="Please provide a data.gouv.fr dataset",
                code=status.HTTP_400_BAD_REQUEST,
            )

        client = DataGouvClient()
        return client.upload_new_file(
            self.product.dataset_id, file.file.getvalue(), file.name
        )
