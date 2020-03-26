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
import time


def timer(f):
    def tmp(*args, **kwargs):
        t = time.time()
        res = f(*args, **kwargs)
        print("function run time: %f" % (time.time()-t))
        return res

    return tmp


@timer
def plot_trajectory(modeling, detector=None):
    print('plot trajectory')
    plt.rcParams['legend.fontsize'] = 10
    fig = plt.figure(1)
    ax = fig.gca(projection='3d')
    if detector is not None:
        ax.scatter(*detector.get_position(), color='r', s=100)

    modeling.get_source().plot_source(ax)
    modeling.get_surface().plot_surface(ax)

    for photon in modeling.get_delete_photones():
        trajectory = photon.get_trajectory()
        ax.plot(trajectory[0], trajectory[1], trajectory[2], '--.')

    plt.savefig('trajectory_{:.1e}_{}.pdf'.format(n, surface_height), bbox_inches='tight')


@timer
def plot_hist(detector):
    print('plot hist')
    plt.figure(2)
    plt.clf()
    plt.grid(linestyle='--')
    x_list, y_list, width_list = detector.get_hist_rate()
    plt.bar(x_list, y_list, width_list, align='edge', edgecolor='r', alpha=0.7)
    plt.ticklabel_format(axis="y", style="sci", scilimits=(-2, 3))
    plt.ticklabel_format(axis="x", style="sci", scilimits=(-2, 3))
    plt.xlabel('Энергия, МэВ')
    plt.ylabel('Плотность потока')
    plt.title('Зависимость вклада от энергии фотона')
    position = detector.get_position()
    plt.suptitle('Шайба высотой {}, координаты детектора ({}, {}, {}), количество частиц {:.1e}'
                 .format(position[2], position[0], position[1], position[2], n))
    plt.savefig('plot_hist_{:.1e}_{}.pdf'.format(n, surface_height), bbox_inches='tight')


n = 1000
start_energy = 3.5
surface_radius = 20
surface_height = 60
source_height = 5
source_width = 5
n_bins_hist = 20


def main():

    start_time = time.process_time()
    surface = CylinderSurface(surface_radius, surface_height)
    source = RectangularSource(source_height, source_width)
    modeling = Modeling(surface, source, n, start_energy)
    detector = Detector(surface_height)

    modeling.start_of_modeling()
    detector.flow_rate(modeling, n_bins_hist)

    print("FULL MODELING TIME: {:g} s".format(time.process_time() - start_time))

    if n <= 10000:
        plot_trajectory(modeling, detector)

    plot_hist(detector)
    plt.show()


if __name__ == '__main__':
    main()
