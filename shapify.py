import sys
from PIL import Image

from shapify.genetic_image.pool import Pool
from shapify.palette.palette_builder import PaletteBuilder


if __name__ == '__main__':
    pic_name = 'test.png'
    image = Image.open(pic_name, 'r').convert('RGB')
    if len(sys.argv) > 1:
        pool = Pool.load(sys.argv[1])
    else:
        pool = Pool(image, total_pop=100)
 
    best_img = pool.run(1)
    best_img.show()
    last = pool.population[-1].get_image()
    last.show()
    pool.save('pool.dat')
 