#! /usr/bin/python3

import os #Library for OS operations, allows for terminal commands
import subprocess #Library for OS subprocesses, may be used for more sophisticated OS commands
from subprocess import call
import sys #Library for system usage
import shlex #Library needed for tokenization of arguments
import time
from smbus import SMBus
import smbus

#Code for controlling Master-Slave i2c interaction with Ardiuno
addr = 0x5 # bus address
bus = SMBus(1) # indicates /dev/ic2-1
time.sleep(1) #Add delay to fix stuff

checkHATflag = True #Global flag for checkingwhat HAT is connected
wrongHATflag = False #Global flag for checking when wrong HAT is connected

while(1):
    #time.sleep(1) #Check every 1 second for HAT connection
    i2cHAT = shlex.split(os.popen("i2cget -y 0 0x50").read())
    i2cArd = shlex.split(os.popen("i2cget -y 1 0x05").read())
    if (i2cHAT):
        print("detected")
        if (checkHATflag == False):
            if (i2cArd):
                print("i2c connection with Arduino")

        if (wrongHATflag):
            checkHATflag = True
        
        while(checkHATflag):
            #Function to call the system, allows for direct string implementation of terminal commands
            #Exact line of code to run the EEPROM flashing and reading back from the terminal to gather the EEPROM information onto a .txt file
            os.system("cd /home/pi/hats/eepromutils/ ; printf yes | sudo ./eepflash.sh -r -f=read_back.eep -t=24c32 ; ./eepdump read_back.eep read_back.txt")
            time.sleep(1)
            a_file = open("/home/pi/hats/eepromutils/read_back.txt") #Command to open file with terminal command, direct location implemented in string to EEPROM .txt file
            lines_to_read = [13] #Reads line 13 of opened .txt file, line 13 has the UUID

            for position, line in enumerate(a_file):
                if position in lines_to_read:
                    chucks = line.split()[1].split('-', 5)
                    #print(chucks[0])

            if (chucks[0] == '9bb69b73' and
                chucks[1] == '7feb' and
                chucks[2] == '498c' and
                chucks[3] == '8692' and
                chucks[4] == '15012100007f'):
                print("Hello Pi Juice")
                #os.system("lxterminal -e python3 /home/pi/Arduino_Retrival_and_PHP_Decryption.py &")

                #call(["python3", "/home/Arduino_Retrival_and_PHP_Decryption.py"])
                #-os.system("open http://localhost")
                #9bb69b73-7feb-498c-8692-15012100007f
                if (i2cArd):
                    print("Go Ard Go")
#                   bus.write_byte(addr, 0x0) # switch it off/brake
                checkHATflag = False
            elif (chucks[0] == '00000000' and
                chucks[1] == '0000' and
                chucks[2] == '0000' and
                chucks[3] == '0000' and
                chucks[4] == '000000000135'):
                print("Hello TestID HAT")
                #os.system("python3 masterslave_rpi_ard.py")
                if (i2cArd):
                    bus.write_byte(addr, 0x1) # switch it on
                    time.sleep(0.2)
                    bus.write_byte(addr, 0x0) # switch it off
                    time.sleep(0.2)
                    bus.write_byte(addr, 0x1) # switch it on
                    time.sleep(0.2)
                    bus.write_byte(addr, 0x0) # switch it off
                    time.sleep(0.2)
                time.sleep(1)
                checkHATflag = False
            else:
                print("Big Ls")
                bus.write_byte(addr, 0x1)
                time.sleep(0.5)
                #os.system("sudo reboot now")
                if (i2cArd):
                    bus.write_byte(addr, 0x0) # switch it off/brakes
                wrongHATflag = True
                checkHATflag = False

    else:
        print("Error: Not detected")
        if (i2cArd):
            bus.write_byte(addr, 0x0) # switch it off
            time.sleep(0.25)
            checkHATflag = True
        checkHATflag = True
        #os.system("sudo reboot now")
