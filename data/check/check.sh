#!/bin/bash

if [[ "$1" = "" ]]; then
    echo "Usage: check.sh <file>"
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
