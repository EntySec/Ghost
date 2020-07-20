#!/bin/bash

G="\033[1;34m[*] \033[0m"
E="\033[1;31m[-] \033[0m"

if [[ "$1" = "" ]]
then
echo "Usage: install.sh <application>"
exit
fi

{
adb install $1
} &> /dev/null
