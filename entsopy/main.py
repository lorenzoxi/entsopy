import os
from classes.httpsclient import HttpsClient
import typer
from components.panels.fail import panel_fail
from components.panels.success import panel_success
from components.welcome import welcome_panel
from components.domain import input_domain
from components.home import home
from components.welcome import welcome_panel
from dotenv import load_dotenv
from components.securitytoken import input_security_token

load_dotenv()

app = typer.Typer(
    help="""Welcome to ENTSOPY your assistant for dowloading data from entso-e transparency platform.""",
)


@app.command(help="Start Entsopy App")
def start():
    token = os.getenv("SECURITY_TOKEN")

    if token is None:
        token = input_security_token()

    client = HttpsClient(token)

    welcome_panel()

    domain = input_domain()

    res = home(client=client, domain=domain)

    if res:
        panel_success(file_name=res)
    else:
        panel_fail()


if __name__ == "__main__":
    app()
