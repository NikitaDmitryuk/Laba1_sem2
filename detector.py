from modeling import Modeling
from photon import Photon
import matplotlib.pyplot as plt
import numpy as np
from math import pi, e, log, exp, sqrt


class Detector:

    def __init__(self, position):
        self.position = position
        self.rate = []
        self.nu = []

    def hist_rate(self, ax):
        sum_hist = []
        nu = np.array(self.nu)
        start = nu.min
        stop = nu.max
        linspace = [i for i in range(1, 1000)]
        step = [1 / x for x in linspace]
        step.reverse()
        ax.hist(self.nu, 10000)

    def flow_rate(self, modeling):
        nu = []
        photones = modeling.get_delete_photones()
        position = self.position
        for photon in photones:
            weight = photon.get_weight()
            mu = photon.get_mu()
            a = photon.get_energy_photon()
            points = photon.get_points_interaction()
            sigma_total = photon.get_sigma_total()
            for i in range(1, len(photon.get_points_interaction())):
                a1 = a[i - 1]
                a2 = a1 * a1
                mu1 = mu[i]
                mu2 = mu1 * mu1

                r_pd2 = (points[i][0] - position[0])**2 +\
                        (points[i][1] - position[1])**2 +\
                        (points[i][2] - position[2])**2

                sigma_relationship = 1 / 4 / pi * (1 + mu2 + a2 * (1 - mu2) / (1 + a1 * (1 - mu1))) /\
                                     (1 + a1*(1 - mu1))**2 /\
                                     ((1 + a1) / a2 * (2 * (1 + a1) / (1 + 2*a1) - log(1 + 2 * a1, e) / a1) +
                                      log(1 + 2 * a1, e) / (2 * a1) - (1 + 3 * a1) / (1 + 2 * a1)**2)

                nu.append(weight[i] * exp(-sigma_total[i] * sqrt(r_pd2)) / r_pd2 * sigma_relationship)

        self.nu = nu

    def get_nu(self):
        return self.nu
