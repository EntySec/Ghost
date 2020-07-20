#!/bin/bash

G="\033[1;34m[*] \033[0m"
E="\033[1;31m[-] \033[0m"

if [[ "$1" = "" ]]
then
echo "Usage: launch.sh <application>"
exit
fi

echo -e ""$G"Launching "$1"..."

{
adb shell monkey -p $1 -v 500
} &> /dev/null
