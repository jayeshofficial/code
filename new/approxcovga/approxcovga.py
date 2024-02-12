import time
import argparse
import random
import os
import math
import sys

def getTuples_rec(lst, sizeLeft, trieNode, count, comb):
    if sizeLeft == 1:
        for x in lst:
            if x not in trieNode: 
                trieNode[x] = True
                count[0] += 1
    else:
        for i in range(len(lst) - sizeLeft + 1):
            if lst[i] not in trieNode:
                trieNode[lst[i]] = {}
            trieNodeNew = trieNode[lst[i]]
            combNew = comb[:] + [lst[i]]
            getTuples_rec(lst[i+1:], sizeLeft - 1, trieNodeNew, count, combNew)

def check_coverage(samplefile, size):
    trie = {}
    count = [0]
    with open(samplefile, "r") as f:
        for line in f:
            s = list(map(int, line.strip().split(',')[1].strip().split(' ')))
            getTuples_rec(s, size, trie, count, [])
    countRes = count[0]
    print("Number of combinations " + str(countRes))
    return countRes

def cnk(n, k):
    res = 1
    for i in range(k):
        res *= n - i
    for i in range(k):
        res /= (i + 1)
    return res

# Genetic Algorithm Functions
def initialize_population(pop_size, nvars, size):
    return [tuple(sorted(random.sample(range(1, nvars+1), size))) for _ in range(pop_size)]

def fitness(individual, data):
    score = 0
    for d in data:
        if set(individual).intersection(d):
            score += 1
    return score

def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    offspring1 = parent1[:crossover_point] + parent2[crossover_point:]
    offspring2 = parent2[:crossover_point] + parent1[crossover_point:]
    return tuple(sorted(offspring1)), tuple(sorted(offspring2))

def mutate(individual):
    idx = random.randint(0, len(individual) - 1)
    mutate_value = random.choice(range(1, max(individual) + 1))
    new_individual = list(individual)
    new_individual[idx] = mutate_value
    return tuple(sorted(new_individual))

def select(population, data):
    tournament_size = 5
    tournament = random.sample(population, tournament_size)
    tournament.sort(key=lambda ind: fitness(ind, data), reverse=True)
    return tournament[0], tournament[1]

def genetic_algorithm_coverage(samplefile, size, population_size, generations):
    with open(samplefile, "r") as f:
        nvars = len(f.readline().strip().split(',')[1].strip().split(' '))

    population = initialize_population(population_size, nvars, size)

    data = []
    with open(samplefile, "r") as f:
        for line in f:
            data.append(tuple(map(int, line.strip().split(',')[1].strip().split(' '))))

    for _ in range(generations):
        new_population = []
        for _ in range(population_size // 2):
            parent1, parent2 = select(population, data)
            offspring1, offspring2 = crossover(parent1, parent2)
            new_population.extend([mutate(offspring1), mutate(offspring2)])
        population = new_population

    final_coverage = sum(fitness(ind, data) for ind in population) / population_size
    print("Estimated coverage with GA: " + str(final_coverage))
    return final_coverage

def run(samples, twise, isApprox, population_size, generations):
    start = time.time()
    if isApprox:
        genetic_algorithm_coverage(samples, twise, population_size, generations)
    else:
        check_coverage(samples, twise)
    print("Time taken: " + str(time.time() - start))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('samples', type=str, default="", help='Input file with samples')
    parser.add_argument("--twise", type=int, help='The size of combinations', required=True)
    parser.add_argument("--approximate", action='store_true', help="Uses a genetic algorithm for estimation", dest='apprx')
    parser.add_argument("--pop_size", type=int, default=50, help="Population size for GA")
    parser.add_argument("--generations", type=int, default=100, help="Number of generations for GA")
    
    args = parser.parse_args()
    run(args.samples, args.twise, args.apprx, args.pop_size, args.generations)

