import typer
from ui.table import createTable
from rich import print
import json


def extractAuction(auctions, autcion_to_extract: str) -> str:
    for a in auctions:
        if a["key"] == autcion_to_extract:
            return a["code"]


def inputAuctionType() -> str:
    element = "Direction"
    f = open("./data/auctions.json", "r")
    data_auctions = json.load(f)

    table = createTable(
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

    return extractAuction(data_auctions, selectedAuction)
