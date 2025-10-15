from core.adaptors.base_adaptor import BaseAdaptor
from core.utils.datagouv_client import DataGouvClient
from core.utils import date_utils


class FranceTransfertAdaptor(BaseAdaptor):
    slug = "france-transfert"

    def __init__(self, is_test=False):
        """Fix to include tests for france-transfert."""
        if is_test:
            self.slug = "france-transfert-tests"
        return super().__init__()

    def calculate_usage_stats(self, dataframe):
        """Calculate indicators value from stats dataframe."""
        return [
            {
                "name": "utilisateurs actifs (téléchargement)",
                "value": dataframe[dataframe["TYPE_ACTION"] == "download"][
                    "HASH_EXPE"
                ].nunique(),
            },
            {
                "name": "utilisateurs actifs (émission)",
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
                "value": dataframe[dataframe["TYPE_ACTION"] == "upload"][
                    "ID_PLIS"
                ].nunique(),
            },
            # Go émis
            # téléchargés
            # taille moyenne d'un pli
            # {"name": "Nombre Go émis", "frequency": "quotidienne", à calculer},
            # Chaque taille contient son unité donc il faudra faire un peu de magie pour reconvertir en B ou en KB
            # sum_go_sent = int(pandas.to_numeric(df["TAILLE"]).sum()) / 1073741824
            # {"name": "Taille moyenne d'un pli (Mo)", "frequency": "quotidienne", df["HASH_EXPE"].nunique()},
            # (bloqué car dépend du calcul Go émis)
            # sum_go_sent / df["TAILLE"].count()
        ]

    def calculate_satisfaction_stats(self, dataframe):
        """Calculate indicators value from satisfaction dataframe."""
        # Not implemented yet
        return []

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
