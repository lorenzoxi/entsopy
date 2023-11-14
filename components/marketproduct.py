from rich.prompt import Prompt
from const import DIRS
from components.table import create_table
from rich import print
import json
from rich import print
from utils.utils import extract_code_from_key


def input_market_product(isStandard: bool = True) -> str:
    element = ""
    data = []
    if isStandard == True:
        element = "Standard Market Product"
    else:
        element = "Original Market Product"
    data = json.load(open(DIRS["type_market_product"], "r"))

    table = create_table(
        [f"{element.capitalize()}", "Code" "Key"],
        title=f"Select the [b]{element}[/b] of the data you want to download from the list below",
        rows=data,
    )
    print(table)

    selected_market_product = str(
        Prompt.ask(
            f"Insert the {element} you want to download data from\n",
            choices=[str(x["key"]) for x in data],
        )
    ).lower()

    market_product = extract_code_from_key(data, selected_market_product)

    return market_product
