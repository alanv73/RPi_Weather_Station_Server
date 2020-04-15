from gpiozero import Button
import time, math, statistics

store_speeds = []
wind_count = 0 # Counts how many half rotations
radius_cm = 9.0 # Radius of your anemometer
wind_interval = 5 # How often (secs) to report speed
CM_IN_A_KM = 100000.0
SECS_IN_AN_HOUR = 3600
ADJUSTMENT = 1.18

# Every half-rotation, add 1 to count
def reset_wind():
    global wind_count
    wind_count = 0
    
def spin():
    global wind_count
    wind_count = wind_count + 1
    #print("spin" + str(wind_count))

# Calculate the wind speed
def calculate_speed(time_sec):
    global wind_count
    circumference_cm = (2 * math.pi) * radius_cm
    rotations = wind_count / 2.0
    
    # Calculate distance travelled by a cup (in km)
    dist_km = (circumference_cm * rotations) / CM_IN_A_KM
    dist_mi = dist_km * 0.62137 # Convert km to mi
    
    km_per_sec = dist_km / time_sec
    km_per_hour = km_per_sec * SECS_IN_AN_HOUR
    
    mi_per_sec = dist_mi / time_sec
    mi_per_hour = mi_per_sec * SECS_IN_AN_HOUR
    
    km_per_hour *= ADJUSTMENT # Calibration factor for Argent anemometer
    mi_per_hour *= ADJUSTMENT
    
    return mi_per_hour


wind_speed_sensor = Button(5)
wind_speed_sensor.when_pressed = spin

# Loop to measure wind speed and report at 5-second intervals
while True:
    start_time = time.time()
    while time.time() - start_time <= wind_interval:
        reset_wind()
        time.sleep(wind_interval)
        final_speed = calculate_speed(wind_interval)
        store_speeds.append(final_speed)
    
    wind_gust = max(store_speeds)
    wind_speed = statistics.mean(store_speeds[-(wind_interval-1):])
    print(wind_speed, wind_gust)
##    wind_count = 0
##    time.sleep(wind_interval)
##    print( calculate_speed(wind_interval), "mph")
    
