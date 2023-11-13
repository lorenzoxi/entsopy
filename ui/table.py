from rich.table import Table


def create_table(
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
            row["code"] if "code" in row else "",
            row["key"]
            if "is_available" in row and row["is_available"] == True
            else (row["key"] if "is_available" not in row else ":x:"),
        )

    return table
