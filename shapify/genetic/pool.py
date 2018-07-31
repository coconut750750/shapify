import random

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

    def seed(self):
        self.population = [Organism(self.image_size, colors=self.palette) for i in range(self.total_pop)]

    def fitness(self, organism):
        return organism.calculate_fitness(self.target)

    def weed(self, top_percent=0.4, lucky_percent=0.1):
        top = int(len(self.population) * top_percent)
        lucky = int(len(self.population) * lucky_percent)

        pop_sorted = sorted(self.population, key=self.fitness)
        pop_sorted.reverse()
        return pop_sorted[:top] + random.sample(self.population[top:], lucky)

    def breed(self, old_pop):
        num_children = self.total_pop - len(old_pop)
        new_pop = []

        for i in range(num_children):
            random_parents = random.sample(old_pop, 2)
            new_pop.append(random_parents[0].bread(random_parents[1]))

        return old_pop + new_pop

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
