#!/usr/bin/env python3

#
# This module requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from ghost.core.cli.badges import Badges


class GhostModule:
    def __init__(self, device):
        self.device = device
        self.badges = Badges()

        self.details = {
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

    def run(self):
        self.badges.output_process("Getting activity information...")

        output = self.device.send_command("dumpsys activity")
        self.badges.output_empty(output)
