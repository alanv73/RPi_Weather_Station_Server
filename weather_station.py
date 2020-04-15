#!/usr/bin/python3
'''
This module includes imported modules and 
heavily modified versions of software developed by
The Raspberry Pi Foundation and Adafruit Industries
'''

from gpiozero import Button
from gpiozero import CPUTemperature
import time, math, statistics
import bme280_sensor
import wind_direction
import ds18b20_therm
import database
import weather_math

wind_count = 0 # Counts how many half rotations
radius_cm = 9.0 # Radius of the anemometer
wind_interval = 5 # How often (secs) to report speed
interval = 300 # measurements recorded every 5 minutes (300 sec)
CM_IN_A_KM = 100000.0
SECS_IN_AN_HOUR = 3600
ADJUSTMENT = 1.18 # instrument calibration
BUCKET_SIZE = 0.2794 # inches of rain per bucket tip
rain_count = 0 
gust = 0
store_speeds = []
store_directions = []

# Every half-rotation, add 1 to count
def spin():
    global wind_count
    wind_count = wind_count + 1
    #print("spin" + str(wind_count))

# Calculate the wind speed
def calculate_speed(time_sec):
    global wind_count
    global gust
    circumference_cm = (2 * math.pi) * radius_cm
    rotations = wind_count / 2.0
    
    # Calculate distance travelled by a cup (in km)
    dist_km = (circumference_cm * rotations) / CM_IN_A_KM
    dist_mi = dist_km * 0.62137 # Convert km to mi
    
    # Speed = distance / time
    km_per_sec = dist_km / time_sec
    km_per_hour = km_per_sec * SECS_IN_AN_HOUR
    
    mi_per_sec = dist_mi / time_sec
    mi_per_hour = mi_per_sec * SECS_IN_AN_HOUR
    
    final_speed_km = km_per_hour * ADJUSTMENT # Calibration factor for Argent anemometer
    final_speed_mph = mi_per_hour * ADJUSTMENT
    
    return final_speed_mph


def bucket_tipped():
    global rain_count
    rain_count += 1

def reset_rainfall():
    global rain_count
    rain_count = 0

def reset_wind():
    global wind_count
    wind_count = 0
    
def reset_gust():
    global gust
    gust = 0
    
# Celsius to Fahrenheit conversion
def c2f(tempc):
    tempf = round((9.0 / 5.0 * tempc + 32.0), 2)
    return tempf

# Fahrenheit to Celsius conversion
def f2c(tempf):
    tempc = round(((tempc - 32.0) * 5.0/9.0),2)
    return tempc

# mm to inches conversion
def mm2in(mmrain):
    inrain = round(mmrain / 25.4, 2)
    return inrain

# returns temp of RPi CPU in fahrenheit
def cpu_temp():
    cpu = CPUTemperature()
    # cpu.temperature returns temp in celsius
    return c2f(cpu.temperature)

wind_speed_sensor = Button(5) # pin 5
rain_sensor = Button(6) # pin 6

wind_speed_sensor.when_pressed = spin
rain_sensor.when_pressed = bucket_tipped
temp_probe = ds18b20_therm.DS18B20()

db = database.weather_database()

print('Begin weather measurment at {} min intervals...'.format(interval/60))
print('{} {:^6} {:^5} {:^6} {:^6} {:^6} {:^6} {:^4} {:^6} {:^7} {:^6} {:^5} {:^6}'.format(time.strftime("%m/%d/%y, %H:%M:%S"),'wdir','wspd','wgst','wchl','hidx','dewp','rnfl','humd','press','temp','gtmp','cpu'))

# Loop to measure wind speed and report at 5-minute intervals
while True:
    start_time = time.time()
    while time.time() - start_time <= interval:
        wind_start_time = time.time()
        reset_wind()
##        time.sleep(wind_interval)
        while time.time() - wind_start_time <= wind_interval:
            store_directions.append(wind_direction.get_value())
            
        final_speed = calculate_speed(wind_interval)
        store_speeds.append(final_speed)
    
    wind_average = round(wind_direction.get_average(store_directions), 2) # direction in degrees
    if wind_average >= 360:
        wind_average -= 360
    
    wind_gust = round(max(store_speeds), 2) # mph
    wind_speed = round(statistics.mean(store_speeds), 2) # mph
    rainfall = rain_count * BUCKET_SIZE # mm rain
    
    # reset rain and wind
    reset_rainfall()
    store_speeds = []
    store_directions = []
    
    ground_temp = temp_probe.read_temp() # deg Celsius
    humidity, pressure, ambient_temp = bme280_sensor.read_all() # ambient temp in deg Celsius
    wchill = weather_math.wind_chill(c2f(ambient_temp),wind_speed) # deg fahrenheit
    hidx = weather_math.heat_index(ambient_temp, humidity) # deg Celsius
    dewpt_c = weather_math.dewPoint_c(humidity, ambient_temp) # deg Celsius
    rpi_temp = round(cpu_temp(), 2) # RPi cpu temp in Fahrenheit
    
##  w_dir w_spd w_gust wchill heatidx dewpt rain hum prsr a_temp g_temp time
    print('{} {:^6} {:^5} {:^6} {:^6} {:^6} {:^6} {:^4} {:^6} {:^7} {:^6} {:^5} {:^6}'.format(time.strftime("%m/%d/%y, %H:%M:%S"), wind_average, wind_speed, wind_gust, wchill, c2f(hidx), c2f(dewpt_c), round(mm2in(rainfall), 2), humidity, pressure, c2f(ambient_temp), c2f(ground_temp), rpi_temp))
    db.insert(c2f(ambient_temp), c2f(ground_temp), 0, pressure, humidity, wind_average, wind_speed, wind_gust, wchill, c2f(hidx), c2f(dewpt_c), round(mm2in(rainfall), 2), rpi_temp)#, time.strftime("%Y-%m-%d %H:%M:%S"))
    
