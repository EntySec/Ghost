"""
This module requires Ghost: https://github.com/EntySec/Ghost
Current source: https://github.com/EntySec/Ghost
"""

import os

from badges.cmd import Command


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

    def run(self, args):
        self.print_process(f"Taking screenshot...")
        self.device.send_command("screencap /data/local/tmp/screenshot.png")

        self.device.download('/data/local/tmp/screenshot.png', args[1])
        self.device.send_command("rm /data/local/tmp/screenshot.png")
