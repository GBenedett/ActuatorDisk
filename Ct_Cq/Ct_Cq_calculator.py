## Ct and Cq calculator ##

# chord length of blade assumed costant with radius
from math import atan, pi

import numpy as np
import pandas as pd

from fun_velocity_correction import velocity_correction
from fun_initialization import init_calc
from fun_plot import plot_function

## initializations
thrust_coefficient = np.empty(61)
torque_coefficent = np.empty(61)
advanced_ratio = np.empty(61)
efficiency = np.array([])

df = pd.read_csv("input_data.csv", skiprows=1)

chord, pitch, diameter, rpm, rho, blade_numbers, v_max = df.iloc[:, 1]

r_hub, r_tip, steps_vector, r_step, omega, n = init_calc(diameter, rpm)

# velocity step
for v in range(1, int(v_max + 1)):
    thrust = 0.0
    torque = 0.0
    for j in range(len(steps_vector + 1)):
        rad = steps_vector[j]
        # calculate local blade element setting angle
        theta = atan(pitch / 2 / pi / rad)

        solidity = 2 * chord / 2 / pi / rad
        # guess initial value of inflow and swirl factor
        a = 0.1
        b = 0.01

        DtDr, DqDr, local_velocity = velocity_correction(
            a, b, v, omega, rad, theta, rho, blade_numbers, chord
        )

        thrust += DtDr * r_step
        torque += DqDr * r_step

        thrust_coefficient[v] = thrust / (rho * n**2 * diameter**4)
        torque_coefficent[v] = torque / (rho * n**2 * diameter**5)
        advanced_ratio[v] = v / (n * diameter)

        print(local_velocity)

torque_coefficent = np.delete(torque_coefficent, 0)
thrust_coefficient = np.delete(thrust_coefficient, 0)
advanced_ratio = np.delete(advanced_ratio, 0)

efficiency = np.append(
    efficiency, advanced_ratio / 2.0 / pi * thrust_coefficient / torque_coefficent
)

advanced_ratio_max = max(advanced_ratio)
thrust_max = max(thrust_coefficient)

plot_function(
    advanced_ratio, thrust_coefficient, torque_coefficent, thrust_max, efficiency
)
