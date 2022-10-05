# Calculation without correction
from math import pi
import numpy as np
import matplotlib.pyplot as plt

from velocity_correction import velocity_corr

delta_thrust = np.array([])
advanced_ratio = np.array([])
vloc = np.array([])
local_thrust_coefficient = np.array([])
total_thrust_coefficient = np.array([])

# Input

radius = 1  # [m]
rho = 1.225  # [kg/m^3]
free_stream_velocity = 160  # [m/s]
n_step = 10
chord = 0.1  # [m]
theta = 10
# pitch = 1
rpm = 1900
blade_numbers = 2

# prelimanary calculation
r_hub = 0.1 * radius
r_tip = radius
r_step = (r_tip - r_hub) / n_step
steps_vector = np.arange(r_hub, (r_tip + 0.01), r_step)
n = rpm / 60
omega = 2 * pi * n
advanced_ratio = free_stream_velocity / (n * radius * 2)
print(advanced_ratio)

# calculation

for i in range(len(steps_vector + 1)):

    blade_thrust = 0.0
    blade_torque = 0.0

    dr = steps_vector[i]

    a = 0.1
    b = 0.01

    dT, dQ, dP, local_velocity = velocity_corr(
        free_stream_velocity, a, b, omega, dr, theta, rho, blade_numbers, chord
    )

    blade_thrust += dT * r_step
    blade_torque += dQ * r_step

local_thrust_coefficient = np.append(
    local_thrust_coefficient,
    dT / (0.5 * rho * local_velocity**2 * 2 * pi * steps_vector),
)

# total_thrust_coefficient = np.append(
#    total_thrust_coefficient, blade_thrust / (rho * n**2 * (2 * radius) ** 4)
# )

# local power
dP = dT * local_velocity

power_coefficient = dP / (rho * n**2 * (2 * radius) ** 4)

# vel = np.array([50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60])
# advanced_ratio = np.append(advanced_ratio, vel / (n * 2 * radius))

# plt.subplot(2, 2, 1)
# plt.suptitle(
#    "Thrust and thrust coeffient in function of x/r",
#    fontweight="bold",
#    size=13,
# )
#
# plt.plot(steps_vector, delta_thrust)
# plt.title("dT vs x/r")
# plt.xlabel("x/r")
# plt.ylabel("dT")
#
# plt.subplot(2, 2, 2)

plt.plot(steps_vector, local_thrust_coefficient)
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


# plt.plot(advanced_ratio, total_thrust_coefficient)
# plt.title("thrust_coefficient vs advanced ratio")
# plt.xlabel("advance_ratio")
# plt.ylabel("thrust_coefficient")
# plt.show()
#
# plt.plot(step_vector, vloc)
# plt.title("local velocity vs x/r")
# plt.xlabel("x/r")
# plt.ylabel("local velocity")
# plt.show()
