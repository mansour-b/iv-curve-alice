import numpy as np
from drivers import Ammeter, DCVoltageGenerator, Voltmeter

generator = DCVoltageGenerator()
voltmeter = Voltmeter()
ammeter = Ammeter()

for voltage in np.arange(-5, 6):
    generator.set_voltage(voltage)

    measured_voltage = voltmeter.measure()
    measured_current = ammeter.measure()

    print(measured_voltage, measured_current)
