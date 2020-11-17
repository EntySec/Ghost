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

import os

class fsmanip:
    def __init__(self):
        self.error = '\033[1;31m[-] \033[0m'

    def exists_directory(self, path):
        if os.path.isdir(path):
            if os.path.exists(path):
                return (True, "directory")
            else:
                print(self.error + "Local directory: " + path + ": does not exist!")
                return (False, "")
        else:
            directory = os.path.split(path)[0]
            if directory == "":
                directory = "."
            if os.path.exists(directory):
                if os.path.isdir(directory):
                    return (True, "file")
                else:
                    print(self.error + "Error: " + directory + ": not a directory!")
                    return (False, "")
            else:
                print(self.error + "Local directory: " + directory + ": does not exist!")
                return (False, "")

    def file(self, path):
        if os.path.exists(path):
            if os.path.isdir(path):
                print(self.error + "Error: " + path + ": not a file!")
                return False
            else:
                return True
        else:
            print(self.error + "Local file: " + path + ": does not exist!")
            return False
