#!/usr/bin/env python3

#
# This module requires Ghost: https://github.com/EntySec/Ghost
# Current source: https://github.com/EntySec/Ghost
#

from ghost.lib.module import Module


class GhostModule(Module):
    details = {
        'Category': "manage",
        'Name': "download",
        'Authors': [
            'enty8080'
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

        if self.device.download(argv[0], argv[1]):
            self.print_success("File has been downloaded!")