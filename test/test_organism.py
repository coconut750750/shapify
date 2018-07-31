"""
Testing module for Organism
"""

import numpy as np
from PIL import Image

from shapify.genetic.organism import Organism
from shapify.palette.palette_builder import PaletteBuilder


class TestOrganism:
    def setup_method(self):
        self.image = Image.open('test.png', 'r').convert('RGB')
        self.image_size = self.image.size

    def test_simple_organism(self):
        pb = PaletteBuilder(self.image)
        palette = pb.get_new_palette()

        o1 = Organism(self.image_size, starting_polys=2, colors=palette)
        o2 = Organism(self.image_size, starting_polys=2, colors=palette)
        child = o1.breed(o2)
        assert child.polygons[0] == o1.polygons[0]
        assert child.polygons[1] == o2.polygons[1]
