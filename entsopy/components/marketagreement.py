from rich.prompt import Prompt
from const import DIRS
from components.table import create_table
from rich import print
import json
from rich import print
from utils.utils import extract_code_from_key


def input_market_agreement(is_type: bool = False) -> str:
    element = ""
    data = []
    if is_type:
        f = open(DIRS["type_market_agreement_type"], "r")
        element = "Type Market Agreement"
    else:
        f = open(DIRS["type_market_agreement_contract"], "r")
        element = "Contract Market Agreement"
    data = json.load(f)

    table = create_table(
        [f"{element.capitalize()}", "Code" "Key"],
        title=f"Select the [b]{element}[/b] of the data you want to download from the list below",
        rows=data,
    )
    print(table)

    selected_market_agreement = str(
        Prompt.ask(
            f"Insert the {element} you want to download data from\n",
            choices=[str(x["key"]) for x in data],
        )
    ).lower()

    market_agreement = extract_code_from_key(data, selected_market_agreement)

    return market_agreement
