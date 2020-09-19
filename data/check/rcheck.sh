#!/bin/bash

{
chr=$(adb shell which su)
} &> /dev/null

if [[ $chr = "" ]]; then
    echo "1"
else
    echo "0"
fi
