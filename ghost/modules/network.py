"""
This module requires Ghost: https://github.com/EntySec/Ghost
Current source: https://github.com/EntySec/Ghost
"""

from badges.cmd import Command
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align

_PURPLE = "#7B61FF"
_console = Console()


class ExternalCommand(Command):
    def __init__(self):
        super().__init__({
            'Category': "manage",
            'Name': "network",
            'Authors': [
                'Loubaris - module developer'
            ],
            'Description': "Retrieve network informations.",
            'NeedsRoot': False,
            'MinArgs': 1,
            'Options': [
                (
                    ('-a', '--arp'),
                    {'help': "Show device ARP table.", 'action': 'store_true'}
                ),
                (
                    ('-i', '--ipconfig'),
                    {'help': "Show device IP configuration.", 'action': 'store_true'}
                ),
                (
                    ('-I', '--iproute'),
                    {'help': "Show device route table.", 'action': 'store_true'}
                ),
                (
                    ('-l', '--locate'),
                    {'help': "Show device location.", 'action': 'store_true'}
                ),
                (
                    ('-s', '--stats'),
                    {'help': "Show device network stats.", 'action': 'store_true'}
                ),
                (
                    ('-p', '--ports'),
                    {'help': "Show device open ports.", 'action': 'store_true'}
                ),
                (
                    ('-S', '--services'),
                    {'help': "Show device services.", 'action': 'store_true'}
                ),
                (
                    ('-f', '--forwarding'),
                    {'help': "Show device forwarding rules.", 'action': 'store_true'}
                )
            ]
        })

    def print_panel(self, title: str, message: str, color: str = _PURPLE):
        panel = Panel.fit(
            Align.left(Text(message if message else "No output.")),
            title=Text(title, style=f"bold white on {color}"),
            border_style=color
        )
        _console.print(panel)

    def run(self, args):
        outputs = []

        if args.arp:
            outputs.append(self.device.send_command('cat /proc/net/arp'))

        if args.ipconfig:
            outputs.append(self.device.send_command('ip addr show'))

        if args.iproute:
            outputs.append(self.device.send_command('ip route show'))

        if args.locate:
            outputs.append(self.device.send_command('dumpsys location'))

        if args.stats:
            outputs.append(self.device.send_command('cat /proc/net/netstat'))

        if args.ports:
            outputs.append(self.device.send_command('busybox netstat -an'))

        if args.services:
            outputs.append(self.device.send_command('service list'))

        if args.forwarding:
            outputs.append(self.device.send_command('cat /proc/sys/net/ipv4/ip_forward'))

        self.print_panel("NETWORK OUTPUT", '\n'.join(outputs))
