from math import atan2, cos, pi, sin, sqrt

import matplotlib.pyplot as plt
import numpy as np

local_thrust = np.array([])
local_thrust_coefficient = np.array([])
alpha_f = np.array([])
phi_f = np.array([])
cd_f = np.array([])
cl_f = np.array([])
Ct2 = np.array([])
total_thrust_coefficient = np.array([])

# input

radius = 2.52  # [m]
rho = 1  # [kg/m^3]
free_stream_velocity = 231.5  # [m/s]
n_step = 10
chord_f = np.array(
    [0.18, 0.2, 0.22, 0.25, 0.28, 0.3, 0.3, 0.32, 0.31, 0.24, 0.15]
)  # [m]
theta_f = np.array([1.43, 1.35, 1.3, 1.25, 1.2, 1.15, 1.10, 1.05, 1.0, 0.95, 0.9])
rpm = 981
blade_numbers = 2

# prelimanary calculation
r_hub = 0.2 * radius
r_tip = radius
r_step = (r_tip - r_hub) / n_step
steps_vector = np.arange(r_hub, (r_tip + 0.01), r_step)
n = rpm / 60
omega = 2 * pi * n
advanced_ratio = free_stream_velocity / (n * radius * 2)
print(f"advanced ratio= {advanced_ratio}")

# calculation

for i in range(len(steps_vector + 1)):

    blade_thrust = 0.0

    dr = steps_vector[i]
    theta = theta_f[i]
    chord = chord_f[i]

    axial_velocity = free_stream_velocity
    rotational_velocity = omega * dr
    phi = atan2(float(axial_velocity), float(rotational_velocity))
    alpha = theta - phi
    cl = 2 * pi * alpha
    cd = 0.008 - 0.003 * cl + 0.01 * cl**2
    local_velocity = sqrt(axial_velocity**2 + rotational_velocity**2)
    dT = (
        0.5
        * rho
        * local_velocity**2
        * blade_numbers
        * chord
        * (cl * cos(phi) - cd * sin(phi))
    )

    phi_f = np.append(phi_f, phi)
    alpha_f = np.append(alpha_f, alpha)

    cd_f = np.append(cd_f, cd)
    cl_f = np.append(cl_f, cl)

    local_thrust = np.append(local_thrust, dT)

    local_thrust_coefficient = np.append(
        local_thrust_coefficient,
        dT / (0.5 * rho * local_velocity**2 * 2 * pi * dr),
    )

    # print(f"local thrust= {local_thrust}")

    total_thrust_coefficient = np.append(
        total_thrust_coefficient,
        blade_thrust / (rho * n**2 * (2 * radius) ** 4),
    )

plt.figure(figsize=(10, 8))

rs = np.array([0.2, 0.26, 0.36, 0.46, 0.55, 0.63, 0.71, 0.79, 0.87, 0.95, 1])
ct = np.array(
    [0.02, 0.024, 0.064, 0.136, 0.211, 0.291, 0.365, 0.427, 0.468, 0.435, 0.377]
)

plt.subplot(2, 1, 1)
plt.plot(steps_vector / radius, local_thrust, label="T_loc")
plt.plot(rs, ct * (0.5 * rho * local_velocity**2 * 2 * pi * dr), label="T_loc_Saetta")
plt.title("thrust(r) vs x/r")
plt.xlabel("x/r")
plt.ylabel("thrust")
plt.legend()
plt.grid()

plt.subplot(2, 1, 2)
plt.plot(steps_vector / radius, local_thrust_coefficient, label="Ct")
plt.plot(rs, ct, label="Ct_Saetta")
plt.title("thrust_coefficient(r) vs x/r")
plt.xlabel("x/r")
plt.ylabel("thrust_coefficient")
plt.legend()
plt.grid()

plt.tight_layout(pad=1)

plt.show()

plt.plot(steps_vector / radius, 180 * theta_f / pi, label="theta")
plt.plot(steps_vector / radius, 180 * alpha_f / pi, label="alpha")
plt.plot(steps_vector / radius, 180 * phi_f / pi, label="phi")
plt.title("angles")
plt.xlabel("dr")
plt.ylabel("theta, alpha, phi")
plt.grid()
plt.legend()
plt.show()

color = "grey"
plt.plot(steps_vector / radius, chord_f, color)
plt.plot(steps_vector / radius, -(chord_f), color)
plt.title("chord function")
plt.xlabel("dr")
plt.ylabel("chord")
plt.ylim(-0.9, 0.9)
plt.grid()
plt.show()

plt.plot(steps_vector / radius, cd_f, label="cd")
plt.plot(steps_vector / radius, cl_f, label="cl")
plt.title("cd and cl vs dr")
plt.xlabel("dr")
plt.ylabel("cd and cl")
plt.grid()
plt.legend()
plt.show()
