"""
This module requires Ghost: https://github.com/EntySec/Ghost
Current source: https://github.com/EntySec/Ghost
"""

import sys
import termios
import tty

from badges.cmd import Command


class ExternalCommand(Command):
    def __init__(self):
        super().__init__({
            'Category': "manage",
            'Name': "keyboard",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - module developer'
            ],
            'Description': "Interact with device keyboard.",
            'Usage': "keyboard",
            'MinArgs': 0,
            'NeedsRoot': False
        })

    @staticmethod
    def get_char():
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

    def run(self, _):
        self.print_process("Interacting with keyboard...")
        self.print_success("Interactive connection spawned!")

        self.print_information("Type text below.")
        while True:
            self.device.send_command(f"input text {self.get_char()}")
