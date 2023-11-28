import datetime
from matplotlib.dates import relativedelta


def check_date_not_tomorrow(date: datetime.datetime) -> bool:
    """
    Check if the given date is not tomorrow.

    Args:
        date (datetime.datetime): The date to check.

    Returns:
        bool: True if the date is not tomorrow, False otherwise.
    """
    today = datetime.datetime.today()
    if date > today:
        return False
    else:
        return True


def is_dates_diff_more_than_one_year(
    date1: datetime.datetime, date2: datetime.datetime
) -> bool:
    """
    Check if the difference between two dates is more than one year.

    Args:
        date1 (datetime.datetime): The first date.
        date2 (datetime.datetime): The second date.

    Returns:
        bool: True if the difference is more than one year, False otherwise.
    """
    if date2 - date1 > datetime.timedelta(days=365):
        return True
    else:
        return False


def calculate_dates_interval(
    date1: datetime.datetime, date2: datetime.datetime, time_type: str
) -> str:
    """
    Calculate the interval between two dates based on the given time type.

    Args:
        date1 (datetime.datetime): The first date.
        date2 (datetime.datetime): The second date.
        time_type (str): The type of time interval to calculate.

    Returns:
        str: The calculated time interval.
    """
    end_interval = date2.strftime("%Y-%m-%d")

    if time_type == "yyyy-mm-dd":
        # from 23 of the day before date1 to the 23 of the day date2
        day_before_start = (date1 - relativedelta(days=1)).strftime("%Y-%m-%d")
        end_day = end_interval

    elif time_type == "yyyy-mm":
        day_before_start = (date1 - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        end_day = (date2 + relativedelta(day=31)).strftime("%Y-%m-%d")

    elif time_type == "yyyy":
        day_before_start = (date1 - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        end_day = (date2 + relativedelta(yearday=365)).strftime("%Y-%m-%d")

    time_interval = f"{day_before_start}T23:00Z/{end_day}T23:00Z"

    return time_interval


def get_interval(date1: datetime.datetime, date2: datetime.datetime) -> str:
    """
    Get the interval between two dates in a specific format.

    Args:
        date1 (datetime.datetime): The first date.
        date2 (datetime.datetime): The second date.

    Returns:
        str: The interval between the two dates.
    """
    tmp_date1 = date1.strftime("%Y-%m-%dT%H:%MZ")
    tmp_date2 = date2.strftime("%Y-%m-%dT%H:%MZ")
    date = f"{tmp_date1}/{tmp_date2}"
    return date


def split_interval(interval: str) -> tuple:
    """
    Split the interval string into two datetime objects.

    Args:
        interval (str): The interval string.

    Returns:
        tuple: A tuple containing the two datetime objects.
    """
    dates = interval.split("/")
    date1 = datetime.datetime.strptime(dates[0], "%Y-%m-%dT%H:%MZ")
    date2 = datetime.datetime.strptime(dates[1], "%Y-%m-%dT%H:%MZ")
    return date1, date2


def get_format(time_type: str) -> str:
    """
    Get the date format based on the given time type.

    Args:
        time_type (str): The type of time interval.

    Returns:
        str: The date format.
    """
    time_format = ""
    if time_type == "yyyy-mm-dd":
        time_format = "%Y-%m-%d"
    elif time_type == "yyyy-mm":
        time_format = "%Y-%m"
    else:
        time_format = "%Y"

    return time_format


def date_diff(date1: datetime.datetime, date2: datetime.datetime) -> int:
    """
    Calculate the difference in days between two dates.

    Args:
        date1 (datetime.datetime): The first date.
        date2 (datetime.datetime): The second date.

    Returns:
        int: The difference in days.
    """
    diff = date2 - date1
    return diff.days
