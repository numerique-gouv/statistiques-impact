from datetime import date, timedelta


def get_previous_day(input_date):
    day = date.fromisoformat(input_date)
    previous_day = day - timedelta(days=1)
    return previous_day


def get_last_day_of_month(input_date):
    day = date.fromisoformat(input_date)
    last_day = day.replace(month=day.month + 1, day=1) - timedelta(days=1)
    return last_day
