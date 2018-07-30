from shapify.genetic.organism import Organism
from shapify.palette.palette_builder import PaletteBuilder


class Pool:
    def __init__(self, target,
                 starting_pop=100,
                 mutation_rate=0.25,
                 generations=100):
        self.target = target
        self.starting_pop = 100
        self.mutation_rate = mutation_rate
        self.generations = generations

        pb = PaletteBuilder(self.target)
        self.palette = pb.get_new_palette()

        self.image_size = self.target.size
        self.organisms = [Organism(self.image_size, colors=self.palette) for i in range(starting_pop)]

    def get_organism_image(self, organism_index):
        return self.organisms[organism_index].get_image()

    def get_organism_fitness(self, organism_index):
        return self.organisms[organism_index].calculate_fitness(self.target)

    def get_best_organism(self):
        best = 0
        max_fitness = self.organisms[best].calculate_fitness(self.target)

        for i, organism in enumerate(self.organisms[1:]):
            fitness = organism.calculate_fitness(self.target)
            if fitness > max_fitness:
                max_fitness = fitness
                best = i

        return self.organisms[i]

    def get_best(self):
        return self.get_best_organism().get_image()
