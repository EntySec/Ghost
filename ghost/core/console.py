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

# --- Rich UI imports for styling (visual-only; logic untouched) ---
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
from rich.markdown import Markdown

# Theme colors
PURPLE = "#7B61FF"
WHITE_ON_PURPLE = Style(color="white", bgcolor=PURPLE, bold=True)
INFO_STYLE = Style(color=PURPLE, bold=True)
WARN_STYLE = Style(color="yellow", bold=True)
ERR_STYLE = Style(color="red", bold=True)
SUCCESS_STYLE = Style(color="green", bold=True)


class Console(Cmd):
    """ Subclass of ghost.core module.

    This subclass of ghost.core modules is intended for providing
    main Ghost Framework console interface.
    """

    def __init__(self) -> None:
        # keep original prompt/intro tokens so framework behavior is unchanged
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

        # preserve devices dict & logic
        self.devices = {}

        # create rich console for all visual outputs
        self.rich = RichConsole()
        self._render_header()

    # -------------------------
    # Visual helpers (only)
    # -------------------------
    def _render_header(self) -> None:
        """Render a fancy hacker-style header with tools table and quick help."""
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

        # Quick Help / Shortcuts table
        quick_help = Table(box=box.SIMPLE_HEAVY, expand=False, border_style=PURPLE)
        quick_help.add_column("Command / Alias", style="bold white", no_wrap=True)
        quick_help.add_column("Description", style="dim")

        quick_help.add_row("connect <host>:[port]", "Connect to device via ADB (default port 5555)")
        quick_help.add_row("devices", "List connected devices")
        quick_help.add_row("disconnect <id>", "Disconnect device by ID")
        quick_help.add_row("interact <id>", "Interact with a connected device")
        quick_help.add_row("analyze <id>", "Run Device Analyzer")
        quick_help.add_row("an <id>", "Alias for analyze")
        quick_help.add_row("logcat <id>", "Start live logcat stream")
        quick_help.add_row("lc <id>", "Alias for logcat")
        quick_help.add_row("exit", "Quit Ghost Framework")
        quick_help.add_row("Index 99", "Return to Menu / Exit (UI helper)")

        right_panel = Panel(
            Align.left(
                Text.assemble(subtitle, "\n\n", "Theme: ", (PURPLE, "Hacker • Purple"))
            ),
            border_style=PURPLE,
            box=box.ROUNDED,
            padding=(0, 1),
            title="[bold]Info",
        )

        header_columns = Columns([left, Panel(Padding(quick_help, (1, 2)), border_style=PURPLE), right_panel])
        self.rich.print(header_columns)
        self.rich.print(Rule(style=PURPLE))
        self.rich.print(Align.center(Text("Type [bold]devices[/bold] to list connected devices — Index 99 → Exit", style=INFO_STYLE)))
        self.rich.print()


    def print_empty(self, message: str = "") -> None:
        # preserve signature and behavior, but print a small spacer
        self.rich.print("")  # purely visual

    def print_information(self, message: str) -> None:
        # visually enhanced info box (preserves semantics)
        self.rich.print(Panel(Text(message), border_style=PURPLE, title="[bold white]INFO", box=box.MINIMAL))

    def print_warning(self, message: str) -> None:
        self.rich.print(Panel(Text(message), border_style="yellow", title="[bold white]WARNING", box=box.MINIMAL))

    def print_error(self, message: str) -> None:
        self.rich.print(Panel(Text(message), border_style="red", title="[bold white]ERROR", box=box.MINIMAL))

    def print_success(self, message: str) -> None:
        self.rich.print(Panel(Text(message), border_style="green", title="[bold white]SUCCESS", box=box.MINIMAL))

    def print_usage(self, usage: str) -> None:
        # show usage in an emphasized box
        usage_text = Text.assemble(("Usage: ", "bold"), (usage, ""))
        footer = Text("Index 99 → Return to Menu", style=INFO_STYLE)
        self.rich.print(Panel(usage_text, border_style=PURPLE, title="[bold]USAGE", subtitle=footer))

    def print_process(self, message: str) -> None:
        # lightweight status indicator (visual only)
        with self.rich.status(Text(message, style=INFO_STYLE), spinner="bouncingBall", spinner_style=PURPLE):
            # no blocking logic here — just visual affordance
            pass

    def print_table(self, title: str, columns: tuple, *rows) -> None:
        """Render a stylized table for lists like connected devices."""
        table = Table(title=title, box=box.SIMPLE_HEAVY, expand=False, border_style=PURPLE)
        for col in columns:
            table.add_column(str(col), header_style="bold white")
        for row in rows:
            # ensure each item is string (matching original behavior)
            table.add_row(*[str(x) for x in row])
        footer = Text("Index 99 → Return to Menu", style=INFO_STYLE)
        wrapper = Panel(Padding(table, (0, 1)), subtitle=footer, border_style=PURPLE)
        self.rich.print(wrapper)

    # -------------------------
    # Original command logic (UNCHANGED)
    # -------------------------
    def do_exit(self, _) -> None:
        """ Exit Ghost Framework.

        :return None: None
        :raises EOFError: EOF error
        """

        for device in list(self.devices):
            self.devices[device]['device'].disconnect()
            del self.devices[device]

        raise EOFError

    def do_connect(self, args: list) -> None:
        """ Connect device.

        :param list args: arguments
        :return None: None
        """

        if len(args) < 2:
            self.print_usage("connect <host>:[port]")
            return

        address = args[1].split(':')

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
            self.print_empty("")

            self.print_information(
                f"Type %greendevices%end to list all connected devices.")
            self.print_information(
                f"Type %greeninteract {str(len(self.devices) - 1)}%end "
                "to interact this device."
            )

    def do_devices(self, _) -> None:
        """ Show connected devices.

        :return None: None
        """

        if not self.devices:
            self.print_warning("No devices connected.")
            return

        devices = []

        for device in self.devices:
            devices.append(
                (device, self.devices[device]['host'],
                 self.devices[device]['port']))

        self.print_table("Connected Devices", ('ID', 'Host', 'Port'), *devices)

    def do_disconnect(self, args: list) -> None:
        """ Disconnect device.

        :param list args: arguments
        :return None: None
        """

        if len(args) < 2:
            self.print_usage("disconnect <id>")
            return

        device_id = int(args[1])

        if device_id not in self.devices:
            self.print_error("Invalid device ID!")
            return

        self.devices[device_id]['device'].disconnect()
        self.devices.pop(device_id)

    def do_interact(self, args: list) -> None:
        """ Interact with device.

        :param list args: arguments
        :return None: None
        """

        if len(args) < 2:
            self.print_usage("interact <id>")
            return

        device_id = int(args[1])

        if device_id not in self.devices:
            self.print_error("Invalid device ID!")
            return

        self.print_process(f"Interacting with device {str(device_id)}...")
        self.devices[device_id]['device'].interact()
    
    def shell(self) -> None:
        """ Run console shell.

        :return None: None
        """

        self.loop()
