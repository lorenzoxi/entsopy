from rich.table import Table
from rich import print
from entsopy.utils.const import *
from entsopy.components.panels.fail import panel_fail


def logtable(
    filename: str,
) -> None:
    name = DIRS[f"{filename}"]
    rows = open(name, "r").readlines()

    if len(rows) <= 0:
        panel_fail(
            "No logs found...",
            f"Please make sure you have downloaded some data.",
        )
        return None

    else:
        table = Table(
            title="LOG FILE",
            expand=True,
            title_style="yellow bold",
            show_lines=True,
        )
        table.add_column("Date", justify="left")
        table.add_column("API Call", justify="left")

        for row in rows:
            date = row.split("] ")[0] if len(row.split("] ")) > 1 else "No Date"
            date = date.replace("[", "")
            api_call = row.split("] ")[1] if len(row.split("] ")) > 1 else "No API Call"
            
            if (date == "No Date") or (api_call == "No API Call"):
                continue
            table.add_row(date, api_call)

        print(table)
