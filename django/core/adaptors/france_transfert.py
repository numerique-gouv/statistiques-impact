from core.adaptors.base_adaptor import BaseAdaptor
from core.utils.datagouv_client import DataGouvClient
from core.utils import date_utils
from pandas import to_numeric


class FranceTransfertAdaptor(BaseAdaptor):
    slug = "france-transfert"

    def __init__(self, is_test=False):
        """Fix to include tests for france-transfert."""
        if is_test:
            self.slug = "france-transfert-tests"
        return super().__init__()

    def get_last_month_data(self):
        """Get last month data and return indicators."""
        month = str(date_utils.get_last_month_limits()[0])[0:-3]

        client = DataGouvClient()
        df_stats, df_satisfaction = client.aggregate_monthly_stats(
            self.product.dataset_id, month
        )
        return self.calculate_usage_stats(df_stats) + self.calculate_satisfaction_stats(
            df_satisfaction
        )

    def calculate_usage_stats(self, dataframe):
        """Calculate indicators value from stats dataframe."""
        if str(dataframe.dtypes["TAILLE"]) != "float64":
            dataframe["TAILLE2"] = dataframe["TAILLE"]
            dataframe["TAILLE2"] = to_numeric(
                dataframe["TAILLE"].str.replace(r" [GMK]?B", "", regex=True)
            )
            dataframe.loc[dataframe["TAILLE"].str.contains("K"), "TAILLE2"] = (
                dataframe.loc[dataframe["TAILLE"].str.contains("K"), "TAILLE2"] * 1000
            )
            dataframe.loc[dataframe["TAILLE"].str.contains("M"), "TAILLE2"] = (
                dataframe.loc[dataframe["TAILLE"].str.contains("M"), "TAILLE2"]
                * (1000 * 1000)
            )
            dataframe.loc[dataframe["TAILLE"].str.contains("G"), "TAILLE2"] = (
                dataframe.loc[dataframe["TAILLE"].str.contains("G"), "TAILLE2"]
                * (1000 * 1000 * 1000)
            )
            dataframe["TAILLE"] = dataframe["TAILLE2"]

        go_emis = float(
            dataframe[dataframe["TYPE_ACTION"] == "upload"]["TAILLE"].sum()
            / (1000 * 1000 * 1000)
        )
        plis_emis = dataframe[dataframe["TYPE_ACTION"] == "upload"]["ID_PLIS"].nunique()
        return [
            {
                "name": "utilisateurs actifs (téléchargement)",
                "value": dataframe[dataframe["TYPE_ACTION"] == "download"][
                    "HASH_EXPE"
                ].nunique(),
            },
            {
                "name": "utilisateurs actifs (envoi)",
                "value": dataframe[dataframe["TYPE_ACTION"] == "upload"][
                    "HASH_EXPE"
                ].nunique(),
            },
            {
                "name": "utilisateurs actifs",
                "value": dataframe["HASH_EXPE"].nunique(),
            },
            {
                "name": "téléchargements",
                "value": int(
                    dataframe[dataframe["TYPE_ACTION"] == "download"]["ID_PLIS"].count()
                ),
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
                        dataframe[dataframe["TYPE_ACTION"] == "download"][
                            "TAILLE"
                        ].sum()
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
                    dataframe["DOMAINE_EXPEDITEUR"].value_counts().index.tolist()[:5]
                ),
            },
        ]

    def calculate_satisfaction_stats(self, dataframe):
        """Calculate indicators value from satisfaction dataframe."""
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

    def process_file(self, file):
        """Upon reception, send stat and satisfaction files to data.gouv.fr."""
        # A temporary hack for test products to send data to demo.data.gouv.fr
        env = (
            "demo"
            if self.product.nom_service_public_numerique == "france-transfert-tests"
            else "prod"
        )

        client = DataGouvClient()
        return client.upload_file(file, self.product, env)
