import random
import csv
import os
from pathlib import Path

def clamp(val, min_val=0.0, max_val=1.0):
    return max(min_val, min(max_val, val))

def run_empirical_simulation():
    print("==================================================")
    print("GAL 1.0: THE FINAL EXTINCTION (200 MILLION YEARS)")
    print("==================================================")
    
    total_years = 200_000_000
    generation_length_years = 10_000
    total_generations = total_years // generation_length_years
    
    population_size = 1000
    mutation_rate = 0.02
    
    population = [[0.2, 0.2, 0.2] for _ in range(population_size)]
    history = []
    
    print(f"Simulating {total_generations:,} generations over {total_years:,} years...")
    
    for gen in range(total_generations):
        current_year = gen * generation_length_years
        
        req_thermal = 0.1
        req_radiation = 0.1
        req_efficiency = 0.1
        
        # 0-100M: The Historical Epochs
        if 39_000_000 <= current_year <= 45_000_000:
            req_radiation = 0.75
        elif 49_000_000 <= current_year <= 55_000_000:
            req_thermal = 0.85
            req_radiation = 0.50
        elif 80_000_000 <= current_year <= 100_000_000:
            req_efficiency = 0.90
            req_thermal = 0.05 
            
        # 100M - 130M: The Great Filter (Multi-crisis)
        elif 120_000_000 <= current_year <= 130_000_000:
            req_thermal = 0.85
            req_radiation = 0.85
            req_efficiency = 0.85
            
        # 150M - 200M: Absolute Heat Death (Slowly grinding to impossible 1.0)
        elif current_year >= 150_000_000:
            # Efficiency requirement scales from 0.90 to 1.00 as time goes on
            progress = (current_year - 150_000_000) / 50_000_000.0
            req_efficiency = 0.90 + (0.10 * progress)
            req_radiation = 0.90 # High cosmic radiation from decaying protons
        
        # Selection
        survivors = []
        for agent in population:
            score = 0
            if agent[0] >= req_thermal: score += 1
            if agent[1] >= req_radiation: score += 1
            if agent[2] >= req_efficiency: score += 1
            
            survival_chance = (score / 3.0) * 0.9 + 0.1 
            if random.random() < survival_chance:
                survivors.append(agent)
                
        if not survivors:
            print(f"\n[EXTINCTION EVENT] Population eradicated at Year {current_year:,}!")
            print(f"Final Requirements: Thermal={req_thermal:.2f}, Rad={req_radiation:.2f}, Eff={req_efficiency:.2f}")
            break
            
        # Reproduction
        next_gen = []
        while len(next_gen) < population_size:
            parent = random.choice(survivors)
            child = [
                clamp(parent[0] + random.gauss(0, mutation_rate)),
                clamp(parent[1] + random.gauss(0, mutation_rate)),
                clamp(parent[2] + random.gauss(0, mutation_rate))
            ]
            next_gen.append(child)
            
        population = next_gen
        
        # Logging
        if current_year % 10_000_000 == 0:
            avg_thermal = sum(a[0] for a in population) / population_size
            avg_rad = sum(a[1] for a in population) / population_size
            avg_eff = sum(a[2] for a in population) / population_size
            survival_rate = len(survivors) / population_size
            
            history.append({
                "Year": current_year,
                "Avg_Thermal": round(avg_thermal, 4),
                "Avg_Radiation": round(avg_rad, 4),
                "Avg_Efficiency": round(avg_eff, 4),
                "Survival_Rate": round(survival_rate, 4)
            })
            
            print(f"Year {current_year:>11,} | Survival: {survival_rate*100:>5.1f}% | Thermal: {avg_thermal:>5.2f} | Rad: {avg_rad:>5.2f} | Eff: {avg_eff:>5.2f}")

    if survivors:
        print(f"\n[MIRACLE] The population survived all 200,000,000 years!")
        
    print("==================================================")

if __name__ == "__main__":
    run_empirical_simulation()
