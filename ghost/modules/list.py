#!/usr/bin/env python3

#
# This module requires Ghost: https://github.com/EntySec/Ghost
# Current source: https://github.com/EntySec/Ghost
#

from ghost.lib.module import Module


class GhostModule(Module):
    details = {
        'Category': "manage",
        'Name': "list",
        'Authors': [
            'Ivan Nikolsky (enty8080) - module developer'
        ],
        'Description': "List directory contents.",
        'Comments': [
            ''
        ],
        'Usage': "list <remote_path>",
        'MinArgs': 1,
        'NeedsRoot': False
    }

    def run(self, argc, argv):
        output = self.device.list(argv[0])

        if output:
            self.print_empty(output)
