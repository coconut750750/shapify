"""
Testing module for Pool
"""
from PIL import Image

from shapify.genetic_image.pool import Pool


class TestPool:
    def setup_method(self):
        self.image = Image.open('test.png', 'r').convert('RGB')
        self.pool = Pool(self.image, total_pop=6)

    def test_pool_weed(self):
        next_gen = self.pool.weed(top_percent=0.5, lucky_percent=0)
        assert len(next_gen) == self.pool.total_pop // 2

    def test_pool_breed(self):
        orig = self.pool.weed(top_percent=0.5, lucky_percent=0)
        old_len = len(orig)
        new = self.pool.breed()
        assert len(new) == old_len * 2

    def test_pool_mutate(self):
        mutate_pop = self.pool.mutate()

    def test_pool_run(self):
        best_img = self.pool.run(1)
