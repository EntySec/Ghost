#!/bin/bash

if [[ "$1" = "" ]]; then
    echo "Usage: keycode.sh {hidden}"
    echo
    echo "Note: This file only for Ghost Framework, if you execute it without"
    echo "Ghost Framework it will not work, this is only a part of main code."
else
    {
    adb shell input keyevent $1
    } &> /dev/null
fi
