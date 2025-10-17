"""
This module requires Ghost: https://github.com/EntySec/Ghost
Current source: https://github.com/EntySec/Ghost
"""

import datetime
from badges.cmd import Command
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align

_PURPLE = "#7B61FF"
_console = Console()


class ExternalCommand(Command):
    def __init__(self):
        super().__init__({
            'Category': "manage",
            'Name': "list",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - module developer'
            ],
            'Description': "List directory contents.",
            'Usage': "list <remote_path>",
            'MinArgs': 1,
            'NeedsRoot': False
        })

    def print_panel(self, title: str, message: str):
        panel = Panel.fit(
            Align.left(Text(message)),
            title=Text(title, style=f"bold white on {_PURPLE}"),
            border_style=_PURPLE
        )
        _console.print(panel)

    def print_table_rich(self, title: str, headers: tuple, rows: list):
        table = Table(title=title, header_style=f"bold {_PURPLE}", border_style=_PURPLE)
        for h in headers:
            table.add_column(h, style="white", no_wrap=True)
        for row in rows:
            table.add_row(*[str(i) for i in row])
        _console.print(table)

    def run(self, args):
        self.print_panel("PROCESS", f"Listing directory: {args[1]}")

        output = self.device.list(args[1])
        if output:
            headers = ('Name', 'Mode', 'Size', 'Modification Time')
            rows = []
            for entry in sorted(output):
                timestamp = datetime.datetime.fromtimestamp(entry[3]).strftime("%Y-%m-%d %H:%M:%S")
                rows.append((entry[0].decode(), str(entry[1]), str(entry[2]), timestamp))
            self.print_table_rich(f"Directory {args[1]}", headers, rows)
        else:
            self.print_panel("INFO", "No files found in this directory.")
