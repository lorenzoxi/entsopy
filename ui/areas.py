import typer
from const import DIRS
from ui.table import create_table
from rich import print
import json


def input_areas(area: str) -> str:
    end = False
    selectedAreas = []
    element = ""
    areas = []

    if area == "CTA":
        f = open(DIRS["areas_control_area"], "r")
        element = "control area"
    elif area == "BZN":
        f = open(DIRS["areas_bidding_zone"], "r")
        element = "bidding zone"
    elif area == "BZNS":
        f = open(DIRS["areas_border_bidding_zone"], "r")
        element = "border bidding zone"
    elif area == "MBAS":
        f = open(DIRS["areas_border_market_balancing_area"], "r")
        element = "border market balance area"

    areas = json.load(f)

    table = create_table(
        [f"{element.capitalize()}", "Code", "Key"],
        title=f"Select the {element} of the data you want to download from the list below",
        rows=areas,
    )
    print(table)

    while end == False:
        key = str(
            typer.prompt(
                f"Insert the {element} of the data you want to download",
            )
        ).lower()

        for area in areas:
            if key == area["key"]:
                tmp_area = area

        if tmp_area:
            selectedAreas.append(tmp_area)
            areas = [a for a in areas if a["key"] != tmp_area["key"]]

            if len(areas) > 0:
                end = typer.confirm(f"Do you want to add another {element}?")

                if end:
                    table = create_table(
                        ["Control Area", "Code"],
                        title=f"Select one of the remaining {element} of the data you want to download from the list below",
                        rows=areas,
                    )
                    print(table)
            else:
                print(f"No more {element}s available !")
                end = True

        else:
            print(
                f"[b][red]The {element} you inserted is not available![/red][b] Insert another one."
            )

    return selectedAreas
