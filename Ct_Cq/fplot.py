import matplotlib.pyplot as plt


def plot_function(
    advanced_ratio, thrust_coefficient, torque_coefficent, thrust_max, efficiency
):

    efficiency[[efficiency <= 0] and [efficiency > 1]] = -1

    plt.figure(figsize=(7, 8))

    plt.subplot(2, 1, 1)
    plt.suptitle(
        "Thrust coefficent, torque coeffcient and propeller efficiency",
        fontweight="bold",
        size=13,
    )
    plt.plot(advanced_ratio, thrust_coefficient, label="Ct")
    plt.plot(advanced_ratio, torque_coefficent, label="Cq")
    plt.xlim(0, 0.65)
    plt.ylim(0, 1.1 * thrust_max)
    plt.title("Thrust and Torque Coefficients")
    plt.xlabel("Advance Ratio (J)")
    plt.ylabel("Ct, Cq")
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(advanced_ratio, efficiency)
    plt.title("Propeller Efficiency")
    plt.xlabel("Advance Ratio (J)")
    plt.ylabel("Efficiency")
    plt.xlim(0, 0.65)
    plt.ylim(0, 1)

    plt.tight_layout(pad=1.2)

    return plt.show()
