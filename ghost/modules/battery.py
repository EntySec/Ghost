"""
This module requires Ghost: https://github.com/EntySec/Ghost
Current source: https://github.com/EntySec/Ghost
"""

from badges.cmd import Command
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align

# Main theme color
_PURPLE = "#7B61FF"
_console = Console()


class ExternalCommand(Command):
    def __init__(self):
        super().__init__({
            'Category': "settings",
            'Name': "battery",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - module developer'
            ],
            'Description': "Show device battery information.",
            'Usage': "battery",
            'MinArgs': 0,
            'NeedsRoot': False
        })

    def print_process(self, message: str):
        panel = Panel.fit(
            Align.left(Text(message)),
            title=Text("PROCESS", style="bold white on " + _PURPLE),
            border_style=_PURPLE
        )
        _console.print(panel)

    def print_empty(self, message: str = ""):
        panel = Panel.fit(
            Align.left(Text(message if message else "No output.")),
            title=Text("OUTPUT", style="bold white on " + _PURPLE),
            border_style=_PURPLE
        )
        _console.print(panel)

    def run(self, _):
        self.print_process("Getting battery information...")

        output = self.device.send_command("dumpsys battery")
        self.print_empty(output)
