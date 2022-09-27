## Ct and Cq calculator ##

# chord length of blade assumed costant with radius
from math import atan, pi

import matplotlib.pyplot as plt
import numpy as np

from function_vel import convergence
from initialization import init_calc

## initializations
thrust_coefficient = np.empty(61)
torque_coefficent = np.empty(61)
advanced_ratio = np.empty(61)
efficiency = np.array([])

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
    thrust_coefficient[v] = thrust / (rho * n**2 * diameter**4)
    torque_coefficent[v] = torque / (rho * n**2 * diameter**5)
    advanced_ratio[v] = v / (n * diameter)
thrust_coefficient = np.delete(thrust_coefficient, 0)
torque_coefficent = np.delete(torque_coefficent, 0)
print(advanced_ratio)
advanced_ratio = np.delete(advanced_ratio, 0)

efficiency = np.append(
    efficiency, advanced_ratio / 2.0 / pi * thrust_coefficient / torque_coefficent
)
efficiency[[efficiency <= 0] and [efficiency > 1]] = -1

advanced_ratio_max = max(advanced_ratio)
thrust_max = max(thrust_coefficient)

plt.figure(figsize=(7, 8))

plt.subplot(2, 1, 1)
plt.suptitle("Thrust coefficent, torque coeffcient and propeller efficiency")
plt.plot(advanced_ratio, thrust_coefficient, label="Ct")
plt.plot(advanced_ratio, torque_coefficent, label="Cq")
plt.xlim(0, 0.65)
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
plt.xlim(0, 0.65)
plt.ylim(0, 1)


plt.tight_layout(pad=1.2)
plt.show()
