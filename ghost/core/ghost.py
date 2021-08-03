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
import subprocess
import sys

from adb_shell.adb_device import AdbDeviceTcp

from ghost.core.badges import Badges
from ghost.core.transfer import Transfer


class Ghost:
    def __init__(self, host, port, timeout=10):
        self.badges = Badges()

        self.device = AdbDeviceTcp(host, int(port), default_transport_timeout_s=10)

    def send_command(self, command, output=True):
        try:
            cmd_output = self.device.shell(command)
        except Exception:
            self.badges.output_error("Socket is not connected!")
        if output:
            return cmd_output
        return None
            
    def connect(self):
        if not self.device.connect():
            self.badges.output_error("Failed to connect!")

    def disconnect(self, target_addr):
        self.device.close()

    def download(self, input_file, output_path):
        try:
            self.device.pull(input_file, output_path)
        except Exception:
            self.badges.output_error("Failed to download!")

    def upload(self, input_file, output_path):
        try:
            self.device.push(input_file, output_path)
        except Exception:
            self.badges.output_error("Failed to upload!")
