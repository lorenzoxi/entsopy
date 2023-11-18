from rich.panel import Panel
from rich import print


def welcome_panel() -> None:
    print(
        Panel(
            "Welcome to [cornflower_blue]ENTSOPY[/cornflower_blue]: your assistant for downloading data from entso-e "
            "transparency platform.\nVisit the official entso-e website here: ["
            "link=https://transparency.entsoe.eu/]transparency.entsoe.eu[/link]",
            style="white",
            title="[b][cornflower_blue]ENTSOPY[/cornflower_blue][/b]",
            title_align="center",
        )
    )
