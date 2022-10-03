import matplotlib.pyplot as plt


def plot_function(
    advanced_ratio,
    total_thrust_coefficient,
    total_torque_coefficent,
    total_power_coefficient,
    thrust_max,
    efficiency,
    advanced_ratio_max,
    local_thrust_coefficient,
    local_power_coefficient,
    steps_vector,
    radius,
):

    plt.figure(figsize=(9.5, 7))

    plt.subplot(2, 2, 1)
    plt.suptitle(
        "Thrust, torque, power coefficient and propeller efficiency",
        fontweight="bold",
        size=13,
    )
    plt.plot(advanced_ratio, total_thrust_coefficient, label="Ct")
    plt.plot(advanced_ratio, total_torque_coefficent, label="Cq")
    plt.plot(advanced_ratio, total_power_coefficient, label="Cp")
    plt.xlim(0, advanced_ratio_max)
    plt.ylim(0, 1.1 * thrust_max)
    plt.title("Thrust torque and power coefficients vs advanced ratio")
    plt.xlabel("Advance Ratio (J)")
    plt.ylabel("Ct, Cq, Cp")
    plt.legend()

    plt.subplot(2, 2, 2)
    plt.plot(advanced_ratio, efficiency)
    plt.title("Propeller Efficiency")
    plt.xlabel("Advance Ratio (J)")
    plt.ylabel("Efficiency")
    plt.xlim(0, advanced_ratio_max)
    plt.ylim(0, 1)

    plt.subplot(2, 2, 3)
    plt.plot(steps_vector / radius, local_thrust_coefficient)
    plt.title("thrust_coefficient(r) vs x/r")
    plt.xlabel("x/r")
    plt.ylabel("thrust_coefficient")

    plt.subplot(2, 2, 4)
    plt.plot(steps_vector / radius, local_power_coefficient)
    plt.title("power_coefficient(r) vs x/r")
    plt.xlabel("x/r")
    plt.ylabel("power_coefficient")

    plt.tight_layout(pad=1.2)

    return plt.show()
