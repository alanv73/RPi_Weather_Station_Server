#!/usr/bin/python

def heat_index(tempc, hum_pcnt):
    # Returns HeatIndexC
    
    # Convert celius to fahrenheit (heat-index is only fahrenheit compatible)
    fahrenheit = ((tempc * 9.0/5.0) + 32.0)

    # Creating multiples of 'fahrenheit' & 'hum' values for the coefficients
    T2 = pow(fahrenheit, 2)
    T3 = pow(fahrenheit, 3)
    hum = hum_pcnt
    H2 = pow(hum_pcnt, 2)
    H3 = pow(hum_pcnt, 3)

    # Coefficients for the calculations
    C1 = [ -42.379, 2.04901523, 10.14333127, -0.22475541, -6.83783e-03, -5.481717e-02, 1.22874e-03, 8.5282e-04, -1.99e-06]
    C2 = [ 0.363445176, 0.988622465, 4.777114035, -0.114037667, -0.000850208, -0.020716198, 0.000687678, 0.000274954, 0]
    C3 = [ 16.923, 0.185212, 5.37941, -0.100254, 0.00941695, 0.00728898, 0.000345372, -0.000814971, 0.0000102102, -0.000038646, 0.0000291583, 0.00000142721, 0.000000197483, -0.0000000218429, 0.000000000843296, -0.0000000000481975]

    # Calculating heat-indexes with 3 different formula

    heatindexF = []

    heatindexF.append(C1[0] + (C1[1] * fahrenheit) + (C1[2] * hum) + (C1[3] * fahrenheit * hum) + (C1[4] * T2) + (C1[5] * H2) + (C1[6] * T2 * hum) + (C1[7] * fahrenheit * H2) + (C1[8] * T2 * H2))
    heatindexF.append(C2[0] + (C2[1] * fahrenheit) + (C2[2] * hum) + (C2[3] * fahrenheit * hum) + (C2[4] * T2) + (C2[5] * H2) + (C2[6] * T2 * hum) + (C2[7] * fahrenheit * H2) + (C2[8] * T2 * H2))
    heatindexF.append(C3[0] + (C3[1] * fahrenheit) + (C3[2] * hum) + (C3[3] * fahrenheit * hum) + (C3[4] * T2) + (C3[5] * H2) + (C3[6] * T2 * hum) + (C3[7] * fahrenheit * H2) + (C3[8] * T2 * H2) + (C3[9] * T3) + (C3[10] * H3) + (C3[11] * T3 * hum) + (C3[12] * fahrenheit * H3) + (C3[13] * T3 * H2) + (C3[14] * T2 * H3) + (C3[15] * T3 * H3))

    heatindexC = []

    for heatindex in range(len(heatindexF)):
        heatindexC.append(round(((heatindexF[heatindex] - 32.0) * 5.0/9.0), 2))
        heatindexF[heatindex] = round(heatindexF[heatindex],2)
    
    return heatindexC[1]

if __name__ == "__main__":
    print("\nHeat-Index calculator v0.1\n")

    # Ask for the current temperature in celsius-grade...
    t = float(input('Temperature(*C): '))
    # ...then wait for the relative humidity in % value
    h = float(input('Humidity(%): '))
    print("\nThe Heat index or the feels-like temperature is:")

    heatindexC=heat_index(t,h)

    print("%s *C" % (heatindexC)),
