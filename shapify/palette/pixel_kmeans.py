import numpy as np
import pandas as pd


CLOSEST = 'closest'

class PixelKMeans:
    def __init__(self, pixels, k=3):
        self.pixels_df = pd.DataFrame(pixels, columns=['r', 'g', 'b'])
        self.starting_k = k
        self.k = k

    def run(self, max_iters=50):
        np.random.seed(1)
        centroids = self.initialize()
        prev_error = -1
        for i in range(max_iters):
            if len(centroids) < self.starting_k:
                self.add_centroids(centroids)
            error = self.assign(centroids)
            if prev_error == error:
                break
            centroids = self.update()
            prev_error = error
        return [list(map(int, i)) for i in set(tuple(x) for x in centroids)]

    def initialize(self):
        centroids = [
            [
                np.random.randint(0, 255),
                np.random.randint(0, 255),
                np.random.randint(0, 255)
            ] for i in range(self.k)
        ]
        return centroids

    def assign(self, centroids):
        dist_cols = [i for i in range(len(centroids))]
        for key, center in enumerate(centroids):
            dists = np.sqrt(
                (self.pixels_df['r'] - center[0]) ** 2 +
                (self.pixels_df['g'] - center[1]) ** 2 +
                (self.pixels_df['b'] - center[2]) ** 2
            )
            self.pixels_df[dist_cols[key]] = dists
        self.pixels_df[CLOSEST] = self.pixels_df.loc[:, dist_cols].idxmin(axis=1)
        return self.pixels_df[dist_cols].min(axis=1).max()

    def update(self):
        centroids = [
            [
                np.mean(self.pixels_df[self.pixels_df[CLOSEST] == i]['r']),
                np.mean(self.pixels_df[self.pixels_df[CLOSEST] == i]['g']),
                np.mean(self.pixels_df[self.pixels_df[CLOSEST] == i]['b']) 
            ] for i in range(self.k)
        ]
        return self.remove_nan_centroids(centroids)

    def remove_nan_centroids(self, centroids):
        new_centroids = []
        for centroid in centroids:
            if not np.isnan(centroid[0]):
                new_centroids.append(centroid)
        self.k = len(new_centroids)
        return new_centroids

    def add_centroids(self, centroids):
        dist_cols = [i for i in range(len(centroids))]
        df = self.pixels_df
        max_out = df.iloc[df[dist_cols].min(axis=1).idxmax()]
        centroids.append((max_out.r, max_out.g, max_out.b))

