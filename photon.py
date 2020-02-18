
from math import *
from numpy import random


class Photon:

    def __init__(self, xy0, xy1, energy):
        random.seed()
        self.point_interaction = [0, 0, 0]
        self.point_born = [0, 0, 0]
        self.point_born[0] = random.uniform(xy0[0], xy1[0])
        self.point_born[1] = random.uniform(xy0[1], xy1[1])
        self.point_born[2] = 0
        self.energy = energy
        self.phi = random.uniform(0, 2 * pi)
        self.psi = random.uniform(0, pi)

    def set_point_of_interaction(self):
        length = - log(random.uniform(0, 1), e) / 0.039
        self.point_interaction[0] = length * cos(self.psi) * cos(self.phi) + self.point_born[0]
        self.point_interaction[1] = length * cos(self.psi) * sin(self.phi) + self.point_born[1]
        self.point_interaction[2] = length * sin(self.psi) + self.point_born[2]

    def get_trajectory(self):
        trajectory = [[born, interaction] for born, interaction in zip(self.point_born, self.point_interaction)]
        return trajectory
