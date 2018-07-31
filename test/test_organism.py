"""
Testing module for Organism
"""

import numpy as np
from PIL import Image

from shapify.tools.env_constants import Constants
from shapify.genetic_image.organism import Organism
from shapify.palette.palette_builder import PaletteBuilder


class TestOrganism:
    def setup_class(cls):
        cls.image = Image.open('test.png', 'r').convert('RGB')
        pb = PaletteBuilder(TestOrganism.image)
        cls.palette = pb.get_new_palette()
        cls.image_size = cls.image.size
        Constants.init(cls.palette, cls.image_size)

    def test_simple_organism(self):
        o1 = Organism(starting_polys=2)
        o2 = Organism(starting_polys=2)
        child = o1.breed(o2)
        assert child.polygons[0] == o1.polygons[0]
        assert child.polygons[1] == o2.polygons[1]

    def test_simple_organism_draw(self):
        o1 = Organism(starting_polys=10)
        o1.get_image().show()