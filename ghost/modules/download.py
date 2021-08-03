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
            'Name': "download",
            'Authors': [
                'enty8080'
            ],
            'Description': "Download remote file.",
            'Comments': [
                ''
            ],
            'Usage': "download <remote_file> <local_path>",
            'MinArgs': 2,
            'NeedsRoot': False
        }

    def run(self, args):
        self.device.download(args.split()[0], args.split()[1])
