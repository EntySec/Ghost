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

# Main theme color
_PURPLE = "#7B61FF"
_console = Console()


class ExternalCommand(Command):
    def __init__(self):
        super().__init__({
            'Category': "manage",
            'Name': "download",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - module developer'
            ],
            'Description': "Download file from device.",
            'Usage': "download <remote_file> <local_path>",
            'MinArgs': 2,
            'NeedsRoot': False
        })

    def print_process(self, message: str):
        panel = Panel.fit(
            Align.left(Text(message)),
            title=Text("PROCESS", style="bold white on " + _PURPLE),
            border_style=_PURPLE
        )
        _console.print(panel)

    def print_success(self, message: str):
        panel = Panel.fit(
            Align.left(Text(message)),
            title=Text("SUCCESS", style="bold white on " + _PURPLE),
            border_style=_PURPLE
        )
        _console.print(panel)

    def print_error(self, message: str):
        panel = Panel.fit(
            Align.left(Text(message)),
            title=Text("ERROR", style="bold white on " + _PURPLE),
            border_style="red"
        )
        _console.print(panel)

    def run(self, args):
        remote_file, local_path = args[1], args[2]
        self.print_process(f"Downloading {remote_file}...")

        success = self.device.download(remote_file, local_path)
        if success:
            self.print_success(f"File saved to {local_path}")
        else:
            self.print_error("Download failed!")
