## Ct and Cq calculator ##

from math import pi, atan2, sin, cos, sqrt

import matplotlib.pyplot as plt
import numpy as np

from fun_plot import plot_function

local_thrust = np.array([])
local_thrust_coefficient = np.array([])
alpha_f = np.array([])
phi_f = np.array([])
cd_f = np.array([])
cl_f = np.array([])
blades_thrust = 0.0
blades_thrust_coefficent = 0.0

# read profile and settings
with open("propreal.txt", "r") as f:
    lines = f.readlines()

adimensional_radius = []
for line in lines[2:]:
    r_R, c_R, beta = line.split()
    adimensional_radius.append(float(r_R))

chord_radius_ratio = []
for line in lines[2:]:
    r_R, c_R, beta = line.split()
    chord_radius_ratio.append(float(c_R))

theta = []
for line in lines[2:]:
    r_R, c_R, beta = line.split()
    theta.append(float(beta))

with open("settings_propreal.txt", "r") as f:
    input_data = f.read().splitlines()
    data = [i.split()[2] for i in input_data[2:] if any(j.isnumeric() for j in i)]
    data = [float(x) for x in data]
    radius, rpm, blades_number, free_stream_velocity, RHO = data[0:]

# with open("optimalpropdata.txt", "r") as f:
#    lines = f.readlines()

# ct = []
# for line in lines[2:]:
#    print(line)
#    ct_real, ct_confr, ct_1, ct_2 = line.split()
#    ct.append(float(ct_confr))

# prelimanary calculation
n_step = len(adimensional_radius)
n = rpm / 60
advanced_ratio = free_stream_velocity / (n * 2 * radius)
r_hub = adimensional_radius[1] * radius
r_tip = adimensional_radius[-1] * radius
r_step = (r_tip - r_hub) / n_step
omega = 2 * pi * n

print(f"free stream velocity= {free_stream_velocity}")
print(f"advanced ratio= {advanced_ratio}")

cli = np.array(
    [
        3.9,
        3.4197,
        2.7506,
        2.2962,
        1.9023,
        1.6379,
        1.4054,
        1.2389,
        1.2055,
        1.1054,
        1.0720,
        1.0820,
        1.08,
        1.1054,
        1.2055,
        1.2389,
        1.3389,
        1.4387,
        1.5384,
        1.6047,
    ]
)

# calculation
for i in range(len(adimensional_radius)):

    dr = adimensional_radius[i] * radius
    theta_c = theta[i]
    chord_c = chord_radius_ratio[i] * radius
    cl = cli[i]
    axial_velocity = free_stream_velocity
    rotational_velocity = omega * dr
    phi_rad = atan2(float(axial_velocity), float(rotational_velocity))
    phi = phi_rad * 180 / pi
    alpha = theta_c - phi
    # cl = 2 * pi * (alpha * pi / 180)
    cd = 0.008 - 0.003 * cl + 0.01 * cl**2
    local_velocity = sqrt(axial_velocity**2 + rotational_velocity**2)
    print(local_velocity)
    dT = (
        0.5
        * RHO
        * local_velocity**2
        * blades_number
        * chord_c
        * ((2 * cl * cos(phi_rad)) - (cd * sin(phi_rad)))
        * dr
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

total_thrust_coefficient = blades_thrust / (RHO * n**2 * (2 * radius) ** 4)
print(f"total thrust coefficient= {total_thrust_coefficient}")

plt.figure(figsize=(10, 8))

ct = np.array(
    [
        0.0009043,
        0.0072734,
        0.0247512,
        0.0592727,
        0.1170596,
        0.2044887,
        0.3278528,
        0.4930604,
        0.7053310,
        0.9689362,
        1.2870211,
        1.6615208,
        2.0931698,
        2.5815871,
        3.1254179,
        3.7225050,
        4.3700732,
        5.0649068,
        5.8035126,
        6.5822598,
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