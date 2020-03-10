

from photon import Photon
from numpy import random
from source import Source
import numpy as np


class Modeling:

    def __init__(self, surface, source, n, start_energy):
        self.photones = []
        self.dell_photones = []
        self.surface = surface
        self.source = source
        self.n = n
        self.start_energy = start_energy
        self.set_photones(n, start_energy)

    def get_surface(self):
        return self.surface

    def get_source(self):
        return self.source

    def set_photones(self, n, energy):
        for _ in range(n):
            photon = self.source.born_photon(energy)
            if self.surface.is_in(photon):
                self.photones.append(photon)
            else:
                self.set_photones(1, energy)

    def set_point_interaction(self):
        photones = []
        for i in range(len(self.photones)):
            if self.photones[i].is_compton_interaction() and self.photones[i].is_interaction_likely():
                self.photones[i].set_point_of_interaction()
                if self.surface.is_in(self.photones[i]):
                    self.photones[i].set_new_energy()
                    photones.append(self.photones[i])
                else:
                    self.photones[i].delete_last_position()
                    self.dell_photones.append(self.photones[i])
            else:
                self.dell_photones.append(self.photones[i])

        self.photones = photones

    def get_delete_photones(self):
        return self.dell_photones

    def get_photones(self):
        return self.photones

    def is_empty_photones(self):
        return len(self.photones) == 0

    def start_of_modeling(self):
        while not self.is_empty_photones():
            self.set_point_interaction()
