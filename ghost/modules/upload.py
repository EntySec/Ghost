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
        'Name': "upload",
        'Authors': [
            'Ivan Nikolsky (enty8080) - module developer'
        ],
        'Description': "Upload file to device.",
        'Comments': [
            ''
        ],
        'Usage': "upload <local_file> <remote_path>",
        'MinArgs': 2,
        'NeedsRoot': False
    }

    def run(self, argc, argv):
        self.print_process(f"Uploading {argv[0]}...")

        if self.fs.file(argv[0]):
            self.device.upload(argv[0], argv[1])
