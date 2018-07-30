import numpy as np
from PIL import Image
import sys
import colorsys

from shapify.palette.pixel_kmeans import PixelKMeans

class PaletteBuilder:
    def __init__(self, img, filename=None, colors=5):
        self.img = img
        self.colors = colors
        if not img and filename:
            self.img = Image.open(filename, mode='r').convert('RGB')

    def get_new_palette(self):
        frequent_pix = self.get_frequent_pix(num_pix=200)
        kmeans = PixelKMeans(frequent_pix, k=self.colors)
        palette = kmeans.run()
        return PaletteBuilder.sort_palette(palette)

    def get_frequent_pix(self, num_pix=-1):
        """
        Return pixels in descending order of frequency
        """
        arr = np.asarray(self.img)
        hex_pix = PaletteBuilder.to_void(arr)
        unique_pix, indicies = np.unique(hex_pix.ravel(), return_inverse=True)
        unique_pix = unique_pix.view(arr.dtype).reshape(-1, arr.shape[-1])
        count = np.bincount(indicies)
        order = np.argsort(count)
        freq_pix = unique_pix[order[::-1]]
        if num_pix != -1:
            return freq_pix[:num_pix]
        else:
            return freq_pix

    @staticmethod
    def to_void(arr):
        arr = np.ascontiguousarray(arr)
        return arr.view(np.dtype((np.void, arr.dtype.itemsize * arr.shape[-1])))

    @staticmethod
    def sort_palette(palette):
        sorted_palette = sorted(palette, key=lambda rgb: colorsys.rgb_to_hsv(*rgb))
        return np.array(sorted_palette)

    @staticmethod
    def create_palette(palette, square_size=100):
        n_colors = len(palette)
        palette_pic = Image.new('RGB', (square_size * n_colors, square_size))
        pix = palette_pic.load()
        for c in range(n_colors):
            for i in range(square_size * c, square_size * (c + 1)):
                for j in range(square_size):
                    pix[i,j] = tuple(palette[c])
        return palette_pic

    @staticmethod
    def show_palette(palette, square_size=100):
        palette_pic = PaletteBuilder.create_palette(palette, square_size=square_size)
        palette_pic.show()
