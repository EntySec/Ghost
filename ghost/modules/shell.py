"""
This module requires Ghost: https://github.com/EntySec/Ghost
Current source: https://github.com/EntySec/Ghost
"""

from badges.cmd import Command
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align

_PURPLE = "#7B61FF"
_console = Console()


class ExternalCommand(Command):
    def __init__(self):
        super().__init__({
            'Category': "manage",
            'Name': "shell",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - module developer'
            ],
            'Description': "Execute shell command on device.",
            'Usage': "shell <command>",
            'MinArgs': 1,
            'NeedsRoot': False
        })

    def print_panel(self, title: str, message: str, color: str = _PURPLE):
        panel = Panel.fit(
            Align.left(Text(message if message else "No output.")),
            title=Text(title, style=f"bold white on {color}"),
            border_style=color
        )
        _console.print(panel)

    def run(self, args):
        command = ' '.join(args[1:])
        self.print_panel("PROCESS", f"Executing shell command: {command}")
        output = self.device.send_command(command)
        self.print_panel("OUTPUT", output)
