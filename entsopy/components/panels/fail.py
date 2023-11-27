from rich.panel import Panel
from const import DIRS
from rich import print


def panel_fail(
    message: str = "Something went wrong, file not downloaded",
    error_description: str = "No error description provided",
) -> None:
    print(
        Panel(
            f"[b][red]{message}[/red][/b]\n. Error: {error_description}.",
            highlight=True,
        )
    )
    return
