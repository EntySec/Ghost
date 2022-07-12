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
        'Usage': "broadcast",
        'MinArgs': 0,
        'NeedsRoot': False
    }

    def run(self, argc, argv):
        body = input("Message to broadcast >")
        output = self.device.send_command(f'am start -a "android.intent.action.SEND" --es "android.intent.extra.TEXT" {body} -t "text/plain"')
        self.print_empty(output)
