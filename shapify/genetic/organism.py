import numpy as np
from PIL import Image, ImageDraw

from shapify.genetic.art_tools.polygon import Polygon


class Organism:
    def __init__(self, image_size, starting_polys=1, colors=None):
        self.image_size = image_size
        self.polygons = [Polygon.random(image_size[0], image_size[1], colors=colors) for _ in range(starting_polys)]

    def get_image(self):
        new_image = Image.new('RGB', self.image_size)
        image_draw = ImageDraw.Draw(new_image)

        for polygon in self.polygons:
            polygon.draw(image_draw)

        return new_image

    def calculate_fitness(self, target, organism_image=None):
        target_arr = np.asarray(target)
        if organism_image is None:
            organism_arr = np.asarray(self.get_image())
        else:
            organism_arr = np.asarray(organism_image)
        diff = target_arr - organism_arr
        normed_diff = np.linalg.norm(diff)
        return -normed_diff

    def breed(self, other):
        num_child_polys = round((len(self.polygons) + len(other.polygons)) / 2)
        parents = [self, other]

        child_polys = []

        for i in range(num_child_polys):
            cur_parent = parents[i % 2]
            if i < len(cur_parent.polygons):
                child_polys.append(cur_parent.polygons[i].clone())
            else:
                child_polys.append(parents.polygons[(i + 1) % 2][i].clone())

        child = Organism(self.image_size, starting_polys=0)
        child.polygons = child_polys
        return child
