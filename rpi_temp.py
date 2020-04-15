from gpiozero import CPUTemperature

cpu = CPUTemperature()
tempc = round(cpu.temperature, 2)
tempf = round((9.0 / 5.0 * tempc + 32.0), 2)

# \u unicode 00b0 unicode for °
print('cpu temp: %3.2f\u00b0C\t %3.2f\u00b0F' % (tempc, tempf))
