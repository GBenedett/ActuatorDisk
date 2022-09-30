# Calculation without correction
from math import cos, sin, pi, sqrt, atan2, atan
import numpy as np
import matplotlib.pyplot as plt

dT = np.array([])

# Input

radius = 1  # [m]
rho = 1.225  # [kg/m^3]
free_stream_velocity = 150  # [m/s]
n_step = 10
chord = 1
pitch = 10
rpm = 1500

# prelimanary calculation
r_hub = 0.1 * radius
r_tip = radius
r_step = (r_tip - r_hub) / n_step
step_vector = np.arange(r_hub, (r_tip + 0.01), r_step)
n = rpm / 60
omega = 2 * pi * n


# calculation

for i in range(len(step_vector + 1)):

    dr = step_vector[i]
    rotational_velocity = np.array(omega * dr)
    local_velocity = sqrt(rotational_velocity**2 + free_stream_velocity**2)
    phi = atan2(free_stream_velocity, rotational_velocity)
    theta = atan(pitch / 2 / pi / dr)
    alpha = theta - phi
    cl = 6.2 * alpha
    cd = 0.008 - 0.003 * cl + 0.01 * cl**2

    # local thurst
    dT = np.append(
        dT, 0.5 * rho * local_velocity**2 * chord * (cl * cos(phi) - cd * sin(phi))
    )

plt.plot(step_vector, dT)
plt.show()
