from rich.panel import Panel
from rich import print
import toml 

def welcome_panel() -> None:
    """
    Displays a welcome panel with information about ENTSOPY and a link to the official entso-e website.
    """
    
    # Reading the TOML file
    with open("pyproject.toml", 'r') as toml_file:
        data = toml.load(toml_file)
    
    version = data['tool']['poetry']['version']
    
    print(
        Panel(
            f"Welcome to [cornflower_blue]ENTSOPY[/cornflower_blue] {version}: your assistant for downloading data from entso-e "
            "transparency platform.\nVisit the official entso-e website here: ["
            "link=https://transparency.entsoe.eu/]transparency.entsoe.eu[/link]",
            style="white",
            title="[b][cornflower_blue]ENTSOPY[/cornflower_blue][/b]",
            title_align="center",
        )
    )
