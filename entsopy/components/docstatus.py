from rich.prompt import Prompt
from const import DIRS
from components.table import create_table
from rich import print
import json
from utils.utils import extract_code_from_key


def input_docstatus() -> str:
    """
    Prompts the user to select a document status from a list and returns the corresponding code.

    Returns:
        str: The code of the selected document status.
    """
    element = "DocStatus"
    data = json.load(open(DIRS["type_docstatus"], "r"))

    table = create_table(
        [f"{element}", "Code", "Key"],
        title=f"Select the [b]{element}[/b] of the data you want to download from the list below",
        rows=data,
    )
    print(table)

    selected_docstatus = str(
        Prompt.ask(
            f"Insert the [b gold1]{element}[/b gold1] of the data you want to download",
            choices=[str(x["key"]) for x in data],
        )
    ).lower()

    docstatus = extract_code_from_key(data, selected_docstatus)
    return docstatus
