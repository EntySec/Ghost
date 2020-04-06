#!/bin/bash

adb shell su 0 'cp /data/misc/wifi/wpa_supplicant.conf /sdcard/'
adb pull /sdcard/wpa_supplicant.conf $2
                                    
adb shell screencap /sdcard/screen.png > /dev/null
adb pull /sdcard/screen.png $2
                                    
adb shell screenrecord /sdcard/screen.mp4
adb pull /sdcard/screen.mp4 $2
                                    
