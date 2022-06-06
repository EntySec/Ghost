"""
MIT License

Copyright (c) 2020-2022 EntySec

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

import os

from ghost.core.cli.badges import Badges


class FSTools:
    badges = Badges()

    def exists(self, path):
        if os.path.isdir(path):
            return True, True
        directory = os.path.split(path)[0]

        if not directory:
            return True, False

        if self.exists_dir(directory):
            return True, False
        return False, False

    def exists_dir(self, path):
        if os.path.exists(path):
            if not os.path.isdir(path):
                self.badges.print_error(f"Error: {path}: not a directory!")
                return False
            return True

        self.badges.print_error(f"Local directory: {directory}: does not exist!")
        return False

    def exists_file(self, path):
        if os.path.exists(path):
            if os.path.isdir(path):
                self.badges.print_error(f"Error: {path}: not a file!")
                return False
            return True

        self.badges.print_error(f"Local file: {path}: does not exist!")
        return False
