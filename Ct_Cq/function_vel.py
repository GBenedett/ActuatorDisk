from math import cos, pi, sin, sqrt
from math import atan2

MAXITER = 500


def convergence(a, b, v, omega, rad, theta, rho, blade_numbers, chord):
    for _ in range(1, MAXITER + 1):
        axial_inflow_velocity = v * (1 + a)
        angular_inflow_velocity = omega * rad * (1 - b)
        # flow angle
        phi = atan2(float(axial_inflow_velocity), float(angular_inflow_velocity))
        # blade angle of attack
        alpha = theta - phi
        cl = 6.2 * alpha
        cd = 0.008 - 0.003 * cl + 0.01 * cl**2
        local_velocity = sqrt(axial_inflow_velocity**2 + angular_inflow_velocity**2)
        # thrust grading
        DtDr = (
            0.5
            * rho
            * local_velocity**2
            * blade_numbers
            * chord
            * (cl * cos(phi) - cd * sin(phi))
        )
        # torque grading
        DqDr = (
            0.5
            * rho
            * local_velocity**2
            * blade_numbers
            * chord
            * rad
            * (cd * cos(phi) + cl * sin(phi))
        )
        # momentum conservation check
        axial_momentum = DtDr / (4 * pi * rad * rho * v**2 * (1 + a))
        angular_momentum = DqDr / (4 * pi * rad**3 * rho * v * (1 + a) * omega)
        # stabilise iteration
        anew = 0.5 * (a + axial_momentum)
        bnew = 0.5 * (b + angular_momentum)

        # check for convergence
        if abs(anew - a) < 1e-5 and abs(bnew - b) < 1e-5:
            break

        a = anew
        b = bnew

    return DtDr, DqDr
