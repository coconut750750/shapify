"""
Testing module for palette builder
"""

import numpy as np
from PIL import Image

from shapify.palette.palette_builder import PaletteBuilder


class TestPaletteBuilder:
    def setup_method(self):
        self.palette_simple = [
            [0, 0, 0],
            [255, 255, 255],
            [255, 255, 255]
        ]
        self.pix_arr_simple = np.array([
            [[0, 0, 0], [1, 1, 1]],
            [[1, 1, 1], [0, 0, 0]]
        ])

        self.simple_image = PaletteBuilder.create_palette(self.palette_simple)

    def test_simple_image(self):
        pb = PaletteBuilder(self.simple_image)
        palette = pb.get_new_palette()
        assert (palette[0] == [0, 0, 0]).all()
        assert (palette[1] == [255, 255, 255]).all()

    def test_freq_pix(self):
        pb = PaletteBuilder(self.simple_image)
        freq_pix = pb.get_frequent_pix()
        assert (freq_pix[1] == [0, 0, 0]).all()
        assert (freq_pix[0] == [255, 255, 255]).all()

    def test_sort_palette(self):
        sorted = PaletteBuilder.sort_palette(self.palette_simple)
        assert (sorted[0] == [0, 0, 0]).all()
        assert (sorted[1] == [255, 255, 255]).all()
        assert (sorted[2] == [255, 255, 255]).all()

    def test_to_void(self):
        void_palette = PaletteBuilder.to_void(self.pix_arr_simple)
        assert void_palette.shape[0] == self.pix_arr_simple.shape[0]
        assert void_palette.shape[1] == self.pix_arr_simple.shape[1]
        assert void_palette.shape[2] == 1

