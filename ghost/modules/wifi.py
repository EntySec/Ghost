"""
This module requires Ghost: https://github.com/EntySec/Ghost
Current source: https://github.com/EntySec/Ghost
"""

from ghost.lib.module import Module


class GhostModule(Module):
    details = {
        'Category': "settings",
        'Name': "wifi",
        'Authors': [
            'Ivan Nikolsky (enty8080) - module developer'
        ],
        'Description': "Set device wifi service state.",
        'Comments': [
            ''
        ],
        'Usage': "wifi <on|off>",
        'MinArgs': 1,
        'NeedsRoot': False
    }

    def run(self, argc, argv):
        if argv[1] in ['on', 'off']:
            if argv[1] == 'on':
                self.device.send_command("svc wifi enable")
            else:
                self.device.send_command("svc wifi disable")
        else:
            self.print_empty(f"Usage: {self.details['Usage']}")
