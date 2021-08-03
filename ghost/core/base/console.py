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

import sys
import readline

from ghost.core.cli.badges import Badges
from ghost.core.cli.colors import Colors
from ghost.core.cli.tables import Tables

from ghost.core.base.device import Device


class Console:
    def __init__(self):
        self.badges = Badges()
        self.colors = Colors()
        self.tables = Tables()

        self.devices = dict()
        self.banner = """
 .--. .-.               .-.
: .--': :              .' `.
: : _ : `-.  .--.  .--.`. .'
: :; :: .. :' .; :`._-.': :
`.__.':_;:_;`.__.'`.__.':_;

{}You has been ghosted!{}
""".format(self.colors.BOLD + self.colors.WHITE,
           self.colors.END)

    def shell(self):
         readline.parse_and_bind('tab: complete')
         while True:
            try:
                command = input('ghost> ').strip()
                command = command.split()

                if command[0] == 'help':
                    self.tables.print_table("Core Commands", ('Command', 'Description'), [
                        ('connect', 'Connect device.'),
                        ('devices', 'Show connected devices.'),
                        ('exit', 'Exit Ghost Framework.'),
                        ('help', 'Show available commands.'),
                        ('interact', 'Interact with device.')
                    ])

                elif command[0] == 'exit':
                    sys.exit(0)

                elif command[0] == 'connect':
                    if len(command) < 2:
                        self.badges.print_empty("Usage: connect <address>")
                    else:
                        self.badges.print_process("Connecting to device...")
                        args = command[1].split(':')

                        if len(args) == 2:
                            device = Device(args[0], args[1])
                            connected = device.connect()
                        else:
                            device = Device(args[0])
                            connected = device.connect()

                        if connected:
                            self.devices.update({
                                len(self.devices): {
                                    'address': args[0],
                                    'device': device
                                }
                            })
                            self.badges.print_success("Connection succeed!")
                        else:
                            self.badges.print_error("Connection failed!")

                elif command[0] == 'devices':
                    if self.devices:
                        devices = list()
                        for device in self.devices:
                            devices.append((device, self.devices[device]['address']))

                        self.tables.print_table("Connected Devices", ('ID', 'Address'), devices)
                    else:
                        self.badges.print_warning("No devices connected.")

                elif command[0] == 'interact':
                    if len(command) < 2:
                        self.badges.print_empty("Usage: interact <id>")
                    else:
                        if int(command[1]) in self.devices:
                            device = self.devices[int(command[1])]['device']
                            device.interact()
                        else:
                            self.badges.print_error("Invalid device id!")
                else:
                    self.badges.print_error("Unrecognized command!")
            except (EOFError, KeyboardInterrupt):
                pass
            except Exception as e:
                self.badges.print_error("An error occurred: " + str(e) + "!")
