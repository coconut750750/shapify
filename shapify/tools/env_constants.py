from numpy.linalg import norm as npnorm
 
 
class Constants:
    @classmethod
    def init(cls, colors, image_size, 
             max_shift_percent=0.1,
             max_radius_percent=0.5,
             alpha_range=(127, 255),
             max_alpha_shift=5):
        cls.colors = colors
        cls.image_size = image_size

        cls.polygon_max_shift = int(npnorm(image_size) * max_shift_percent)
        cls.polygon_max_radius = int(npnorm(image_size) * max_radius_percent)
        cls.alpha_range = alpha_range
        cls.max_alpha_shift = max_alpha_shift
