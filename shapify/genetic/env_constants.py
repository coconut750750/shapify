from numpy.linalg import norm as npnorm


class Constants:
    @classmethod
    def init(cls, colors, image_size, max_shift_percent=0.1):
        cls.colors = colors
        cls.image_size = image_size

        cls.polygon_max_shift = npnorm(image_size) * max_shift_percent
