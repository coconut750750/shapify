"""
Testing module for Organism
"""

import numpy as np
from PIL import Image

from shapify.tools.env_constants import Constants
from shapify.genetic_image.art_tools.cartesian_polygon import CartesianPolygon
from shapify.genetic_image.organism import Organism
from shapify.palette.palette_builder import PaletteBuilder


class TestOrganism:
    def setup_class(cls):
        cls.image = Image.open('test.png', 'r').convert('RGB')
        pb = PaletteBuilder(TestOrganism.image)
        cls.palette = pb.get_new_palette()
        cls.image_size = cls.image.size
        Constants.init(cls.palette, cls.image_size)

    def test_organism_breed(self):
        o1 = Organism(CartesianPolygon, starting_polys=2)
        o2 = Organism(CartesianPolygon, starting_polys=2)
        child = o1.breed(o2)
        assert child.polygons[0] == o1.polygons[0]
        assert child.polygons[1] == o2.polygons[1]
