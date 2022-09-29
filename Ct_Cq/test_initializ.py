import numpy as np
from pytest import approx

from initialization import init_calc


def test_init():
    (xs, xt, r1, rstep, omega, n) = init_calc(1.6, 2100)
    assert xs == approx(0.08)
    assert xt == 0.8
    assert rstep == 0.072
    assert omega == approx(219.91, rel=1e-5)
    assert n == 35
    np.testing.assert_almost_equal(
        r1, [0.08, 0.152, 0.224, 0.296, 0.368, 0.44, 0.512, 0.584, 0.656, 0.728, 0.8]
    )
