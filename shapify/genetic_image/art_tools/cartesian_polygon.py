import math
import numpy as np
import random

from shapify.genetic_image.art_tools.genetic_polygon import GeneticPolygon
from shapify.tools.env_constants import Constants
from shapify.genetic_image.art_tools.polar import sort_by_polar


class CartesianPolygon(GeneticPolygon):
    def __init__(self, color, origin=None, cartesian_points=None):
        super().__init__(color, origin, cartesian_points)

    def draw(self, image_draw):
        points = [tuple(i) for i in sort_by_polar(self.points)]
        image_draw.polygon(points, fill=self.color)

    def mutate_origin(self):
        x_delta = random.randint(0, Constants.polygon_max_shift) * random.randint(-1, 1)
        y_delta = random.randint(0, Constants.polygon_max_shift) * random.randint(-1, 1)
        self.origin[0] = min(max(0, self.origin[0] + x_delta), Constants.image_size[0])
        self.origin[1] = min(max(0, self.origin[1] + y_delta), Constants.image_size[1])

    def mutate_pos(self):
        n_points = len(self.points)
        to_move = random.randint(0, n_points - 1)

        x_delta = random.randint(0, Constants.polygon_max_shift) * random.randint(-1, 1)
        y_delta = random.randint(0, Constants.polygon_max_shift) * random.randint(-1, 1)

        new_x = min(max(0, self.points[to_move][0] + x_delta), Constants.polygon_max_radius // 2)
        new_y = min(max(0, self.points[to_move][1] + y_delta), Constants.polygon_max_radius // 2)

        self.points[to_move][0] = new_x
        self.points[to_move][1] = new_y

    @staticmethod
    def random(sides=3):
        color = GeneticPolygon.get_random_color()
        origin = GeneticPolygon.get_random_origin()
        perim = GeneticPolygon.get_random_perimeter(CartesianPolygon, origin=origin)

        return CartesianPolygon(color, origin, perim)

    @staticmethod
    def get_random_point(origin=(0,0)):
        x = random.randint(-Constants.polygon_max_radius // 2, Constants.polygon_max_radius // 2) + origin[0]
        y = random.randint(-Constants.polygon_max_radius // 2, Constants.polygon_max_radius // 2) + origin[1]
        return np.array([x, y])
