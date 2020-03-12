

from photon import Photon
from numpy import random
from source import Source
import numpy as np
import collections
from multiprocessing import Pool


class Modeling:

    def __init__(self, surface, source, n, start_energy):
        self.photones = []
        self.dell_photones = []
        self.surface = surface
        self.source = source
        self.n = n
        self.start_energy = start_energy
        self.set_photones(start_energy)

    def get_surface(self):
        return self.surface

    def get_source(self):
        return self.source

    def set_photones_process(self, n, energy):
        for _ in range(n):
            photon = self.source.born_photon(energy)
            if self.surface.is_in(photon):
                self.photones.append(photon)

        if n != 0:
            self.set_photones_process(n, energy)


    def set_photones(self, energy):
        while len(self.photones) < self.n:
            photon = self.source.born_photon(energy)
            if self.surface.is_in(photon):
                self.photones.append(photon)

    def set_point_interaction(self, photones_list):
        photones = []
        dell_photones = []
        for i in range(len(photones_list)):
            photon = photones_list[i]
            if photon.is_compton_interaction() and photon.is_interaction_likely():
                photon.set_point_of_interaction()
                if self.surface.is_in(photon):
                    photon.set_new_energy()
                    photones.append(photon)
                else:
                    photon.delete_last_position()
                    dell_photones.append(photon)
            else:
                dell_photones.append(photon)

        return [photones, dell_photones]

    def get_delete_photones(self):
        return self.dell_photones

    def get_photones(self):
        return self.photones

    def start_of_modeling(self):
        pool = Pool(processes=6)
        while len(self.photones) != 0:
            photones = []
            step = int(len(self.photones) / 6)
            if step != 0:
                list_p = [self.photones[d:d+step] for d in range(0, len(self.photones), step)]
            else:
                list_p = [self.photones]

            result = pool.map(self.set_point_interaction, list_p)

            for elem in result:
                photones += elem[0]
                self.dell_photones += elem[1]

            self.photones = photones