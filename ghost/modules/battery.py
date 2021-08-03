#!/usr/bin/env python3

#
# This module requires Ghost: https://github.com/EntySec/Ghost
# Current source: https://github.com/EntySec/Ghost
#

from ghost.core.cli.badges import Badges


class GhostModule:
    def __init__(self, device):
        self.device = device
        self.badges = Badges()

        self.details = {
            'Category': "settings",
            'Name': "battery",
            'Authors': [
                'enty8080'
            ],
            'Description': "Show device battery state.",
            'Comments': [
                ''
            ],
            'Usage': "battery",
            'MinArgs': 0,
            'NeedsRoot': False
        }

    def run(self):
        output = self.ghost.send_command("dumpsys battery")

        self.badges.print_information("Device Battery Information:")
        self.badges.print_empty(output)
