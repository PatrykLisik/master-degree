from dataclasses import dataclass
import numpy as np
from tqdm import tqdm

GEN_SIZE = 10


@dataclass
class Genotype:
    gene: np.array = np.random.rand(GEN_SIZE) * np.pi
    # fitness: float = 0.0

    @property
    def fitness(self):
        return self.value()

    def value(self):
        return np.prod(np.sin(self.gene)) * 1000


current = Genotype()
start_one = Genotype(gene=current.gene.copy())
print(f"Start fit: {current.fitness}")

stop_treshshol = np.float64(999.999)
print(f"Stop fitness {stop_treshshol}")

bar = tqdm(range(10**10))

for i in bar:
    gen_to_change = np.random.randint(GEN_SIZE)
    new_one = Genotype(gene=current.gene.copy())
    new_one.gene[gen_to_change] += np.random.uniform(-0.2, 0.2)
    new_one.gene[gen_to_change] = np.min([np.pi, new_one.gene[gen_to_change]])
    new_one.gene[gen_to_change] = np.max([0, new_one.gene[gen_to_change]])

    # print(f"New one {new_one} fitness={new_one.fitness}")
    if new_one.fitness > current.fitness:
        current = new_one
        # print("Current change")
    if current.fitness >= stop_treshshol:
        print(f"Break fitness single {current.fitness}")
        print(f"Iteration single {i}")
        break
    bar.set_description(f"I: {i} fit: {current.fitness} ")

print("Single end\n\n\n\n")

current = start_one
bar = tqdm(range(10**10))

for i in bar:
    gen_to_change = np.random.randint(GEN_SIZE)
    new_one = Genotype(gene=current.gene.copy())
    for gen_to_change in range(new_one.gene.shape[0]):
        new_one.gene[gen_to_change] += np.random.uniform(-0.2, 0.2)
        new_one.gene[gen_to_change] = np.min([np.pi, new_one.gene[gen_to_change]])
        new_one.gene[gen_to_change] = np.max([0, new_one.gene[gen_to_change]])

    # print(f"New one {new_one} fitness={new_one.fitness}")
    if new_one.fitness > current.fitness:
        current = new_one
        # print("Current change")

    bar.set_description(f"I: {i} fit: {current.fitness} ")

    if current.fitness >= stop_treshshol:
        print(f"Break fitness {current.fitness}")
        print(f"Iteration {i}")
        break
