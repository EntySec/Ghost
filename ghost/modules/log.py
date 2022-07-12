"""
This module requires Ghost: https://github.com/EntySec/Ghost
Current source: https://github.com/EntySec/Ghost
"""

from ghost.lib.module import Module
import os

class GhostModule(Module):
    details = {
        'Category': "manage",
        'Name': "log",
        'Authors': [
            'Loubaris Adam (Loubaris) - module developer'
        ],
        'Description': "Save Ghost Framework usage history logs.",
        'Comments': [
            ''
        ],
        'Usage': "log <local_path> <number_of_lines>",
        'MinArgs': 2,
        'NeedsRoot': False
    }

    def run(self, argc, argv):
        self.print_information(f"Saving history to ", argv[1])
        if os.path.exists("history.log"):
            history_f = open('history.log', "r")
            lines = len(history_f.readlines())
            history_f.close()
            log_f = open(f"{argv[1]}/ghost_usage.log", "w")
            with open("history.log", "r") as file_log:
                content_f = file_log.readlines()
                for i in range(int(argv[2])):
                    log_f.write(f'{content_f[lines-(int(argv[2])-i)]}')
            log_f.close()
            self.print_information("Log file successfully created.")


        else: self.print_information(f"Ghost Framework History not available.")
        