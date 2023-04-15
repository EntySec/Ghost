"""
This module requires Ghost: https://github.com/EntySec/Ghost
Current source: https://github.com/EntySec/Ghost
"""

import sys
import termios
import tty

from ghost.lib.module import Module


class GhostModule(Module):
    def __init__(self):
        super().__init__()

        self.details = {
            'Category': "manage",
            'Name': "keyboard",
            'Authors': [
                'Ivan Nikolsky (enty8080) - module developer'
            ],
            'Description': "Interact with device keyboard.",
            'Usage': "keyboard",
            'MinArgs': 0,
            'NeedsRoot': False
        }

    @staticmethod
    def get_char():
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

    def run(self, argc, argv):
        self.print_process("Interacting with keyboard...")
        self.print_success("Interactive connection spawned!")

        self.print_information("Type text below.")
        while True:
            self.device.send_command(f"input text {self.get_char()}")
