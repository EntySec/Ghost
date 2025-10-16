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
            'Name': "press",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - module developer'
            ],
            'Description': "Press device button by keycode.",
            'Usage': "press <keycode>",
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
        keycode = int(args[1])
        if keycode < 124:
            self.print_panel("PROCESS", f"Pressing device button with keycode: {keycode}")
            self.device.send_command(f"input keyevent {keycode}")
            self.print_panel("SUCCESS", "Key event sent successfully!")
        else:
            self.print_panel("ERROR", "Invalid keycode!", color="red")
