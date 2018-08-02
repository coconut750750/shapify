import numpy as np

def to_cartesian(polar_points, origin=(0,0)):
    r = polar_points[...,0]
    theta = np.deg2rad(polar_points[...,1])
    x = np.array([r * np.cos(theta)])
    y = np.array([r * np.sin(theta)])
    return np.append(x.T, y.T, axis=1) + origin


def sort_polar(points):
    return np.array(sorted(points, key=lambda x: x[1]))


def sort_by_polar(cartesian_points):
    n_points = len(cartesian_points)
    centroid = cartesian_points.sum(axis=0) / n_points

    key = lambda p: np.arctan2(*(p - centroid)[::-1])
    return np.array(sorted(cartesian_points, key=key))
