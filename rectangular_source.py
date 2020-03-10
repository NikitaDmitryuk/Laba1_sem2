
from photon import Photon
from numpy import random
from source import Source
import numpy as np
import matplotlib.pyplot as plt


class RectangularSource(Source):

    def __init__(self, source_height, source_width):
        self.xy0 = [-source_width / 2, -source_height / 2]
        self.xy1 = [source_width / 2, source_height / 2]

    def born_photon(self, energy):
        point_born = [0, 0, 0]
        point_born[0] = random.uniform(self.xy0[0], self.xy1[0])
        point_born[1] = random.uniform(self.xy0[1], self.xy1[1])
        point_born[2] = 0
        return Photon(point_born, energy)

    def plot_source(self, ax):
        x0 = self.xy0[0]
        x1 = self.xy1[0]
        y0 = self.xy0[1]
        y1 = self.xy1[1]
        x = [x0, x0, x1, x1, x0]
        y = [y0, y1, y1, y0, y0]
        z = [0, 0, 0, 0, 0]
        ax.plot(x, y, z)
