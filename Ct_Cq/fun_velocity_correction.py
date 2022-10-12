# velocity correction

from math import atan2, cos, pi, sin, sqrt


def velocity_correction(
    dr, theta_c, free_stream_velocity, omega, RHO, blades_number, chord_c
):

    MAXITER = 500
    a = 0.1
    b = 0.01

    for _ in range(1, MAXITER + 1):

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
            * RHO
            * local_velocity**2
            * blades_number
            * chord_c
            * ((cl * cos(phi_rad)) - (cd * sin(phi_rad)))
        )

        dQ = (
            0.5
            * RHO
            * local_velocity**2
            * blades_number
            * chord_c
            * dr
            * (cd * cos(phi) + cl * sin(phi))
        )

        axial_momentum = dT / (4 * pi * dr * RHO * free_stream_velocity**2 * (1 + a))
        angular_momentum = dQ / (
            4 * pi * dr**3 * RHO * free_stream_velocity * (1 + a) * omega
        )

        anew = 0.5 * (a + axial_momentum)
        bnew = 0.5 * (b + angular_momentum)

        if abs(anew - a) < 1e-5 and abs(bnew - b) < 1e-5:
            break

        a = anew
        b = bnew

    return dT, local_velocity, phi, alpha, cl, cd, axial_velocity
