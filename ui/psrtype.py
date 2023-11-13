import typer
from const import DIRS
from ui.table import create_table
from rich import print
import json
from rich import print


def input_psr_type() -> str:
    element = "PsrType"
    data_directions = json.load(DIRS["type_psrtypes"], "r")

    table = create_table(
        [f"{element}", "Code", "Key"],
        title=f"Select the {element} of the data you want to download from the list below",
        rows=data_directions,
    )
    print(table)

    psr_type = str(
        typer.prompt(
            f"Insert the {element} of the data you want to download",
        )
    ).lower()

    return psr_type
