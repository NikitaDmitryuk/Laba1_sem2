
from math import *
from numpy import *
import numpy as np
import matplotlib.pyplot as plt


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
    sigma_total_interp = data[:, 2]
    sigma_compton_interp = data[:, 1]
    energy_photon_interp = data[:, 0]

    mc2 = 0.511

    def __init__(self, point_born, energy_photon):
        self.trajectory = []
        self.energy_photon = []
        self.weight = 1.0
        self.trajectory.append(point_born)
        self.energy_photon.append(energy_photon)
        self.phi = random.uniform(0, 2 * pi)
        self.psi = random.uniform(0, pi)
        self.sigma_compton, self.sigma_total = self.interpolate_linear(energy_photon)

    def interpolate_linear(self, energy):

        left = 0
        right = len(self.energy_photon_interp) - 1
        energy_photon_left = self.energy_photon_interp[left]
        energy_photon_right = self.energy_photon_interp[right]

        if energy <= energy_photon_left:
            return [self.sigma_compton_interp[0], self.sigma_total_interp[0]]

        if energy >= energy_photon_right:
            return [self.sigma_compton_interp[-1], self.sigma_total_interp[-1]]

        while right - left > 1:
            i = (right - left) // 2 + left
            if energy < self.energy_photon_interp[i]:
                right = i
                energy_photon_right = self.energy_photon_interp[right]
            else:
                left = i
                energy_photon_left = self.energy_photon_interp[left]

        sigma_compton_0 = self.sigma_compton_interp[left]
        sigma_compton_1 = self.sigma_compton_interp[right]

        sigma_total_0 = self.sigma_total_interp[left]
        sigma_total_1 = self.sigma_total_interp[right]

        if energy_photon_right - energy_photon_left == 0:
            print('херня')

        sigma_compton = sigma_compton_0 + (sigma_compton_1 - sigma_compton_0) *\
                        (energy - energy_photon_left) / (energy_photon_right - energy_photon_left)

        sigma_total = sigma_total_0 + (sigma_total_1 - sigma_total_0) * \
                        (energy - energy_photon_left) / (energy_photon_right - energy_photon_left)

        return [sigma_compton, sigma_total]

    def set_point_of_interaction(self):

        self.weight = self.weight * self.sigma_compton / self.sigma_total
        length = - math.log(random.uniform(0, 1), math.e) / self.sigma_total

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

    def is_compton_interaction_and_set_sigma(self):
        self.sigma_compton, self.sigma_total = self.interpolate_linear(self.get_last_energy())
        return self.sigma_compton / self.sigma_total > random.uniform(0, 1)

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
