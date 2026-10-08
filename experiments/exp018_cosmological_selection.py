import random
import math

def calculate_black_holes(G, Lambda, Alpha):
    # Optimal target for this mathematical model: G=1.0, Lambda=0.0, Alpha=0.5
    g_efficiency = math.exp(-((G - 1.0) ** 2) / 0.1)
    lambda_efficiency = math.exp(-(Lambda ** 2) / 0.05)
    alpha_efficiency = math.exp(-((Alpha - 0.5) ** 2) / 0.1)
    
    base_production = 1000
    bh_count = int(base_production * g_efficiency * lambda_efficiency * alpha_efficiency)
    return max(0, bh_count)

def run_cosmological_selection():
    print("==================================================")
    print("PURE MATH: COSMOLOGICAL NATURAL SELECTION")
    print("==================================================")
    
    # Generation 0: A population of 20 random, unoptimized starting universes
    current_generation = [{
        "G": random.uniform(0.5, 1.5),
        "Lambda": random.uniform(0.0, 0.5),
        "Alpha": random.uniform(0.2, 0.8)
    } for _ in range(20)]
    
    generations_to_run = 20
    mutation_rate = 0.05
    
    for gen in range(generations_to_run):
        total_universes = len(current_generation)
        
        next_generation = []
        total_black_holes = 0
        
        avg_G = sum(u["G"] for u in current_generation) / total_universes
        avg_Lambda = sum(u["Lambda"] for u in current_generation) / total_universes
        avg_Alpha = sum(u["Alpha"] for u in current_generation) / total_universes
        
        for universe in current_generation:
            bh_count = calculate_black_holes(universe["G"], universe["Lambda"], universe["Alpha"])
            total_black_holes += bh_count
            
            for _ in range(bh_count):
                child = {
                    "G": max(0.01, universe["G"] + random.gauss(0, mutation_rate)),
                    "Lambda": max(0.0, universe["Lambda"] + random.gauss(0, mutation_rate)),
                    "Alpha": max(0.01, universe["Alpha"] + random.gauss(0, mutation_rate))
                }
                next_generation.append(child)
                
        # Population control 
        if len(next_generation) > 1000:
            next_generation = random.sample(next_generation, 1000)
            
        print(f"Gen {gen:02d} | Total Black Holes (Children Born): {total_black_holes:<6} | Avg G: {avg_G:.3f} | Avg Lambda: {avg_Lambda:.3f} | Avg Alpha: {avg_Alpha:.3f}")
        
        if not next_generation:
            print("Extinction: No black holes formed.")
            break
            
        current_generation = next_generation

if __name__ == "__main__":
    run_cosmological_selection()
