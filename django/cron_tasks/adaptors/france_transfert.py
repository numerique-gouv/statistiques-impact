import pandas
from cron_tasks.adaptors.base_adaptor import BaseAdaptor
from core import models
from core.api import serializers


class FranceTransfertAdaptor(BaseAdaptor):
    slug = "france-transfert"

    def create_indicators_from_csv(self, file):
        df = pandas.read_csv(file, delimiter=",")
        date = file.name.split("_")[2]
        code_machine = file.name.split("_")[0].split("-")[4]

        response = []

        if "upload_stats" in file.name:
            indicators = [
                {
                    "name": f"plis émis (M{code_machine})",
                    "frequency": "quotidienne",
                    "value": df["ID_PLIS"].nunique(),
                },
                {
                    "name": f"utilisateurs en envoi (M{code_machine})",
                    "frequency": "quotidienne",
                    "value": df["HASH_EXPE"].nunique(),
                },
                # {"name": "Nombre Go émis", "frequency": "quotidienne", à calculer},
                # Chaque taille contient son unité donc il faudra faire un peu de magie pour reconvertir en B ou en KB
                # sum_go_sent = int(pandas.to_numeric(df["TAILLE"]).sum()) / 1073741824
                # {"name": "Taille moyenne d'un pli (Mo)", "frequency": "quotidienne", df["HASH_EXPE"].nunique()},
                # (bloqué car dépend du calcul Go émis)
                # sum_go_sent / df["TAILLE"].count()
            ]

            for indicator in indicators:
                result = self.create_indicator(indicator, date, indicator["value"])
                if isinstance(result, models.Indicator):
                    response.append(serializers.IndicatorSerializer(result).data)
                else:
                    response.append(result)
        else:
            # FICHIERS DONNEES DE TELECHARGEMENT
            # Nombre de téléchargements des plis
            # Go téléchargés
            # Nombre d’utilisateurs téléchargements
            response.append("Not implemented yet.")
            pass

        return response
