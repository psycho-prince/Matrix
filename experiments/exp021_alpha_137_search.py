import random
import math

def run_137_search():
    print("==================================================")
    print("PURE MATH: SEARCHING THE MULTIVERSE FOR '137'")
    print("==================================================")
    
    # The real-world Fine Structure Constant
    target_alpha = 1.0 / 137.035999
    
    # We simulate a universe's fitness. The closer Alpha is to 1/137, 
    # the more stable stars it forms, and thus the more black holes (children) it produces.
    def calculate_fitness(alpha):
        # Gaussian fitness curve peaking at the target_alpha
        return math.exp(-((alpha - target_alpha) ** 2) / 0.0001)

    # Gen 0: Start with 100 universes with completely random Alpha values between 0.1 and 1.0
    population = [random.uniform(0.1, 1.0) for _ in range(100)]
    
    max_generations = 5000
    mutation_rate = 0.01
    
    print(f"Targeting Alpha = {target_alpha:.8f} (1/137.035999)")
    print("Simulating multiverse generations...\n")
    
    found_generation = -1
    
    for gen in range(max_generations):
        # Calculate fitness for all universes
        fitness_scores = [calculate_fitness(alpha) for alpha in population]
        
        # Check if any universe has hit the '137' target (within 99.9% accuracy)
        best_alpha = min(population, key=lambda x: abs(x - target_alpha))
        if abs(best_alpha - target_alpha) < 0.00001:
            found_generation = gen
            print(f"\n[TARGET AQUIRED] Universe Iteration {gen:,} mathematically locked onto '137'!")
            print(f"Best Alpha in this generation: {best_alpha:.8f}")
            break
            
        # Log progress every 50 generations
        if gen % 50 == 0:
            avg_alpha = sum(population) / len(population)
            print(f"Generation {gen:<4} | Closest Alpha: {best_alpha:.8f} | Multiverse Avg: {avg_alpha:.8f}")
            
        # Reproduction (Survival of the fittest)
        next_generation = []
        for _ in range(len(population)):
            # Tournament selection (pick 2 random, the fitter one reproduces)
            parent1, parent2 = random.sample(list(zip(population, fitness_scores)), 2)
            winner_alpha = parent1[0] if parent1[1] > parent2[1] else parent2[0]
            
            # Mutate
            child_alpha = max(0.0001, winner_alpha + random.gauss(0, mutation_rate))
            next_generation.append(child_alpha)
            
        population = next_generation

    if found_generation == -1:
        print("\n[FAILED] The multiverse did not find 137 within the simulation limit.")
        
    print("\n==================================================")
    print("SIMULATION COMPLETE")
    print("==================================================")

if __name__ == "__main__":
    run_137_search()
