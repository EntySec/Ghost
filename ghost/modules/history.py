"""
This module requires Ghost: https://github.com/EntySec/Ghost
Current source: https://github.com/EntySec/Ghost
"""

from ghost.lib.module import Module
import os

class GhostModule(Module):
    details = {
        'Category': "manage",
        'Name': "history",
        'Authors': [
            'Loubaris Adam (Loubaris) - module developer'
        ],
        'Description': "Show Ghost Framework usage history.",
        'Comments': [
            ''
        ],
        'Usage': "history",
        'MinArgs': 0,
        'NeedsRoot': False
    }

    def run(self, argc, argv):
        self.print_process(f"Preparing history...")
        if os.path.exists("history.log"):
            history_f = open('history.log', "r")
            print(history_f.read())
            history_f.close()
        else: self.print_process(f"Ghost Framework History not available.")

        