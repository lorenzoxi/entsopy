import datetime
from rich.prompt import Prompt
from utils.date import *


def input_date(
    time_type: str,
    range="",
) -> datetime.datetime:
    # TODO: check consistency of dates (date_1 > date_2)

    format = get_format(time_type)
    element = "start date"
    date_1 = str(
        Prompt.ask(
            f"Insert the [b gold1]{element}[/b gold1] with the format {time_type}",
        )
    ).lower()
    date_1 = datetime.datetime.strptime(date_1, f"{format}")

    element = "end date"
    date_2 = str(
        Prompt.ask(
            f"Insert the [b gold1]{element}[/b gold1] with the format {time_type}",
        )
    ).lower()
    date_2 = datetime.datetime.strptime(date_2, f"{format}")

    date = dates_interval(date_1, date_2, time_type)

    return date
