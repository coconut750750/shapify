from bisect import bisect_left
import numpy as np

def to_cartesian(polar_points, origin=(0,0)):
    r = polar_points[...,0]
    theta = np.deg2rad(polar_points[...,1])
    x = np.array([r * np.cos(theta)])
    y = np.array([r * np.sin(theta)])
    return np.append(x.T, y.T, axis=1) + origin

def sort_polar(points):
    return np.array(sorted(points, key=lambda x: x[1]))

def sorted_polar_insert(points, polar):
    keys = [x[1] for x in points]
    k = polar[1]
    i = bisect_left(keys, k)
    p = np.insert(points, i, polar, axis=0)
    return np.insert(points, i, polar, axis=0)
