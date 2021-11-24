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
        self.print_process(f"Downloading {argv[0]}...")

        exists, is_dir = self.exists(argv[1])
        if exists:
            if is_dir:
                path = argv[1] + '/' + os.path.split(argv[0])[1]
            else:
                path = argv[1]

            if self.device.download(argv[0], argv[1]):
                self.print_success("File has been downloaded!")
