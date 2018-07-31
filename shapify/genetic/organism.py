import numpy as np
from PIL import Image, ImageDraw
import random

from shapify.genetic.env_constants import Constants
from shapify.genetic.art_tools.polygon import Polygon


class Organism:
    def __init__(self, starting_polys=100):
        self.polygons = [Polygon.random() for _ in range(starting_polys)]

    def get_image(self):
        new_image = Image.new('RGB', Constants.image_size)
        image_draw = ImageDraw.Draw(new_image, 'RGBA')

        for polygon in self.polygons:
            polygon.draw(image_draw)

        del image_draw

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

        child = Organism(starting_polys=0)
        child.polygons = child_polys
        return child

    def mutate(self):
        mutation_type = random.randint(1, 3)
        if mutation_type == 1: # add poly
            self.polygons.append(Polygon.random())
        elif mutation_type == 2: # move polys
            self.mutate_polys()
        else: # remove poly
            to_remove = random.randint(0, len(self.polygons) - 1)
            del self.polygons[to_remove]

    def mutate_polys(self):
        for i, _ in enumerate(self.polygons):
            if random.random() < 0.5:
                self.polygons[i].mutate()
