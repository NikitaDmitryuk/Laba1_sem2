from photon import Photon
from source import Source
from surface import Surface
from cylinder_surface import CylinderSurface
from rectangular_source import RectangularSource
from modeling import Modeling
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def plot_trajectory(modeling):
    plt.rcParams['legend.fontsize'] = 10
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    modeling.get_source().plot_source(ax)
    modeling.get_surface().plot_surface(ax)

    for photon in modeling.get_photones():
        trajectory = photon.get_trajectory()
        ax.plot(trajectory[0], trajectory[1], trajectory[2], '--.')

    plt.show()

    # fig = plt.figure()
    # ax = fig.gca()
    # for photon in modeling.get_photones():
    #     trajectory = photon.get_trajectory()
    #     ax.scatter(trajectory[0][0], trajectory[1][0])
    #
    # plt.show()


def main():

    surface = CylinderSurface(5, 2)
    source = RectangularSource([-2.5, -2.5], [2.5, 2.5])
    modeling = Modeling(surface, source)
    modeling.set_photones(50, 3.5)
    modeling.start_of_modeling()

    plot_trajectory(modeling)


if __name__ == '__main__':
    main()
