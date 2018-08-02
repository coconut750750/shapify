import math
import numpy as np
import random

from shapify.genetic_image.art_tools.genetic_polygon import GeneticPolygon
from shapify.genetic_image.art_tools.polar import to_cartesian
from shapify.tools.env_constants import Constants


class PolarPolygon(GeneticPolygon):
    def __init__(self, color, origin=None, polar_points=None):
        super().__init__(color, origin, polar_points)

    def draw(self, image_draw):
        cartesian = [tuple(i) for i in to_cartesian(self.points, self.origin)]
        image_draw.polygon(cartesian, fill=self.color)

    def mutate_pos(self):
        n_points = len(self.points)
        to_move = random.randint(0, n_points - 1)

        r_delta = random.randint(0, Constants.polygon_max_shift) * random.randint(-1, 1)
        new_r = min(max(0, self.points[to_move][0] + r_delta), Constants.polygon_max_radius)
        self.points[to_move][0] = new_r

        lower = 0 if to_move == 0 else self.points[to_move - 1][1]
        upper = 360 if to_move == n_points - 1 else self.points[to_move + 1][1]
        if upper - lower < 2:
            return
        new_theta = random.randint(lower + 1, upper - 1)
        self.points[to_move][1] = new_theta

    @staticmethod
    def random(sides=3):
        color = GeneticPolygon.get_random_color()
        origin = GeneticPolygon.get_random_origin()
        perim = GeneticPolygon.get_random_perimeter(PolarPolygon)

        return PolarPolygon(color, origin, perim)

    @staticmethod
    def get_random_point():
        r = random.randint(0, Constants.polygon_max_radius)
        theta = random.randint(0, 360)
        return np.array([r, theta])
