"""
This module requires Ghost: https://github.com/EntySec/Ghost
Current source: https://github.com/EntySec/Ghost
"""

from badges.cmd import Command


class ExternalCommand(Command):
    def __init__(self):
        super().__init__({
            'Category': "manage",
            'Name': "press",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - module developer'
            ],
            'Description': "Press device button by keycode.",
            'Usage': "press <keycode>",
            'MinArgs': 1,
            'NeedsRoot': False
        })

    def run(self, args):
        if int(args[1]) < 124:
            self.device.send_command(f"input keyevent {args[1]}")
        else:
            self.print_error("Invalid keycode!")
