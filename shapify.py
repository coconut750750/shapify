import sys
from PIL import Image

from shapify.genetic_image.pool import Pool
from shapify.palette.palette_builder import PaletteBuilder


if __name__ == '__main__':
    pic_name = 'test2.png'
    image = Image.open(pic_name, 'r').convert('RGB')
    if len(sys.argv) > 1:
        pool = Pool.load(sys.argv[1])
    else:
        pool = Pool(image, total_pop=300)

    best_img = pool.run(0)
    best_img.show()

    # pool.get_image(0).show()
    # pool.get_image(50).show()
    # pool.get_image(100).show()
    # pool.get_image(150).show()

    pool.save('pool.dat')
 