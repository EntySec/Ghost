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

from ghost.core.cli.badges import Badges


class Tables:
    badges = Badges()

    def print_table(self, name, headers, *args, **kwargs) -> None:
        extra_fill = kwargs.get("extra_fill", 4)
        header_separator = kwargs.get("header_separator", "-")

        if not all(map(lambda x: len(x) == len(headers), args)):
            return

        def custom_len(x):
            x = str(x)
            try:
                if '\033' in x:
                    return len(x) - 9 * x.count('\033') // 2
                return len(x)
            except TypeError:
                return 0

        fill = list()
        headers_line = '    '
        headers_separator_line = '    '
        for idx, header in enumerate(headers):
            column = [custom_len(arg[idx]) for arg in args]
            column.append(len(header))

            current_line_fill = max(column) + extra_fill
            fill.append(current_line_fill)
            headers_line = "".join((headers_line, "{header:<{fill}}".format(header=header, fill=current_line_fill)))
            headers_separator_line = "".join((
                headers_separator_line,
                "{:<{}}".format(header_separator * len(header), current_line_fill)
            ))

        self.badges.print_empty('\n' + name.split()[0].title() + name[len(name.split()[0]):] + ':')
        self.badges.print_empty()
        self.badges.print_empty(headers_line)
        self.badges.print_empty(headers_separator_line)
        for arg in args:
            content_line = "    "
            for idx, element in enumerate(arg):
                element = str(element)
                fill_line = fill[idx]

                if '\033' in element:
                    fill_line = fill[idx] + 9 * element.count('\033') // 2

                content_line = "".join((
                    content_line,
                    "{:<{}}".format(element, fill_line)
                ))
            self.badges.print_empty(content_line)
        self.badges.print_empty()
