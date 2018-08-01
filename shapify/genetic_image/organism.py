import numpy as np
from PIL import Image, ImageDraw
import random

from shapify.tools.env_constants import Constants
from shapify.genetic_image.art_tools.polygon import Polygon


class Organism:
    def __init__(self, num_polys=50):
        self.polygons = [Polygon.random() for _ in range(num_polys)]

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

        child = Organism(num_polys=0)
        child.polygons = child_polys

        child.mutate()
        return child

    # def mutate(self):
    #     mutation_type = random.randint(1, 4)
    #     if mutation_type == 1: # add poly
    #         self.polygons.append(Polygon.random())
    #     elif mutation_type == 2: # move polys
    #         self.mutate_poly(Polygon.mutate_pos)
    #     elif mutation_type == 3: # remove poly
    #         to_remove = random.randint(0, len(self.polygons) - 1)
    #         del self.polygons[to_remove]
    #     elif mutation_type == 4: # change color
    #         self.mutate_poly(Polygon.mutate_color)

    def mutate(self):
        mutation_type = random.randint(1, 4)
        if mutation_type == 1: # move polys
            self.mutate_poly(Polygon.mutate_pos)
        elif mutation_type == 2: # change color
            self.mutate_poly(Polygon.mutate_color)
        elif mutation_type == 3: # add poly point
            self.mutate_poly(Polygon.add_point)
        elif mutation_type == 4: # remove poly point
            self.mutate_poly(Polygon.remove_point)

    def mutate_poly(self, mutation):
        for i, _ in enumerate(self.polygons):
            if random.random() < 0.5:
                mutation(self.polygons[i])
