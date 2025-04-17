import matplotlib.pyplot as plt
import numpy as np
from electronic_circuits.circuits import MeasuringCircuit
from electronic_circuits.components import Thermistor
from electronic_circuits.environment_control import TemperatureControlledChamber
from scipy.stats import linregress


def sweep_voltage(circuit):
    voltages = []
    currents = []

    for voltage in np.arange(-5, 6):
        circuit.generator.set_voltage(voltage)

        measured_voltage = circuit.voltmeter.measure()
        measured_current = circuit.ammeter.measure()

        voltages.append(measured_voltage)
        currents.append(measured_current)
    return voltages, currents


def measure_resistance(voltages, currents):
    result = linregress(x=currents, y=voltages)
    return result.slope


def plot_iv_curve(ax, temperature, voltages, currents):
    resistance = measure_resistance(voltages, currents)

    # Useful parameters for clean plot
    min_v = min(voltages)
    max_v = max(voltages)
    amp_v = max_v - min_v
    plot_x_limits = [min_v - 0.1 * amp_v, max_v + 0.1 * amp_v]

    min_c = min(currents)
    max_c = max(currents)
    amp_c = max_c - min_c
    plot_y_limits = [min_c - 0.1 * amp_c, max_c + 0.1 * amp_c]

    # Plot the measurements
    ax.errorbar(voltages, currents, xerr=0.1 * np.ones(len(voltages)), yerr=5e-4 * np.ones(len(currents)), fmt="-o", label=f"T = {temperature:.0f} K, R = {resistance:.0f} Ohm")

    # Configure display
    ax.set_title("I-C curve of the thermistor")
    ax.set_xlabel("Voltage (V)")
    ax.set_ylabel("Current (A)")
    ax.set_xlim(plot_x_limits)
    ax.set_ylim(plot_y_limits)
    ax.legend(loc="best")


def plot_rt_curve(ax, temperatures, resistances):
    ax.scatter(temperatures, resistances)
    ax.set_xlabel("Temperature (K)")
    ax.set_ylabel("Resistance (Ohm)")
    ax.set_title("R(T) relation")


if __name__ == "__main__":
    component = Thermistor()
    circuit = MeasuringCircuit(component)
    chamber = TemperatureControlledChamber(circuit)

    fig, (ax1, ax2) = plt.subplots(1, 2)

    temperatures = []
    resistances = []
    for temperature in np.arange(270, 300, step=5):
        chamber.set_temperature(temperature)
        voltages, currents = sweep_voltage(circuit)

        plot_iv_curve(ax1, temperature, voltages, currents)

        temperatures.append(temperature)
        resistances.append(measure_resistance(voltages, currents))

    plot_rt_curve(ax2, temperatures, resistances)

    # Tell python to show the figure
    plt.show()
