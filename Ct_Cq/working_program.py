from math import atan, pi

import numpy as np
import pandas as pd

from fplot import plot_function
from initialization import init_calc
from velocity_correction import velocity_corr

## initializations
total_thrust_coefficient = np.empty(61)
total_torque_coefficent = np.empty(61)
total_power_coefficient = np.empty(61)
advanced_ratio = np.empty(61)
efficiency = np.array([])
local_thrust_coefficient = np.array([])
local_power_coefficient = np.array([])

df = pd.read_csv("input_data.csv", skiprows=1)
(
    chord,
    pitch_length,
    radius,
    rpm,
    rho,
    n_steps,
    blade_numbers,
    free_stream_velocity_max,
) = df.iloc[:, 1]

r_hub, r_tip, steps_vector, r_step, omega, n, diameter = init_calc(radius, rpm, n_steps)

# velocity step
for v in range(1, int(free_stream_velocity_max + 1)):

    blade_thrust = 0.0
    blade_torque = 0.0
    blade_power = 0.0

    for i in range(len(steps_vector + 1)):
        dr = steps_vector[i]
        # calculate local blade element setting angle
        theta = atan(pitch_length / (2 * pi * dr))

        solidity = 2 * chord / (2 * pi * dr)

        # guess initial value of inflow and swirl factor
        a = 0.1
        b = 0.01

        dT, dQ, dP, local_velocity = velocity_corr(
            v, a, b, omega, dr, theta, rho, blade_numbers, chord
        )

        blade_thrust += dT * r_step
        blade_torque += dQ * r_step
        blade_power += dP * r_step

        total_thrust_coefficient[v] = blade_thrust / (rho * n**2 * diameter**4)
        total_torque_coefficent[v] = blade_torque / (rho * n**2 * diameter**5)
        total_power_coefficient[v] = blade_power / (rho * n**3 * diameter**5)
        advanced_ratio[v] = v / (n * diameter)

    local_thrust_coefficient = np.append(
        local_thrust_coefficient, dT / (rho * n**2 * diameter**4)
    )

    print(local_thrust_coefficient)

    local_power_coefficient = np.append(
        local_power_coefficient, dP / (rho * n**2 * diameter**5)
    )

total_torque_coefficent = np.delete(total_torque_coefficent, 0)
total_thrust_coefficient = np.delete(total_thrust_coefficient, 0)
total_power_coefficient = np.delete(total_power_coefficient, 0)
advanced_ratio = np.delete(advanced_ratio, 0)

efficiency = np.append(
    efficiency,
    advanced_ratio / 2.0 / pi * total_thrust_coefficient / total_torque_coefficent,
)

advanced_ratio_max = max(advanced_ratio)
thrust_max = max(total_thrust_coefficient)

plot_function(
    advanced_ratio,
    total_thrust_coefficient,
    total_torque_coefficent,
    total_power_coefficient,
    thrust_max,
    efficiency,
    advanced_ratio_max,
    local_thrust_coefficient,
    local_power_coefficient,
    steps_vector,
    radius,
)
