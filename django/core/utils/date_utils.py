from datetime import date, timedelta


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
