from pytest import approx

from function_vel import convergence


def test_conv():
    DtDr, DqDr = convergence(
        -0.06677,
        -0.00666,
        60,
        219.911,
        0.8,
        0.19637,
        1.225,
        2,
        0.1,
    )
    assert DtDr == approx(-2763.0059, rel=1e-3)
    assert DqDr == approx(-646.79, rel=1e-3)
