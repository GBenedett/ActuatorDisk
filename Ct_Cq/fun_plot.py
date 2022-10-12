import matplotlib.pyplot as plt


def plot_function(
    adimensional_radius,
    theta,
    chord_radius_ratio,
    local_thrust,
    ct,
    RHO,
    n,
    local_thrust_coefficient,
    phi_f,
    alpha_f,
    cl_f,
    cd_f,
    radius,
):

    plt.plot(adimensional_radius, theta, label="theta")
    plt.xlabel("r/R")
    plt.ylabel("theta")
    plt.grid()
    plt.show()

    plt.plot(adimensional_radius, chord_radius_ratio, label="r/R")
    plt.xlabel("r/R")
    plt.ylabel("c/R")
    plt.ylim(0, 0.5)
    plt.grid()
    plt.show()

    plt.figure(figsize=(10, 8))

    plt.subplot(2, 1, 1)
    plt.plot(adimensional_radius, local_thrust, label="T_loc")
    plt.plot(
        adimensional_radius,
        ct * (RHO * n**2 * (2 * radius) ** 4),
        label="T_loc_Saetta",
    )
    plt.title("thrust(r) vs x/r")
    plt.xlabel("x/r")
    plt.ylabel("thrust")
    plt.legend()
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.plot(adimensional_radius, local_thrust_coefficient, label="Ct")
    plt.plot(adimensional_radius, ct, label="Ct_Saetta")
    plt.title("thrust_coefficient(r) vs x/r")
    plt.xlabel("x/r")
    plt.ylabel("thrust_coefficient")
    plt.legend()
    plt.grid(True)
    plt.show()

    plt.tight_layout(pad=1)

    plt.plot(adimensional_radius, phi_f, label="phi")
    plt.plot(adimensional_radius, alpha_f, label="alpha")
    plt.plot(adimensional_radius, theta, label="theta")
    plt.legend()
    plt.grid(True)
    plt.show()

    plt.plot(adimensional_radius, cl_f, label="cl")
    plt.plot(adimensional_radius, cd_f, label="cd")
    plt.legend()
    plt.grid(True)
    plt.show()

    return plt.show()
