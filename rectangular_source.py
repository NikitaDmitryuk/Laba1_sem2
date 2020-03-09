
from photon import Photon
from numpy import random
from source import Source
import numpy as np


class RectangularSource(Source):

    def __init__(self, xy0, xy1):
        self.xy0 = xy0
        self.xy1 = xy1

    def born_photon(self, energy):
        point_born = [0, 0, 0]
        point_born[0] = random.uniform(self.xy0[0], self.xy1[0])
        point_born[1] = random.uniform(self.xy0[1], self.xy1[1])
        point_born[2] = 0
        return Photon(point_born, energy)
