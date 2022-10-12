from math import pi

import matplotlib.pyplot as plt
import numpy as np

from fun_plot import plot_function
from fun_velocity_correction import velocity_correction

local_thrust = np.array([])
local_thrust_coefficient = np.array([])
alpha_f = np.array([])
phi_f = np.array([])
cd_f = np.array([])
cl_f = np.array([])
blades_thrust = 0.0
blades_thrust_coefficent = 0.0

# read profile and settings
with open("prop2opt.txt", "r") as f:
    lines = f.readlines()

adimensional_radius = []
for line in lines[3:]:
    r_R, c_R, beta = line.split()
    adimensional_radius.append(float(r_R))

chord_radius_ratio = []
for line in lines[3:]:
    r_R, c_R, beta = line.split()
    chord_radius_ratio.append(float(c_R))

theta = []
for line in lines[3:]:
    r_R, c_R, beta = line.split()
    theta.append(float(beta))

with open("settings_prop2.txt", "r") as f:
    input_data = f.read().splitlines()
    data = [i.split()[2] for i in input_data[2:] if any(j.isnumeric() for j in i)]
    data = [float(x) for x in data]
    radius, rpm, blades_number, free_stream_velocity, RHO = data[0:]

# prelimanary calculation
n_step = len(adimensional_radius) - 1
n = rpm / 60
advanced_ratio = free_stream_velocity / (n * 2 * radius)
r_hub = adimensional_radius[1] * radius
r_tip = adimensional_radius[-1] * radius
r_step = (r_tip - r_hub) / n_step
omega = 2 * pi * n

print(f"free stream velocity= {free_stream_velocity}")
print(f"advanced ratio= {advanced_ratio}")

# calculation
for i in range(len(adimensional_radius)):

    dr = adimensional_radius[i] * radius
    theta_c = theta[i]
    chord_c = chord_radius_ratio[i] * radius

    dT, local_velocity, phi, alpha, cl, cd, axial_velocity = velocity_correction(
        dr, theta_c, free_stream_velocity, omega, RHO, blades_number, chord_c
    )

    phi_f = np.append(phi_f, phi)
    alpha_f = np.append(alpha_f, alpha)
    cd_f = np.append(cd_f, cd)
    cl_f = np.append(cl_f, cl)
    local_thrust = np.append(local_thrust, dT)
    local_thrust_coefficient = np.append(
        local_thrust_coefficient,
        dT / (RHO * n**2 * (2 * radius) ** 4),
    )

    blades_thrust += dT * r_step

print(f"thrust= {blades_thrust}")
print(f"free stream velovity corrected= {axial_velocity}")

total_thrust_coefficient = blades_thrust / (RHO * n**2 * (2 * radius) ** 4)
print(f"total thrust coefficient= {total_thrust_coefficient}")

plt.figure(figsize=(10, 8))

ct = np.array(
    [
        0.0013614,
        0.0059562,
        0.0113506,
        0.0164221,
        0.0206370,
        0.0230940,
        0.0215604,
        0.0000000,
    ]
)

# plot function
plot_function(
    adimensional_radius,
    theta,
    chord_radius_ratio,
    local_thrust,
    ct,
    RHO,
    n,
    local_thrust_coefficient,
    phi_f,
    alpha_f,
    cl_f,
    cd_f,
    radius,
)
