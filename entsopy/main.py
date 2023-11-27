from classes.httpsclient import HttpsClient
import typer
from components.panels.fail import panel_fail
from components.panels.success import panel_success
from components.welcome import welcome_panel
from components.domain import input_domain
from components.home import main_flow
from components.welcome import welcome_panel
from environs import Env

env = Env()

app = typer.Typer(
    help="""Welcome to ENTSOPY your assistant for downloadcing data from entso-e transparency platform.""",
)


@app.command(help="Start Entsopy App")
def start():
    env.read_env()
    client = HttpsClient(env.str("SECURITY_TOKEN"))

    welcome_panel()

    domain = input_domain()

    res = main_flow(client=client, domain=domain)

    if res:
        panel_success(file_name=res)
    else:
        panel_fail()


if __name__ == "__main__":
    app()
