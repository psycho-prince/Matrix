import numpy as np

def generate_ultimate_shifts():
    # Mix Fibonacci, Pi, and Primes
    fib = [1, 1, 2, 3, 5, 8, 13, 21, 34]
    pi_dig = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9, 7]
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    
    # We repeat the sequence to get a longer limit test
    intervals = (fib + pi_dig + primes) * 5
    
    shifts = set()
    current_gen = 0
    for i in intervals:
        current_gen += i
        shifts.add(current_gen)
        
    return shifts, current_gen

def test_factor(f, shifts, max_generations):
    skill_A = 0.0
    skill_B = 0.0
    capacity = 1.0
    learn_amount = 0.4 
    
    active_is_A = True
    total_success = 0.0
    
    for g in range(max_generations):
        if g in shifts:
            active_is_A = not active_is_A
            
        # Inherit
        skill_A *= f
        skill_B *= f
        
        # Learn
        if active_is_A:
            skill_A += learn_amount
        else:
            skill_B += learn_amount
            
        # Enforce capacity
        total = skill_A + skill_B
        if total > capacity:
            skill_A *= (capacity / total)
            skill_B *= (capacity / total)
            
        # Evaluate
        active_skill = skill_A if active_is_A else skill_B
        success = min(1.0, active_skill)
        total_success += success
            
    return total_success / max_generations

if __name__ == "__main__":
    shifts, max_gens = generate_ultimate_shifts()
    
    # Famous Mathematical Constants (Inverses, so they are < 1.0)
    PHI = (1 + np.sqrt(5)) / 2          # Golden Ratio
    SILVER = 1 + np.sqrt(2)             # Silver Ratio
    BRONZE = (3 + np.sqrt(13)) / 2      # Bronze Ratio
    EULER = np.e                        # Euler's number e
    PI = np.pi                          # Pi
    
    constants = {
        "Golden Ratio (1/φ)": 1.0 / PHI,
        "Silver Ratio (1/δ_S)": 1.0 / SILVER,
        "Bronze Ratio (1/δ_B)": 1.0 / BRONZE,
        "Inverse Euler (1/e)": 1.0 / EULER,
        "Inverse Pi (1/π)": 1.0 / PI,
        "Exact Copying (1)": 1.0,
        "Standard Lossy (1/2)": 0.5
    }
    
    print("=== The Battle of Mathematical Constants ===")
    print("Testing against the ultimate hyper-chaotic sequence limit.\n")
    
    results = {}
    for name, f in constants.items():
        score = test_factor(f, shifts, max_gens)
        results[name] = (f, score)
        
    sorted_res = sorted(results.items(), key=lambda x: x[1][1], reverse=True)
    
    print("Constant               | Value (f)  | Pure Math Limit Success")
    print("-" * 65)
    for name, (f, score) in sorted_res:
        print(f"{name:22s} | {f:.6f}   | {score:.6f}")
        
    print("\n=== Finding the 'Ultra' Theoretical Limit ===")
    # Sweep at high resolution
    factors = np.linspace(0.4, 0.8, 10000)
    best_f = 0
    best_score = 0
    for f in factors:
        score = test_factor(f, shifts, max_gens)
        if score > best_score:
            best_score = score
            best_f = f
            
    print(f"Absolute Peak Empiric f: {best_f:.6f}")
    print(f"Absolute Peak Score    : {best_score:.6f}")
