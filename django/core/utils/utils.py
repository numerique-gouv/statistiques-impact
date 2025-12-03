from datetime import date, timedelta
import pandas
from django.core import exceptions
from datetime import date as dtdate
from core import models


def str_to_datetime(input_date: str) -> date:
    if type(input_date) is str:
        input_date = date.fromisoformat(input_date)
    return input_date


def get_last_day_of_month(input_date: str) -> date:
    # timedelta doesn't have a "month" attribute so we have to :
    next_month = str_to_datetime(input_date).replace(day=28) + timedelta(
        days=4
    )  # go through next month
    return next_month - timedelta(days=next_month.day)  # substract a few days


def get_last_month_limits():
    """Get last month's first and last day."""
    date_end = date.today().replace(day=1) - timedelta(days=1)
    date_start = date_end.replace(day=1)
    return date_start, date_end


def read_csv(filepath):
    try:
        return pandas.read_csv(filepath, delimiter=",")
    except UnicodeDecodeError:
        return pandas.read_csv(filepath, delimiter=",", compression="gzip")


def create_indicator(product, name, date, value, frequency, automatic_call=True):
    """Create indicator"""
    if type(date) is str:
        date = dtdate.fromisoformat(date)

    if type(product) is str:
        product = models.Product.objects.get(nom_service_public_numerique=product)

    try:
        new_entry = models.Indicator.objects.create(
            productid=product,
            indicateur=name,
            valeur=value,
            unite_mesure="unite",
            frequence_monitoring=frequency,
            date=date,
            date_debut=date.replace(day=1)
            if frequency == "mensuelle"
            else date
            if frequency == "quotidienne"
            else "",
            est_automatise=automatic_call,
            est_periode=True,
        )
    except exceptions.ValidationError as e:
        return e
    else:
        return new_entry
