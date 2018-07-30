"""
Testing module for Pool
"""
from PIL import Image

from shapify.genetic.pool import Pool


class TestPool:
    def setup_method(self):
        self.image = Image.open('test.png', 'r').convert('RGB')

    def test_simple_pool(self):
        pool = Pool(self.image, starting_pop=5)
        best = pool.get_best()
        best.show()

