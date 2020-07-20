#!/bin/bash

#            ---------------------------------------------------
#                              Ghost Framework                                                  
#            ---------------------------------------------------
#                Copyright (C) <2019-2020>  <Entynetproject>
#
#        This program is free software: you can redistribute it and/or modify
#        it under the terms of the GNU General Public License as published by
#        the Free Software Foundation, either version 3 of the License, or
#        any later version.
#
#        This program is distributed in the hope that it will be useful,
#        but WITHOUT ANY WARRANTY; without even the implied warranty of
#        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#        GNU General Public License for more details.
#
#        You should have received a copy of the GNU General Public License
#        along with this program.  If not, see <http://www.gnu.org/licenses/>.

printf '\033]2;install.sh\a'

G="\033[1;34m[*] \033[0m"
S="\033[1;32m[+] \033[0m"
I="\033[1;77m[i] \033[0m"
E="\033[1;31m[-] \033[0m"

if [[ $(id -u) != 0 ]]
then
   echo -e ""$E"Permission denied!"
   exit
fi

{
ASESR="$(ping -c 1 -q www.google.com >&/dev/null; echo $?)"
} &> /dev/null
if [[ "$ASESR" != 0 ]]
then 
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
apt-get update
apt-get -y install git
apt-get -y install python3
apt-get -y install adb
apt-get -y install android-tools-adb
apt-get -y install android-tools-fastboot
apk update
apk add git
apk add python3
apk add android-tools
pacman -Sy
pacman -S --noconfirm git
pacman -S --noconfirm python3
pacman -S --noconfirm android-tools
zypper refresh
zypper install -y git
zypper install -y python3
zypper install -y android-tools
yum -y install git
yum -y install python3
yum -y install android-tools
dnf -y install git
dnf -y install python3
dnf -y install android-tools
eopkg update-repo
eopkg -y install git
eopkg -y install python3
eopkg -y install android-tools
xbps-install -S
xbps-install -y git
xbps-install -y python3
xbps-install -y android-tools
} &> /dev/null

if [[ -d ~/ghost ]]
then
sleep 0
else
cd ~
{
git clone https://github.com/entynetproject/ghost.git
} &> /dev/null
fi

if [[ -d ~/ghost ]]
then
cd ~/ghost
else
echo -e ""$E"Installation failed!"
exit
fi

{
cd bin
cp ghost /usr/local/bin
chmod +x /usr/local/bin/ghost
cp ghost /bin
chmod +x /bin/ghost
cp ghost /data/data/com.termux/files/usr/bin
chmod +x /data/data/com.termux/files/usr/bin/ghost
} &> /dev/null

sleep 1
echo -e ""$S"Successfully installed!"
sleep 1
