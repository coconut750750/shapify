from numpy.linalg import norm as npnorm
 
 
class Constants:
    @classmethod
    def init(cls, colors, image_size, 
             max_shift_percent=0.1,
             max_radius_percent=0.1,
             alpha_range=(64, 191)):
        cls.colors = colors
        cls.image_size = image_size
 
        cls.polygon_max_shift = npnorm(image_size) * max_shift_percent
        cls.polygon_max_radius = int(npnorm(image_size) * max_radius_percent)
        cls.alpha_range = alpha_range
