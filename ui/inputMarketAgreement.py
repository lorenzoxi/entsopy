import typer
from const import (
    CONTRACT_MARKET_AGREEMENT,
    TYPE_MARKET_AGREEMENT,
)
from ui.table import createTable
from rich import print


def extractMarketAgreement(agreements, agreement_to_extract: str) -> str:
    for art in agreements:
        if art["key"] == agreement_to_extract:
            print("the code is", art["code"])
            return art["code"]


def inputMarketAgreement(isType: bool = False) -> str:
    element = ""
    data = []
    if isType == False:
        data = CONTRACT_MARKET_AGREEMENT
        element = "Contract Market Agreement"
    else:
        data = TYPE_MARKET_AGREEMENT
        element = "Type Market Agreement"

    data

    table = createTable(
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
    return extractMarketAgreement(data, selected_market_agreement)
