from photon import Photon
from source import Source
from surface import Surface
from cylinder_surface import CylinderSurface
from rectangular_source import RectangularSource
from modeling import Modeling
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import time
from detector import Detector


def plot_trajectory(modeling):
    plt.rcParams['legend.fontsize'] = 10
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    modeling.get_source().plot_source(ax)
    modeling.get_surface().plot_surface(ax)

    for photon in modeling.get_delete_photones():
        trajectory = photon.get_trajectory()
        ax.plot(trajectory[0], trajectory[1], trajectory[2], '--.')

    plt.show()


def plot_hist(detector):
    _, ax = plt.subplots()
    detector.hist_rate(ax)
    plt.show()


def main():

    n = 10000
    start_energy = 3.5
    surface_radius = 10
    surface_height = 6
    source_height = 5
    source_width = 5

    start_time = time.process_time()

    surface = CylinderSurface(surface_radius, surface_height)
    source = RectangularSource(source_height, source_width)
    modeling = Modeling(surface, source, n, start_energy)
    detector = Detector([0, 0, surface_height])

    modeling.start_of_modeling()

    detector.flow_rate(modeling)

    print("{:g} s".format(time.process_time() - start_time))

    plot_trajectory(modeling)
    # plot_hist(detector)


if __name__ == '__main__':
    main()
