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

if [[ "$1" = "" ]] 
then
    echo -e "Usage: dctl.sh [connect|disconnect] <target>"
else
    if [[ "$1" = "connect" ]]
    then
        if [[ "$2" = "" ]]
        then
            echo -e "Usage: dctl.sh [connect|disconnect] <target>"
        else
            {
            adb connect $2
            sleep 1
            } &> /dev/null
        fi
    elif [[ "$1" = "disconnect" ]]
    then
        if [[ "$2" = "" ]]
        then
            echo -e "Usage: dctl.sh [connect|disconnect] <target>"
        else
            {
            adb disconnect $2
            } &> /dev/null
        fi
    else
        echo -e "Usage: dctl.sh [connect|disconnect] <target>"
    fi
fi
