import sys
from PIL import Image

from shapify.genetic.pool import Pool


if __name__ == '__main__':
    if len(sys.argv) > 1:
        pic_name = sys.argv[1]
    else:
        pic_name = 'test.png'
    image = Image.open(pic_name, 'r').convert('RGB')
    pool = Pool(image, total_pop=500, generations=100)
    best_img = pool.run()
    best_img.show()
