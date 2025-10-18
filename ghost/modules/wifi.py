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
            'Category': "settings",
            'Name': "wifi",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - module developer'
            ],
            'Description': "Set device wifi service state.",
            'Usage': "wifi <on|off>",
            'MinArgs': 1,
            'NeedsRoot': False
        })

    def print_panel(self, title: str, message: str, color: str = _PURPLE):
        panel = Panel.fit(
            Align.left(Text(message)),
            title=Text(title, style=f"bold white on {color}"),
            border_style=color
        )
        _console.print(panel)

    def run(self, args):
        state = args[1].lower()
        if state in ['on', 'off']:
            action = "enable" if state == 'on' else "disable"
            self.print_panel("PROCESS", f"Turning WiFi {state}...")
            self.device.send_command(f"svc wifi {action}")
            self.print_panel("SUCCESS", f"WiFi turned {state} successfully!")
        else:
            self.print_panel("USAGE", f"Usage: {self.info['Usage']}", color="red")
