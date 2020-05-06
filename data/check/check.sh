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
