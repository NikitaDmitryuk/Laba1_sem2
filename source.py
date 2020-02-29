
from photon import Photon
from numpy import random
import numpy as np


class Source:

    photones = []

    def __init__(self, xy0, xy1, surface):
        self.xy0 = xy0
        self.xy1 = xy1
        self.surface = surface
        self.load_energy()

    def born_photon(self, n, energy):
        [self.photones.append(Photon(self.xy0, self.xy1, energy)) for _ in range(n)]

    def set_point_interaction(self):
        [photon.set_point_of_interaction() for photon in self.photones]

    def get_photones(self):
        return self.photones

    def delete_photones(self):
        self.photones = [photon for photon in self.photones if self.surface.is_in(photon)]

    def load_energy(self):

        def loadData(name):
            data = []
            with open(name) as f:
                for line in f:
                    data.append([float(x) for x in line.split()])
            return data

        data = np.array(loadData('energy.txt'))
        self.photon_energy_list = data[:, 0]
        self.compton_energy_list = data[:, 1]
