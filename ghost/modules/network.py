"""
This module requires Ghost: https://github.com/EntySec/Ghost
Current source: https://github.com/EntySec/Ghost
"""

from badges.cmd import Command


class ExternalCommand(Command):
    def __init__(self):
        super().__init__({
            'Category': "manage",
            'Name': "network",
            'Authors': [
                'Loubaris - module developer'
            ],
            'Description': "Retrieve network informations.",
            'Usage': "network [option]",
            'MinArgs': 1,
            'NeedsRoot': False,
            'Options': {
                'arptable': ['', 'Show device ARP table.'],
                'ipconfig': ['', 'Show device IP configuration.'],
                'iproute': ['', 'Show device route table.'],
                'location': ['', 'Show device location.'],
                'statistics': ['', 'Show network stats.'],
                'open_ports': ['', 'Show opened ports.'],
                'service_list': ['', 'Show services list.'],
                'forwarding': ['', 'Show forwarding rules.']
            }
        })

    def run(self, args):
        output = ""

        if args[1] == 'arptable':
            output = self.device.send_command('cat /proc/net/arp')

        elif args[1] == 'ipconfig':
            output = self.device.send_command('ip addr show')

        elif args[1] == 'iproute':
            output = self.device.send_command('ip route show')

        elif args[1] == 'location':
            output = self.device.send_command('dumpsys location')

        elif args[1] == 'statistics':
            output = self.device.send_command('cat /proc/net/netstat')

        elif args[1] == 'open_ports':
            output = self.device.send_command('busybox netstat -an')

        elif args[1] == 'service_list':
            output = self.device.send_command('service list')

        elif args[1] == 'forwarding':
            output = self.device.send_command('cat /proc/sys/net/ipv4/ip_forward')

        self.print_empty(output)
