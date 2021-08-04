#!/usr/bin/env python3

#
# This module requires Ghost: https://github.com/EntySec/Ghost
# Current source: https://github.com/EntySec/Ghost
#

from ghost.lib.module import Module


class Module(Module):
    details = {
        'Category': "settings",
        'Name': "activity",
        'Authors': [
            'enty8080'
        ],
        'Description': "Show device activity information.",
        'Comments': [
            ''
        ],
        'Usage': "activity",
        'MinArgs': 0,
        'NeedsRoot': False
    }

    def run(self, argc, argv):
        self.print_process("Getting activity information...")

        output = self.device.send_command("dumpsys activity")
        self.print_empty(output)
