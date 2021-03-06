#!/usr/bin/python3
'''
This module includes software developed by 
The Raspberry Pi Foundation
https://github.com/RaspberryPiFoundation/weather-station
Copyright (c) 2012-2013 Limor Fried, Kevin Townsend and Mikey Sklar for Adafruit Industries. All rights reserved.
Copyright (c) 2017, Raspberry Pi Foundation. All rights reserved.
'''

# ground temperature
import os, glob, time, subprocess

# add the lines below to /etc/modules (reboot to take effect)
# w1-gpio
# w1-therm

class DS18B20(object):

    def __init__(self):        
        self.device_file = glob.glob("/sys/bus/w1/devices/28*")[0] + "/w1_slave"
        
    def read_temp_raw(self):
        f = open(self.device_file, "r")
        lines = f.readlines()
        f.close()
        return lines
    
    def crc_check(self, lines):
        return lines[0].strip()[-3:] == "YES"
        
    def read_temp(self):
        temp_c = -255
        attempts = 0
        
        lines = self.read_temp_raw()
        success = self.crc_check(lines)
        
        while not success and attempts < 3:
            time.sleep(.2)
            lines = self.read_temp_raw()            
            success = self.crc_check(lines)
            attempts += 1
        
        if success:
            temp_line = lines[1]
            equal_pos = temp_line.find("t=")            
            if equal_pos != -1:
                temp_string = temp_line[equal_pos+2:]
                temp_c = float(temp_string)/1000.0
        
        return temp_c
    
if __name__ == "__main__":
    obj = DS18B20()
    tempc=obj.read_temp()
    tempf = round((9.0 / 5.0 * tempc + 32.0),2)
    print("Temp: %s F : %s C" % (tempf,tempc))
