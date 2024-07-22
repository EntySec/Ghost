"""
This module requires Ghost: https://github.com/EntySec/Ghost
Current source: https://github.com/EntySec/Ghost
"""

from badges.cmd import Command


class ExternalCommand(Command):
    def __init__(self):
        super().__init__({
            'Category': "manage",
            'Name': "sleep",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - module developer'
            ],
            'Description': "Put device into sleep mode.",
            'Usage': "sleep",
            'MinArgs': 0,
            'NeedsRoot': False
        })

    def run(self, _):
        self.device.send_command("input keyevent 26")
