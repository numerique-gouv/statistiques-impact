from datetime import date, timedelta


def get_previous_day(input_date):
    day = date.fromisoformat(input_date)
    previous_day = day - timedelta(days=1)
    return previous_day
