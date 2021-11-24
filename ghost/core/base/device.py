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
from ghost.core.cli.tables import Tables
from ghost.core.cli.colors import Colors
from ghost.core.base.loader import Loader


class Device:
    def __init__(self, host, port=5555, timeout=10):
        self.badges = Badges()
        self.tables = Tables()
        self.colors = Colors()
        self.loader = Loader()

        self.host = host
        self.port = int(port)

        self.device = AdbDeviceTcp(self.host, self.port, default_transport_timeout_s=10)

    def send_command(self, command, output=True):
        try:
            cmd_output = self.device.shell(command)
        except Exception:
            self.badges.print_error("Socket is not connected!")
        if output:
            return cmd_output
        return None
    
    def list(self, path):
        try:
            return self.device.list(path)
        except Exception:
            self.badges.print_error("Failed to list directory!")
        return None

    def connect(self):
        self.badges.print_process(f"Connecting to {self.host}...")
        try:
            self.device.connect()
            self.badges.print_success(f"Connected to {self.host}!")
            return True
        except Exception:
            self.badges.print_error(f"Failed to connect to {self.host}!")
        return False

    def disconnect(self):
        self.device.close()
        return True

    def download(self, input_file, output_path):
        try:
            self.device.pull(input_file, output_path)
            return True
        except Exception:
            self.badges.print_error(f"Failed to download from {self.host}!")
        return False

    def upload(self, input_file, output_path):
        try:
            self.device.push(input_file, output_path)
            return True
        except Exception:
            self.badges.print_error(f"Failed to upload to {self.host}!")
        return False

    def is_rooted(self):
        responder = self.send_command('which su')
        if not responder or responder.isspace():
            return False
        return True

    def interact(self):
        self.badges.print_success("Interactive connection spawned!")

        self.badges.print_empty("")
        self.badges.print_process("Loading device modules...")

        commands = self.loader.load_modules(self)
        self.badges.print_information(f"Modules loaded: {str(len(commands))}")

        while True:
            try:
                command = input(
                    f'{self.colors.REMOVE}(ghost: {self.colors.RED}'
                    f'{self.host}{self.colors.END})> '
                ).strip()
                command = command.split()

                if not command:
                    continue

                if command[0] == 'help':
                    self.tables.print_table("Core Commands", ('Command', 'Description'), *[
                        ('exit', 'Exit current device.'),
                        ('help', 'Show available commands.')
                    ])

                    if commands:
                        commands_data = dict()
                        headers = ("Command", "Description")
                        for cmd in sorted(commands):
                            label = commands[cmd].details['Category']
                            commands_data[label] = list()
                        for cmd in sorted(commands):
                            label = commands[cmd].details['Category']
                            commands_data[label].append((cmd, commands[cmd].details['Description']))
                        for label in commands_data:
                            self.tables.print_table(label.title() + " Commands", headers, *commands_data[label])

                elif command[0] == 'exit':
                    break

                else:
                    if command[0] in commands:
                        if (len(command) - 1) < int(commands[command[0]].details['MinArgs']):
                            self.badges.print_empty("Usage: " + commands[command[0]].details['Usage'])
                        else:
                            if commands[command[0]].details['NeedsRoot']:
                                if self.is_rooted():
                                    commands[command[0]].run(len(command), command)
                                else:
                                    self.badges.print_error("Target device is not rooted!")
                            else:
                                commands[command[0]].run(len(command), command)
                    else:
                        self.badges.print_error("Unrecognized command!")
            except (EOFError, KeyboardInterrupt):
                pass
            except Exception as e:
                self.badges.print_error("An error occurred: " + str(e) + "!")
