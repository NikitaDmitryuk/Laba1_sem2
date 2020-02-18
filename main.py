from photon import Photon
from source import Source
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def main():
    plt.rcParams['legend.fontsize'] = 10
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    source = Source([-2.5, -2.5], [2.5, 2.5])
    source.born_photon(100, 3.5)
    source.set_point_interaction()

    for photon in source.get_photones():
        trajectory = photon.get_trajectory()
        ax.plot(trajectory[0], trajectory[1], trajectory[2])

    # ax.legend()
    plt.show()

    fig = plt.figure()
    ax = fig.gca()
    for photon in source.get_photones():
        trajectory = photon.get_trajectory()
        ax.scatter(trajectory[0][0], trajectory[1][0])

    plt.show()


if __name__ == '__main__':
    main()
