from rich.panel import Panel
from const import DIRS
from rich import print


def panel_success(
    message: str = f"File [file_name] sucessfully downloaded", file_name: str = ""
) -> None:
    if file_name != "":
        message = message.replace("[file_name]", file_name)

    print(
        Panel(
            f"[b][green]{message}[/green][/b]",
            highlight=True,
        )
    )
    return
