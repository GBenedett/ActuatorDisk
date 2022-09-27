## Ct and Cq calculator ##

# chord length of blade assumed costant with radius
from math import atan, pi

import matplotlib.pyplot as plt
import numpy as np

from function_vel import convergence
from initialization import init_calc

import pandas as pd

## initializations
thrust_coefficient = np.array([])
torque_coefficent = np.array([])
advanced_ratio = np.array([])
efficiency = np.array([])
v = np.array([])

# input
chord = 0.10  # [m]
pitch = 1.0  # [m]
diameter = 1.6  # [m]
rpm = 2100
rho = 1.225  # [kg/m^2]
blade_numbers = 2
v_max = 60

xs, xt, r1, rstep, omega, n = init_calc(diameter, rpm)

# velocity step
for v in range(1, v_max + 1):
    thrust = 0.0
    torque = 0.0
    for j in range(len(r1 + 1)):
        rad = r1[j]
        # calculate local blade element setting angle
        theta = atan(pitch / 2 / pi / rad)

        solidity = 2 * chord / 2 / pi / rad
        # guess initial value of inflow and swirl factor
        a = 0.1
        b = 0.01
        DtDr, DqDr = convergence(a, b, v, omega, rad, theta, rho, blade_numbers, chord)

        thrust += DtDr * rstep
        torque += DqDr * rstep

    thrust_coefficient = np.append(
        thrust_coefficient, thrust / (rho * n**2 * diameter**4)
    )
    torque_coefficent = np.append(
        torque_coefficent, torque / (rho * n**2 * diameter**5)
    )
    advanced_ratio = np.append(advanced_ratio, v / (n * diameter))

efficiency = np.append(
    efficiency, advanced_ratio / 2.0 / pi * thrust_coefficient / torque_coefficent
)
advanced_ratio_max = max(advanced_ratio)
thrust_max = max(thrust_coefficient)

plt.figure(figsize=(6, 9))

plt.subplot(2, 1, 1)
plt.plot(advanced_ratio, thrust_coefficient, label="Ct")
plt.plot(advanced_ratio, torque_coefficent, label="Cq")
plt.xlim(0, advanced_ratio_max)
plt.ylim(0, 1.1 * thrust_max)
plt.title("Thrust and Torque Coefficients")
plt.xlabel("Advance Ratio (J)")
plt.ylabel("Ct, Cq")
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(advanced_ratio, efficiency)
plt.title("Propeller Efficiency")
plt.xlabel("Advance Ratio (J)")
plt.ylabel("Efficiency")
plt.xlim(0, advanced_ratio_max)
plt.ylim(0, 1)


plt.tight_layout(pad=1.2)
plt.show()
