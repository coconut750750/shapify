import copy
import math
import numpy as np
import random

from shapify.tools.env_constants import Constants


class GeneticPolygon:
    def __init__(self, color, origin=None, points=None):
        self.color = color
        self.origin = origin
        self.points = points

    def draw(self, image_draw):
        raise RuntimeError('Override this method in your subclass')

    def mutate_origin(self):
        x_delta = random.randint(0, Constants.polygon_max_shift) * random.randint(-1, 1)
        y_delta = random.randint(0, Constants.polygon_max_shift) * random.randint(-1, 1)
        self.origin[0] = min(max(0, self.origin[0] + x_delta), Constants.image_size[0])
        self.origin[1] = min(max(0, self.origin[1] + y_delta), Constants.image_size[1])

    def mutate_pos(self):
        raise RuntimeError('Override this method in your subclass')

    def mutate_color(self):
        self.color = self.color[:-1] + (random.randint(*Constants.alpha_range), )

    def mutate(self):
        mutation_type = random.randint(1, 3)
        if mutation_type == 1:
            self.mutate_origin()
        elif mutation_type == 2:
            self.mutate_pos()
        elif mutation_type == 3:
            self.mutate_color()

    def clone(self):
        return copy.deepcopy(self)

    def __eq__(self, other):
        if other is None:
            return False
        return other.color == self.color and other.points == self.points

    def __str__(self):
        return "[Polygon | color : {} points : {}]".format(self.color, self.points)

    @staticmethod
    def get_random_color():
        if Constants.colors is not None:
            color = tuple(random.choice(Constants.colors))
        else:
            color = tuple(random.randint(0, 255) for i in range(3))
        return color + (random.randint(*Constants.alpha_range), )

    @staticmethod
    def get_random_origin():
        return np.array([random.randint(0, i) for i in Constants.image_size])

    @staticmethod
    def get_random_perimeter(polygon_class, points=3, **kwargs):
        perim = []
        for _ in range(points):
            perim.append(polygon_class.get_random_point(**kwargs))
        perim = np.array(perim)
        return perim
