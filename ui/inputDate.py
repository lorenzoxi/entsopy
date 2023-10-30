import datetime
import typer
from utils.date import *


def inputDate(
    time_type: str,
    range="",
) -> datetime.datetime:
    # TODO: check consistency of dates (date_1 > date_2)

    format = get_format(time_type)

    date_1 = str(
        typer.prompt(
            f"Insert the [b]start date[/b] with the format {time_type}",
        )
    ).lower()
    date_1 = datetime.datetime.strptime(date_1, f"{format}")

    date_2 = str(
        typer.prompt(
            f"Insert the [b]end date[/b] with the format {time_type}",
        )
    ).lower()
    date_2 = datetime.datetime.strptime(date_2, f"{format}")

    date = dates_interval(date_1, date_2, time_type)

    return date
