from math import atan2, cos, pi, sin, sqrt

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

local_thrust = np.array([])
local_thrust_coefficient = np.array([])
alpha_f = np.array([])
phi_f = np.array([])
cd_f = np.array([])
cl_f = np.array([])
blades_thrust = 0.0
blades_thrust_coefficent = 0.0

# input

df = pd.read_csv("prop1.csv")

radius = 0.24  # [m]
rho = 1.225  # [kg/m^3]
adimensional_radius = df.iloc[:, 0]
chord_radius_ratio = df.iloc[:, 1]
theta = df.iloc[:, 2]
n_step = len(adimensional_radius) - 1
rpm = 3007
total_thrust_coefficient = 0.068
advanced_ratio = 0.427
n = rpm / 60
free_stream_velocity = advanced_ratio * n * 2 * radius
blade_numbers = 2

print(f"total_thrust_coefficient= {total_thrust_coefficient}")
print(f"free_stream_velocity= {free_stream_velocity}")

# prelimanary calculation
r_hub = adimensional_radius[0] * radius
r_tip = adimensional_radius[17] * radius
r_step = (r_tip - r_hub) / n_step

omega = 2 * pi * n

print(f"advanced ratio= {advanced_ratio}")

# calculation

for i in range(len(adimensional_radius)):

    MAXITER = 1000
    a = 0.1
    b = 0.01

    for _ in range(1, MAXITER + 1):
        dr = adimensional_radius[i] * radius
        theta_c = theta[i]
        chord_c = chord_radius_ratio[i] * radius
        axial_velocity = free_stream_velocity * (1 + a)
        rotational_velocity = omega * dr * (1 - b)

        phi_rad = atan2(float(axial_velocity), float(rotational_velocity))
        phi = phi_rad * 180 / pi
        alpha = theta_c - phi
        cl = 2 * pi * (alpha * pi / 180)
        cd = 0.008 - 0.003 * cl + 0.01 * cl**2
        local_velocity = sqrt(axial_velocity**2 + rotational_velocity**2)

        dT = (
            0.5
            * rho
            * local_velocity**2
            * blade_numbers
            * chord_c
            * ((cl * cos(phi_rad)) - (cd * sin(phi_rad)))
        )

        dQ = (
            0.5
            * rho
            * local_velocity**2
            * blade_numbers
            * chord_c
            * dr
            * (cd * cos(phi) + cl * sin(phi))
        )

        axial_momentum = dT / (4 * pi * dr * rho * free_stream_velocity**2 * (1 + a))
        angular_momentum = dQ / (
            4 * pi * dr**3 * rho * free_stream_velocity * (1 + a) * omega
        )

        anew = 0.5 * (a + axial_momentum)
        bnew = 0.5 * (b + angular_momentum)

        if abs(anew - a) < 1e-5 and abs(bnew - b) < 1e-5:
            break

        a = anew
        b = bnew

    phi_f = np.append(phi_f, phi)
    alpha_f = np.append(alpha_f, alpha)
    cd_f = np.append(cd_f, cd)
    cl_f = np.append(cl_f, cl)
    local_thrust = np.append(local_thrust, dT)
    local_thrust_coefficient = np.append(
        local_thrust_coefficient,
        dT / (rho * n**2 * (2 * radius) ** 4),
    )

    blades_thrust += dT * r_step

print(f"free_stream_velovity_corrected= {axial_velocity}")

total_thrust_coefficient_new = blades_thrust / (rho * n**2 * (2 * radius) ** 4)
print(f"total_thrust_coefficient_new= {total_thrust_coefficient_new}")

plt.figure(figsize=(10, 8))

# rs = np.array([0.2, 0.26, 0.36, 0.46, 0.55, 0.63, 0.71, 0.79, 0.87, 0.95, 1])
ct = np.array(
    [
        0.0008252,
        0.0054180,
        0.0140078,
        0.0249331,
        0.0368152,
        0.0489288,
        0.0609381,
        0.0726705,
        0.0839898,
        0.0947232,
        0.1046003,
        0.1131831,
        0.1197629,
        0.1231991,
        0.1216340,
        0.1118740,
        0.0873221,
        0.0000000,
    ]
)

plt.plot(adimensional_radius, theta, label="theta")
plt.xlabel("r/R")
plt.ylabel("theta")
plt.grid()
plt.show()

plt.plot(adimensional_radius, chord_radius_ratio, label="r/R")
plt.xlabel("r/R")
plt.ylabel("c/R")
plt.grid()
plt.show()

plt.figure(figsize=(10, 8))
plt.subplot(2, 1, 1)
plt.plot(adimensional_radius, local_thrust, label="T_loc")
plt.plot(
    adimensional_radius,
    ct * (rho * n**2 * (2 * radius) ** 4),
    label="T_loc_Saetta",
)
plt.title("thrust(r) vs x/r")
plt.xlabel("x/r")
plt.ylabel("thrust")
plt.legend()
plt.grid(True)

plt.subplot(2, 1, 2)
plt.plot(adimensional_radius, local_thrust_coefficient, label="Ct")
plt.plot(adimensional_radius, ct, label="Ct_Saetta")
plt.title("thrust_coefficient(r) vs x/r")
plt.xlabel("x/r")
plt.ylabel("thrust_coefficient")
plt.legend()
plt.grid(True)

plt.tight_layout(pad=1)

plt.show()

plt.plot(adimensional_radius, phi_f, label="phi")
plt.plot(adimensional_radius, alpha_f, label="alpha")
plt.plot(adimensional_radius, theta, label="theta")
plt.legend()
plt.grid(True)

plt.show()

plt.plot(adimensional_radius, cl_f, label="cl")
plt.plot(adimensional_radius, cd_f, label="cd")
plt.legend()
plt.grid(True)

plt.show()
