#!/usr/bin/python3
'''
This module includes imported modules and 
modified versions of software developed by
The Raspberry Pi Foundation and Adafruit Industries
Copyright (c) 2012-2013 Limor Fried, Kevin Townsend and Mikey Sklar for Adafruit Industries. All rights reserved.
Copyright (c) 2017, Raspberry Pi Foundation. All rights reserved.
'''
import bme280
import smbus2

# ambient temperature, pressure, humidity

port = 1
address = 0x77 # Adafruit BME280 address. Other BME280s may be different
bus = smbus2.SMBus(port)

bme280.load_calibration_params(bus,address)

def read_all():
    bme280_data = bme280.sample(bus,address)
    return round(bme280_data.humidity, 2), round(bme280_data.pressure, 2), bme280_data.temperature
    
if __name__ == "__main__":
    print(read_all())
