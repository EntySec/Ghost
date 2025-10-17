"""
This module requires Ghost: https://github.com/EntySec/Ghost
Current source: https://github.com/EntySec/Ghost
"""

import os
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
            'Name': "screenshot",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - module developer'
            ],
            'Description': "Take device screenshot.",
            'Usage': "screenshot <local_path>",
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
        local_path = args[1]
        self.print_panel("PROCESS", "Taking screenshot on device...")

        self.device.send_command("screencap /data/local/tmp/screenshot.png")
        success = self.device.download('/data/local/tmp/screenshot.png', local_path)

        if success:
            self.print_panel("SUCCESS", f"Screenshot saved to {local_path}")
        else:
            self.print_panel("ERROR", "Failed to download screenshot!", color="red")

        self.device.send_command("rm /data/local/tmp/screenshot.png")
