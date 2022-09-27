import numpy as np
from math import pi


def init_calc(diameter, chord, rpm):
    ## initializations
    thrust_coefficient = np.array([])
    torque_coefficent = np.array([])
    advanced_ratio = np.array([])
    efficiency = np.array([])
    v = np.array([])

    ## Calculation
    radius = diameter / 2.0
    tickness_chord_ratio = 0.12 * chord
    n = rpm / 60
    omega = n * 2.0 * pi

    # use 10 blade segments (starting a 10%R to R)
    xs = 0.1 * radius
    xt = radius
    rstep = (xt - xs) / 10
    r1 = np.arange(xs, (xt + 0.01), rstep)

    return (
        xs,
        xt,
        r1,
        rstep,
        omega,
        n,
        thrust_coefficient,
        torque_coefficent,
        advanced_ratio,
        efficiency,
        v,
    )
