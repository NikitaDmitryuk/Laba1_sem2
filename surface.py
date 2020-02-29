from photon import Photon


class Surface:

    def __init__(self, r, h):
        self.r = r
        self.h = h

    def is_in(self, photon):
        point_interaction = photon.get_point_interaction()
        is_in_surface = True
        is_in_surface *= (point_interaction[2] < self.h) and (point_interaction[2] > 0)
        is_in_surface *= point_interaction[0] ** 2 + point_interaction[1] ** 2 < self.r ** 2

        return is_in_surface
