import numpy as np
from math import pi


def init_calc(diameter, rpm):

    ## Calculation
    radius = diameter / 2.0
    n = rpm / 60
    omega = n * 2.0 * pi

    # use 10 blade segments (starting a 10%R to R)
    xs = 0.1 * radius
    xt = radius
    rstep = (xt - xs) / 10
    r1 = np.arange(xs, (xt + 0.01), rstep)

    return (xs, xt, r1, rstep, omega, n)
