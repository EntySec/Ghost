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
            'Category': "managing",
            'Name': "click",
            'Authors': [
                'jaxparrow07'
            ],
            'Description': "Click the specified x and y axis.",
            'Comments': [
                ''
            ],
            'Usage': "click <x> <y>",
            'MinArgs': 2,
            'NeedsRoot': False
        }

    def run(self, args):
        self.device.send_command("\"input tap " + args + "\"")
