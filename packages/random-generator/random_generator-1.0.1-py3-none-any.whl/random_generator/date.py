import random as random_libs
from datetime import datetime, timedelta


def date(start_date: str = '1980-01-01', end_date: str = 'Today'):
    if end_date == 'Today':
        end_date = datetime.now().strftime("%Y-%m-%d")

    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    delta = end - start
    random_days = random_libs.randrange(delta.days)
    random_date = start + timedelta(days=random_days)
    return random_date.strftime("%Y-%m-%d")
