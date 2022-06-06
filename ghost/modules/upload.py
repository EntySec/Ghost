"""
This module requires Ghost: https://github.com/EntySec/Ghost
Current source: https://github.com/EntySec/Ghost
"""

import os

from ghost.lib.module import Module


class GhostModule(Module):
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
        self.device.upload(argv[1], argv[2])
