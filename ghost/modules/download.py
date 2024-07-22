"""
This module requires Ghost: https://github.com/EntySec/Ghost
Current source: https://github.com/EntySec/Ghost
"""

import os

from badges.cmd import Command


class ExternalCommand(Command):
    def __init__(self):
        super().__init__({
            'Category': "manage",
            'Name': "download",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - module developer'
            ],
            'Description': "Download file from device.",
            'Usage': "download <remote_file> <local_path>",
            'MinArgs': 2,
            'NeedsRoot': False
        })

    def run(self, args):
        self.device.download(args[1], args[2])
