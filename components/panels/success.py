from rich.panel import Panel
from const import DIRS
from rich import print


def panel_success(message: str = "File sucessfully downloaded") -> None:
    print(
        Panel(
            f"[b][green]{message}[/green][/b]",
            highlight=True,
        )
    )
    return
