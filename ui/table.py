from rich.table import Table
from classes.article import Article


def createTable(
    headers: list,
    title: str,
    rows: list,
) -> Table:
    table = Table(
        *headers, expand=True, title=title, title_style="yellow bold", show_lines=True
    )

    for row in rows:
        table.add_row(
            row["name"],
            row["code"],
            row["key"] if row["is_available"] else ":x:",
        )

    return table
