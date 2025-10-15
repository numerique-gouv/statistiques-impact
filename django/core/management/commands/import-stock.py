"""Management command to fill database with some demo objects."""

from django.core.management.base import BaseCommand, CommandError
from core import models
import os
import json
from core.utils import date_utils
from datetime import date as dtdate


class Command(BaseCommand):
    """
    If product exists, create indicators from files.
    """

    def add_arguments(self, parser):
        parser.add_argument("product", help="slug of the product you want to populate")
        parser.add_argument("filename", help="path to file you want imported")

    def handle(self, *args, **options):
        try:
            product = models.Product.objects.get(slug=options["product"])
        except models.Product.DoesNotExist:
            raise CommandError(f"Le produit '{options['product']}' n'existe pas.")

        file_path = options["filename"]
        try:
            os.path.isfile(file_path)
        except FileNotFoundError:
            raise CommandError(f"File '{file_path}'not found")

        if str(product) == "webinaire":
            self.import_webinaire_stock(product, file_path)

    def import_webinaire_stock(self, product, file_path, verbose=False):
        """Parse and create missing indicators for 'webinaire'."""
        if "nombre_de_participants" in file_path:
            indicateur = "participants"
            cle_valeur = "Somme de Attendee Count"
        elif "visio_par_mois" in file_path:
            indicateur = "visios"
            cle_valeur = "Nombre de lignes"
        else:
            raise CommandError("Ce type de fichier n'est pas encore traité.")

        self.stdout.write("Loading file ...")
        with open(file_path, "rb") as infile:
            data = json.load(infile)

            # remove current month as we only save count for whole months
            if data[-1]["Created At: Mois"].split("T")[0] == str(
                dtdate.today().replace(day=1)
            ):
                data.pop(-1)

            existing_records = models.Indicator.objects.filter(
                productid=product, indicateur=indicateur
            )
            nb_indicators_created = 0
            nb_errors = 0
            self.stdout.write("Date\tValeur enregistrée\tComparaison valeur fichier")
            for entry in data:
                date = entry["Created At: Mois"].split("T")[0]
                valeur = entry[cle_valeur]
                self.stdout.write(f"{date}", ending="\t")
                try:
                    record = existing_records.get(date_debut=date)
                    self.stdout.write(str(int(record.valeur)), ending="\t")
                    if valeur == record.valeur:
                        self.stdout.write("OK")
                    else:
                        nb_errors += 1
                        self.stdout.write(self.style.ERROR(f"!= {valeur}"))
                except models.Indicator.DoesNotExist:
                    nb_indicators_created += 1
                    models.Indicator.objects.create(
                        productid=product,
                        indicateur=indicateur,
                        valeur=valeur,
                        date_debut=date,
                        date=date_utils.get_last_day_of_month(date),
                        unite_mesure="unite",
                        frequence_monitoring="mensuelle",
                        est_automatise=False,
                        est_periode=True,
                    )
                    self.stdout.write(f"N/A\t+ {valeur}")

        self.stdout.write(
            f"Import terminé ! {nb_indicators_created} indicateurs ajoutés, {nb_errors} erreurs."
        )
