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

import readline
import sys

from ghost.core.base.device import Device
from ghost.core.cli.badges import Badges
from ghost.core.cli.colors import Colors
from ghost.core.cli.tables import Tables


class Console:
    """ Subclass of ghost.core.base module.

    This subclass of ghost.core.base modules is intended for providing
    main Ghost Framework console interface.
    """

    def __init__(self) -> None:
        """ Initialize console.

        :return None: None
        """

        self.badges = Badges()
        self.colors = Colors()
        self.tables = Tables()

        self.devices = dict()
        self.banner = """{}{}
   .--. .-.               .-.
  : .--': :              .' `.
  : : _ : `-.  .--.  .--.`. .'
  : :; :: .. :' .; :`._-.': :
  `.__.':_;:_;`.__.'`.__.':_;

--=[ {}Ghost Framework 8.0.0{}
--=[ Developed by EntySec ({}https://entysec.netlify.app/{})
""".format(self.colors.CLEAR, self.colors.END,
           self.colors.BOLD + self.colors.WHITE,
           self.colors.END, self.colors.LINE, self.colors.END)

    def shell(self) -> None:
        """ Run console shell.

        :return None: None
        """

        self.badges.print_empty(self.banner)

        readline.parse_and_bind('tab: complete')
        while True:
            try:
                command = input(
                    f'{self.colors.REMOVE}(ghost)> '
                ).strip()
                command = command.split()

                if not command:
                    continue

                if command[0] == 'help':
                    self.tables.print_table("Core Commands", ('Command', 'Description'), *[
                        ('clear', 'Clear terminal window.'),
                        ('connect', 'Connect device.'),
                        ('devices', 'Show connected devices.'),
                        ('disconnect', 'Disconnect device.'),
                        ('exit', 'Exit Ghost Framework.'),
                        ('help', 'Show available commands.'),
                        ('interact', 'Interact with device.')
                    ])

                elif command[0] == 'exit':
                    for device in list(self.devices):
                        self.devices[device]['device'].disconnect()
                        del self.devices[device]
                    sys.exit(0)

                elif command[0] == 'clear':
                    self.badges.print_empty(self.colors.CLEAR, end='')

                elif command[0] == 'connect':
                    if len(command) < 2:
                        self.badges.print_empty("Usage: connect <address>")
                    else:
                        args = command[1].split(':')

                        if len(args) == 2:
                            host, port = args[0], args[1]

                            device = Device(args[0], args[1])
                            connected = device.connect()
                        else:
                            host, port = args[0], 5555

                            device = Device(args[0])
                            connected = device.connect()

                        if connected:
                            self.devices.update({
                                len(self.devices): {
                                    'host': host,
                                    'port': str(port),
                                    'device': device
                                }
                            })
                            self.badges.print_empty("")

                            self.badges.print_information(
                                f"Type {self.colors.GREEN}devices{self.colors.END} to list all connected devices.")
                            self.badges.print_information(
                                f"Type {self.colors.GREEN}interact {str(len(self.devices) - 1) + self.colors.END} to interact this device."
                            )

                elif command[0] == 'devices':
                    if self.devices:
                        devices = list()
                        for device in self.devices:
                            devices.append((device, self.devices[device]['host'], self.devices[device]['port']))

                        self.tables.print_table("Connected Devices", ('ID', 'Host', 'Port'), *devices)
                    else:
                        self.badges.print_warning("No devices connected.")

                elif command[0] == 'disconnect':
                    if len(command) < 2:
                        self.badges.print_empty("Usage: disconnect <id>")
                    else:
                        if int(command[1]) in self.devices:
                            self.devices[int(command[1])]['device'].disconnect()
                            del self.devices[int(command[1])]
                        else:
                            self.badges.print_error("Invalud device id!")

                elif command[0] == 'interact':
                    if len(command) < 2:
                        self.badges.print_empty("Usage: interact <id>")
                    else:
                        if int(command[1]) in self.devices:
                            self.badges.print_process(f"Interacting with device {command[1]}...")
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
