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

from adb_shell.adb_device import AdbDeviceTcp

from ghost.core.cli.badges import Badges
from ghost.core.base.loader import Loader


class Device:
    def __init__(self, host, port=5555, timeout=10):
        self.badges = Badges()
        self.loader = Loader(self)

        self.host = host
        self.port = int(port)

        self.address = f"{self.host}:{str(self.port)}"
        self.device = AdbDeviceTcp(self.host, self.port, default_transport_timeout_s=10)

    def send_command(self, command, output=True):
        try:
            cmd_output = self.device.shell(command)
        except Exception:
            self.badges.print_error("Socket is not connected!")
        if output:
            return cmd_output
        return None

    def connect(self):
        self.badges.print_process(f"Connecting to {self.address}...")
        if not self.device.connect():
            self.badges.print_error(f"Failed to connect to {self.address}!")

    def disconnect(self, target_addr):
        self.device.close()

    def download(self, input_file, output_path):
        try:
            self.device.pull(input_file, output_path)
        except Exception:
            self.badges.print_error(f"Failed to download from {self.address}!")

    def upload(self, input_file, output_path):
        try:
            self.device.push(input_file, output_path)
        except Exception:
            self.badges.print_error(f"Failed to upload to {self.address}!")

    def is_rooted(self):
        responder = self.send_command('which su')
        if not responder or responder.isspace():
            return False
        return True

    def interact(self):
        commands = sorted(self.loader.load_modules())

        while True:
            try:
                command = input(f'ghost({self.address})> ').strip()
                command = command.split()

                if command[0] == 'help':
                    self.tables.print_table("Core Commands", ('Command', 'Description'), [
                        ('exit', 'Exit current device.'),
                        ('help', 'Show available commands.')
                    ])

                    if commands:
                        commands_data = dict()
                        headers = ("Command", "Description")
                        for cmd in commands:
                            label = commands[cmd].details['category']
                            commands_data[label] = list()
                        for cmd in commands:
                            label = commands[cmd].details['category']
                            commands_data[label].append((cmd, commands[cmd].details['description']))
                        for label in commands_data:
                            self.print_table(label.title() + " Commands", headers, *commands_data[label])

                elif command[0] == 'exit':
                    break

                else:
                    if command[0] in commands:
                        if commands[command[0]].details['needs_args']:
                            if (len(command) - 1) < int(commands[command[0]].details['args']):
                                self.badges.print_empty("Usage: " + commands[command[0]].details['usage'])
                            else:
                                if commands[command[0]].details['needs_root']:
                                    if self.is_rooted():
                                        commands[command[0]].run(arguments)
                                    else:
                                        self.badges.print_error("Target device is not rooted!")
                                else:
                                    commands[command[0]].run(arguments)
                        else:
                            if commands[command[0]].details['needs_root']:
                                if self.is_rooted():
                                    commands[command[0]].run()
                                else:
                                    self.badges.print_error("Target device is not rooted!")
                            else:
                                commands[command[0]].run()
                    else:
                        self.badges.print_error("Unrecognized command!")
            except (EOFError, KeyboardInterrupt):
                pass
            except Exception as e:
                self.badges.print_error("An error occurred: " + str(e) + "!")
