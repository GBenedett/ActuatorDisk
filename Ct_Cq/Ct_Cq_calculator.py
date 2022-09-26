## Ct and Cq calculator ##

# chord length of blade assumed costant with radius
from array import array
from cProfile import label
from calendar import c
from math import atan, cos, e, pi, sin, sqrt
from math import atan2
import matplotlib.pyplot as plt
import numpy as np

# initializations
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


## Calculation

radius = diameter / 2.0
tickness_chord_ratio = 0.12 * chord
n = rpm / 60
omega = n * 2.0 * pi

# use 10 blade segments (starting a 10%R to R)
xs = 0.1 * radius
xt = radius
rstep = (xt - xs) / 10
r1 = np.arange(xs, (xt + 0.01), rstep)

# velocity step
for v in range(1, 61):
    thrust = 0.0
    torque = 0.0
    for j in range(len(r1 + 1)):
        rad = r1[j]
        # calculate local blade element setting angle
        theta = atan(pitch / 2 / pi / rad)
        # calculate solidity
        sigma = 2 * chord / 2 / pi / rad
        # guess initial value of inflow and swirl factor
        a = 0.1
        b = 0.01
        finished = False
        sum = 1
        while not finished:
            axial_inflow_velocity = v * (1 + a)
            angular_inflow_velocity = omega * rad * (1 - b)
            # flow angle
            phi = atan2(float(axial_inflow_velocity), float(angular_inflow_velocity))
            # blade angle of attack
            alpha = theta - phi
            cl = 6.2 * alpha
            cd = 0.008 - 0.003 * cl + 0.01 * cl**2
            local_velocity = sqrt(
                axial_inflow_velocity**2 + angular_inflow_velocity**2
            )
            # thrust grading
            DtDr = (
                0.5
                * rho
                * local_velocity**2
                * blade_numbers
                * chord
                * (cl * cos(phi) - cd * sin(phi))
            )
            # torque grading
            DqDr = (
                0.5
                * rho
                * local_velocity**2
                * blade_numbers
                * chord
                * rad
                * (cd * cos(phi) + cl * sin(phi))
            )
            # momentum conservation check
            axial_momentum = DtDr / (4 * pi * rad * rho * v**2 * (1 + a))
            angular_momentum = DqDr / (4 * pi * rad**3 * rho * v * (1 + a) * omega)
            # stabilise iteration
            anew = 0.5 * (a + axial_momentum)
            bnew = 0.5 * (b + angular_momentum)

            # check for convergence
            if abs(anew - a) < 1e-5:
                if abs(bnew - b) < 1e-5:
                    finished == True

            a = anew
            b = bnew

            sum = sum + 1

            if sum > 500:
                finished = True

        thrust = thrust + DtDr * rstep
        torque = torque + DqDr * rstep
        finished = True

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

plt.plot(advanced_ratio, thrust_coefficient, label="Ct")
plt.plot(advanced_ratio, torque_coefficent, label="Cq")
plt.xlim(0, advanced_ratio_max)
plt.ylim(0, 1.1 * thrust_max)

plt.title("Thrust and Torque Coefficients")
plt.xlabel("Advance Ratio (J)")
plt.ylabel("Ct, Cq")
plt.legend()
plt.show()

plt.plot(advanced_ratio, efficiency)
plt.title("Propeller Efficiency")
plt.xlabel("Advance Ratio (J)")
plt.ylabel("Efficiency")
plt.xlim(0, advanced_ratio_max)
plt.ylim(0, 1)
plt.show()
