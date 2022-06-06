"""
This module requires Ghost: https://github.com/EntySec/Ghost
Current source: https://github.com/EntySec/Ghost
"""

from ghost.lib.module import Module


class GhostModule(Module):
    details = {
        'Category': "settings",
        'Name': "battery",
        'Authors': [
            'Ivan Nikolsky (enty8080) - module developer'
        ],
        'Description': "Show device battery information.",
        'Comments': [
            ''
        ],
        'Usage': "battery",
        'MinArgs': 0,
        'NeedsRoot': False
    }

    def run(self, argc, argv):
        self.print_process("Getting battery information...")

        output = self.device.send_command("dumpsys battery")
        self.print_empty(output)
