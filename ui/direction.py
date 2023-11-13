import typer
from const import DIRS
from ui.table import create_table
from rich import print
import json


def input_direction() -> str:
    element = "Direction"
    data_directions = json.load(open(DIRS["type_directions"], "r"))

    table = create_table(
        [f"{element}", "Code", "Key"],
        title=f"Select the {element} of the data you want to download from the list below",
        rows=data_directions,
    )
    print(table)

    direction = str(
        typer.prompt(
            f"Insert the {element} of the data you want to download",
        )
    ).lower()

    return direction
