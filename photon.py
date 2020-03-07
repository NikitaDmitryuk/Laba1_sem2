
from math import *
from numpy import random
import numpy as np


def loadData(name):
    data = []
    with open(name) as f:
        for line in f:
            data.append([float(x) for x in line.split()])
    return data


class Photon:

    data = np.array(loadData('energy.txt'))
    photon_energy_list = data[:, 0]
    compton_energy_list = data[:, 1]
    total_energy = data[:, 2]

    def __init__(self, xy0, xy1, energy_photon):
        self.trajectory = []
        point_born = [0, 0, 0]
        point_born[0] = random.uniform(xy0[0], xy1[0])
        point_born[1] = random.uniform(xy0[1], xy1[1])
        point_born[2] = 0
        self.trajectory.append(point_born)
        self.energy_photon = energy_photon
        self.phi = random.uniform(0, 2 * pi)
        self.psi = random.uniform(0, pi)

    def set_point_of_interaction(self):
        energy_total, _ = self.linear_inter(self.energy_photon)
        length = - log(random.uniform(0, 1), e) / energy_total
        point_interaction = [0, 0, 0]
        point_interaction[0] = length * cos(self.psi) * cos(self.phi) + self.trajectory[-1][0]
        point_interaction[1] = length * cos(self.psi) * sin(self.phi) + self.trajectory[-1][1]
        point_interaction[2] = length * sin(self.psi) + self.trajectory[-1][2]
        self.trajectory.append(point_interaction)

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
