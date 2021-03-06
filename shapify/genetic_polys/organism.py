import copy
import random

from shapify.tools.env_constants import Constants

class Organism:
    def __init__(self, color=None, origin=None, points=None):
        self.color = Organism.get_random_color() if color is None else color
        self.origin = Organism.get_random_origin() if origin is None else origin
        self.points = Organism.get_random_points(self.origin) if points is None else points

    def draw(self, image_draw):
        image_draw.polygon(self.points, fill=self.color)

    def mutate_pos(self):
        self.points = Polygon.get_random_points(self.origin)

    def mutate_color(self):
        self.color = Polygon.get_random_color()

    def __eq__(self, other):
        if type(other) != Polygon:
            return False
        return other.color == self.color and other.points == self.points

    def __str__(self):
        return "[Organism | color : {} points : {}]".format(self.color, self.points)

    @staticmethod
    def get_random_color():
        if Constants.colors is not None:
            color = tuple(random.choice(Constants.colors))
        else:
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            color = (r, g, b)
        return color + (random.randint(*Constants.alpha_range), )

    @staticmethod
    def get_random_origin():
        x = random.randint(0, Constants.image_size[0])
        y = random.randint(0, Constants.image_size[1])
        return (x, y)

    @staticmethod
    def get_random_points(origin, side=3):
        perim = []
        for i in range(side):
            x_radius = random.randint(-Constants.polygon_max_radius, Constants.polygon_max_radius)
            x = min(max(0, origin[0] + x_radius), Constants.image_size[0]);

            y_radius = random.randint(-Constants.polygon_max_radius, Constants.polygon_max_radius)
            y = min(max(0, origin[1] + y_radius), Constants.image_size[1]);

            perim.append((x, y))
        return perim
