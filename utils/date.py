import datetime
from dateutil import relativedelta


def checkDateIsNotFuture(date: datetime.datetime) -> bool:
    today = datetime.datetime.today()
    if date > today:
        return False
    else:
        return True


def isDatesDifferenceLongerThanAYear(
    date1: datetime.datetime, date2: datetime.datetime
) -> bool:
    if date2 - date1 > datetime.timedelta(days=365):
        return True
    else:
        return False


def dates_interval(
    date1: datetime.datetime, date2: datetime.datetime, time_type: str
) -> str:
    tmp_date1 = date1.strftime("%Y-%m-%d")

    days = months = years = 0

    if time_type == "yyyy-mm-dd":
        days = 1
    elif time_type == "yyyy-mm":
        months = 1
    elif time_type == "yyyy":
        years = 1

    tmp_date2 = date2 + relativedelta.relativedelta(
        years=years, months=months, days=days
    )
    tmp_date2 = tmp_date2.strftime("%Y-%m-%d")
    date = f"{tmp_date1}T00:00Z/{tmp_date2}T00:00Z"

    return date


def get_interval(date1: datetime.datetime, date2: datetime.datetime) -> str:
    tmp_date1 = date1.strftime("%Y-%m-%dT%H:%MZ")
    tmp_date2 = date2.strftime("%Y-%m-%dT%H:%MZ")
    date = f"{tmp_date1}/{tmp_date2}"
    return date


def split_interval(interval: str) -> dict:
    dates = interval.split("/")
    date1 = datetime.datetime.strptime(dates[0], "%Y-%m-%dT%H:%MZ")
    date2 = datetime.datetime.strptime(dates[1], "%Y-%m-%dT%H:%MZ")
    return date1, date2


def get_format(time_type: str):
    format = ""
    if time_type == "yyyy-mm-dd":
        format = "%Y-%m-%d"
    elif time_type == "yyyy-mm":
        format = "%Y-%m"
    else:
        format = "%Y"

    return format


def date_diff(date1: datetime.datetime, date2: datetime.datetime) -> int:
    diff = date2 - date1
    return diff.days
