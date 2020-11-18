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

import time
import sys
import os

from core.badges import badges
from core.ghost import ghost
from core.helper import helper

class server:
    def __init__(self):
        self.badges = badges()
        self.ghost = ghost()
        self.helper = helper()

    def get_module(self, mu, name, folderpath):
        folderpath_list = folderpath.split(".")
        for i in dir(mu):
            if i == name:
                pass
                return getattr(mu, name)
            else:
                if i in folderpath_list:
                    i = getattr(mu, i)
                    return self.get_module(i, name, folderpath)

    def import_modules(self, path):
        modules = dict()

        for mod in os.listdir(path):
            if mod == '__init__.py' or mod[-3:] != '.py':
                continue
            else:
                md = path.replace("/", ".").replace("\\", ".") + "." + mod[:-3]
                mt = __import__(md)

                m = self.get_module(mt, mod[:-3], md)
                m = m.GhostModule()

                modules[m.name] = m
        return modules

    def load_modules(self):
        global target_commands
        target_commands = self.import_modules("modules")

    def help(self):
        self.helper.show_commands(target_commands)

    def shell(self, target_addr):
        while True:
            try:
                command = str(input('\033[4mghost\033[0m(\033[1;31m'+target_addr+'\033[0m)> '))
                while not command.strip():
                    command = str(input('\033[4mghost\033[0m(\033[1;31m' + target_addr + '\033[0m)> '))
                command = command.strip()
                arguments = "".join(command.split(command.split(" ")[0])).strip()
                command = command.split(" ")
                if command[0] == "help":
                    self.help()
                elif command[0] == "exit":
                    print(self.badges.G + "Cleaning up...")
                    self.ghost.disconnect(target_addr)
                    self.ghost.stop_server()
                    sys.exit()
                elif command[0] == "exec":
                    if len(command) < 2:
                        print("Usage: exec <command>")
                    else:
                        print(self.badges.I + "exec:")
                        os.system(arguments)
                        print("")
                elif command[0] == "clear":
                    os.system("clear")
                else:
                    if command[0] in target_commands.keys():
                        if len(command) < int(target_commands[command[0]].args):
                            print(target_commands[command[0]].usage)
                        else:
                            target_commands[command[0]].run(arguments)
                    else:
                        print(self.badges.E + "Unrecognized command!")
            except (KeyboardInterrupt, EOFError):
                print("")
            except Exception as e:
                print(self.badges.E + "An error occured: " + str(e) + "!")

    def connect(self, rhost, rport):
        target_addr = rhost + ":" + rport
        print(self.badges.G + "Connecting to "+target_addr+"...")
        self.ghost.start_server()
        self.ghost.connect(target_addr)
        is_connected = self.ghost.send_command("devices", "| grep "+target_addr)
        is_offline = self.ghost.send_command("devices", "| grep offline")
        if is_connected == "":
            print(self.badges.E + "Failed to connect to "+target_addr+"!")
            self.ghost.disconnect(target_addr)
            sys.exit()
        else:
            if is_offline != "":
                print(self.badges.E + "Failed to connect to " + target_addr + "!")
                self.ghost.disconnect(target_addr)
                sys.exit()
        time.sleep(0.5)
        self.load_modules()
        self.shell(target_addr)
