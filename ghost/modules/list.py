"""
This module requires Ghost: https://github.com/EntySec/Ghost
Current source: https://github.com/EntySec/Ghost
"""

import datetime

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
        output = self.device.list(argv[1])

        if output:
            headers = ('Name', 'Mode', 'Size', 'Modification Time')
            data = list()

            for entry in sorted(output):
                timestamp = datetime.datetime.fromtimestamp(entry[3])
                data.append((entry[0].decode(), str(entry[1]), str(entry[2]), timestamp))

            self.print_table(f"Directory {argv[1]}", headers, *data)
