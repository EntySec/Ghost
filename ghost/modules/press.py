"""
This module requires Ghost: https://github.com/EntySec/Ghost
Current source: https://github.com/EntySec/Ghost
"""

from ghost.lib.module import Module


class GhostModule(Module):
    details = {
        'Category': "manage",
        'Name': "press",
        'Authors': [
            'Ivan Nikolsky (enty8080) - module developer'
        ],
        'Description': "Press device button by keycode.",
        'Comments': [
            ''
        ],
        'Usage': "press <keycode>",
        'MinArgs': 1,
        'NeedsRoot': False
    }

    def run(self, argc, argv):
        if int(argv[1]) < 124:
            self.device.send_command(f"input keyevent {argv[1]}")
        else:
            self.print_error("Invalid keycode!")
