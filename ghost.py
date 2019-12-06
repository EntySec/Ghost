#-*- coding: utf-8 -*-


#=============================
#Imports
import os
import sys
import random
import time as  t
from colorama import Fore, init

reload(sys)
sys.setdefaultencoding("utf-8")

def autocomplete(text, state):
    import readline
    line = readline.get_line_buffer()
    splitted = line.lstrip().split(" ")

    # no space, autocomplete will be the basic commands:
    options = [x + " " for x in actions if x.startswith(text)]
    options.extend([x + " " for x in remap if x.startswith(text)])
    try:
        return options[state]
    except:
        return None

def get_input(prompt, auto_complete_fn=None, basefile_fn=None):
    try:
        if auto_complete_fn != None:
            import readline
            readline.set_completer_delims(' \t\n;/')
            readline.parse_and_bind("tab: complete")
            readline.set_completer(auto_complete_fn)
    except Exception as e:
        pass

    cmd = raw_input("%s" % prompt)
    return cmd.strip()

#=============================
# Variables
CurrentDir = os.path.dirname(os.path.abspath(__file__))
readline.set_completer(autocomplete)
readline.parse_and_bind("tab: complete")
load_count = 0
page2 = False

#=============================
#Install Functions
# def ColoringModeStartup():
#     coloring_file = open(CurrentDir+"\\install\\coloring.txt", "a+")
#     line = open(CurrentDir+"\\install\\coloring.txt", "a+").readline()
#     if 'init' in line:
#         init(convert=True)
#         main()
#     if 'false' in line:
#         main()
#     if "NOT_LOADED" in line:
#         platform_choice = raw_input("Are you loading this script in (W)indows or (L)inux: ")
#         open(CurrentDir+"\\install\\coloring.txt", "w").close()
#         if platform_choice.lower() == 'w':
#             coloring_file.write("init")
#         else:
#             coloring_file.write("false")
#             yn = raw_input(Fore.WHITE + "Have you already installed adb via command line "+Fore.GREEN + "Y"+Fore.WHITE+"/"+Fore.RED+"N "+Fore.WHITE)
#             if yn == "n":
#                 os.system("sudo apt install adb")
#             else:
#                 main()

#=============================
# Graphics # http://patorjk.com/software/taag/#p=display&f=Graffiti&t=Type%20Something%20

arrow = Fore.RED + "  └──>".decode("utf-8").strip() + Fore.WHITE
arrow = str(arrow)
connect = Fore.RED + "│".decode("utf-8").strip() + Fore.WHITE

page_1 = ''' 
     .-.          {0}[{1}Ghost Framework{0}]{2}
   .'   `.   {2}Developed by Entynetproject{2} 
   :0 0   :        {0}({2}Ivan Nikolsky{0}){2}      
   : o    `.             
  :         ``.                {0}[{1}1{0}] {2}Show connected devices
 :             `.              {0}[{1}2{0}] {2}Disconect all devices
:  :         .   `.            {0}[{1}3{0}] {2}Connect a new device
:   :          ` . `.          {0}[{1}4{0}] {2}Access shell on a device
 `.. :            `. ``;       {0}[{1}5{0}] {2}Install an apk on a device
    `:;             `:'        {0}[{1}6{0}] {2}Screen record a device
       :              `.       {0}[{1}7{0}] {2}Get device screenshot
        `.              `.     {0}[{1}8{0}] {2}Restart ADB Server
          `'`'`'`---..,___`.   {0}[{1}9{0}] {2}Pull folders from device       
                     
{0}[{1}10{0}] {2}Shutdown the device       {0}[{1}19{0}]{2} Extract apk from app                         
{0}[{1}11{0}] {2}Uninstall an app          {0}[{1}20{0}]{2} Get Battery Status
{0}[{1}12{0}] {2}Show device log           {0}[{1}21{0}]{2} Network status
{0}[{1}13{0}] {2}Dump System Info          {0}[{1}22{0}]{2} Turn WiFi on/off
{0}[{1}14{0}] {2}List all device apps      {0}[{1}23{0}]{2} Remove Password
{0}[{1}15{0}] {2}Run a device app          {0}[{1}24{0}]{2} Use Ghost Keycode
{0}[{1}16{0}]{2} Port Forwarding           {0}[{1}25{0}]{2} Get Current Activity
{0}[{1}17{0}]{2} Grab wpa_supplicant       {0}[{1}26{0}]{2} Update Ghost Framework
{0}[{1}18{0}]{2} Show Mac/Inet             {0}[{1}27{0}]{2} Exit Ghost Framework
'''.format(Fore.GREEN, Fore.RED, Fore.WHITE)

page_2 = '''\n
'''.format(Fore.GREEN, Fore.RED, Fore.WHITE)


#=============================
#Main
def main():
    page_num = 1
    option = raw_input(Fore.WHITE + "ghost"+Fore.RED + "(main_menu)"+Fore.WHITE + "> ")
    while(1):
        if option == '':
            option = raw_input(Fore.WHITE + "ghost"+Fore.RED + "(main_menu)"+Fore.WHITE + "> ")
        
        if option == '1':
            os.system("adb devices -l")
            option = raw_input(Fore.WHITE + "ghost"+Fore.RED + "(main_menu)"+Fore.WHITE + "> ")

        elif option  ==  '2':
            os.system("adb disconnect")
            main()

        elif option == '3':
            os.system("adb tcpip 5555")
            print (("\n[{0}+{1}] Enter a phone IP address.").format(Fore.RED, Fore.WHITE))
            try:
                device_name = raw_input (arrow+" ghost"+Fore.RED + "(connect_phone)"+Fore.WHITE + "> ")
            except KeyboardInterrupt:
                main()
            if device_name == '':
                main()
            if device_name == '27':
                exit()
                
            os.system("adb connect "+device_name+":5555")
            option = raw_input(Fore.WHITE + "ghost"+Fore.RED + "(main_menu)"+Fore.WHITE + "> ")

        elif option  == '4':
            os.system("adb -s "+device_name+" shell")
            option = raw_input(Fore.WHITE + "ghost"+Fore.RED + "(main_menu)"+Fore.WHITE + "> ")

        elif option == '5':
            print (("     "+connect))
            print (("    [{0}+{1}] Enter the apk location.").format(Fore.RED, Fore.WHITE))
            apk_location = raw_input("    "+arrow + "ghost"+Fore.RED + "(apk_install)"+Fore.WHITE + "> ")
            os.system("adb -s  "+device_name+" install "+apk_location)
            print (Fore.GREEN  +  "Apk has been installed.")
            option = raw_input(Fore.WHITE + "ghost"+Fore.RED + "(main_menu)"+Fore.WHITE + "> ")

        elif option ==  '6':
            print (("     "+connect))
            print (("    [{0}+{1}] Please wait 3m its recording").format(Fore.RED, Fore.WHITE))
            print (("     "+connect))
            os.system("adb -s "+device_name+" shell screenrecord /sdcard/demo.mp4")
            print (("    [{0}+{1}] Enter where you would like the video to be saved.[Default: present working directory]").format(Fore.RED, Fore.WHITE))
            place_location = raw_input("    "+arrow + "ghost"+Fore.RED + "(screen_record)"+Fore.WHITE + "> ")
            os.system("adb -s "+device_name+" pull /sdcard/demo.mp4 "+place_location)
            option = raw_input(Fore.WHITE + "ghost"+Fore.RED + "(main_menu)"+Fore.WHITE + "> ")

        elif option  == '7':
            os.system("adb -s "+device_name+" shell screencap /sdcard/screen.png")
            print (("     "+connect))
            print (("    [{0}+{1}] Enter where you would like the screenshot to be saved.[Default: present working directory]").format(Fore.RED, Fore.WHITE))
            place_location = raw_input("    "+arrow + "ghost"+Fore.RED + "(screenshot)"+Fore.WHITE + "> ")
            os.system("adb -s "+device_name+" pull /sdcard/screen.png "+place_location)
            option = raw_input(Fore.WHITE + "ghost"+Fore.RED + "(main_menu)"+Fore.WHITE + "> ")

        elif option == '8':
            os.system("adb kill-server && adb start-server")
            option = raw_input(Fore.WHITE + "ghost"+Fore.RED + "(main_menu)"+Fore.WHITE + "> ")

        elif option == '9':
            print (("     "+connect))
            print (("    [{0}+{1}] Enter a file location on a device").format(Fore.RED, Fore.WHITE))
            file_location = raw_input("    "+arrow + "ghost"+Fore.RED + "(file_pull)"+Fore.WHITE + "> ")
            print (("        "+connect))
            print (("       [{0}+{1}] Enter where you would like the file to be saved.[Default: present working directory]").format(Fore.RED, Fore.WHITE))
            place_location = raw_input("       "+arrow + "ghost"+Fore.RED + "(file_pull)"+Fore.WHITE + "> ")
            os.system("adb -s "+device_name+" pull "+file_location+" "+place_location)
            option = raw_input(Fore.WHITE + "ghost"+Fore.RED + "(main_menu)"+Fore.WHITE + "> ")

        elif option == '10':
            os.system("adb -s "+device_name+ " reboot ")
            option = raw_input(Fore.WHITE + "ghost"+Fore.RED + "(main_menu)"+Fore.WHITE + "> ")

        elif option ==  '11':
            print (("     "+connect))
            print (("    [{0}+{1}] Enter a package name.").format(Fore.RED, Fore.WHITE))
            package_name = raw_input("    "+arrow + "ghost"+Fore.RED + "(app_delete)"+Fore.WHITE + "> ")
            os.system("adb -s "+device_name+" unistall "+package_name)
            option = raw_input(Fore.WHITE + "ghost"+Fore.RED + "(main_menu)"+Fore.WHITE + "> ")

        elif option == '12':
            os.system('adb -s '+device_name+" logcat ")
            option = raw_input(Fore.WHITE + "ghost"+Fore.RED + "(main_menu)"+Fore.WHITE + "> ")

        elif option == '13':
            os.system("adb  -s "+device_name+" dumpsys")
            option = raw_input(Fore.WHITE + "ghost"+Fore.RED + "(main_menu)"+Fore.WHITE + "> ")

        elif option == '14':
            os.system("adb -s " +device_name+ " shell pm list packages -f")
            option = raw_input(Fore.WHITE + "ghost"+Fore.RED + "(main_menu)"+Fore.WHITE + "> ")

        elif option == '15':
            print (("     "+connect))
            print (("    [{0}+{1}] Enter a package name. They look like this --> com.snapchat.android").format(Fore.RED, Fore.WHITE))
            package_name = raw_input("    "+arrow + "ghost"+Fore.RED + "(app_run)"+Fore.WHITE + "> ")
            os.system("adb -s "+device_name+" shell monkey -p "+package_name+" -v 500")
            option = raw_input(Fore.WHITE + "ghost"+Fore.RED + "(main_menu)"+Fore.WHITE + "> ")

        elif option == '16':
            print (("     "+connect))
            print (("    [{0}+{1}] Enter a port on the device.").format(Fore.RED, Fore.WHITE))
            port_device = raw_input("    "+arrow + "ghost"+Fore.RED + "(port_forward)"+Fore.WHITE + "> ")
            print (("         "+connect))
            print (("        [{0}+{1}] Enter a port to forward it too.").format(Fore.RED, Fore.WHITE))
            forward_port = raw_input("        "+arrow + "ghost"+Fore.RED + "(port_forward)"+Fore.WHITE + "> ")
            os.system("adb -s "+device_name+" forward tcp:"+port_device+" tcp:"+forward_port)
            option = raw_input(Fore.WHITE + "ghost"+Fore.RED + "(main_menu)"+Fore.WHITE + "> ")

        elif option == '17':
            try:
                print ((Fore.WHITE + "    [{0}+{1}]{1}THE DEVICE NEEDS TO BE ROOTED TO CONTINUE TO EXIT USE CTRL +C").format(Fore.RED, Fore.WHITE))
                print (("     "+connect))
                print (("    [{0}+{1}] Enter where you want the file to be saved.[Default: present working directory]").format(Fore.RED, Fore.WHITE))
                location = raw_input("    "+arrow + "ghost"+Fore.RED + "(wpa_grab)"+Fore.WHITE + "> ")
                os.system("adb -s "+device_name+" shell "+"su -c 'cp /data/misc/wifi/wpa_supplicant.conf /sdcard/'")
                os.system("adb -s "+device_name+" pull /sdcard/wpa_supplicant.conf "+location)
                option = raw_input(Fore.WHITE + "ghost"+Fore.RED + "(main_menu)"+Fore.WHITE + "> ")

            except KeyboardInterrupt:
                option = raw_input(Fore.WHITE + "ghost"+Fore.RED + "(main_menu)"+Fore.WHITE + "> ")

        elif option == '18':
            os.system("adb -s " +device_name+ " shell ip address show wlan0")
            option = raw_input(Fore.WHITE + "ghost"+Fore.RED + "(main_menu)"+Fore.WHITE + "> ")

        elif option == '19':
            print (("     "+connect))
            print (("    [{0}+{1}] Enter a package name. They look like this --> com.snapchat.android").format(Fore.RED, Fore.WHITE))
            package_name = raw_input("    "+arrow + "ghost"+Fore.RED + "(pull_apk)"+Fore.WHITE + "> ")
            os.system("adb -s "+device_name+" shell pm path "+package_name)
            print (("         "+connect))
            print (("        [{0}+{1}] Enter The path.looks like this /data/app/com.snapchat.android-qWgDcBiCEvANq6op_NPqeA==/base.apk").format(Fore.RED, Fore.WHITE))
            path = raw_input("        "+arrow + "ghost"+Fore.RED + "(pull_apk)"+Fore.WHITE + "> ")
            print (("             "+connect))
            print (("            [{0}+{1}] Enter The location to store the apk: [Default: present working directory]")  .format(Fore.RED, Fore.WHITE))
            location =   raw_input("            "+arrow + "ghost"+Fore.RED + "(pull_apk)"+Fore.WHITE + "> ")
            os.system("adb -s " +device_name+" pull "+path+" "+location)
            option = raw_input(Fore.WHITE + "ghost"+Fore.RED + "(main_menu)"+Fore.WHITE + "> ")

        elif option == '20':
            os.system("adb -s " +device_name+ " shell dumpsys battery")
            option = raw_input(Fore.WHITE + "ghost"+Fore.RED + "(main_menu)"+Fore.WHITE + "> ")

        elif option == '21':
            os.system("adb -s " +device_name+ " shell netstat")
            option = raw_input(Fore.WHITE + "ghost"+Fore.RED + "(main_menu)"+Fore.WHITE + "> ")

        elif option == '22':
            print (("     "+connect))
            print (("    [{0}+{1}] To turn wifi back on you need the device to be pluged in.").format(Fore.RED, Fore.WHITE))
            print (("     "+connect))
            on_off = raw_input(Fore.WHITE + "    ["+Fore.RED+"+"+Fore.WHITE+"]Would you like the wifi "+Fore.GREEN +"on"+Fore.WHITE +"/"+Fore.RED +"off "+Fore.WHITE)
            if on_off == 'off':
                command = " shell svc wifi disable"
            else:
                command = " shell svc wifi enable"

            os.system("adb -s "+device_name+command)
            option = raw_input(Fore.WHITE + "ghost"+Fore.RED + "(main_menu)"+Fore.WHITE + "> ")

        elif option == '23':
            print ((Fore.WHITE + "    [{0}+{1}]{1}THE DEVICE NEEDS TO BE ROOTED TO CONTINUE TO EXIT USE CTRL +C THIS IS ALSO UNTESTED").format(Fore.RED, Fore.WHITE))
            print (("     "+connect))
            print (Fore.RED + "******************TRYING TO REMOVE PASS******************")
            os.system("adb -s "+device_name+" shell su 0 'rm /data/system/gesture.key'")
            os.system("adb -s "+device_name+" shell su 0 'rm /data/system/locksettings.db'")
            os.system("adb -s "+device_name+" shell su 0 'rm /data/system/locksettings.db-wal'")
            os.system("adb -s "+device_name+" shell su 0 'rm /data/system/locksettings.db-shm'")
            print (Fore.RED + "******************TRYING TO REMOVE PASS******************")
            option = raw_input(Fore.WHITE + "ghost"+Fore.RED + "(main_menu)"+Fore.WHITE + "> ")

        elif option == '24':
            print ('''
    0 -->  "KEYCODE_UNKNOWN"
    1 -->  "KEYCODE_MENU"
    2 -->  "KEYCODE_SOFT_RIGHT"
    3 -->  "KEYCODE_HOME"
    4 -->  "KEYCODE_BACK"
    5 -->  "KEYCODE_CALL"
    6 -->  "KEYCODE_ENDCALL"
    7 -->  "KEYCODE_0"
    8 -->  "KEYCODE_1"
    9 -->  "KEYCODE_2"
    10 -->  "KEYCODE_3"
    11 -->  "KEYCODE_4"
    12 -->  "KEYCODE_5"
    13 -->  "KEYCODE_6"
    14 -->  "KEYCODE_7"
    15 -->  "KEYCODE_8"
    16 -->  "KEYCODE_9"
    17 -->  "KEYCODE_STAR"
    18 -->  "KEYCODE_POUND"
    19 -->  "KEYCODE_DPAD_UP"
    20 -->  "KEYCODE_DPAD_DOWN"
    21 -->  "KEYCODE_DPAD_LEFT"
    22 -->  "KEYCODE_DPAD_RIGHT"
    23 -->  "KEYCODE_DPAD_CENTER"
    24 -->  "KEYCODE_VOLUME_UP"
    25 -->  "KEYCODE_VOLUME_DOWN"
    26 -->  "KEYCODE_POWER"
    27 -->  "KEYCODE_CAMERA"
    28 -->  "KEYCODE_CLEAR"
    29 -->  "KEYCODE_A"
    30 -->  "KEYCODE_B"
    31 -->  "KEYCODE_C"
    32 -->  "KEYCODE_D"
    33 -->  "KEYCODE_E"
    34 -->  "KEYCODE_F"
    35 -->  "KEYCODE_G"
    36 -->  "KEYCODE_H"
    37 -->  "KEYCODE_I"
    38 -->  "KEYCODE_J"
    39 -->  "KEYCODE_K"
    40 -->  "KEYCODE_L"
    41 -->  "KEYCODE_M"
    42 -->  "KEYCODE_N"
    43 -->  "KEYCODE_O"
    44 -->  "KEYCODE_P"
    45 -->  "KEYCODE_Q"
    46 -->  "KEYCODE_R"
    47 -->  "KEYCODE_S"
    48 -->  "KEYCODE_T"
    49 -->  "KEYCODE_U"
    50 -->  "KEYCODE_V"
    51 -->  "KEYCODE_W"
    52 -->  "KEYCODE_X"
    53 -->  "KEYCODE_Y"
    54 -->  "KEYCODE_Z"
    55 -->  "KEYCODE_COMMA"
    56 -->  "KEYCODE_PERIOD"
    57 -->  "KEYCODE_ALT_LEFT"
    58 -->  "KEYCODE_ALT_RIGHT"
    59 -->  "KEYCODE_SHIFT_LEFT"
    60 -->  "KEYCODE_SHIFT_RIGHT"
    61 -->  "KEYCODE_TAB"
    62 -->  "KEYCODE_SPACE"
    63 -->  "KEYCODE_SYM"
    64 -->  "KEYCODE_EXPLORER"
    65 -->  "KEYCODE_ENVELOPE"
    66 -->  "KEYCODE_ENTER"
    67 -->  "KEYCODE_DEL"
    68 -->  "KEYCODE_GRAVE"
    69 -->  "KEYCODE_MINUS"
    70 -->  "KEYCODE_EQUALS"
    71 -->  "KEYCODE_LEFT_BRACKET"
    72 -->  "KEYCODE_RIGHT_BRACKET"
    73 -->  "KEYCODE_BACKSLASH"
    74 -->  "KEYCODE_SEMICOLON"
    75 -->  "KEYCODE_APOSTROPHE"
    76 -->  "KEYCODE_SLASH"
    77 -->  "KEYCODE_AT"
    78 -->  "KEYCODE_NUM"
    79 -->  "KEYCODE_HEADSETHOOK"
    80 -->  "KEYCODE_FOCUS"
    81 -->  "KEYCODE_PLUS"
    82 -->  "KEYCODE_MENU"
    83 -->  "KEYCODE_NOTIFICATION"
    84 -->  "KEYCODE_SEARCH"
    85 -->  "TAG_LAST_KEYCODE"
            ''')
            print (("[{0}+{1}] Enter a number.").format(Fore.RED, Fore.WHITE))
            num = raw_input(arrow + "ghost"+Fore.RED + "(keycode)"+Fore.WHITE + "> ")
            os.system("adb -s "+device_name+" shell input keyevent "+num)
            option = raw_input(Fore.WHITE + "ghost"+Fore.RED + "(main_menu)"+Fore.WHITE + "> ")

        elif option == '25':
            os.system("adb -s " +device_name+ " dumpsys activity")
            option = raw_input(Fore.WHITE + "ghost"+Fore.RED + "(main_menu)"+Fore.WHITE + "> ")

        elif option == '26':
           os.system("chmod +x bin/ghost && bin/ghost -u")
           option = raw_input(Fore.WHITE + "ghost"+Fore.RED + "(main_menu)"+Fore.WHITE + "> ")

        elif option == '27':
            exit()
            break
        else:
            print("ghost: error: invalid command")
            option = raw_input(Fore.WHITE + "ghost"+Fore.RED + "(main_menu)"+Fore.WHITE + "> ")


    main()

#=============================
#=============================  
# Run
yn = raw_input(Fore.WHITE + "Have you already installed adb "+Fore.GREEN + "Y"+Fore.WHITE+"/"+Fore.RED+"n "+Fore.WHITE)
if yn == "n":
    os.system("sudo apt install adb")
print (Fore.RED + "Starting  adb server...")
os.system("adb tcpip 5555")
t.sleep(4)
os.system('clear')
print (page_1)
main()
