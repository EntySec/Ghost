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

from badges.cmd import Cmd
from ghost.core.device import Device
from rich.console import Console as RichConsole
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich import box
from rich.style import Style
from rich.rule import Rule
from rich.padding import Padding
from rich.columns import Columns

PURPLE = "#7B61FF"
INFO_STYLE = Style(color=PURPLE, bold=True)

class Console(Cmd):
    """ Subclass of ghost.core module using badges for printing. """

    def __init__(self) -> None:
        super().__init__(
            prompt='(%lineghost%end)> ',
            intro="""%clear%end
   .--. .-.               .-.
  : .--': :              .' `.
  : : _ : `-.  .--.  .--.`. .'
  : :; :: .. :' .; :`._-.': :
  `.__.':_;:_;`.__.'`.__.':_;

--=[ %bold%whiteGhost Framework 8.0.0%end
--=[ Developed by EntySec (%linehttps://entysec.com/%end)
"""
        )

        self.devices = {}
        self._render_header()

    def _render_header(self) -> None:
        """Render fancy header with modern Help table using Rich."""
        title = Text("Ghost Framework 8.0.0", style="bold white")
        subtitle = Text("Developed by EntySec — https://entysec.com/", style="dim")

        ascii_art = Text(
            "   .--. .-.               .-.\n"
            "  : .--': :              .' `.\n"
            "  : : _ : `-.  .--.  .--.`. .'\n"
            "  : :; :: .. :' .; :`._-.': :\n"
            "  `.__.':_;:_;`.__.'`.__.':_;",
            justify="center",
        )

        left = Panel(
            Align.center(ascii_art),
            border_style=PURPLE,
            box=box.HEAVY,
            padding=(0, 2),
            title="[bold]GHOST",
            subtitle=title,
        )

        # Help table
        help_table = Table(
            title=Text("🚀 Ghost Framework Commands", style="bold white on " + PURPLE, justify="center"),
            box=box.DOUBLE_EDGE,
            border_style=PURPLE,
            expand=False,
            show_lines=True
        )

        help_table.add_column("Command", style="bold white on #5A3EFF", no_wrap=True, justify="center")
        help_table.add_column("Description", style="italic dim", justify="left")

        commands = [
            ("🔌 connect <host>:[port]", "Connect to device via ADB (default port 5555)"),
            ("📱 devices", "List connected devices"),
            ("❌ disconnect <id>", "Disconnect device by ID"),
            ("💬 interact <id>", "Interact with a connected device"),
            ("🔍 analyze <id> / an <id>", "Run Device Analyzer"),
            ("📜 logcat <id> / lc <id>", "Start live logcat stream"),
            ("🚪 exit", "Quit Ghost Framework"),
            ("🔄 Index 99", "Return to Menu / Exit (UI helper)")
        ]

        ALT_ROW = "#2E2E2E"
        for i, (cmd, desc) in enumerate(commands):
            style = Style(bgcolor=ALT_ROW) if i % 2 else Style()
            help_table.add_row(cmd, desc, style=style)

        right_panel = Panel(
            Align.left(
                Text.assemble(subtitle, "\n\n", "Theme: ", (PURPLE, "Hacker • Purple"))
            ),
            border_style=PURPLE,
            box=box.ROUNDED,
            padding=(0, 1),
            title="[bold]Info",
        )

        header_columns = Columns([left, Panel(help_table, padding=(1, 2), border_style=PURPLE), right_panel])
        self.print(header_columns)
        self.print(Rule(style=PURPLE))
        self.print(Align.center(Text("Type [bold]devices[/bold] to list connected devices — Index 99 → Exit", style=INFO_STYLE)))
        self.print()

    # ===== Device commands =====
    def do_exit(self, _) -> None:
        for device in list(self.devices):
            self.devices[device]['device'].disconnect()
            del self.devices[device]
        raise EOFError

    def do_connect(self, args: list) -> None:
        if len(args) < 2:
            self.usage("connect <host>:[port]")
            return

        address = args[1].split(':')
        host, port = (address[0], 5555) if len(address) < 2 else (address[0], int(address[1]))
        device = Device(host=host, port=port)

        if device.connect():
            self.devices.update({len(self.devices): {'host': host, 'port': str(port), 'device': device}})
            self.info(f"Type %greendevices%end to list all connected devices.")
            self.info(f"Type %greeninteract {len(self.devices) - 1}%end to interact with this device.")

    def do_devices(self, _) -> None:
        if not self.devices:
            self.warn("No devices connected.")
            return

        devices = [(dev, self.devices[dev]['host'], self.devices[dev]['port']) for dev in self.devices]
        self.table("Connected Devices", ("ID", "Host", "Port"), *devices)

    def do_disconnect(self, args: list) -> None:
        if len(args) < 2:
            self.usage("disconnect <id>")
            return
        device_id = int(args[1])
        if device_id not in self.devices:
            self.error("Invalid device ID!")
            return
        self.devices[device_id]['device'].disconnect()
        self.devices.pop(device_id)

    def do_interact(self, args: list) -> None:
        if len(args) < 2:
            self.usage("interact <id>")
            return
        device_id = int(args[1])
        if device_id not in self.devices:
            self.error("Invalid device ID!")
            return
        self.process(f"Interacting with device {device_id}...")
        self.devices[device_id]['device'].interact()

    def shell(self) -> None:
        self.loop()

