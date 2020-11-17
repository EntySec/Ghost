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
import os

from core.badges import badges
from core.fsmanip import fsmanip

class transfer:
    def __init__(self, ghost):
        self.badges = badges()
        self.ghost = ghost
        self.fsmanip = fsmanip()

    def upload(self, input_file, output_path):
        temp_container = os.environ['OLDPWD']
        os.chdir(temp_container)
        if self.fsmanip.file(input_file):
            output_filename = os.path.split(input_file)[1]
            output_directory = output_path
            check_exists = self.ghost.send_command("shell", "stat "+output_path)
            check_directory = self.ghost.send_command("shell", "'if [[ -d \""+output_path+"\" ]]; then echo 0; fi'")
            if check_directory == "0":
                if check_exists == "stat: '"+output_path+"': No such file or directory":
                    print(self.badges.E + "Remote directory: "+output_path+": does not exist!")
                else:
                    if output_directory[-1] == "/":
                        output_directory = output_directory + output_filename
                    else:
                        output_directory = output_directory + "/" + output_filename
                    print(self.badges.G + "Uploading "+input_file+"...")
                    self.ghost.send_command("push", input_file + " " + output_directory)
                    print(self.badges.G + "Saving to "+output_directory+"...")
                    time.sleep(1)
                    print(self.badges.S + "Saved to "+output_directory+"!")
            else:
                directory = os.path.split(output_path)[0]
                if directory == "":
                    directory = "."
                check_exists = self.ghost.send_command("shell", "stat " + directory)
                check_directory = self.ghost.send_command("shell", "'if [[ -d \""+directory+"\" ]]; then echo 0; fi'")
                if check_exists != "stat: "+directory+": No such file or directory":
                    if check_directory == "0":
                        print(self.badges.G + "Uploading " + input_file + "...")
                        self.ghost.send_command("push", input_file + " " + output_directory)
                        print(self.badges.G + "Saving to " + output_directory + "...")
                        time.sleep(1)
                        print(self.badges.S + "Saved to " + output_directory + "!")
                    else:
                        print(self.badges.E + "Error: "+directory+": not a directory!")
                else:
                    print(self.badges.E + "Remote directory: "+directory+": does not exist!")
        main_container = os.environ['HOME']
        os.chdir(main_container + "/ghost")
        
    def download(self, input_file, output_path):
        temp_container = os.environ['OLDPWD']
        os.chdir(temp_container)
        exists, path_type = self.fsmanip.exists_directory(output_path)
        if exists:
            if path_type != "file":
                if output_path[-1] == "/":
                    output_path = output_path + os.path.split(input_file)[1]
                else:
                    output_path = output_path + "/" + os.path.split(input_file)[1]
            check_file_exists = self.ghost.send_command("shell", "stat " + input_file)
            check_file_directory = self.ghost.send_command("shell", "'if [[ -d \""+input_file+"\" ]]; then echo 0; fi'")
            if check_file_exists == "stat: '"+input_file+"': No such file or directory":
                print(self.badges.E + "Remote file: "+input_file+": does not exist!")
            else:
                if check_file_directory == "0":
                    print(self.badges.E + "Error: " + input_file + ": not a file!")
                else:
                    print(self.badges.G + "Downloading "+input_file+"...")
                    self.ghost.send_command("pull", input_file + " " + output_path, False, False)
                    print(self.badges.G + "Saving to "+output_path+"...")
                    time.sleep(1)
                    print(self.badges.S + "Saved to "+output_path+"!")
        main_container = os.environ['HOME']
        os.chdir(main_container + "/ghost")
