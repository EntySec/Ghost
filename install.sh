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

printf '\033]2;install.sh\a'

G="\033[1;34m[*] \033[0m"
S="\033[1;32m[+] \033[0m"
E="\033[1;31m[-] \033[0m"

if [[ $(id -u) != 0 ]]; then
    echo -e ""$E"Permission denied!"
    exit
fi

{
    CHECK="$(ping -c 1 -q www.google.com >&/dev/null; echo $?)"
} &> /dev/null

if [[ "$CHECK" != 0 ]]; then 
    echo -e ""$E"No Internet connection!"
    exit
fi

sleep 0.5
clear
sleep 0.5
cat banner/banner.txt
echo

sleep 1
echo -e ""$G"Installing dependencies..."
sleep 1

{
    pkg update
    pkg -y install git
    pkg -y install python
    pkg -y install android-tools
    pkg -y install scrcpy
    apt-get update
    apt-get -y install git
    apt-get -y install python3
    apt-get -y install adb
    apt-get -y install scrcpy
    apk update
    apk add git
    apk add python3
    apk add android-tools
    apk add scrcpy
    pacman -Sy
    pacman -S --noconfirm git
    pacman -S --noconfirm python3
    pacman -S --noconfirm android-tools
    pacman -S --noconfirm scrcpy
    zypper refresh
    zypper install -y git
    zypper install -y python3
    zypper install -y android-tools
    zypper install -y scrcpy
    yum -y install git
    yum -y install python3
    yum -y install android-tools
    yum -y install scrcpy
    dnf -y install git
    dnf -y install python3
    dnf -y install android-tools
    dnf -y install scrcpy
    eopkg update-repo
    eopkg -y install git
    eopkg -y install python3
    eopkg -y install android-tools
    eopkg -y install scrcpy
    xbps-install -S
    xbps-install -y git
    xbps-install -y python3
    xbps-install -y android-tools
    xbps-install -y scrcpy
} &> /dev/null

if [[ -d ~/ghost ]]; then
    sleep 0
else
    cd ~
    {
        git clone https://github.com/EntySec/ghost.git
    } &> /dev/null
fi

if [[ -d ~/ghost ]]; then
    cd ~/ghost
else
    echo -e ""$E"Installation failed!"
    exit
fi

{
cp bin/ghost /usr/bin
chmod +x /usr/bin/ghost
cp bin/ghost /usr/local/bin
chmod +x /usr/local/bin/ghost
cp bin/ghost /data/data/com.termux/files/usr/bin
chmod +x /data/data/com.termux/files/usr/bin/ghost
} &> /dev/null

sleep 1
echo -e ""$S"Successfully installed!"
sleep 1
