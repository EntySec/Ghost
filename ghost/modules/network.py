"""
This module requires Ghost: https://github.com/EntySec/Ghost
Current source: https://github.com/EntySec/Ghost
"""

from ghost.lib.module import Module


class GhostModule(Module):
    def __init__(self):
        super().__init__()

        self.details.update({
            'Category': "manage",
            'Name': "network",
            'Authors': [
                'Loubaris - module developer'
            ],
            'Description': "Retrieve network informations",
            'Usage': "Arguments:\n - arptable: Show device ARP Table\n - ipconfig: Show device configuration\n - iproute: Show device's routing table\n - location: Retrieve network location\n - statistics: Show network stats\n - open_ports: Check for open ports\n - service_list: Show all network services\n - forwarding: Check for IP forwarding",
            'MinArgs': 1,
            'NeedsRoot': False
        })

    def run(self, argc, argv):
        if argv[1] in ['arptable', 'ipconfig', 'iproute', 'location', 'statistics', 'open_ports', 'service_list', 'forwarding']:
            if argv[1] == 'arptable':
                output = self.device.send_command('cat /proc/net/arp')
            elif argv[1] == 'ipconfig':
                output = self.device.send_command('ip addr show')
            elif argv[1] == 'iproute':
                output = self.device.send_command('ip route show')
            elif argv[1] == 'location':
                output = self.device.send_command('dumpsys location')
            elif argv[1] == 'statistics':
                output = self.device.send_command('cat /proc/net/netstat')
            elif argv[1] == 'open_ports':
                output = self.device.send_command('busybox netstat -an')
            elif argv[1] == 'service_list':
                output = self.device.send_command('service list')
            elif argv[1] == 'forwarding':
                output = self.device.send_command('cat /proc/sys/net/ipv4/ip_forward')
            print(output)

        else:
            self.print_empty(f"Usage: {self.details['Usage']}")
