

from photon import Photon
from numpy import random
from source import Source
import numpy as np
import collections
import multiprocessing


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
            photon = self.photones[i]
            if photon.is_compton_interaction() and photon.is_interaction_likely():
                photon.set_point_of_interaction()
                if self.surface.is_in(photon):
                    photon.set_new_energy()
                    photones.append(photon)
                else:
                    photon.delete_last_position()
                    self.dell_photones.append(photon)
            else:
                self.dell_photones.append(photon)

        self.photones = photones

    def get_delete_photones(self):
        return self.dell_photones

    def get_photones(self):
        return self.photones

    def start_of_modeling(self):
        while len(self.photones) != 0:
            self.set_point_interaction()
