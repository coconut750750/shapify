import random

from shapify.genetic.env_constants import Constants
from shapify.genetic.organism import Organism
from shapify.palette.palette_builder import PaletteBuilder


class Pool:
    def __init__(self, target,
                 total_pop=100,
                 mutation_rate=0.25,
                 generations=100):
        self.target = target
        self.total_pop = 100
        self.mutation_rate = mutation_rate
        self.generations = generations

        pb = PaletteBuilder(self.target)
        self.palette = pb.get_new_palette()

        self.image_size = self.target.size
        self.population = []

        Constants.init(self.palette, self.image_size)

    def seed(self):
        self.population = [Organism() for i in range(self.total_pop)]

    def fitness(self, organism):
        return organism.calculate_fitness(self.target)

    def weed(self, top_percent=0.4, lucky_percent=0.1):
        top = int(len(self.population) * top_percent)
        lucky = int(len(self.population) * lucky_percent)

        pop_sorted = sorted(self.population, key=self.fitness)
        pop_sorted.reverse()
        self.population = pop_sorted[:top] + random.sample(self.population[top:], lucky)
        return self.population

    def breed(self):
        num_children = self.total_pop - len(self.population)
        new_pop = []

        for i in range(num_children):
            random_parents = random.sample(self.population, 2)
            new_pop.append(random_parents[0].breed(random_parents[1]))

        self.population += new_pop
        return self.population

    def mutate(self):
        for organism in self.population:
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

        return self.population[i]

    def get_best(self):
        return self.get_best_organism().get_image()
