from urllib.request import urlopen
import re
import bme280_sensor
import math

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

slp = seaLevelPressure_hPa('kmdt')
humidity, pressure_hPa, ambient_tempc = bme280_sensor.read_all()
dpc=dewPoint_c(humidity,ambient_tempc)
elevation_ft = altitude_ft(pressure_hPa,slp)
phg=pressure_inHg(pressure_hPa)
phg=round(phg,2)
pressure_hPa=round(pressure_hPa,2)
ambient_tempc=round(ambient_tempc,2)
humidity=round(humidity,2)
print('elevation: %s ft\tbarometer: %s hPa, %s inHg\ttemp: %s c, %s F\thumidity: %s %%\tdewpoint: %s c, %s F' % (elevation_ft,pressure_hPa,phg,ambient_tempc,c2f(ambient_tempc),humidity,dpc,c2f(dpc)))

