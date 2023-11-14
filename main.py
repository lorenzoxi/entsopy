from rich.prompt import Prompt
from classes.httpsclient import HttpsClient
import typer
from rich import print
from rich.panel import Panel
from rich.console import Console
from components.domain import input_domain
from components.home import main_flow
from dotenv import load_dotenv
from components.panels.fail import panel_fail
from components.panels.success import panel_success
from components.welcome import welcome

load_dotenv()

app = typer.Typer(
    help="""Welcome to ENTSOPY your assistant for downloading data from entso-e transparency platform.""",
)


@app.command(help="Start Entsopy App")
def start():
    client = HttpsClient()

    welcome()

    domain = input_domain()

    res = main_flow(client=client, domain=domain)

    if res:
        panel_success()
    else:
        panel_fail()


if __name__ == "__main__":
    app()
