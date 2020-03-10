
from math import *
from numpy import random
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate


def load_data(name):
    data = []
    with open(name) as f:
        for line in f:
            data.append([float(x) for x in line.split()])
    return data


def plot_energy(x, y, _xlim):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(x, y, '--.')
    ax.grid(True)
    plt.xlim(_xlim)
    plt.show()


class Photon:

    data = np.array(load_data('energy.txt'))
    interp_sigma_total = interpolate.interp1d(data[:, 0], data[:, 2], kind='linear')
    interp_sigma_compton = interpolate.interp1d(data[:, 0], data[:, 1], kind='linear')
    mc2 = 0.511

    def __init__(self, point_born, energy_photon):
        self.trajectory = []
        self.energy_photon = []
        self.weight = 1.0
        self.trajectory.append(point_born)
        self.energy_photon.append(energy_photon)
        self.phi = random.uniform(0, 2 * pi)
        self.psi = random.uniform(0, pi)
        self.set_point_of_interaction()
        self.set_new_energy()

    def set_point_of_interaction(self):
        energy_photon = self.get_last_energy()
        sigma_total = self.interp_sigma_total(energy_photon)
        sigma_compton = self.interp_sigma_compton(energy_photon)
        self.weight = self.weight * sigma_compton / sigma_total

        length = - log(random.uniform(0, 1), e) / sigma_total

        point_interaction = [0, 0, 0]
        point_interaction[0] = length * cos(self.psi) * cos(self.phi) + self.trajectory[-1][0]
        point_interaction[1] = length * cos(self.psi) * sin(self.phi) + self.trajectory[-1][1]
        point_interaction[2] = length * sin(self.psi) + self.trajectory[-1][2]

        self.trajectory.append(point_interaction)

    def set_new_energy(self):
        a_old = self.get_last_energy() / self.mc2
        while True:
            g1 = random.uniform(0, 1)
            g2 = random.uniform(0, 1)
            a = a_old * (1 + 2 * a_old * g1) / (1 + 2 * a_old)
            if g2 * (1 + 2 * a_old + 1 / (1 + 2 * a_old)) < self.p(a, a_old):
                break

        mu = 1 - 1 / a + 1 / a_old
        self.psi = acos(mu) - pi / 2
        self.phi = random.uniform(0, 2 * pi)
        self.energy_photon.append(a_old * self.mc2 / (1 + a_old * (1 - mu)))

    def p(self, x, a_old):
        return x / a_old + a_old / x + (1 / a_old - 1 / x) * (2 + 1 / a_old - 1 / x)

    def is_compton_interaction(self):
        energy_photon = self.get_last_energy()
        sigma_total = self.interp_sigma_total(energy_photon)
        sigma_compton = self.interp_sigma_compton(energy_photon)
        return sigma_compton / sigma_total > random.uniform(0, 1)

    def get_trajectory(self):
        x = []
        y = []
        z = []
        for point in self.trajectory:
            x.append(point[0])
            y.append(point[1])
            z.append(point[2])
        trajectory = [x, y, z]
        return trajectory

    def get_last_position(self):
        return self.trajectory[-1]

    def get_last_energy(self):
        return self.energy_photon[-1]

    def delete_last_position(self):
        self.trajectory.pop()

    def is_interaction_likely(self):
        return self.weight > 10e-11
