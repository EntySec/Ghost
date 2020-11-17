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
import subprocess

from core.badges import badges
from core.transfer import transfer

class ghost:
    def __init__(self):
        self.badges = badges()
        self.transfer = transfer(self)

    def send_command(self, command, arguments="", multi_output=False, output=True):
        if multi_output:
            os.system("adb " + command + " " + arguments)
        else:
            command_output = subprocess.getoutput("adb " + command + " " + arguments)
            if output:
                return command_output.strip()

    def start_server(self):
        self.send_command("start-server", "", False, False)

    def stop_server(self):
        self.send_command("kill-server", "", False, False)

    def connect(self, target_addr):
        self.send_command("connect", target_addr, False, False)

    def disconnect(self, target_addr):
        self.send_command("disconnect", target_addr, False, False)

    def download(self, input_file, output_path):
        self.transfer.download(input_file, output_path)

    def upload(self, input_file, output_path):
        self.transfer.upload(input_file, output_path)

    def is_root(self):
        check_root = self.send_command("shell", "which su")
        if check_root == "":
            return False
        return True
