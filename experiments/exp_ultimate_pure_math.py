import numpy as np

def generate_ultimate_shifts():
    # Mix Fibonacci, Pi, and Primes
    fib = [1, 1, 2, 3, 5, 8, 13]
    pi_dig = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
    primes = [2, 3, 5, 7, 11, 13, 17]
    
    intervals = fib + pi_dig + primes
    
    shifts = set()
    current_gen = 0
    for i in intervals:
        current_gen += i
        shifts.add(current_gen)
        
    return shifts, current_gen

def adaptive_retention(era_length):
    f = 0.80 - (0.018 * era_length)
    return max(0.30, min(0.95, f))

def pure_math_ultimate_simulation():
    shifts, max_generations = generate_ultimate_shifts()
    
    modes = ['Exact', 'Lossy_50', 'Golden_Ratio', 'Adaptive_Law']
    
    # State tracking
    skills_A = {m: 0.0 for m in modes}
    skills_B = {m: 0.0 for m in modes}
    total_success = {m: 0.0 for m in modes}
    
    capacity = 1.0
    learn_amount = 0.4 # deterministic
    
    active_is_A = True
    era_length = 0
    
    PHI = (1 + np.sqrt(5)) / 2
    INV_PHI = 1.0 / PHI
    
    for g in range(max_generations):
        if g in shifts:
            active_is_A = not active_is_A
            era_length_for_shift = era_length
            era_length = 0
        else:
            era_length_for_shift = era_length
            era_length += 1
            
        for m in modes:
            # 1. Determine f
            if m == 'Exact':
                f = 1.0
            elif m == 'Lossy_50':
                f = 0.5
            elif m == 'Golden_Ratio':
                f = INV_PHI
            elif m == 'Adaptive_Law':
                if g in shifts:
                    f = adaptive_retention(era_length_for_shift)
                else:
                    f = 1.0
                    
            # 2. Inherit
            skills_A[m] *= f
            skills_B[m] *= f
            
            # 3. Learn
            if active_is_A:
                skills_A[m] += learn_amount
            else:
                skills_B[m] += learn_amount
                
            # 4. Enforce capacity
            total = skills_A[m] + skills_B[m]
            if total > capacity:
                skills_A[m] *= (capacity / total)
                skills_B[m] *= (capacity / total)
                
            # 5. Evaluate deterministic success
            active_skill = skills_A[m] if active_is_A else skills_B[m]
            success = min(1.0, active_skill)
            total_success[m] += success
            
    return {m: total_success[m] / max_generations for m in modes}

if __name__ == "__main__":
    print("=== Pure Mathematical Limit: Ultimate Law ===")
    print("Strictly deterministic evaluation (No RNG, No 'nonsense' probabilistic trials).")
    print("Mathematical integrals over the mixed sequence (Fibonacci -> Pi -> Primes).\n")
    
    results = pure_math_ultimate_simulation()
    
    sorted_res = sorted(results.items(), key=lambda x: x[1], reverse=True)
    
    print("Strategy             | Mathematical Limit Success (0 to 1)")
    print("-" * 60)
    for m, score in sorted_res:
        print(f"{m:20s} | {score:.6f}")
