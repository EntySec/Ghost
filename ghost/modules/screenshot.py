"""
This module requires Ghost: https://github.com/EntySec/Ghost
Current source: https://github.com/EntySec/Ghost
"""

import os

from ghost.lib.module import Module


class GhostModule(Module):
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

    def run(self, argc, argv):
        self.print_process(f"Taking screenshot...")
        self.device.send_command("screencap /data/local/tmp/screenshot.png")

        self.device.download('/data/local/tmp/screenshot.png', argv[1])
        self.device.send_command("rm /data/local/tmp/screenshot.png")
