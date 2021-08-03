#!/usr/bin/env python3

#
# MIT License
#
# Copyright (c) 2020 EntySec
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import os
import readline

from ghost.core.cli.badges import Badges
from ghost.core.cli.ghost import Ghost


class Console:
    def __init__(self):
        self.badges = Badges()
        self.helper = Helper()

    def banner(self):
        print("""
  ________.__                    __        ,
 /  _____/|  |__   ____  _______/  |_       \\`-,      ,     =-
/   \\  ___|  |  \\ /  _ \\/  ___/\\   __\\  .-._/   \\_____)\\
\\    \\_\\  \\   Y  (  <_> )___ \\  |  |   ("              / =-
 \\______  /___|  /\\____/____  > |__|    '-;   ,_____.-'       =-
        \\/     \\/           \\/            /__.'
""")

        print("Ghost Framework " + self.helper.version)
        print("--------------------")

    def shell(self):
         readline.parse_and_bind('tab: complete')
         while True:
            try:
                command = input('ghost> ').strip()
                command = command.split()

                if command[0] == 'connect':
                    if len(command) < 2:
                        self.badges.output_empty("Usage: connect <>")

                else:
                    print(self.badges.E + "Unrecognized command!")
             except (EOFError, KeyboardInterrupt):
                 pass
             except Exception as e:
                 print("An error occurred: " + str(e) + "!")
