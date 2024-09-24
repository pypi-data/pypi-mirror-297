import datetime

import rich
from rich.columns import Columns
from rich.console import Group
from rich.padding import Padding
from rich.panel import Panel
from rich.prompt import Prompt
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

console = rich.get_console()


def ask_with_help(title: str, desc: str, enter: str):
    console.print(
        Panel(
            Group(
                Padding(Text(title, style="bold cyan"), (0, 1)),
                Padding(Text(desc, style="italic"), (0, 2)),
            ),
            expand=False,
            border_style="dim white",
        )
    )
    return Prompt.ask(Text(enter, style="cyan"))


def spinner(title):
    return console.status(title, spinner_style="green")


def title(msg: str):
    console.print(msg, style="bold cyan")


def section_start(text: str):
    console.print(Panel(Text(text, style="bold cyan"), border_style="cyan"))
    console.rule(style="dim cyan bold")


def section_end():
    console.rule(style="dim cyan bold")


def success(title: str, lines: list):
    console.print(
        Panel(
            Group(
                Text(title, style="bold green"),
                Rule(style="dim green"),
                Padding(Group(*lines), (0, 1)),
            ),
            expand=False,
            border_style="dim green",
        )
    )


def highlight(text: str):
    return f"[bold blue]{text}[/]"


def command(text: str):
    return f"[bold cyan]{text.upper()}[/]"


def config(app: str, client: str, project: str, project_id: str):
    table = Table(show_header=False, box=rich.box.SIMPLE_HEAD)
    table.add_column("", style="cyan", justify="right")
    table.add_column("", justify="right")
    table.add_row("App:", app)
    table.add_row("Client:", client)
    table.add_row("Project:", project)
    table.add_row("Project ID:", project_id)

    console.print(table)


def log(time: datetime.datetime, message: str):
    time_str = time.strftime("%H:%M:%S")
    console.print(Columns([Text(f"{time_str}", style="dim cyan"), message]))


def error(title: str = None, lines: list = []):
    texts = []
    if title:
        texts.append(Text(title, style="bold red"))
    texts.extend(map(lambda m: Text(m, style="red"), lines))

    console.print(
        Panel(
            Group(*texts),
            expand=False,
            title_align="left",
            title=Text("ERROR", style="dim red bold"),
            highlight=True,
            border_style="red",
        )
    )
