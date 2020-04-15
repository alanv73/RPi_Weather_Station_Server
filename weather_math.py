from urllib.request import urlopen
import re
import bme280_sensor
import math
from heatindex import heat_index

def seaLevelPressure_hPa(location):
    found = []

    URL="http://www.ogimet.com/display_metars2.php?lang=en&lugar="+ location + "&tipo=SA&ord=REV&nil=SI&fmt=html&send=send"
    f = urlopen(URL)
    data = f.read()

    r=re.compile('<pre>([^<]*)')
    found=r.findall(str(data))

    found=found[0].split()
    
    if any('SLP' in item for item in found):
        r=re.compile(".*SLP")
        metarslp=list(filter(r.match,found))
        slp=int('10' + metarslp[0][3:])/10.0
        return slp
    else:
        return False

def pressure_inHg(pressure_hPa):
    return pressure_hPa * 0.02953

def altitude_ft(pressure_hPa, slPressure_hPa):
    alt_ft = (1.0-(pressure_hPa/slPressure_hPa)**0.190284)*145366.45
    return round(alt_ft, 2)

def dewPoint_c(humidity_pcnt, temp_c):
    dewpc = 243.04*((math.log(humidity_pcnt/100))+((17.625*temp_c)/(243.04+temp_c)))/(17.625-(math.log(humidity_pcnt/100))-((17.625*temp_c)/(243.04+temp_c)))
    return round(dewpc, 2)

def c2f(tempc):
    tempf = round((9.0 / 5.0 * tempc + 32.0), 2)
    return tempf

def f2c(tempf):
    tempc = round(((tempc - 32.0) * 5.0/9.0),2)
    return tempc
    
def wind_chill(tempf, windspd_mph):

    if tempf >= 70.0 and windspd_mph <= 3.0:
        windchill = tempf - 1.5 * windspd_mph
    else:
        windchill = 35.74 + (0.6215*tempf) - 35.75*(windspd_mph**0.16) + 0.4275*tempf*(windspd_mph**0.16)
    
    return round(windchill, 2)

def avg_val(num_list):
    sum = 0
    for number in num_list:
        sum += number
    avg = sum / len(num_list)
    return avg

if __name__ == "__main__":
    slp = seaLevelPressure_hPa('kmdt')
    humidity, pressure_hPa, ambient_tempc = bme280_sensor.read_all()
    dpc = dewPoint_c(humidity,ambient_tempc)

    if slp:
        elevation_ft = altitude_ft(pressure_hPa,slp)
    else:
        elevation_ft = 'n/a'
        
    phg = pressure_inHg(pressure_hPa)
    phg = round(phg,2)
    pressure_hPa = round(pressure_hPa,2)
    ambient_tempc = round(ambient_tempc,2)
    humidity = round(humidity,2)
    hidxc = heat_index(ambient_tempc,humidity)
##    print(avg_val(hidxc), avg_val(hidxf), c2f(avg_val(hidxc)))
    print('barometer: %s hPa, %s inHg\n\
pressure @ sea level: %s hPa %s inHg\n\
elevation: %s ft\n\
temp: %s c, %s F\n\
humidity: %s %%\n\
heat index: %s C %s F \n\
dewpoint: %s c, %s F' % (pressure_hPa,phg,
slp,round(pressure_inHg(slp),2),
elevation_ft,
ambient_tempc,c2f(ambient_tempc),
humidity,
hidxc,c2f(hidxc),
dpc,c2f(dpc)))

