"""
This module requires Ghost: https://github.com/EntySec/Ghost
Current source: https://github.com/EntySec/Ghost
"""

from ghost.lib.module import Module


class GhostModule(Module):
    details = {
        'Category': "manage",
        'Name': "sms",
        'Authors': [
            'Loubaris Adam (Loubaris) - module developer'
        ],
        'Description': "Send an SMS using remote device.",
        'Comments': [
            ''
        ],
        'Usage': "sms <+phone_number>",
        'MinArgs': 1,
        'NeedsRoot': True
    }

    def run(self, argc, argv):
        sms_body = input("SMS_Body >")
        try:
            output = self.device.send_command(f'am start -a "android.intent.action.SENDTO" -d sms:{argv[1]} --es "sms_body" "{sms_body}" {argv[1]} --ez "exit_on_sent" true')
            self.print_empty(output)
            self.device.send_command(f"input keyevent 22")
            self.device.send_command(f"input keyevent 66")
            self.print_information("SMS Succesfully sent")
        except Exception as e:
                self.badges.print_error("An error occurred: " + str(e) + "!")
