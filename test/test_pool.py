"""
Testing module for Pool
"""
from PIL import Image

from shapify.genetic.pool import Pool


class TestPool:
    def setup_method(self):
        self.image = Image.open('test.png', 'r').convert('RGB')
        self.pool = Pool(self.image, total_pop=10)
        self.pool.seed()

    def test_pool_seed(self):
        best = self.pool.get_best()
        best.show()

    def test_pool_weed(self):
        next_gen = self.pool.weed()
        assert len(next_gen) == self.pool.total_pop // 2

        next_gen[0].get_image().show()
