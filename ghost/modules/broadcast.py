"""
This module requires Ghost: https://github.com/EntySec/Ghost
Current source: https://github.com/EntySec/Ghost
"""

from ghost.lib.module import Module


class GhostModule(Module):
    details = {
        'Category': "manage",
        'Name': "broadcast",
        'Authors': [
            'Loubaris Adam (Loubaris) - module developer'
        ],
        'Description': "Broadcast a notification on device.",
        'Comments': [
            ''
        ],
        'Usage': "broadcast 'message_with_underscores'",
        'MinArgs': 1,
        'NeedsRoot': False
    }

    def run(self, argc, argv):
        argv[1] = argv[1].replace("_", "")
        print(argv[1])
        output = self.device.send_command(f'am start -a "android.intent.action.SEND" --es "android.intent.extra.TEXT" {argv[1]} -t "text/plain"')
        self.print_empty(output)
