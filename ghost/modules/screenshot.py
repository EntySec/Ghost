#!/usr/bin/env python3

#
# This module requires Ghost: https://github.com/EntySec/Ghost
# Current source: https://github.com/EntySec/Ghost
#

import os

from ghost.lib.module import Module


class GhostModule(Module, FSTools):
    details = {
        'Category': "manage",
        'Name': "screenshot",
        'Authors': [
            'Ivan Nikolsky (enty8080) - module developer'
        ],
        'Description': "Take device screenshot.",
        'Comments': [
            ''
        ],
        'Usage': "screenshot <local_path>",
        'MinArgs': 1,
        'NeedsRoot': False
    }

    def run(self, argc, argv):
        self.print_process(f"Taking screenshot...")
        self.device.send_command("screencap /data/local/tmp/screenshot.png")

        exists, is_dir = self.exists(argv[0])
        if exists:
            if is_dir:
                path = argv[0] + '/screenshot.png'
            else:
                path = argv[0]

            if self.device.download('/data/local/tmp/screenshot.png', path):
                self.print_success("Screenshot has been downloaded!")

        self.device.send_command("rm /data/local/tmp/screenshot.png")
