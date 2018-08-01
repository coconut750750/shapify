import numpy as np
from PIL import Image, ImageDraw
import random

from shapify.tools.env_constants import Constants


class Organism:
    def __init__(self, poly_type, starting_polys=50, max_polys=100):
        self.poly_type = poly_type
        self.max_polys = max_polys
        self.polygons = [self.poly_type.random() for _ in range(starting_polys)]

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
                child_polys.append(parents[(i + 1) % 2].polygons[i].clone())

        child = Organism(self.poly_type, starting_polys=0, max_polys=self.max_polys)
        child.polygons = child_polys

        child.mutate()
        return child

    def add_poly(self):
        if len(self.polygons) < self.max_polys:
            to_add = random.randint(0, len(self.polygons))
            self.polygons.insert(to_add, self.poly_type.random())

    def remove_poly(self):
        if len(self.polygons) > 1:
            to_remove = random.randint(0, len(self.polygons) - 1)
            del self.polygons[to_remove]

    def mutate_poly(self):
        to_mutate = random.randint(0, len(self.polygons) - 1)
        self.polygons[to_mutate].mutate()

    def randomize_polys(self):
        random.shuffle(self.polygons)

    def mutate(self):
        mutation_type = random.randint(1, 4)
        if mutation_type == 1:
            self.add_poly()
        elif mutation_type == 2:
            self.remove_poly()
        elif mutation_type == 3:
            self.mutate_poly()
        elif mutation_type == 4:
            self.randomize_polys
