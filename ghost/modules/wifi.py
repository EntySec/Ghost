"""
This module requires Ghost: https://github.com/EntySec/Ghost
Current source: https://github.com/EntySec/Ghost
"""

from badges.cmd import Command


class ExternalCommand(Command):
    def __init__(self):
        super().__init__({
            'Category': "settings",
            'Name': "wifi",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - module developer'
            ],
            'Description': "Set device wifi service state.",
            'Usage': "wifi <on|off>",
            'MinArgs': 1,
            'NeedsRoot': False
        })

    def run(self, args):
        if args[1] in ['on', 'off']:
            if args[1] == 'on':
                self.device.send_command("svc wifi enable")
            else:
                self.device.send_command("svc wifi disable")
        else:
            self.print_usage(self.info['Usage'])
