from const import DIRS
from components.table import create_table
from rich import print
import json
from rich.prompt import Prompt

from utils.utils import extract_code_from_key


def input_auctiont_type(isCategory: bool = False) -> str:
    element = "Auction Type"
    if isCategory == True:
        f = open(DIRS["type_auctions_type"], "r")
        element = "Auction Category"
    else:
        f = open(DIRS["type_auctions_category"], "r")
        element = "Auction Type"

    data = json.load(f)

    table = create_table(
        [f"{element}", "Code", "Key"],
        title=f"Select the [b]{element}[/b] of the data you want to download from the list below",
        rows=data,
    )
    print(table)

    selected_auction = str(
        Prompt.ask(
            f"Insert the [b gold1]{element}[/b gold1] of the data you want to download",
            choices=[str(x["key"]) for x in data],
        )
    ).lower()

    auction = extract_code_from_key(data, selected_auction)
    return auction
