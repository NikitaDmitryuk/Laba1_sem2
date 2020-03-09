
from math import *
from numpy import random
import numpy as np


def load_data(name):
    data = []
    with open(name) as f:
        for line in f:
            data.append([float(x) for x in line.split()])
    return data


class Photon:

    data = np.array(load_data('energy.txt'))
    photon_energy_list = data[:, 0]
    compton_energy_list = data[:, 1]
    total_energy = data[:, 2]

    def __init__(self, point_born, energy_photon):
        self.trajectory = []
        self.energy_photon = []
        self.trajectory.append(point_born)
        self.energy_photon.append(energy_photon)
        self.phi = random.uniform(0, 2 * pi)
        self.psi = random.uniform(0, pi)

    def set_point_of_interaction(self):
        length = - log(random.uniform(0, 1), e) / self.energy_photon[-1]
        point_interaction = [0, 0, 0]
        point_interaction[0] = length * cos(self.psi) * cos(self.phi) + self.trajectory[-1][0]
        point_interaction[1] = length * cos(self.psi) * sin(self.phi) + self.trajectory[-1][1]
        point_interaction[2] = length * sin(self.psi) + self.trajectory[-1][2]
        self.trajectory.append(point_interaction)

    def set_new_energy(self):
        a_old = self.get_last_energy() / 0.511
        while True:
            g1 = random.uniform(0, 1)
            g2 = random.uniform(0, 1)
            a = a_old * (1 + 2 * a_old * g1) / (1 + 2 * a_old)
            if g2 * (1 + 2 * a_old + 1 / (1 + 2 * a_old)) < self.p(a, a_old):
                break

        mu = 1 - 1 / a + 1 / a_old
        self.psi = acos(mu) - pi / 2
        self.phi = random.uniform(0, 2 * pi)
        self.energy_photon.append(a_old * 0.511 / (1 + a_old * (1 - mu)))

    def p(self, x, a_old):
        return x / a_old + a_old / x + (1 / a_old - 1 / x) * (2 + 1 / a_old - 1 / x)

    def is_compton_interaction(self):
        energy_total, energy_compton = self.linear_inter(self.get_last_energy())
        return energy_compton / energy_total > random.uniform(0, 1)

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

    def linear_inter(self, energy):
        for i in range(len(self.photon_energy_list)-1):
            if (self.photon_energy_list[i] < energy) and (self.photon_energy_list[i+1] > energy):
                energy_total = self.total_energy[i] + (self.total_energy[i+1] - self.total_energy[i]) /\
                               (self.photon_energy_list[i+1] - self.photon_energy_list[i]) *\
                               (energy - self.photon_energy_list[i])

                energy_compton = self.compton_energy_list[i] + (self.compton_energy_list[i+1] - self.compton_energy_list[i]) /\
                               (self.photon_energy_list[i+1] - self.photon_energy_list[i]) *\
                               (energy - self.photon_energy_list[i])

                return [energy_total, energy_compton]

        print("Выход за пределы энергий")
