import copy
import random

from shapify.genetic.env_constants import Constants

class Polygon:
    def __init__(self, color, points):
        self.color = color
        self.points = points

    def draw(self, image_draw):
        image_draw.polygon(self.points, fill=self.color)

    def clone(self):
        return copy.deepcopy(self)

    def __eq__(self, other):
        if type(other) != Polygon:
            return False
        return other.color == self.color and other.points == self.points

    @staticmethod
    def random(sides=3):
        if Constants.colors is not None:
            color = tuple(random.choice(Constants.colors))
        else:
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            color = (r, g, b)
        color += (random.randint(25, 50), )

        points = []
        for i in range(sides):
            x = random.randint(0, Constants.image_size[0])
            y = random.randint(0, Constants.image_size[1])
            points.append((x, y))

        return Polygon(color, points)
