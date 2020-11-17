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

from core.badges import badges
from core.ghost import ghost

class GhostModule:
    def __init__(self):
        self.badges = badges()
        self.ghost = ghost()

        self.name = "sysinfo"
        self.description = "Get device system information."
        self.usage = "Usage: sysinfo"
        self.type = "settings"
        self.args = 1

    def run(self, cmd_data):
        system = "Android"
        hostname = self.ghost.send_command("shell", "getprop net.hostname")
        username = self.ghost.send_command("shell", "getprop ro.product.name")
        version = self.ghost.send_command("shell", "getprop ro.build.version.release")
        architecture = self.ghost.send_command("shell", "getprop ro.product.cpu.abi")
        information = ""
        information += f"{self.badges.I}Operating System: {system}\n"
        information += f"{self.badges.I}Computer Hostname: {hostname}\n"
        information += f"{self.badges.I}Computer Username: {username}\n"
        information += f"{self.badges.I}Release Version: {version}\n"
        information += f"{self.badges.I}Processor Architecture: {architecture}"
        print(information)
