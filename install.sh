#!/bin/bash

# Copyright (C) 2016 - 2018 Entynetproject
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use the software except in compliance with the License.
#
# You may obtain a copy of the License at:
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

RS="\033[0;31m"
YS="\033[1;33m"
CE="\033[0;97m"

#blue start 
	BS="\033[1;34m"
#color end
	CE="\033[0;97m"
	C="\033[0m"
#red start
	RS="\033[0;31m"
#green start
	GNS="-e \033[1;32m"
#white start
   WHS="\033[0;97m"

if [[ $EUID -ne 0 ]]
then
   sleep 1
   echo -e ""$CE"["$RS"+"$CE"] This script must be run as root!"$C"" 1>&2
   sleep 1
   exit
fi

if [[ -d ~/ghost ]]
then
sleep 0
else
cd ~
{
git clone https://github.com/entynetproject/ghost.git
} &> /dev/null
fi
sleep 0.5
clear
sleep 0.5
cd ~/ghost
cat banner/banner.txt
echo

if [[ -f /etc/ghost.conf ]]
then

CONF="$( cat /etc/ghost.conf )"
sleep 1

if [[ "$CONF" = "arm" ]]
then
if [[ -d /System/Library/CoreServices/SpringBoard.app ]]
then
echo -e ""$CE"["$RS"+"$CE"] Installing dependencies..."$C""
{
if ! which pip > /dev/null; then
	curl https://bootstrap.pypa.io/get-pip.py | python
fi
} &> /dev/null
else 
echo -e ""$CE"["$RS"+"$CE"] Installing dependencies..."$C""
pkg update
pkg -y install python
fi
fi

if [[ "$CONF" = "amd" ]]
then
if [[ -d /System/Library/CoreServices/Finder.app ]]
then
echo -e ""$CE"["$RS"+"$CE"] Installing dependencies..."$C"" 
{
if ! which pip > /dev/null; then
	curl https://bootstrap.pypa.io/get-pip.py | python
fi
} &> /dev/null
else 
echo -e ""$CE"["$RS"+"$CE"] Installing dependencies..."$C"" 
apt-get update
apt-get -y install python
apt-get -y install python-pip
fi
fi

if [[ "$CONF" = "intel" ]]
then
if [[ -d /System/Library/CoreServices/Finder.app ]]
then
echo -e ""$CE"["$RS"+"$CE"] Installing dependencies..."$C"" 
{
if ! which pip > /dev/null; then
	curl https://bootstrap.pypa.io/get-pip.py | python
fi
} &> /dev/null
else 
echo -e ""$CE"["$RS"+"$CE"] Installing dependencies..."$C"" 
apt-get update
apt-get -y install python
apt-get -y install python-pip
fi
fi

else
read -e -p $'\033[0;97m[\033[0;31m+\033[0;97m] Select your architecture (amd/intel/arm):' CONF
if [[ "$CONF" = "" ]]
then
exit
else
if [[ "$CONF" = "arm" ]]
then
read -e -p $'\033[0;97m[\033[0;31m+\033[0;97m] Is this a single board computer (yes/no):' PI
if [[ "$PI" = "yes" ]]
then
echo "amd" >> /etc/ghost.conf
CONF="amd"
else
echo "$CONF" >> /etc/ghost.conf
fi
else
echo "$CONF" >> /etc/ghost.conf
fi
fi
sleep 1

if [[ "$CONF" = "arm" ]]
then
if [[ -d /System/Library/CoreServices/SpringBoard.app ]]
then
echo -e ""$CE"["$RS"+"$CE"] Installing dependencies..."$C"" 
{
if ! which pip > /dev/null; then
	curl https://bootstrap.pypa.io/get-pip.py | python
fi
} &> /dev/null
else 
echo -e ""$CE"["$RS"+"$CE"] Installing dependencies..."$C"" 
pkg update
pkg -y install python
fi
fi

if [[ "$CONF" = "amd" ]]
then
if [[ -d /System/Library/CoreServices/Finder.app ]]
then
echo -e ""$CE"["$RS"+"$CE"] Installing dependencies..."$C"" 
{
if ! which pip > /dev/null; then
	curl https://bootstrap.pypa.io/get-pip.py | python
fi
} &> /dev/null
else 
echo -e ""$CE"["$RS"+"$CE"] Installing dependencies..."$C"" 
apt-get update
apt-get -y install python
apt-get -y install python-pip
fi
fi

if [[ "$CONF" = "intel" ]]
then
if [[ -d /System/Library/CoreServices/Finder.app ]]
then
echo -e ""$CE"["$RS"+"$CE"] Installing dependencies..."$C"" 
{
if ! which pip > /dev/null; then
	curl https://bootstrap.pypa.io/get-pip.py | python
fi
} &> /dev/null
else 
echo -e ""$CE"["$RS"+"$CE"] Installing dependencies..."$C"" 
apt-get update
apt-get -y install python
apt-get -y install python-pip
fi
fi
fi

{
pip install -r requirements.txt
} &> /dev/null

{
cd ~/ghost/bin
cp ghost /usr/local/bin
chmod +x /usr/local/bin/ghost
cp ghost /bin
chmod +x /bin/ghost
cp ghost /data/data/com.termux/files/usr/bin
chmod +x /data/data/com.termux/files/usr/bin/ghost
} &> /dev/null
