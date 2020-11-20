#!/bin/bash

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

G="\033[1;34m[*] \033[0m"
S="\033[1;32m[+] \033[0m"
E="\033[1;31m[-] \033[0m"

if [[ $(id -u) != 0 ]]; then
    echo -e ""$E"Permission denied!"
    exit
fi

if [[ -f /data/data/com.termux/files/usr/bin/ghost ]]; then
    update=true
else
    if [[ -f /usr/local/bin/ghost ]]; then
        update=true
    else
        if [[ -f /usr/bin/ghost ]]; then
            update=true
        else
            update=false
        fi
    fi
fi

sleep 1
echo -e ""$G"Installing update..."
{
    rm -rf ~/ghost
    rm /usr/bin/ghost
    rm /usr/local/bin/ghost
    rm /data/data/com.termux/files/usr/bin/ghost
    cd ~
    git clone https://github.com/EntySec/ghost.git
    if [[ $update ]]; then
        cd ghost
        chmod +x install.sh
        ./install.sh
    fi
} &> /dev/null

if [[ ! -d ~/ghost ]]; then
    echo -e ""$E"Installation failed!"
    exit
fi

echo -e ""$S"Successfully updated!"
cd .
touch .updated
sleep 1
exit
