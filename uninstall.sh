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
C="\033[0m"
GN="\033[0;32m"
WHS="\033[0;97m"

if [[ $EUID -ne 0 ]]
then
   sleep 1
   echo -e ""$GN"["$RS"+"$GN"]"$CE" This script must be run as root!"$C"" 1>&2
   sleep 1
   exit
fi

{
rm /bin/ghost
rm /usr/local/bin/ghost
rm -r ~/ghost
rm /etc/ghost.conf
rm /data/data/com.termux/files/usr/bin/ghost
} &> /dev/null
