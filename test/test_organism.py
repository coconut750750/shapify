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

        
        o = Organism(self.image_size, colors=palette)
        o.get_image().show()
