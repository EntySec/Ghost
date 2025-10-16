"""
MIT License

Copyright (c) 2020-2024 EntySec

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

import os

from badges.cmd import Cmd

from adb_shell.adb_device import AdbDeviceTcp
from adb_shell.auth.keygen import keygen
from adb_shell.auth.sign_pythonrsa import PythonRSASigner

from pex.fs import FS

# Rich UI imports (visuals only — program logic is NOT modified)
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align

# Main purple theme
_PURPLE = "#7B61FF"

_console = Console()


class Device(Cmd, FS):
    """ Subclass of ghost.core module.

    This subclass of ghost.core module is intended for providing
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

        self.host = host
        self.port = int(port)

        self.key_file = key_filename
        self.device = AdbDeviceTcp(self.host, self.port, default_transport_timeout_s=timeout)

        super().__init__(
            prompt=f'(%lineghost%end: %red{self.host}%end)> ',
            path=[f'{os.path.dirname(os.path.dirname(__file__))}/modules'],
            device=self
        )

    # -------------------------
    # Rich-based Print Methods
    # (Presentation only — do NOT change program logic)
    # -------------------------
    def _footer_return_to_menu(self) -> Text:
        """Small helper to produce the 'Return to Menu' footer text."""
        t = Text("Index 99 → Exit", style="bold")
        t.stylize(f"bold {_PURPLE}")
        return t

    def print_process(self, message: str) -> None:
        """Display a process/info message using Rich Panel."""
        panel = Panel.fit(
            Align.left(Text(message)),
            title=Text("PROCESS", style="bold white on " + _PURPLE),
            border_style=_PURPLE
        )
        _console.print(panel)

    def print_success(self, message: str) -> None:
        """Display a success message using Rich Panel."""
        panel = Panel.fit(
            Align.left(Text(message)),
            title=Text("SUCCESS", style="bold white on " + _PURPLE),
            border_style=_PURPLE
        )
        _console.print(panel)

    def print_error(self, message: str) -> None:
        """Display an error message using Rich Panel."""
        panel = Panel.fit(
            Align.left(Text(message)),
            title=Text("ERROR", style="bold white on " + _PURPLE),
            border_style="red"
        )
        _console.print(panel)

    def print_information(self, message: str) -> None:
        """Display an informational message using Rich Table for clarity."""
        table = Table.grid(padding=(0, 1))
        table.add_column(justify="left")
        table.add_row(Text(message))
        panel = Panel.fit(
            table,
            title=Text("INFO", style="bold white on " + _PURPLE),
            border_style=_PURPLE
        )
        _console.print(panel)

    def print_empty(self) -> None:
        """Print an empty line/space using Rich (visual spacer)."""
        _console.print()

    # -------------------------
    # Original methods (logic unchanged)
    # -------------------------
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
            self.print_error("Socket is not connected!")
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
            self.print_error("Failed to list directory!")
        return []

    def connect(self) -> bool:
        """ Connect the specified device.

        :return bool: True if connection succeed
        """

        self.print_process(f"Connecting to {self.host}...")

        try:
            keys = self.get_keys()
            signer = PythonRSASigner(*keys)

            self.device.connect(rsa_keys=[signer], auth_timeout_s=5)
            self.print_success(f"Connected to {self.host}!")

            return True

        except Exception:
            self.print_error(f"Failed to connect to {self.host}!")

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

        exists, is_dir = self.exists(output_path)

        if exists:
            if is_dir:
                output_path = output_path + '/' + os.path.split(input_file)[1]

            try:
                self.print_process(f"Downloading {input_file}...")
                self.device.pull(input_file, output_path)

                self.print_process(f"Saving to {output_path}...")
                self.print_success(f"Saved to {output_path}!")

                return True

            except Exception:
                self.print_error(f"Remote file: {input_file}: does not exist or a directory!")

        return False

    def upload(self, input_file: str, output_path: str) -> bool:
        """ Upload file to the specified device.

        :param str input_file: path of the file to upload
        :param str output_path: path to output the file to
        :return bool: True if upload succeed
        """

        if self.check_file(input_file):
            try:
                self.print_process(f"Uploading {input_file}...")
                self.device.push(input_file, output_path)

                self.print_process(f"Saving to {output_path}...")
                self.print_success(f"Saved to {output_path}!")

                return True

            except Exception:
                try:
                    output_path = output_path + '/' + os.path.split(input_file)[1]
                    self.device.push(input_file, output_path)

                except Exception:
                    self.print_error(f"Remote directory: {output_path}: does not exist!")

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

        self.print_success("Interactive connection spawned!")

        self.print_empty()
        self.print_process("Loading device modules...")

        self.print_information(f"Modules loaded: {str(len(self.external))}")
        self.loop()
