import pickle
import random
import pickle

from PIL import Image 

from PIL import Image

from shapify.tools.env_constants import Constants
from shapify.genetic_image.organism import Organism
from shapify.palette.palette_builder import PaletteBuilder
from shapify.genetic_image.art_tools.polar_polygon import PolarPolygon
from shapify.genetic_image.art_tools.cartesian_polygon import CartesianPolygon


class Pool:
    def __init__(self, target,
                 total_pop=100,
                 mutation_rate=0.3):
        self.target = target
        self.total_pop = total_pop
        self.mutation_rate = mutation_rate
        self.generation = 0

        pb = PaletteBuilder(self.target, colors=10, palette_type='kmeans')
        self.palette = pb.get_new_palette()
        self.image_size = self.target.size
        Constants.init(self.palette, self.image_size)

        self.population = []
        self.seed()

    def run(self, generations=100):
        for i in range(generations):
            self.generation += 1
            self.weed()
            self.breed()
            self.mutate()
            print('Generation {}'.format(self.generation))
        print('Best fitness: {}'.format(self.get_best_organism()[1]))
        return self.get_best()

    def seed(self):
        self.population = [Organism(CartesianPolygon) for i in range(self.total_pop)]

    def fitness(self, organism):
        return organism.calculate_fitness(self.target)

    def weed(self, top_percent=0.3, lucky_percent=0.2):
        top = int(len(self.population) * top_percent)
        lucky = int(len(self.population) * lucky_percent)

        pop_sorted = sorted(self.population, key=self.fitness)
        self.population = pop_sorted[-top:] + random.sample(pop_sorted[:-top], lucky)
        return self.population

    def breed(self):
        num_children = self.total_pop - len(self.population)
        new_pop = []

        for i in range(num_children):
            random_parents = random.sample(self.population, 2)
            child = random_parents[0].breed(random_parents[1])
            child.mutate()
            new_pop.append(child)

        self.population += new_pop
        return self.population

    def mutate(self):
        for organism in self.population[1:]:
            if random.random() < self.mutation_rate:
                organism.mutate()
        return self.population

    def get_best_organism(self):
        best = 0
        max_fitness = self.population[best].calculate_fitness(self.target)

        for i, organism in enumerate(self.population[1:]):
            fitness = organism.calculate_fitness(self.target)
            if fitness > max_fitness:
                max_fitness = fitness
                best = i

        return self.population[best], max_fitness

    def get_best(self):
        return self.get_best_organism()[0].get_image()

    def get_image(self, i):
        return self.population[i].get_image()

    def save(self, filename): 
        with open(filename, 'wb') as f: 
            self.target = self.target.tobytes() 
            pickle.dump(self, f) 
 
    @staticmethod 
    def load(filename): 
        with open(filename, 'rb') as f: 
            pool = pickle.load(f) 
            pool.target = Image.frombytes('RGB', pool.image_size, pool.target) 
            Constants.init(pool.palette, pool.image_size) 
            return pool 
