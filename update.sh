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
P="\033[1;77m[>] \033[0m"

clear
cat banner/banner.txt
echo

while [[ $(sudo -n id -u 2>&1) != 0 ]]; do
    {
        sudo -v -p "$(echo -e -n $P)Password for $(whoami): " 
    } &> /dev/null
done

echo -e $G"Updating Ghost Framework..."

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

{
    rm -rf ~/.ghost
    sudo rm /usr/bin/ghost
    sudo rm /usr/local/bin/ghost
    sudo rm /data/data/com.termux/files/usr/bin/ghost
    git clone https://github.com/EntySec/ghost.git ~/.ghost
    if [[ $update ]]; then
        cd ~/.ghost/ghost
        chmod +x install.sh
        ./install.sh
    fi
} &> /dev/null

if [[ ! -d ~/.ghost ]]; then
    echo -e $E"Installation failed!"
    exit 1
fi

echo -e $S"Successfully updated!"
exit 0
