from datetime import date, timedelta


def get_last_day_of_month(input_date: date) -> date:
    input_date = date.fromisoformat(input_date)
    last_day = input_date.replace(month=input_date.month + 1, day=1) - timedelta(days=1)
    return last_day
