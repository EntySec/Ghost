"""
This module requires Ghost: https://github.com/EntySec/Ghost
Current source: https://github.com/EntySec/Ghost
"""

from ghost.lib.module import Module


class GhostModule(Module):
    details = {
        'Category': "manage",
        'Name': "sleep",
        'Authors': [
            'Ivan Nikolsky (enty8080) - module developer'
        ],
        'Description': "Put device into sleep mode.",
        'Comments': [
            ''
        ],
        'Usage': "sleep",
        'MinArgs': 0,
        'NeedsRoot': False
    }

    def run(self, argc, argv):
        self.device.send_command("input keyevent 26")
