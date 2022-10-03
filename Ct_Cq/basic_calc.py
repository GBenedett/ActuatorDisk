# Calculation without correction
from math import pi, atan
import numpy as np
import matplotlib.pyplot as plt

from velocity_correction import velocity_corr

delta_thrust = np.array([])
advanced_ratio = np.array([])
vloc = np.array([])
thrust_coefficient_dr = np.array([])
total_thrust_coefficient = np.array([])

# Input

radius = 0.8  # [m]
rho = 1.225  # [kg/m^3]
free_stream_velocity = 60  # [m/s]
n_step = 10
chord = 0.1  # [m]
pitch = 9
rpm = 2100
blade_numbers = 2

# prelimanary calculation
r_hub = 0.1 * radius
r_tip = radius
r_step = (r_tip - r_hub) / n_step
step_vector = np.arange(r_hub, (r_tip + 0.01), r_step)
n = rpm / 60
omega = 2 * pi * n

# calculation

for i in range(len(step_vector + 1)):

    blade_thrust = 0.0
    blade_torque = 0.0

    dr = step_vector[i]
    theta = atan(pitch / 2 / pi / dr)

    a = 0.1
    b = 0.01

    dT, dQ, local_velocity = velocity_corr(
        free_stream_velocity, a, b, omega, dr, theta, rho, blade_numbers, chord
    )

    blade_thrust += dT * r_step
    blade_torque += dQ * r_step

    delta_thrust = np.append(delta_thrust, dT)
    # print(delta_thrust)

    thrust_coefficient_dr = np.append(
        thrust_coefficient_dr, dT / (rho * n**2 * (2 * radius) ** 4)
    )

    total_thrust_coefficient = np.append(
        total_thrust_coefficient, blade_thrust / (rho * n**2 * (2 * radius) ** 4)
    )

    # local power
    dP = dT * local_velocity

    power_coefficient = dP / (rho * n**2 * (2 * radius) ** 4)

vel = np.array([50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60])
advanced_ratio = np.append(advanced_ratio, vel / (n * 2 * radius))

plt.subplot(2, 2, 1)
plt.suptitle(
    "Thrust and thrust coeffient in function of x/r",
    fontweight="bold",
    size=13,
)

plt.plot(step_vector, delta_thrust)
plt.title("dT vs x/r")
plt.xlabel("x/r")
plt.ylabel("dT")

plt.subplot(2, 2, 2)
plt.plot(step_vector, thrust_coefficient_dr)
plt.title("thrust_coefficient(r) vs x/r")
plt.xlabel("x/r")
plt.ylabel("thrust_coefficient")
#
# plt.subplot(2, 2, 3)
# plt.plot(step_vector, dP)
# plt.title("dP vs x/r")
# plt.xlabel("x/r")
# plt.ylabel("dP")
#
# plt.subplot(2, 2, 4)
# plt.plot(step_vector, thrust_coefficient)
# plt.title("power_coefficient vs x/r")
# plt.xlabel("x/r")
# plt.ylabel("power_coefficient")

plt.tight_layout(pad=1.2)

plt.show()


plt.plot(advanced_ratio, total_thrust_coefficient)
plt.title("thrust_coefficient vs advanced ratio")
plt.xlabel("advance_ratio")
plt.ylabel("thrust_coefficient")
plt.show()

"""plt.plot(step_vector, vloc)
plt.title("local velocity vs x/r")
plt.xlabel("x/r")
plt.ylabel("local velocity")
plt.show()"""
