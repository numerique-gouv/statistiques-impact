from datetime import date, timedelta


def get_first_day_of_month(input_date: str) -> date:
    if type(input_date) is str:
        input_date = date.fromisoformat(input_date)
    return input_date.replace(day=1)


def get_last_day_of_month(input_date: str) -> date:
    input_date = date.fromisoformat(input_date)
    # timedelta doesn't have a "month" attribute so we have to :
    next_month = input_date.replace(day=28) + timedelta(days=4)  # go through next month
    return next_month - timedelta(days=next_month.day)  # substract a few days
