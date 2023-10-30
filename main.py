from classes.client import HttpsClient
import typer
from rich import print
from rich.panel import Panel
from rich.console import Console
from ui.table import createTable
import json
from domains.domain import handle
from dotenv import load_dotenv

load_dotenv()

app = typer.Typer(
    help="""Welcome to ENTOPY your assistant for downloading data from entso-e transparency platform.""",
)


@app.command(help="Start entopy app")
def start():
    console = Console()
    client = HttpsClient()

    print(
        Panel(
            "Welcome to [cornflower_blue]ENTOPY[/cornflower_blue]: your assistant for downloading data from entso-e transparency platform.\nVisit the official entso-e website here: [link=https://transparency.entsoe.eu/]https://transparency.entsoe.eu/[/link]",
            style="white",
            title="[b][cornflower_blue]ENTSOPY[/cornflower_blue][/b]",
            title_align="center",
        )
    )

    f = open("./data/domains.data.json", "r")
    data = json.load(f)
    table = createTable(
        ["Domain", "Code", "Key to press"],
        title="Select the domain type of the data you want to download from the list below",
        rows=data,
    )
    console.print(table)

    domain = str(
        typer.prompt(
            "Insert the code of the domain you want to download data from",
        )
    ).lower()

    if domain == "1":
        data = domain(client=client, domain=domain)

    elif domain == "2":
        data = domain(client=client, domain=domain)

    else:
        typer.Abort()

    print(
        Panel(
            "[b][green]File sucessfully downloaded![/green][/b]",
            highlight=True,
        )
    )


if __name__ == "__main__":
    app()
