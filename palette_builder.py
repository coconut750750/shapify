import numpy as np
from PIL import Image
import sys
import colorsys

from pixel_kmeans import PixelKMeans

class PaletteBuilder:
    def __init__(self, img):
        self.img = img

    def get_new_palette(self):
        frequent_pix = self.get_frequent_pix(num_pix=200)
        kmeans = PixelKMeans(frequent_pix, k=5)
        return kmeans.run()

    def get_frequent_pix(self, num_pix=-1):
        """
        Return pixels in descending order of frequency
        """
        arr = np.asarray(self.img)
        hex_pix = self.to_hex(arr)
        unique_pix, indicies = np.unique(hex_pix.ravel(), return_inverse=True)
        unique_pix = unique_pix.view(arr.dtype).reshape(-1, arr.shape[-1])
        count = np.bincount(indicies)
        order = np.argsort(count)
        freq_pix = unique_pix[order[::-1]]
        if num_pix != -1:
            return freq_pix[:num_pix]
        else:
            return freq_pix

    def to_hex(self, arr):
        arr = np.ascontiguousarray(arr)
        return arr.view(np.dtype((np.void, arr.dtype.itemsize * arr.shape[-1])))

    @staticmethod
    def show_palette(palette, square_size=100):
        n_colors = len(palette)
        palette_pic = Image.new('RGB', (square_size * n_colors, square_size))
        pix = palette_pic.load()
        for c in range(n_colors):
            for i in range(square_size * c, square_size * (c + 1)):
                for j in range(square_size):
                    pix[i,j] = tuple(palette[c])
        palette_pic.show()


if __name__ == '__main__':
    pic_name = sys.argv[1]
    img = Image.open(pic_name, 'r').convert('RGB')
    pb = PaletteBuilder(img)
    palette = pb.get_new_palette()
    PaletteBuilder.show_palette(palette)
