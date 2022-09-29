import pandas as pd

# not working

df = pd.read_csv(
    f"/home/cfse/Stage_Giacomo/ActuatorDisk/Ct_Cq/input_data.csv", skiprows=1
)


def diameter_test():
    diameter = df.iloc[3, 1]
    assert diameter == 0
