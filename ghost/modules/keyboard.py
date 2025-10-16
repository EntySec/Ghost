"""
This module requires Ghost: https://github.com/EntySec/Ghost
Current source: https://github.com/EntySec/Ghost
"""

import sys
import termios
import tty
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
            'Name': "keyboard",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - module developer'
            ],
            'Description': "Interact with device keyboard.",
            'Usage': "keyboard",
            'MinArgs': 0,
            'NeedsRoot': False
        })

    def print_panel(self, title: str, message: str, color: str = _PURPLE):
        panel = Panel.fit(
            Align.left(Text(message)),
            title=Text(title, style=f"bold white on {color}"),
            border_style=color
        )
        _console.print(panel)

    @staticmethod
    def get_char():
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

    def run(self, _):
        self.print_panel("PROCESS", "Interacting with keyboard...")
        self.print_panel("SUCCESS", "Interactive connection spawned!")
        self.print_panel("INFO", "Type text below.", color="cyan")

        while True:
            self.device.send_command(f"input text {self.get_char()}")
