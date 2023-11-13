import typer
from const import DIRS
from ui.table import create_table
from rich import print
import json
from rich import print


def extractMarketAgreement(agreements, agreement_to_extract: str) -> str:
    for art in agreements:
        if art["key"] == agreement_to_extract:
            print("the code is", art["code"])
            return art["code"]


def input_market_agreement(isType: bool = False) -> str:
    element = ""
    data = []
    if isType == True:
        f = open(DIRS["type_market_agreement_type"], "r")
        element = "Type Market Agreement"
    else:
        f = open(DIRS["type_market_agreement_contract"], "r")
        element = "Contract Market Agreement"
    data = json.load(f)

    table = create_table(
        [f"{element.capitalize()}", "Code" "Key"],
        title=f"Select the {element} of the data you want to download from the list below",
        rows=data,
    )
    print(table)

    selected_market_agreement = str(
        typer.prompt(
            f"Insert the code of one of the {element} you want to download data from",
        )
    ).lower()

    market_agreement = extractMarketAgreement(data, selected_market_agreement)

    return market_agreement
