#!/bin/bash

if [[ "$1" = "" ]]; then
    echo "Usage: check.sh {hidden}"
    echo
    echo "Note: This file only for Ghost Framework, if you execute it without"
    echo "Ghost Framework it will not work, this is only a part of main code."
else
    {
    adb shell stat $1
    } &> .check
    {
    check="$(cat .check)"
    rm .check
    } &> /dev/null
    if [[ "${check[@]: :4}" = "stat" ]]; then
        echo "1"
    else
        echo "0"
    fi
fi
