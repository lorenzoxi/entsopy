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
from components.logging.logtable import logtable
from const import DIRS
from logger.logger import LOGGER
import sys, traceback

""" Main module of the app. """

load_dotenv()

app = typer.Typer(
    help="""Welcome to ENTSOPY your assistant for dowloading data from entso-e transparency platform.""",
)


@app.command(help="Start Entsopy App")
def start():
    try:
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

    except Exception as e:
        panel_fail("Error!", f"{e}. Traceback: {traceback.format_exc()}")
        LOGGER.info(f"ERROR: {e}.\nTraceback: {traceback.format_exc()}")


@app.command("reset", help="Reset the security token and clear the log file.")
def reset():
    input_security_token()
    open(DIRS["log"], "w").close()
    panel_success("Security token successfully replaced and log file cleared.")


@app.command("log", help="Show logs of the app")
def log(command: str):
    if command == "clear":
        open(DIRS["log"], "w").close()
        panel_success("Log file cleared")
    elif command == "show":
        logtable("log")


if __name__ == "__main__":
    app()
