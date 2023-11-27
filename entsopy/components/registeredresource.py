from rich.prompt import Prompt
from const import DIRS
from components.table import create_table
from rich import print
from rich import print


def input_registeredsource() -> str:
    element = "EIC code"
    data = []

    ask_text = (
        f"Insert the [b gold1]{element}[/b gold1] of the Registered Resource you want to download data from\n. \nYou can find the list of approved EIC codes here: [link=https://www.entsoe.eu/data/energy-identification-codes-eic/eic-approved-codes/]entsoe.eu/data/energy-identification-codes-eic/eic-approved-codes[/link]",
    )

    registered_source = str(Prompt.ask(ask_text)).lower()

    return registered_source
