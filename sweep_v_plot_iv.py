import matplotlib.pyplot as plt
import numpy as np
from electronic_circuits.circuits import MeasuringCircuit
from electronic_circuits.components import Resistor
from scipy.stats import linregress

component = Resistor()
circuit = MeasuringCircuit(component)

generator = circuit.generator
voltmeter = circuit.voltmeter
ammeter = circuit.ammeter

voltages = []
currents = []

for voltage in np.arange(-5, 6):
    generator.set_voltage(voltage)

    measured_voltage = voltmeter.measure()
    measured_current = ammeter.measure()

    voltages.append(measured_voltage)
    currents.append(measured_current)


# Compute resistance through linear regression
result = linregress(x=currents, y=voltages)
resistance = result.slope
bias = result.intercept
resistance_std = result.stderr
bias_std = result.intercept_stderr

# Convert resistance and error bar into plottable values
resistance_value_str, resistance_magnitude_str = f"{resistance:.2e}".split("e")
error_bar_str = f"{resistance_std / (10 ** int(resistance_magnitude_str)):.2f}"

# Useful parameters for clean plot
abscissa = np.arange(-10, 10)

min_v = min(voltages)
max_v = max(voltages)
amp_v = max_v - min_v
plot_x_limits = [min_v - 0.1 * amp_v, max_v + 0.1 * amp_v]

min_c = min(currents)
max_c = max(currents)
amp_c = max_c - min_c
plot_y_limits = [min_c - 0.1 * amp_c, max_c + 0.1 * amp_c]

# Plot the measurements
plt.errorbar(voltages, currents, xerr=0.1 * np.ones(len(voltages)), yerr=5e-4 * np.ones(len(currents)), fmt="o")

# Plot the regression
plt.plot(abscissa, (abscissa - bias) / resistance, zorder=0)
plt.fill_between(abscissa, y1=(abscissa - bias + bias_std) / (resistance - resistance_std), y2=(abscissa - bias - bias_std) / (resistance + resistance_std), zorder=0, alpha=0.5, color="tab:orange")

# Configure display
plt.title(f"I-C curve of the resistor (R = {resistance_value_str} +/- {error_bar_str} x 10^{resistance_magnitude_str})")
plt.xlabel("Voltage (V)")
plt.ylabel("Current (A)")
plt.xlim(plot_x_limits)
plt.ylim(plot_y_limits)

# Tell python to show the figure
plt.show()
