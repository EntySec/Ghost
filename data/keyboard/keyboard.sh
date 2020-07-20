#!/bin/bash

if [[ "$1" = "" ]]; then
    echo "Usage: keyboard.sh {hidden}"
    echo
    echo "Note: This file only for Ghost Framework, if you execute it without"
    echo "Ghost Framework it will not work, this is only a part of main code."
    exit
else
    {
    adb shell input text $1
    } &> /dev/null
fi
