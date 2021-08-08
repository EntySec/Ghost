#!/usr/bin/env python3

#
# This module requires Ghost: https://github.com/EntySec/Ghost
# Current source: https://github.com/EntySec/Ghost
#

import os

from ghost.lib.module import Module
from ghost.utils.fs import FSTools


class GhostModule(Module):
    fs = FSTools()

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

        exists, file = self.fs.exists_directory(argv[0])
        if exists and file == 'file':
            if self.device.download('/data/local/tmp/screenshot.png', argv[0]):
                self.print_success("Screenshot has been downloaded!")

        if exists and file == 'directory':
            if self.device.download('/data/local/tmp/screenshot.png', argv[0] + '/screenshot.png'):
                self.print_success("Screenshot has been downloaded!")
                
        self.device.send_command("rm /data/local/tmp/screenshot.png")
