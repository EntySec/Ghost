"""
This module requires Ghost: https://github.com/EntySec/Ghost
Current source: https://github.com/EntySec/Ghost
"""

import os

from ghost.lib.module import Module


class GhostModule(Module):
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
        self.device.download(argv[1], argv[2])
