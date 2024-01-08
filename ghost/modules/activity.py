"""
This module requires Ghost: https://github.com/EntySec/Ghost
Current source: https://github.com/EntySec/Ghost
"""

from ghost.lib.module import Module


class GhostModule(Module):
    def __init__(self):
        super().__init__()

        self.details.update({
            'Category': "settings",
            'Name': "activity",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - module developer'
            ],
            'Description': "Show device activity information.",
            'Usage': "activity",
            'MinArgs': 0,
            'NeedsRoot': False
        })

    def run(self, argc, argv):
        self.print_process("Getting activity information...")

        output = self.device.send_command("dumpsys activity")
        self.print_empty(output)
