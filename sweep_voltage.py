import numpy as np
from electronic_circuits.circuits import MeasuringCircuit
from electronic_circuits.components import Resistor

component = Resistor()
circuit = MeasuringCircuit(component)

generator = circuit.generator
voltmeter = circuit.voltmeter
ammeter = circuit.ammeter

for voltage in np.arange(-5, 6):
    generator.set_voltage(voltage)

    measured_voltage = voltmeter.measure()
    measured_current = ammeter.measure()

    print(measured_voltage, measured_current)
