

from photon import Photon
from numpy import random
from source import Source
import numpy as np


class Modeling:

    def __init__(self, surface, source):
        self.photones = []
        self.dell_photones = []
        self.surface = surface
        self.source = source

    def get_surface(self):
        return self.surface

    def get_source(self):
        return self.source

    def set_photones(self, n, energy):
        [self.photones.append(self.source.born_photon(energy)) for _ in range(n)]

    def set_point_interaction(self):
        [photon.set_point_of_interaction() for photon in self.photones]

    def get_photones(self):
        return self.dell_photones

    def set_new_energy_photones(self):
        [photon.set_new_energy() for photon in self.photones]

    def delete_photones(self):
        photones = []
        for photon in self.photones:
            if not self.surface.is_in(photon) or not photon.is_compton_interaction():
                photon.delete_last_position()
                self.dell_photones.append(photon)
            else:
                photones.append(photon)

        self.photones = photones

    def is_empty_photones(self):
        return len(self.photones) == 0

    def start_of_modeling(self):
        while not self.is_empty_photones():
            self.set_point_interaction()
            self.delete_photones()
            self.set_new_energy_photones()
