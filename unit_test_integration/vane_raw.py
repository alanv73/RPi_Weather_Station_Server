from gpiozero import MCP3008
import time
adc = MCP3008(channel=0)
count = 0
volts = [0.4, 1.4, 1.2, 2.8,
         2.9, 2.2, 2.5, 1.8,
         2.0, 0.7, 0.8, 0.1,
         0.3, 0.2, 0.6, 2.7]

while True:
    wind =round(adc.value*3.3,1)
    if not wind in volts:
        print('Unknown value: ' + str(wind))
    else:
        print('Match: ' + str(wind))
