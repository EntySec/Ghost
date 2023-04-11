"""
MIT License

Copyright (c) 2020-2023 EntySec

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import cmd
import sys

from ghost.core.base.device import Device
from ghost.core.cli.badges import Badges
from ghost.core.cli.colors import Colors
from ghost.core.cli.tables import Tables


class Console(cmd.Cmd):
    """ Subclass of ghost.core.base module.

    This subclass of ghost.core.base modules is intended for providing
    main Ghost Framework console interface.
    """

    def __init__(self) -> None:
        super().__init__()
        cmd.Cmd.__init__(self)

        self.badges = Badges()
        self.colors = Colors()
        self.tables = Tables()

        self.devices = dict()
        self.intro = """{}{}
   .--. .-.               .-.
  : .--': :              .' `.
  : : _ : `-.  .--.  .--.`. .'
  : :; :: .. :' .; :`._-.': :
  `.__.':_;:_;`.__.'`.__.':_;

--=[ {}Ghost Framework 8.0.0{}
--=[ Developed by EntySec ({}https://entysec.com/{})
""".format(self.colors.CLEAR, self.colors.END,
           self.colors.BOLD + self.colors.WHITE,
           self.colors.END, self.colors.LINE, self.colors.END)

        self.prompt = '(ghost)> '

    def do_help(self, _) -> None:
        """ Show available commands.

        :return None: None
        """

        self.tables.print_table("Core Commands", ('Command', 'Description'), *[
            ('clear', 'Clear terminal window.'),
            ('connect', 'Connect device.'),
            ('devices', 'Show connected devices.'),
            ('disconnect', 'Disconnect device.'),
            ('exit', 'Exit Ghost Framework.'),
            ('help', 'Show available commands.'),
            ('interact', 'Interact with device.')
        ])

    def do_exit(self, _) -> None:
        """ Exit Ghost Framework.

        :return None: None
        """

        for device in list(self.devices):
            self.devices[device]['device'].disconnect()
            del self.devices[device]

        sys.exit(0)

    def do_clear(self, _) -> None:
        """ Clear terminal window.

        :return None: None
        """

        self.badges.print_empty(self.colors.CLEAR, end='')

    def do_connect(self, address: str) -> None:
        """ Connect device.

        :param str address: device host:port or just host
        :return None: None
        """

        if not address:
            self.badges.print_usage("connect <host>:[port]")
            return

        address = address.split(':')

        if len(address) < 2:
            host, port = address[0], 5555
        else:
            host, port = address[0], int(address[1])

        device = Device(host=host, port=port)

        if device.connect():
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
                f"Type {self.colors.GREEN}interact {str(len(self.devices) - 1) + self.colors.END} "
                "to interact this device."
            )

    def do_devices(self, _) -> None:
        """ Show connected devices.

        :return None: None
        """

        if not self.devices:
            self.badges.print_warning("No devices connected.")
            return

        devices = list()

        for device in self.devices:
            devices.append(
                (device, self.devices[device]['host'],
                 self.devices[device]['port']))

        self.tables.print_table("Connected Devices", ('ID', 'Host', 'Port'), *devices)

    def do_disconnect(self, device_id: int) -> None:
        """ Disconnect device.

        :param int device_id: device ID
        :return None: None
        """

        if not device_id:
            self.badges.print_usage("disconnect <id>")
            return

        device_id = int(device_id)

        if device_id not in self.devices:
            self.badges.print_error("Invalid device ID!")
            return

        self.devices[device_id]['device'].disconnect()
        self.devices.pop(device_id)

    def do_interact(self, device_id: int) -> None:
        """ Interact with device.

        :param int device_id: device ID
        """

        if not device_id:
            self.badges.print_usage("interact <id>")
            return

        device_id = int(device_id)

        if device_id not in self.devices:
            self.badges.print_error("Invalid device ID!")
            return

        self.badges.print_process(f"Interacting with device {str(device_id)}")
        self.devices[device_id]['device'].interact()

    def do_EOF(self, _):
        """ Catch EOF.

        :return None: None
        :raises EOFError: EOF error
        """

        raise EOFError

    def default(self, line: str) -> None:
        """ Default unrecognized command handler.

        :param str line: line sent
        :return None: None
        """

        self.badges.print_error(f"Unrecognized command: {line.split()[0]}!")

    def shell(self) -> None:
        """ Run console shell.

        :return None: None
        """

        while True:
            try:
                cmd.Cmd.cmdloop(self)

            except (EOFError, KeyboardInterrupt):
                break

            except Exception as e:
                self.badges.print_error("An error occurred: " + str(e) + "!")
