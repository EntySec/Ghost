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

from core.badges import badges
from core.helper import helper
from core.loader import loader

class shell:
    def __init__(self, ghost):
        self.ghost = ghost
        self.badges = badges()
        self.helper = helper()
        self.loader = loader(ghost)

    def check_root(self):
        return False
        
    def shell(self, target_addr):
        target_commands = self.loader.load_modules()
        while True:
            try:
                command = str(input('\033[4mghost\033[0m(\033[1;31m' + target_addr + '\033[0m)> '))
                while not command.strip():
                    command = str(input('\033[4mghost\033[0m(\033[1;31m' + target_addr + '\033[0m)> '))
                command = command.strip()
                arguments = "".join(command.split(command.split()[0])).strip()
                command = command.split()
                if command[0] == "help":
                    self.helper.show_commands(target_commands)
                elif command[0] == "exit":
                    print(self.badges.G + "Cleaning up...")
                    self.ghost.disconnect(target_addr)
                    self.ghost.stop_server()
                    break
                elif command[0] == "details":
                    if len(command) < 2:
                        print("Usage: details <command>")
                    else:
                        if command[1] in target_commands.keys():
                            print(self.badges.I + "Module Name: " + target_commands[command[1]].details['name'])
                            authors = ""
                            for author in target_commands[command[1]].details['authors']:
                                authors += author + " "
                            print(self.badges.I + "Module Authors: " + authors.strip())
                            print(self.badges.I + "Module Description: " + target_commands[command[1]].details['description'])
                            print(self.badges.I + "Module Usage: " + target_commands[command[1]].details['usage'])
                        else:
                            print(self.badges.E + "No such module command!")
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
                        if target_commands[command[0]].details['needs_args']:
                            if (len(command) - 1) < int(target_commands[command[0]].details['args']):
                                print("Usage: " + target_commands[command[0]].details['usage'])
                            else:
                                if target_commands[command[0]].details['needs_admin']:
                                    if self.check_root():
                                        target_commands[command[0]].run(arguments)
                                    else:
                                        print(self.badges.E + "Target device is not rooted!")
                                else:
                                    target_commands[command[0]].run(arguments)
                        else:
                            if target_commands[command[0]].details['needs_admin']:
                                if self.check_root():
                                    target_commands[command[0]].run()
                                else:
                                    print(self.badges.E + "Target device is not rooted!")
                            else:
                                target_commands[command[0]].run()
                    else:
                        print(self.badges.E + "Unrecognized command!")
            except (KeyboardInterrupt, EOFError):
                print("")
            except Exception as e:
                print(self.badges.E + "An error occured: " + str(e) + "!")
