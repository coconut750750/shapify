import numpy as np

def to_cartesian(polar_points, origin=(0,0)):
    r = polar_points[...,0]
    theta = np.deg2rad(polar_points[...,1])
    x = np.array([r * np.cos(theta)])
    y = np.array([r * np.sin(theta)])
    return np.append(x.T, y.T, axis=1) + origin
