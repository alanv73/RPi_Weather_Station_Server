'''
This module includes imported modules and 
heavily modified versions of software developed by
The Raspberry Pi Foundation and Adafruit Industries
Copyright (c) 2012-2013 Limor Fried, Kevin Townsend and Mikey Sklar for Adafruit Industries. All rights reserved.
Copyright (c) 2017, Raspberry Pi Foundation. All rights reserved.
'''
from gpiozero import MCP3008
import time, math

## RPF values
volts = {0.4: 0.0, 1.4: 22.5, 1.2: 45.0, 2.8: 67.5,
         2.7: 90.0, 2.9: 112.5, 2.2: 135.0, 2.5: 157.5,
         1.8: 180.0, 2.0: 202.5, 0.7: 225.0, 0.8: 247.5,
         0.1: 270.0, 0.3: 292.5, 0.2: 315.0, 0.6: 337.5}

## My changes to RPF values
##volts = {0.4: 0.0, 1.4: 22.5, 1.2: 45.0, 2.8: 67.5, 2.7: 90.0,
##         2.9: 123.8, 3.0: 129.4, 2.1: 135.0, 2.2: 135.0, 2.3: 157.5,
##         2.5: 157.5, 2.6: 168.8, 1.7: 168.8, 1.8: 180.0, 1.9: 202.5,
##         2.0: 202.5, 0.7: 225.0, 0.8: 247.5, 0.1: 270.0, 0.3: 292.5,
##         0.2: 315.0, 0.6: 337.5}

## Experimental values
##volts = {2.9: 0, 1.9: 22.5, 2.1: 45, 0.5: 67.5,
##         0.6: 90, 0.4: 112.5, 1.1: 135, 0.8: 157.5,
##         1.5: 180, 1.3: 202.5, 2.6: 225, 2.5: 247.5,
##         3.2: 270, 3.0: 292.5, 3.1: 315, 2.7: 337.5}

adc = MCP3008(channel=0)
count = 0
values = []

def get_average(angles):
    sin_sum = 0.0
    cos_sum = 0.0

    for angle in angles:
        r = math.radians(angle)
        sin_sum += math.sin(r)
        cos_sum += math.cos(r)

    flen = float(len(angles))
    s = sin_sum / flen
    c = cos_sum / flen
    arc = math.degrees(math.atan(s / c))
    average = 0.0

    if s > 0 and c > 0:
        average = arc
    elif c < 0:
        average = arc + 180
    elif s < 0 and c > 0:
        average = arc + 360

    return 0.0 if average == 360 else average

def get_value(length=5):
    data = []
    winds = []
##    print("Measuring wind direction for %d seconds..." % length)
    start_time = time.time()

    while time.time() - start_time <= length:
        wind =round(adc.value*3.3,1)
        if not wind in volts: # keep only good measurements
            # print('unknown wind-vane voltage value ' + str(wind) + '\r', end = '')
            pass
        else:
            data.append(volts[wind])
            winds.append(wind)

    return get_average(data)#,round(get_average(winds),1)

# while True:
#     print(get_value(10))
if __name__ == "__main__":
    print('wind direction: %f' % get_value())
