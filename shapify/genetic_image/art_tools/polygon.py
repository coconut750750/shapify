import copy
import math
import numpy as np
import random

from shapify.genetic_image.art_tools.polar import to_cartesian, sort_polar, sorted_polar_insert
from shapify.tools.env_constants import Constants


class Polygon:
    def __init__(self, color, origin=None, polar_points=None):
        self.color = color
        self.origin = origin
        self.polar_points = polar_points

    def draw(self, image_draw):
        cartesian = [tuple(i) for i in to_cartesian(self.polar_points, self.origin)]
        image_draw.polygon(cartesian, fill=self.color)

    def mutate_origin(self):
        x_delta = random.randint(0, Constants.polygon_max_shift) * random.randint(-1, 1)
        y_delta = random.randint(0, Constants.polygon_max_shift) * random.randint(-1, 1)
        self.origin[0] = min(max(0, self.origin[0] + x_delta), Constants.image_size[0])
        self.origin[1] = min(max(0, self.origin[1] + y_delta), Constants.image_size[1])

    def mutate_pos(self):
        n_points = len(self.polar_points)
        to_move = random.randint(0, n_points - 1)
        if random.random() < 0.5:
            r_delta = random.randint(0, Constants.polygon_max_shift) * random.randint(-1, 1)
            new_r = max(1, self.polar_points[to_move][0] + r_delta)
            self.polar_points[to_move][0] = new_r
        else: # pick new theta in between neighboring points
            lower = 0 if to_move == 0 else self.polar_points[to_move - 1][1]
            upper = 360 if to_move == n_points - 1 else self.polar_points[to_move + 1][1]
            if upper - lower < 2:
                return
            new_theta = random.randint(lower + 1, upper - 1)
            self.polar_points[to_move][1] = new_theta

    def mutate_color(self):
        self.color = Polygon.get_random_color()

    def add_point(self):
        new_point = Polygon.get_random_point()
        self.polar_points = sorted_polar_insert(self.polar_points, new_point)

    def remove_point(self):
        if self.polar_points.shape[0] > 3:
            to_remove = random.randint(0, len(self.polar_points) - 1)
            left = self.polar_points[: to_remove]
            right = self.polar_points[to_remove + 1:]
            self.polar_points = np.append(left, right, axis=0)

    def mutate(self):
        mutation_type = random.randint(1, 5)
        if mutation_type == 1:
            self.mutate_origin()
        elif mutation_type == 2:
            self.mutate_pos()
        elif mutation_type == 3:
            self.mutate_color()
        elif mutation_type == 4:
            self.add_point()
        elif mutation_type == 5:
            self.remove_point()

    def clone(self):
        return copy.deepcopy(self)

    def __eq__(self, other):
        if type(other) != Polygon:
            return False
        return other.color == self.color and other.points == self.polar_points

    def __str__(self):
        return "[Polygon | color : {} points : {}]".format(self.color, self.polar_points)

    @staticmethod
    def random(sides=3):
        color = Polygon.get_random_color()
        origin = Polygon.get_random_origin()
        perim = Polygon.get_random_perimeter()

        return Polygon(color, origin, perim)

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
    def get_random_perimeter(points=3):
        perim = []
        for _ in range(points):
            perim.append(Polygon.get_random_point())
        perim = np.array(perim)
        return sort_polar(perim)

    @staticmethod
    def get_random_point():
        r = random.randint(0, Constants.polygon_max_radius)
        theta = random.randint(0, 360)
        return np.array([r, theta])
