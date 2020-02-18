
from photon import Photon
from numpy import random


class Source:

    photones = []

    def __init__(self, xy0, xy1):
        self.xy0 = xy0
        self.xy1 = xy1

    def born_photon(self, n, energy):
        [self.photones.append(Photon(self.xy0, self.xy1, energy)) for _ in range(n)]

    def set_point_interaction(self):
        [photon.set_point_of_interaction() for photon in self.photones]

    def get_photones(self):
        return self.photones
