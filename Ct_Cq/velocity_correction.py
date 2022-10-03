# velocity correction

from math import atan2, cos, sin, sqrt, pi

MAXITER = 500


def velocity_corr(
    free_stream_velocity, a, b, omega, dr, theta, rho, blade_numbers, chord
):

    for _ in range(1, MAXITER + 1):
        axial_velocity = free_stream_velocity * (1 + a)
        rotational_velocity = omega * dr * (1 - b)
        phi = atan2(float(axial_velocity), float(rotational_velocity))
        alpha = theta - phi
        cl = 6.2 * alpha
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
        dQ = (
            0.5
            * rho
            * local_velocity**2
            * blade_numbers
            * chord
            * dr
            * (cd * cos(phi) + cl * sin(phi))
        )
        dP = dT * local_velocity

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

    return dT, dQ, dP, local_velocity
