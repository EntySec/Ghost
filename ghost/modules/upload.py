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
            'Name': "upload",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - module developer'
            ],
            'Description': "Upload file to device.",
            'Usage': "upload <local_file> <remote_path>",
            'MinArgs': 2,
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
        local_file, remote_path = args[1], args[2]
        self.print_panel("PROCESS", f"Uploading {local_file} to {remote_path}...")

        success = self.device.upload(local_file, remote_path)
        if success:
            self.print_panel("SUCCESS", f"File uploaded to {remote_path}")
        else:
            self.print_panel("ERROR", "Upload failed!", color="red")
