import typer
from ui.table import createTable
from rich import print
import json


def inputDirection() -> str:
    element = "Direction"
    data_directions = [
        {
            "name": "Import",
            "key": "1",
            "code": "IMPRT",
        },
        {
            "name": "Export",
            "key": "2",
            "code": "EXPRT",
        },
    ]

    table = createTable(
        [f"{element}", "Code", "Key"],
        title=f"Select the {element} of the data you want to download from the list below",
        rows=data_directions,
    )
    print(table)

    selectedDirection = str(
        typer.prompt(
            f"Insert the {element} of the data you want to download",
        )
    ).lower()

    return selectedDirection
