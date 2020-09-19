#!/bin/bash

if [[ "$1" = "" ]]; then
    echo "Usage: dcheck.sh {hidden}"
    echo
    echo "Note: This file only for Ghost Framework, if you execute it without"
    echo "Ghost Framework it will not work, this is only a part of main code."
else
    {
    check="$(adb shell """if [[ -d """$1""" ]]
    then
    echo 0
    fi""")"
    } &> /dev/null
    if [[ "$check" = "0" ]]; then
        echo "0"
    else
        echo "1"
    fi
fi
