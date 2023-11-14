from rich.prompt import Prompt
from const import DIRS
from components.table import create_table
import json
from rich import print

from utils.utils import extract_code_from_key


def input_psrtype() -> str:
    element = "PsrType"
    data = json.load(DIRS["type_psrtypes"], "r")

    table = create_table(
        [f"{element}", "Code", "Key"],
        title=f"Select the [b]{element}[/b] of the data you want to download from the list below",
        rows=data,
    )
    print(table)

    selected_psr_type = str(
        Prompt.ask(
            f"Insert the [b gold1]{element}[/b gold1] of the data you want to download",
            choices=[str(x["key"]) for x in data],
        )
    ).lower()

    psr_type = extract_code_from_key(data, selected_psr_type)

    return psr_type
