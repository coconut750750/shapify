import random

class Polygon:
    def __init__(self, color, points):
        self.color = color
        self.points = points

    def draw(self, image_draw):
        image_draw.polygon(self.points, fill=self.color)

    @staticmethod
    def random(max_width, max_height, colors=None, sides=3):
        if colors is not None:
            color = tuple(random.choice(colors))
        else:
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            color = (r, g, b)
        color += (random.randint(25, 50), )

        points = []
        for i in range(sides):
            x = random.randint(0, max_width)
            y = random.randint(0, max_height)
            points.append((x, y))

        return Polygon(color, points)
