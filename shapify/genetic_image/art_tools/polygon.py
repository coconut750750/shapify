import copy
import random

from shapify.tools.env_constants import Constants

class Polygon:
    def __init__(self, color, origin=None, points=None):
        self.color = color
        self.origin = origin
        self.points = points

    def draw(self, image_draw):
        image_draw.polygon(self.points, fill=self.color)

    def mutate_pos(self):
        to_move = random.randint(0, len(self.points) - 1)
        x_delta = random.randint(0, Constants.polygon_max_shift) * random.randint(-1, 1)
        y_delta = random.randint(0, Constants.polygon_max_shift) * random.randint(-1, 1)
        new_point = (self.points[to_move][0] + x_delta, self.points[to_move][1] + y_delta)
        self.points[to_move] = new_point

    def mutate_color(self):
        self.color = Polygon.get_random_color()

    def add_point(self):
        to_add = random.randint(1, len(self.points) - 1)
        a = self.points[to_add - 1]
        b = self.points[to_add]
        x = (a[0] + b[0]) // 2
        y = (a[1] + b[1]) // 2
        self.points.insert(to_add, (x, y))

    def remove_point(self):
        if len(self.points) > 3:
            to_remove = random.randint(0, len(self.points) - 1)
            del self.points[to_remove]

    def clone(self):
        return copy.deepcopy(self)

    def __eq__(self, other):
        if type(other) != Polygon:
            return False
        return other.color == self.color and other.points == self.points

    def __str__(self):
        return "[Polygon | color : {} points : {}]".format(self.color, self.points)

    @staticmethod
    def random(sides=3):
        color = Polygon.get_random_color()
        origin = Polygon.get_random_origin()
        perim = Polygon.get_random_points(origin)

        return Polygon(color, origin, perim)

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
    def get_random_points(origin, points=3):
        perim = []
        for i in range(points):
            x_radius = random.randint(-Constants.polygon_max_radius, Constants.polygon_max_radius)
            x = min(max(0, origin[0] + x_radius), Constants.image_size[0]);

            y_radius = random.randint(-Constants.polygon_max_radius, Constants.polygon_max_radius)
            y = min(max(0, origin[1] + y_radius), Constants.image_size[1]);

            perim.append((x, y))
        return perim
