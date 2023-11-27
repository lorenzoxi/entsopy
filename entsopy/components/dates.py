import datetime
from rich.prompt import Prompt
from utils.date import *


def input_date(
    time_type: str,
    time_range="",
) -> str:
    time_format = get_format(time_type)
    element = "start date"
    date_1 = str(
        Prompt.ask(
            f"Insert the [b gold1]{element}[/b gold1] with the format {time_type}",
        )
    ).lower()
    date_1 = datetime.datetime.strptime(date_1, f"{time_format}")
    date_2 = date_1 - datetime.timedelta(days=1)

    element = "end date"
    while date_2 < date_1:
        date_2 = str(
            Prompt.ask(
                f"Insert the [b gold1]{element}[/b gold1] with the format {time_type}",
            )
        ).lower()
        date_2 = datetime.datetime.strptime(date_2, f"{time_format}")

        if date_1 > date_2:
            print(
                f"[b red]The end date must be greater than the start date[/b red]. Please insert again the end date."
            )

    dates_interval = calculate_dates_interval(date_1, date_2, time_type)
    print("> the date is: ", dates_interval)
    return dates_interval
