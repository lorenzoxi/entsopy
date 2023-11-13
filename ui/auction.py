import typer
from const import DIRS
from ui.table import create_table
from rich import print
import json


def extractAuction(auctions, autcion_to_extract: str) -> str:
    for a in auctions:
        if a["key"] == autcion_to_extract:
            return a["code"]


def input_auctiont_type() -> str:
    element = "Auction Type"
    data_auctions = json.load(open(DIRS["type_auctions"], "r"))

    table = create_table(
        [f"{element}", "Code", "Key"],
        title=f"Select the {element} of the data you want to download from the list below",
        rows=data_auctions,
    )
    print(table)

    selectedAuction = str(
        typer.prompt(
            f"Insert the {element} of the data you want to download",
        )
    ).lower()

    auction = extractAuction(data_auctions, selectedAuction)
    return auction
