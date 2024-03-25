import numpy as np
import matplotlib.pyplot as plt


def main():
    N_data = 48

    solar_data = np.ndarray(shape=N_data)

    t = np.linspace(0, 24, N_data)

    # parabola
    a = -304.1667
    b = 7300
    c = -32500

    y = a * t**2 + b * t + c
    for index, y_i in enumerate(y):
        if y_i < 0:
            y[index] = 0

    plt.plot(t, y)
    plt.show()

    print(y)


if __name__ == "__main__":
    main()
