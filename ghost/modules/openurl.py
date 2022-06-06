"""
This module requires Ghost: https://github.com/EntySec/Ghost
Current source: https://github.com/EntySec/Ghost
"""

from ghost.lib.module import Module


class GhostModule(Module):
    details = {
        'Category': "manage",
        'Name': "openurl",
        'Authors': [
            'Ivan Nikolsky (enty8080) - module developer'
        ],
        'Description': "Open URL on device.",
        'Comments': [
            ''
        ],
        'Usage': "openurl <url>",
        'MinArgs': 1,
        'NeedsRoot': False
    }

    def run(self, argc, argv):
        if not argv[1].startswith(("http://", "https://")):
            argv[1] = "http://" + argv[1]

        self.device.send_command(f'am start -a android.intent.action.VIEW -d "{argv[1]}"')
