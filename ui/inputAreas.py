import typer
from ui.table import createTable
from rich import print
import json


def inputAreas(area: str, ask_only_two_areas: bool = False) -> str:
    go_on = True
    selectedAreas = []
    element = ""
    areas = []

    f = open("./data/areas/biddingZone.json", "r")
    data_bidding_zones = json.load(f)
    f = open("./data/areas/borderBiddingZone.json", "r")
    data_border_bidding_zones = json.load(f)
    f = open("./data/areas/controlArea.json", "r")
    data_control_areas = json.load(f)

    if area == "CTA":
        areas = data_control_areas
        element = "control area"
    elif area == "BZN":
        areas = data_bidding_zones
        element = "bidding zone"
    elif area == "BZN-BZN":
        areas = data_border_bidding_zones
        element = "border bidding zone"

    if ask_only_two_areas == False:
        table = createTable(
            [f"{element.capitalize()}", "Code", "Key"],
            title=f"Select the {element} of the data you want to download from the list below",
            rows=areas,
        )
        print(table)

        while go_on == True:  # TODO: refactor this
            key = str(
                typer.prompt(
                    f"Insert the {element} of the data you want to download",
                )
            ).lower()

            for area in areas:
                if key == area["key"]:  # TODO: make functions for this
                    tmp_area = area

            if tmp_area:
                selectedAreas.append(tmp_area)
                areas = [a for a in areas if a["key"] != tmp_area["key"]]

                if len(areas) > 0:
                    go_on = typer.confirm(f"Do you want to add another {element}?")

                    if go_on:
                        table = createTable(
                            ["Control Area", "Code"],
                            title=f"Select one of the remaining {element} of the data you want to download from the list below",
                            rows=areas,
                        )
                        print(table)
                else:
                    print(f"No more {element}s available !")
                    go_on = False

            else:
                print(
                    f"[b][red]The {element} you inserted is not available![/red][b] Insert another one."
                )
    else:
        # ask only two areas
        table = createTable(
            [f"{element.capitalize()}", "Code", "Key"],
            title=f"Select the {element} of the data you want to download from the list below",
            rows=areas,
        )
        print(table)
        key = str(
            typer.prompt(
                f"Insert the {element} of the data you want to download",
            )
        ).lower()
        for area in areas:
            if key == area["key"]:
                sel_area = area

        selectedAreas.append(sel_area)

    return selectedAreas
