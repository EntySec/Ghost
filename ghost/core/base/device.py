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
from adb_shell.adb_device import AdbDeviceTcp
from adb_shell.auth.keygen import keygen
from adb_shell.auth.sign_pythonrsa import PythonRSASigner

from ghost.core.base.loader import Loader
from ghost.core.cli.badges import Badges
from ghost.core.cli.colors import Colors
from ghost.core.cli.tables import Tables
from ghost.utils.fs import FSTools


class Device:
    """ Subclass of ghost.core.base module.

    This subclass of ghost.core.base module is intended for providing
    an implementation of device controller.
    """

    def __init__(self, host: str, port: int = 5555, timeout: int = 10,
                 key_filename: str = 'key') -> None:
        """ Initialize device.

        :param str host: device host
        :param int port: device port
        :param int timeout: connection timeout
        :param str key_filename: name of the file containing key
        :return None: None
        """

        self.badges = Badges()
        self.tables = Tables()
        self.colors = Colors()
        self.loader = Loader()

        self.fs = FSTools()
        self.host = host
        self.port = int(port)

        self.key_file = key_filename
        self.device = AdbDeviceTcp(self.host, self.port, default_transport_timeout_s=timeout)

    def get_keys(self) -> tuple:
        """ Get cryptographic keys.

        :return tuple: public key, private key
        """

        if not os.path.exists(self.key_file):
            keygen(self.key_file)

        with open(self.key_file, 'r') as file:
            priv = file.read()

        with open(self.key_file + '.pub', 'r') as file:
            pub = file.read()
        return pub, priv

    def send_command(self, command: str, output: bool = True) -> str:
        """ Send command to the device.

        :param str command: command to send to the device
        :param bool output: return command output or not
        :return str: empty if output is False otherwise command output
        """

        try:
            cmd_output = self.device.shell(command)
        except Exception:
            self.badges.print_error("Socket is not connected!")
            return None

        if output:
            return cmd_output
        return ""

    def list(self, path: str) -> list:
        """ List contents of the specified directory.

        :param str path: directory to list contents from
        :return list: list of directory contents
        """

        try:
            return self.device.list(path)
        except Exception:
            self.badges.print_error("Failed to list directory!")
        return []

    def connect(self) -> bool:
        """ Connect the specified device.

        :return bool: True if connection succeed
        """

        self.badges.print_process(f"Connecting to {self.host}...")
        try:
            keys = self.get_keys()
            signer = PythonRSASigner(*keys)

            self.device.connect(rsa_keys=[signer], auth_timeout_s=5)
            self.badges.print_success(f"Connected to {self.host}!")
            return True
        except Exception:
            self.badges.print_error(f"Failed to connect to {self.host}!")
        return False

    def disconnect(self) -> None:
        """ Disconnect the specified device.

        :return None: None
        """

        self.device.close()

    def download(self, input_file: str, output_path: str) -> bool:
        """ Download file from the specified device.

        :param str input_file: path of the file to download
        :param str output_path: path to output the file to
        :return bool: True if download succeed
        """

        exists, is_dir = self.fs.exists(output_path)

        if exists:
            if is_dir:
                output_path = output_path + '/' + os.path.split(input_file)[1]

            try:
                self.badges.print_process(f"Downloading {input_file}...")
                self.device.pull(input_file, output_path)

                self.badges.print_process(f"Saving to {output_path}...")
                self.badges.print_success(f"Saved to {output_path}!")

                return True
            except Exception:
                self.badges.print_error(f"Remote file: {input_file}: does not exist!")
        return False

    def upload(self, input_file: str, output_path: str) -> bool:
        """ Upload file to the specified device.

        :param str input_file: path of the file to upload
        :param str output_path: path to output the file to
        :return bool: True if upload succeed
        """

        if self.fs.exists_file(input_file):
            try:
                self.badges.print_process(f"Uploading {input_file}...")
                self.device.push(input_file, output_path)

                self.badges.print_process(f"Saving to {output_path}...")
                self.badges.print_success(f"Saved to {output_path}!")

                return True
            except Exception:
                self.badges.print_error(f"Remote directory: {output_path}: does not exist!")
        return False

    def is_rooted(self) -> bool:
        """ Check if the specified device is rooted.

        :return bool: True if device is rooted
        """

        responder = self.send_command('which su')
        if not responder or responder.isspace():
            return False
        return True

    def interact(self) -> None:
        """ Interact with the specified device.

        :return None: None
        """

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
                        ('clear', 'Clear terminal window.'),
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

                elif command[0] == 'clear':
                    self.badges.print_empty(self.colors.CLEAR, end='')

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
