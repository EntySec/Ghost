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
import time
import threading
from badges.cmd import Cmd
from adb_shell.adb_device import AdbDeviceTcp
from adb_shell.auth.keygen import keygen
from adb_shell.auth.sign_pythonrsa import PythonRSASigner
from pex.fs import FS

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align

_PURPLE = "#7B61FF"
_console = Console()

_MAX_RETRIES = 5
_RETRY_DELAY = 3
_HEALTHCHECK_DELAY = 10


class Device(Cmd, FS):
    """Enhanced Device class with auto-reconnect, analyzer & log viewer."""

    def __init__(self, host: str, port: int = 5555, timeout: int = 10, key_filename: str = 'key') -> None:
        self.host = host
        self.port = int(port)
        self.key_file = key_filename
        self.device = AdbDeviceTcp(self.host, self.port, default_transport_timeout_s=timeout)

        self._reconnect_thread = None
        self._stop_reconnect = threading.Event()

        super().__init__(
            prompt=f'(%lineghost%end: %red{self.host}%end)> ',
            path=[f'{os.path.dirname(os.path.dirname(__file__))}/modules'],
            device=self
        )

    # -------------------------
    # Rich Print Helpers
    # -------------------------
    def print_panel(self, message: str, title: str, color: str = _PURPLE) -> None:
        _console.print(Panel.fit(Align.left(Text(message)),
                                 title=Text(title, style=f"bold white on {color}"),
                                 border_style=color))

    def print_process(self, message: str) -> None: self.print_panel(message, "PROCESS", _PURPLE)
    def print_success(self, message: str) -> None: self.print_panel(message, "SUCCESS", "green")
    def print_error(self, message: str) -> None: self.print_panel(message, "ERROR", "red")
    def print_information(self, message: str) -> None: self.print_panel(message, "INFO", _PURPLE)
    def print_empty(self): _console.print()

    # -------------------------
    # Device Keys
    # -------------------------
    def get_keys(self) -> tuple:
        if not os.path.exists(self.key_file):
            keygen(self.key_file)
        with open(self.key_file, 'r') as f:
            priv = f.read()
        with open(self.key_file + '.pub', 'r') as f:
            pub = f.read()
        return pub, priv

    # -------------------------
    # Connection Management
    # -------------------------
    def connect(self, auto_reconnect: bool = True) -> bool:
        self._stop_reconnect.clear()
        self.print_process(f"Connecting to {self.host}...")
        keys = self.get_keys()
        signer = PythonRSASigner(*keys)

        for attempt in range(1, _MAX_RETRIES + 1):
            try:
                self.device.connect(rsa_keys=[signer], auth_timeout_s=5)
                self.print_success(f"Connected to {self.host}!")

                if auto_reconnect:
                    self._start_auto_reconnect_thread()
                return True
            except Exception as e:
                self.print_error(f"[Attempt {attempt}/{_MAX_RETRIES}] Connection failed: {e}")
                if attempt < _MAX_RETRIES:
                    self.print_information(f"Retrying in {_RETRY_DELAY} seconds...")
                    time.sleep(_RETRY_DELAY)

        self.print_error(f"Failed to connect to {self.host} after {_MAX_RETRIES} attempts!")
        return False

    def _start_auto_reconnect_thread(self) -> None:
        if self._reconnect_thread and self._reconnect_thread.is_alive(): return
        self._reconnect_thread = threading.Thread(target=self.auto_reconnect, daemon=True)
        self._reconnect_thread.start()

    def auto_reconnect(self) -> None:
        while not self._stop_reconnect.is_set():
            try:
                self.device.shell("echo ping", transport_timeout_s=3)
            except Exception:
                self.print_error(f"Lost connection to {self.host}, attempting reconnect...")
                if not self.connect(auto_reconnect=False):
                    self.print_error("Auto-reconnect failed, will retry again...")
                else:
                    self.print_success("Reconnected successfully!")
            time.sleep(_HEALTHCHECK_DELAY)

    def disconnect(self) -> None:
        self._stop_reconnect.set()
        if self._reconnect_thread and self._reconnect_thread.is_alive():
            self._reconnect_thread.join(timeout=2)
        try:
            self.device.close()
            self.print_success(f"Disconnected from {self.host}.")
        except Exception:
            self.print_error("Failed to disconnect properly!")

    # -------------------------
    # Command / File Operations
    # -------------------------
    def send_command(self, command: str, output: bool = True) -> str:
        try:
            cmd_output = self.device.shell(command)
        except Exception:
            self.print_error("Socket is not connected!")
            return None
        return cmd_output if output else ""

    def list(self, path: str) -> list:
        try:
            return self.device.list(path)
        except Exception:
            self.print_error("Failed to list directory!")
        return []

    def download(self, input_file: str, output_path: str) -> bool:
        exists, is_dir = self.exists(output_path)
        if exists:
            if is_dir: output_path += '/' + os.path.split(input_file)[1]
            try:
                self.print_process(f"Downloading {input_file}...")
                self.device.pull(input_file, output_path)
                self.print_success(f"Saved to {output_path}!")
                return True
            except Exception:
                self.print_error(f"Remote file {input_file} not found or invalid!")
        return False

    def upload(self, input_file: str, output_path: str) -> bool:
        if self.check_file(input_file):
            try:
                self.print_process(f"Uploading {input_file}...")
                self.device.push(input_file, output_path)
                self.print_success(f"Saved to {output_path}!")
                return True
            except Exception:
                try:
                    output_path += '/' + os.path.split(input_file)[1]
                    self.device.push(input_file, output_path)
                except Exception:
                    self.print_error(f"Remote directory {output_path} does not exist!")
        return False

    def is_rooted(self) -> bool:
        responder = self.send_command('which su')
        return bool(responder and not responder.isspace())

    def interact(self) -> None:
        self.print_success("Interactive connection spawned!")
        self.print_process("Loading device modules...")
        self.print_information(f"Modules loaded: {str(len(self.external))}")
        self.loop()

    # -------------------------
    # Device Analyzer
    # -------------------------
    def analyze_device(self):
        self.print_process(f"Analyzing {self.host} ...")
        try:
            props = {
                "Manufacturer": self.send_command("getprop ro.product.manufacturer"),
                "Model": self.send_command("getprop ro.product.model"),
                "Android Version": self.send_command("getprop ro.build.version.release"),
                "Security Patch": self.send_command("getprop ro.build.version.security_patch"),
                "Architecture": self.send_command("getprop ro.product.cpu.abi"),
                "Rooted": "Yes" if self.is_rooted() else "No"
            }

            table = Table(title=f"📱 Device Analysis — {self.host}", border_style=_PURPLE)
            table.add_column("Property", style="bold white")
            table.add_column("Value", style="dim")

            for k, v in props.items(): table.add_row(k, v.strip() if v else "N/A")
            _console.print(table)
            self.print_success("Analysis complete!")
        except Exception as e:
            self.print_error(f"Analysis failed: {e}")

    # -------------------------
    # Real-Time Log Viewer
    # -------------------------
    def live_logcat(self):
        self.print_information("Starting live logcat stream (Press Ctrl+C to stop)...")

        def stream_logs():
            try:
                shell = self.device.shell("logcat -v time", decode=False)
                for line in shell:
                    decoded = line.decode(errors="ignore").strip()
                    if " E " in decoded: _console.print(Text(decoded, style="red"))
                    elif " W " in decoded: _console.print(Text(decoded, style="yellow"))
                    else: _console.print(Text(decoded, style="dim"))
            except KeyboardInterrupt:
                self.print_process("Log streaming stopped by user.")
            except Exception as e:
                self.print_error(f"Logcat error: {e}")

        t = threading.Thread(target=stream_logs)
        t.daemon = True
        t.start()
