#!/usr/bin/env python3

#
# This module requires Ghost: https://github.com/EntySec/Ghost
# Current source: https://github.com/EntySec/Ghost
#

import os

from ghost.lib.module import Module
from ghost.utils.fs import FSTools


class GhostModule(Module, FSTools):
    details = {
        'Category': "manage",
        'Name': "download",
        'Authors': [
            'Ivan Nikolsky (enty8080) - module developer'
        ],
        'Description': "Download file from device.",
        'Comments': [
            ''
        ],
        'Usage': "download <remote_file> <local_path>",
        'MinArgs': 2,
        'NeedsRoot': False
    }

    def run(self, argc, argv):
        self.print_process(f"Downloading {argv[1]}...")

        exists, is_dir = self.exists(argv[2])
        if exists:
            if is_dir:
                path = argv[2] + '/' + os.path.split(argv[1])[2]
            else:
                path = argv[2]

            if self.device.download(argv[1], argv[2]):
                self.print_success("File has been downloaded!")
