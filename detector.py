from modeling import Modeling
from photon import Photon


class Detector:

    def __init__(self, position):
        self.position = position
        self.rate = []

    def flow_rate(self, modeling):
        photones = modeling.get_delete_photones()
