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

echo -e $G"Installing Ghost Framework..."

if [[ $(uname -s) == "Darwin" && $(uname -m) == "x86_64" || $(uname -m) == "arm64" ]]; then
    {
        if [[ -z $(command -v brew) ]]; then
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
        fi
        brew install git python3 openssl
    } &> /dev/null
elif [[ $(uname -s) == "Linux" ]]; then
    if [[ ! -z $(command -v apt-get) ]]; then
        {
            sudo apt-get update
            sudo apt-get -y install git python3 python3-pip openssl
        } &> /dev/null
    elif [[ ! -z $(command -v pkg) ]]; then
        {
            sudo pkg update
            sudo pkg -y install git python openssl
        } &> /dev/null
    elif [[ ! -z $(command -v apk) ]]; then
        {
            sudo apk update
            sudo apk add git python3 py3-pip openssl
        } &> /dev/null
    elif [[ ! -z $(command -v pacman) ]]; then
        {
            sudo pacman -Sy
            sudo pacman -S --noconfirm git python3 python3-pip openssl
        } &> /dev/null
    elif [[ ! -z $(command -v zypper) ]]; then
        {
            sudo zypper refresh
            sudo zypper install -y git python3 python3-pip openssl
        } &> /dev/null
    elif [[ ! -z $(command -v eopkg) ]]; then
        {
            sudo eopkg update-repo
            sudo eopkg -y install git python3 python3-pip openssl
        } &> /dev/null
    elif [[ ! -z $(command -v xbps-install) ]]; then
        {
            sudo xbps-install -S
            sudo xbps-install -y git python3 python3-pip openssl
        } &> /dev/null
    elif [[ ! -z $(command -v yum) ]]; then
        {
            sudo yum -y install git python3 python3-pip openssl
        } &> /dev/null
    elif [[ ! -z $(command -v dnf) ]]; then
        {
            sudo dnf -y install git python3 python3-pip openssl
        } &> /dev/null
    else
        echo -e $E"Your system is not supported!"
        exit 1
    fi
else
    echo -e $E"Your system is not supported!"
    exit 1
fi

if [[ ! -d /usr/local/bin ]]; then
    {
        mkdir /usr/local/bin
    } &> /dev/null
fi

if [[ ! -d ~/.ghost ]]; then
    {
        git clone https://github.com/EntySec/ghost.git ~/.ghost
    } &> /dev/null
fi

if [[ -d ~/.ghost ]]; then
    cd ~/.ghost
else
    echo -e $E"Installation failed!"
    exit 1
fi

{
    sudo cp bin/ghost /usr/bin
    sudo chmod +x /usr/bin/ghost
    sudo cp bin/ghost /usr/local/bin
    sudo chmod +x /usr/local/bin/ghost
    sudo cp bin/ghost /data/data/com.termux/files/usr/bin
    sudo chmod +x /data/data/com.termux/files/usr/bin/ghost
} &> /dev/null

echo -e $S"Successfully installed!"
exit 0
