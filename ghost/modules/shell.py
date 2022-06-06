"""
This module requires Ghost: https://github.com/EntySec/Ghost
Current source: https://github.com/EntySec/Ghost
"""

from ghost.lib.module import Module


class GhostModule(Module):
    details = {
        'Category': "manage",
        'Name': "shell",
        'Authors': [
            'Ivan Nikolsky (enty8080) - module developer'
        ],
        'Description': "Execute shell command on device.",
        'Comments': [
            ''
        ],
        'Usage': "shell <command>",
        'MinArgs': 1,
        'NeedsRoot': False
    }

    def run(self, argc, argv):
        output = self.device.send_command(argv[1])
        self.print_empty(output)
