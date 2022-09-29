import pandas as pd


def test_input():

    df = pd.read_csv("input_data.csv", skiprows=1)

    chord, pitch, diameter, rpm, rho, blade_numbers, v_max = df.iloc[:, 1]

    assert diameter != 0
    assert v_max != 0
    assert rpm != 0
    assert chord != 0
    assert pitch != 0
    assert blade_numbers != 0
