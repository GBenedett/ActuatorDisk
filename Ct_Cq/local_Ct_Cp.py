from velocity_correction import velocity_corr
import numpy as np

local_thrust_coefficient = np.array([])
local_power_coefficient = np.array([])


def local_coeff(
    v,
    a,
    b,
    omega,
    dr,
    theta,
    rho,
    blade_numbers,
    chord,
    r_step,
    n,
    diameter,
    steps_vector,
):

    for i in range(len(steps_vector + 1)):

        blade_thrust = 0.0
        blade_torque = 0.0

        dr = steps_vector[i]
        theta = atan(pitch / 2 / pi / dr)

        a = 0.1
        b = 0.01

        dT, dQ, dP = velocity_corr(v, a, b, omega, dr, theta, rho, blade_numbers, chord)

        blade_thrust += dT * r_step
        blade_torque += dQ * r_step
        blade_power += dP * r_step

        local_thrust_coefficient = np.append(
            local_thrust_coefficient, dT / (rho * n**2 * diameter**4)
        )

        local_power_coefficient = np.append(
            local_power_coefficient, (rho * n**2 * diameter**5)
        )

    return
