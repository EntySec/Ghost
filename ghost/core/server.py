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
import sys
import time

from ghost.core.badges import Badges
from ghost.core.ghost import Ghost
from ghost.core.helper import Helper


class Server:
    def __init__(self):
        self.badges = Badges()
        self.helper = Helper()
        self.ghost = Ghost()

    def connect(self, rhost, rport):
        target_addr = rhost + ":" + str(rport)
        print(self.badges.G + "Connecting to " + target_addr + "...")
        self.ghost.start_server()
        self.ghost.connect(target_addr)
        is_connected = self.ghost.send_command("devices", "| grep " + target_addr)
        is_offline = self.ghost.send_command("devices", "| grep offline")
        if is_connected == "":
            print(self.badges.E + "Failed to connect to " + target_addr + "!")
            self.ghost.disconnect(target_addr)
            sys.exit()
        else:
            if is_offline != "":
                print(self.badges.E + "Failed to connect to " + target_addr + "!")
                self.ghost.disconnect(target_addr)
                sys.exit()
        time.sleep(0.5)

        from ghost.core.shell import Shell
        shell = Shell(self.ghost)

        shell.shell(target_addr)
