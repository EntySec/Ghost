"""
MIT License

Copyright (c) 2020-2023 EntySec

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


class Colors(object):
    """ Subclass of ghost.cli module.

    This subclass of ghost.cli module is intended for providing
    different color codes.
    """

    def __init__(self) -> None:
        super().__init__()

        self.BLACK = '\033[30m'
        self.RED = '\033[31m'
        self.GREEN = '\033[32m'
        self.YELLOW = '\033[33m'
        self.BLUE = '\033[34m'
        self.PURPLE = '\033[35m'
        self.CYAN = '\033[36m'
        self.WHITE = '\033[77m'

        self.END = '\033[0m'
        self.BOLD = '\033[1m'
        self.DARK = '\033[2m'
        self.BENT = '\033[3m'
        self.LINE = '\033[4m'
        self.TWINK = '\033[5m'
        self.BACK = '\033[7m'

        self.REMOVE = '\033[1K\r'
        self.CLEAR = '\033[H\033[J'
        self.NEWLINE = '\n'
