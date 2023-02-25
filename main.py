import random


def knapsack_genetic(weights, values, capacity, population_size, num_generations, mutation_rate):
    if len(weights) != len(values):
        raise ValueError("The lengths of weights and values lists do not match.")

    # Initialize population
    population = [[random.randint(0, 1) for _ in range(len(weights))] for _ in range(population_size)]

    # Evaluate fitness of initial population
    fitness = [knapsack_fitness(individual, weights, values, capacity) for individual in population]

    # Keep track of the best solution found so far
    best_fitness = max(fitness)
    best_individual = population[fitness.index(best_fitness)]

    # Main loop
    for generation in range(num_generations):
        # Select two individuals to mate based on fitness
        idx1 = random.choices(range(population_size), weights=fitness)[0]
        idx2 = random.choices(range(population_size), weights=fitness)[0]
        while idx2 == idx1:
            idx2 = random.choices(range(population_size), weights=fitness)[0]

        # Mate the two individuals
        offspring = knapsack_crossover(population[idx1], population[idx2])

        # Mutate the offspring
        knapsack_mutate(offspring, mutation_rate)

        # Evaluate fitness of the offspring
        offspring_fitness = knapsack_fitness(offspring, weights, values, capacity)

        # Replace a random individual in the population with the offspring if its fitness is higher
        idx = random.randint(0, population_size - 1)
        if offspring_fitness > fitness[idx]:
            population[idx] = offspring
            fitness[idx] = offspring_fitness

        # Update best solution found so far
        if offspring_fitness > best_fitness:
            best_fitness = offspring_fitness
            best_individual = offspring

    return best_fitness, best_individual


def knapsack_fitness(individual, weights, values, capacity):
    # Calculate the total weight and value of the individual
    total_weight = sum(weight * item for weight, item in zip(weights, individual))
    total_value = sum(value * item for value, item in zip(values, individual))

    # If the total weight exceeds the capacity, return a fitness of zero
    if total_weight > capacity:
        return 0

    # Otherwise, return the total value as fitness
    return total_value


def knapsack_crossover(parent1, parent2):
    # Perform uniform crossover
    offspring = [parent1[i] if random.random() < 0.5 else parent2[i] for i in range(len(parent1))]
    return offspring


def knapsack_mutate(individual, mutation_rate):
    # Mutate each bit with probability mutation_rate
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = 1 - individual[i]

weights = [10, 300, 1, 200, 100]
values = [1000, 4000, 5000, 5000, 2000]
capacity = 400
population_size = 50
num_generations = 100
mutation_rate = 0.01

best_value, best_solution = knapsack_genetic(weights, values, capacity, population_size, num_generations, mutation_rate)

print("Best solution found: ", best_solution)
print("Total value: ", best_value)
