#
# Geometric Differential Evolution
#

import random, copy

### POPULATION LEVEL ###

def gde_search():
    population = create_pop()
    global_best, global_best_fitness = get_best_pop(population)
    print global_best_fitness
    for _ in range(NUM_GENERATIONS):
        population_X1 = random.sample(population, POPULATION_SIZE)
        population_X2 = random.sample(population, POPULATION_SIZE)
        population_X3 = random.sample(population, POPULATION_SIZE)
        population_E = convex_combination_pop(population_X1, population_X3)
        population_U = extension_ray_recombination_pop(population_X2, population_E)
        population_V = convex_combination_pop(population_U, population)
        population = selection_pop(population_V, population)
        global_best, global_best_fitness = get_best_pop(population)
        print global_best_fitness
    return (global_best, global_best_fitness) 

### INDIVIDUAL LEVEL ###

def create_pop():
    return [ create_ind() for _ in range(POPULATION_SIZE) ]

def get_best_pop(population):
    best_ind = max(population, key=evaluate_ind)
    return best_ind, evaluate_ind(best_ind)

def convex_combination_pop(pop1, pop2):
    return [ convex_combination_ind([ind1, ind2]) for (ind1, ind2) in zip(pop1, pop2) ]

def extension_ray_recombination_pop(pop1, pop2):
    return [ extension_ray_recombination_ind(ind1, ind2) for (ind1, ind2) in zip(pop1, pop2) ]

def selection_pop(pop1, pop2):
    return [ max(ind1, ind2, key=evaluate_ind) for (ind1, ind2) in zip(pop1, pop2) ]

### REPRESENTATION LEVEL ###

def create_ind():
    return [ random.randint(0, 1) for _ in range(INDIVIDUAL_SIZE) ]

def evaluate_ind(individual): #one_max
    return sum(individual)

def convex_combination_ind(mating_pool):
    transposed_mating_pool=zip(*mating_pool)
    return map(random.choice, transposed_mating_pool)

def extension_ray_recombination_ind(string1, string2):
    hd = hamming_distance(string1, string2)
    bit_filp_probability = 1.0/2 * hd / (INDIVIDUAL_SIZE - hd) 
    return [ 1-bit2 if bit2==bit1 and random.random()<bit_filp_probability else bit2 for (bit1, bit2) in zip(string1,string2) ]

def hamming_distance(string1, string2):
    return sum([bit1<>bit2 for (bit1, bit2) in zip(string1,string2)])

### EXPERIMENTS ###

NUM_GENERATIONS = 250
POPULATION_SIZE = 25
INDIVIDUAL_SIZE = 100

print gde_search()
